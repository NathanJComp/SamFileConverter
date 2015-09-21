import sys
from cx_Freeze import setup, Executable
includefiles = ['BMF.ico']
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('framesAttempt.py', base=base)
]

setup(name='simple_Tkinter',
      version='0.1',
      options = {'build_exe': {'include_files':includefiles}}, 
      description='Sample cx_Freeze Tkinter script',
      executables=executables
      )