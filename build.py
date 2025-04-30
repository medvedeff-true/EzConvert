import PyInstaller.__main__

PyInstaller.__main__.run([
    'EzConvert.py',
    '--onefile',
    '--windowed',
    '--name=EzConvert',
    '--icon=icon.ico',
    '--add-data=DnD.png;.',
    '--add-data=icon.ico;.',
    '--add-data=flags;flags',
    '--hidden-import=pillow_heif',
    '--runtime-hook=hook_set_cwd.py',
    '--version-file=version_file.txt',
])
