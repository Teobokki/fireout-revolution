# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
d, b, h = collect_all('pymupdf')
a = Analysis(['fireout_revolution.py'], datas=[('logo.ico','.'),('logo256.png','.'),('logo48.png','.')] + d, binaries=b, hiddenimports=['fitz','pymupdf'] + h, noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='FIREOUT REVOLUTION', console=False, upx=False, version='version.txt', icon=['logo.ico'])
coll = COLLECT(exe, a.binaries, a.datas, upx=False, name='FIREOUT REVOLUTION')
