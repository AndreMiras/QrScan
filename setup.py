import os

from setuptools import find_packages, setup

from src.qrscan import version


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


# exposing the params so it can be imported
setup_params = {
    'name': 'QrScan',
    'version': version.__version__,
    'description': 'QR Code & Barcode scanner cross-platform application',
    'long_description': read('README.md'),
    'long_description_content_type': 'text/markdown',
    'author': 'Andre Miras',
    'url': 'https://github.com/AndreMiras/QrScan',
    'packages': find_packages(
        where='src',
        exclude=(
            'tests',
        )
    ),
    'package_data': {'qrscan': ('*.kv',)},
    'package_dir': {'': 'src'},
    'entry_points': {
        'console_scripts': ('qrscan=qrscan.main:main',),
    },
    'install_requires': (
        'kivy-garden.kivymd',
        'opencv-python>=4',
        'raven',
        'validators',
        'zbarcam',
    ),
}


def run_setup():
    setup(**setup_params)


# makes sure the setup doesn't run at import time
if __name__ == '__main__':
    run_setup()
