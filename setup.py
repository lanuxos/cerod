from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, target_name = 'crod')
]

setup(name='crod',
      version = '0.0.1',
      description = 'Currency Exchange Rate and Oil Price Daily',
      options = {'build_exe': build_options},
      executables = executables)
