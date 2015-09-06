import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mwget",
    version = "3.2.0",
    author = "ruifengyun",
    author_email = "rfyiamcool@163.com",
    description = "support threading download file",
    license = "MIT",
    keywords = ["mwget support threading and break download","fengyun"],
    url = "https://github.com/rfyiamcool/mwget",
    packages = ['mwget'],
    long_description = read('README.md'),
    classifiers = [
         'Development Status :: 2 - Pre-Alpha',
         'Intended Audience :: Developers',
         'License :: OSI Approved :: MIT License',
         'Programming Language :: Python :: 2.7',
         'Programming Language :: Python :: 3.0',
         'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
