import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


requires = [
    'kivy',
    'pygame'
]

setup(name='kraken-workflow',
      version='0.0',
      description='kraken-workflow',
      long_description=README + '\n\n',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Kivy"
      ],
      author='Attasuntorn Traisuwan',
      author_email='attasuntorn@gmail.com',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="",
      scripts=['kraken/bin/kraken']
      )
