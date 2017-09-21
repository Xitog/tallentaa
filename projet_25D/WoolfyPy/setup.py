from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'Woolfy app',
  ext_modules = cythonize("Woolfy.py"),
)
