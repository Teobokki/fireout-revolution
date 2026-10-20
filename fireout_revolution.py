"""FIREOUT REVOLUTION(TM) - live slides viewer by EX Inc.
\u00a92026 EX Inc."""
import json, os, random, re, sys, threading, urllib.request, webbrowser
import tkinter as tk
from tkinter import messagebox

APP = "FIREOUT REVOLUTION\u2122"
APP_VERSION = "1.0.3"
COPYRIGHT = "\u00a92026 EX Inc./HYPERION DIGITAL \u00a92026"
UPDATE_URL = "https://raw.githubusercontent.com/Teobokki/fireout-revolution/main/latest.json"
BG, PANEL, CARD2 = "#000000", "#0d0d0f", "#2a2a2d"
TXT, MUT, GREEN = "#f2f2f4", "#9a9aa0", "#afd067"
FIRE = ["#ff453a", "#ff9f0a", "#ffd60a"]
FONT, MONO = "Segoe UI", "Consolas"


def res_path(n):
    return os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))), n)


def vtuple(v):
    return tuple(int(x) for x in re.findall(r"\d+", str(v))[:4]) or (0,)


def check_update():
    try:
        req = urllib.request.Request(UPDATE_URL, headers={"User-Agent": "FIREOUT-REVOLUTION/" + APP_VERSION})
        with urllib.request.urlopen(req, timeout=8) as r:
            m = json.loads(r.read(65536).decode("utf-8"))
        ver = str(m["version"])
    except Exception as e:
        return "error", "Could not check for updates (%s)." % (getattr(e, "reason", None) or e)
    if vtuple(ver) > vtuple(APP_VERSION):
        return "newer", {"version": ver, "notes": str(m.get("notes", "")),
                         "link": str(m.get("installer_url") or m.get("url", ""))}
    return "latest", "You have the latest version (%s)." % APP_VERSION


SLIDES_PDF = os.path.join(os.path.expanduser("~"), "Downloads", "FIREOUT REVOLUTION Slides.pdf")


class SlideViewer(tk.Tk):
    """Shows every page of the slides PDF, fit to window (no cropping), live-reloading on change."""
    POLL_MS = 2000

    def __init__(self):
        super().__init__()
        self.title(APP); self.configure(bg=BG); self.geometry("1100x700"); self.minsize(480, 320)
        try: self.iconbitmap(default=res_path("logo.ico"))
        except Exception: pass
        try: self._ic = tk.PhotoImage(file=res_path("logo256.png")); self.iconphoto(True, self._ic)
        except Exception: pass
        top = tk.Frame(self, bg=PANEL); top.pack(fill="x")
        tk.Label(top, text="  \U0001F525 " + APP, bg=PANEL, fg=FIRE[1], font=(FONT, 10, "bold")).pack(side="left", pady=4)
        u = tk.Label(top, text=" \u27f3 Updates ", bg=PANEL, fg=GREEN, font=(FONT, 9, "bold"), cursor="hand2")
        u.pack(side="right", padx=6); u.bind("<Button-1>", lambda e: self.check_updates())
        u.bind("<Enter>", lambda e: u.configure(bg=CARD2)); u.bind("<Leave>", lambda e: u.configure(bg=PANEL))
        tk.Label(self, text=COPYRIGHT, bg=PANEL, fg="#5a5a60", font=(FONT, 8)).pack(side="bottom", fill="x")
        bar = tk.Frame(self, bg=PANEL); bar.pack(fill="x")
        def btn(t, cmd):
            b = tk.Label(bar, text=t, bg=PANEL, fg=TXT, font=(FONT, 10, "bold"), cursor="hand2", padx=10, pady=5)
            b.bind("<Button-1>", lambda e: cmd()); b.bind("<Enter>", lambda e: b.configure(bg=CARD2)); b.bind("<Leave>", lambda e: b.configure(bg=PANEL))
            b.pack(side="left"); return b
        btn("\u25c0 Prev", self.prev); btn("Next \u25b6", self.next)
        self.counter = tk.Label(bar, text="", bg=PANEL, fg=GREEN, font=(FONT, 10, "bold")); self.counter.pack(side="left", padx=12)
        self.fit = True
        self.fit_btn = btn("Fit: window", self.toggle_fit)
        self.status = tk.Label(bar, text="", bg=PANEL, fg=MUT, font=(FONT, 9)); self.status.pack(side="right", padx=10)
        wrap = tk.Frame(self, bg=BG); wrap.pack(fill="both", expand=True)
        self.c = tk.Canvas(wrap, bg="#050506", highlightthickness=0)
        self.vs = tk.Scrollbar(wrap, orient="vertical", command=self.c.yview); self.hs = tk.Scrollbar(wrap, orient="horizontal", command=self.c.xview)
        self.c.configure(yscrollcommand=self.vs.set, xscrollcommand=self.hs.set)
        self.vs.pack(side="right", fill="y"); self.hs.pack(side="bottom", fill="x"); self.c.pack(fill="both", expand=True)
        for k, f in (("<Left>", self.prev), ("<Right>", self.next), ("<Prior>", self.prev), ("<Next>", self.next),
                     ("<Home>", lambda: self.go(0)), ("<End>", lambda: self.go(self.count - 1)), ("<f>", self.toggle_fit)):
            self.bind(k, lambda e, f=f: f())
        self.bind("<MouseWheel>", lambda e: self.c.yview_scroll(-1 if e.delta > 0 else 1, "units") if not self.fit else (self.prev() if e.delta > 0 else self.next()))
        self.c.bind("<Configure>", lambda e: self.schedule_render())
        self.doc = None; self.count = 0; self.page = 0; self.mtime = None; self.img = None; self._rj = None
        self.focus_set(); self.poll()

    def check_updates(self):
        threading.Thread(target=lambda: (lambda r: self.after(0, lambda: self.show_update(*r)))(check_update()), daemon=True).start()

    def show_update(self, st, d):
        if st != "newer":
            (messagebox.showinfo if st == "latest" else messagebox.showwarning)(APP, d); return
        if d["link"].startswith("http") and messagebox.askyesno(APP, "%s %s is available (you have %s).\n\n%s\n\nOpen the installer download?" % (APP, d["version"], APP_VERSION, d["notes"])):
            webbrowser.open(d["link"])

    def load(self):
        try: import pymupdf as fitz
        except ImportError: import fitz
        with open(SLIDES_PDF, "rb") as fh: data = fh.read()  # read into memory so the file is never held open
        doc = fitz.open(stream=data, filetype="pdf")
        if doc.page_count == 0: raise ValueError("empty PDF")
        if self.doc is not None:
            try: self.doc.close()
            except Exception: pass
        self.doc = doc; self.count = doc.page_count; self.page = min(self.page, self.count - 1)

    def poll(self):
        if not self.winfo_exists(): return
        try:
            m = os.stat(SLIDES_PDF).st_mtime
            if m != self.mtime:
                self.load(); self.mtime = m; self.render()
                self.status.configure(text="Live \u00b7 updated " + __import__("time").strftime("%H:%M:%S"), fg=MUT)
        except FileNotFoundError:
            self.mtime = None; self.doc = None; self.count = 0; self.show_msg("Slides not found", SLIDES_PDF + "\nRetrying\u2026")
        except Exception as e:  # locked / half-written: keep old pages, retry next poll
            self.mtime = None
            if self.doc is None: self.show_msg("Slides not found", "Could not open the PDF yet (%s). Retrying\u2026" % e)
            else: self.status.configure(text="File busy, retrying\u2026", fg=FIRE[1])
        self.after(self.POLL_MS, self.poll)

    def show_msg(self, title, sub):
        c = self.c; c.delete("all"); w, h = max(c.winfo_width(), 200), max(c.winfo_height(), 200)
        c.create_text(w/2, h/2 - 16, text=title, fill=FIRE[0], font=(FONT, 20, "bold"))
        c.create_text(w/2, h/2 + 20, text=sub, fill=MUT, font=(FONT, 10), width=w - 40, justify="center")
        c.configure(scrollregion=(0, 0, w, h)); self.counter.configure(text="0 / 0"); self.status.configure(text="")

    def schedule_render(self):
        if self._rj: self.after_cancel(self._rj)
        self._rj = self.after(80, self.render)

    def render(self):
        self._rj = None
        if self.doc is None: return
        import base64
        try: import pymupdf as fitz
        except ImportError: import fitz
        pg = self.doc[self.page]; r = pg.rect
        cw, ch = max(self.c.winfo_width(), 50), max(self.c.winfo_height(), 50)
        z = min((cw - 16) / r.width, (ch - 16) / r.height) if self.fit else 1.5
        z = max(z, 0.05)
        pix = pg.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False)
        self.img = tk.PhotoImage(data=base64.b64encode(pix.tobytes("png")))
        c = self.c; c.delete("all")
        W, H = max(cw, pix.width + 16), max(ch, pix.height + 16)
        c.create_image(W/2, H/2, image=self.img)
        c.configure(scrollregion=(0, 0, W, H)); c.xview_moveto(0); c.yview_moveto(0)
        self.counter.configure(text="%d / %d" % (self.page + 1, self.count))

    def go(self, i):
        if self.count: self.page = max(0, min(self.count - 1, i)); self.render()
    def prev(self): self.go(self.page - 1)
    def next(self): self.go(self.page + 1)

    def toggle_fit(self):
        self.fit = not self.fit; self.fit_btn.configure(text="Fit: window" if self.fit else "Zoom: 150% (scroll)"); self.render()


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--selftest-slides":  # build check
        SLIDES_PDF = sys.argv[2]; v = SlideViewer()
        def done():
            open(sys.argv[3], "w").write("pages=%d counter=%s img=%s title=%s" % (v.count, v.counter.cget("text"), v.img and (v.img.width(), v.img.height()), v.title().encode("ascii", "replace").decode()))
            v.destroy()
        v.after(4000, done); v.mainloop(); sys.exit()
    SlideViewer().mainloop()
