from distutils.core import setup

setup(name='chase',
      version='1.0',
      py_modules=['__main__', 'sheep', 'wolf', 'direction','__init__'],
      data_files=[('config', ['conf.ini'])]
      )