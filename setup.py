import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mwget",
    version = "3.0.0",
    author = "ruifengyun",
    author_email = "rfyiamcool@163.com",
    description = "support threading download file",
    license = "MIT",
    keywords = "mwget support threading and break download fengyun",
    url = "https://github.com/rfyiamcool/mwget",
    packages = ['mwget'],
    long_description = read('README.md'),
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 2.7',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: System :: Archiving',
        ],
)
