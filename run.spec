# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['run.py'],
             pathex=['D:\\work\\opencv\\photobooth'],
             binaries=[],
             datas=[('C:\\Users\\jechun\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\site-packages\\eel\\eel.js', 'eel'), ('web', 'web')],
             hiddenimports=['pkg_resources.py2_warn', 'bottle_websocket', 'common_sound', 'common_data', 'common_makingvideo'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='run',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
