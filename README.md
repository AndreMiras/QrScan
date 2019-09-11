# QrScan

[![Build Status](https://secure.travis-ci.org/AndreMiras/QrScan.png?branch=develop)](http://travis-ci.org/AndreMiras/QrScan)
[![PyPI version](https://badge.fury.io/py/QrScan.svg)](https://badge.fury.io/py/QrScan)

<a href="https://play.google.com/store/apps/details?id=com.github.andremiras.qrscan"><img src="https://cdn.rawgit.com/steverichey/google-play-badge-svg/master/img/en_get.svg" alt="Play Store" width="20%"></a>

QR Code &amp; Barcode scanner cross-platform application

<img src="https://raw.githubusercontent.com/AndreMiras/QrScan/develop/docs/images/play_feature_graphic.png" alt="Feature graphics">

## Key features
* All QR Code and Barcode supported
* Cross-platform (Windows, Linux, macOS, Android, iOS)

## Install & Usage
[QrScan is available on PyPI](https://pypi.org/project/QrScan/).
Therefore it can be installed via `pip`.
```sh
pip3 install --user QrScan
```
Once installed, it should be available in your `PATH` and can be ran from the command line.
```sh
qrscan
```

## Develop & Contribute
If you want to experiment with the project or contribute, you can clone it and install dependencies.
```sh
make
```
Later run the code on desktop via the `run` target.
```sh
make run
```
Unit tests are also available.
```sh
make test
```
On Android you can build, deploy and run using [Buildozer](https://github.com/kivy/buildozer).
```sh
buildozer android debug deploy run logcat
```
And debug with `logcat`.
```sh
buildozer android adb -- logcat
```

## Credits
Icon made by [Pixel perfect](https://www.flaticon.com/authors/pixel-perfect) from [Flaticon.com](https://www.flaticon.com/) and licensed by [Creative Commons 3.0](http://creativecommons.org/licenses/by/3.0/).
