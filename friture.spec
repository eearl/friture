# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files
import platform

block_cipher = None

if platform.system() == "Windows":
  sounddevice_data = collect_data_files("sounddevice", subdir="_sounddevice_data")
  libportaudio = [(file[0], "_sounddevice_data/portaudio-binaries") for file in sounddevice_data if "libportaudio" in file[0]]

  print(libportaudio)
  if len(libportaudio) != 1:
    raise ValueError('libportaudio dll could not be found')

  # workaround for PyInstaller that does not look where the new PyQt5 official wheels put the Qt dlls
  from PyInstaller.compat import getsitepackages
  pathex = [os.path.join(x, 'PyQt5', 'Qt', 'bin') for x in getsitepackages()]

  # add vcruntime140.dll - PyInstaller excludes it by default because it thinks it comes from c:\Windows
  binaries = [('vcruntime140.dll', 'C:\\Python35\\vcruntime140.dll', 'BINARY')]
else:
  libportaudio = []
  pathex = []
  binaries = []

a = Analysis(['main.py'],
             pathex=pathex,
             binaries=None,
             datas=libportaudio,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='friture',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon="resources/images/friture.ico")
coll = COLLECT(exe,
               a.binaries + binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='friture')
