# QrScan

[![Build Status](https://secure.travis-ci.org/AndreMiras/QrScan.png?branch=develop)](http://travis-ci.org/AndreMiras/QrScan)

<a href="https://play.google.com/store/apps/details?id=com.github.andremiras.qrscan"><img src="https://cdn.rawgit.com/steverichey/google-play-badge-svg/master/img/en_get.svg" alt="Play Store" width="20%"></a>

QR Code &amp; Barcode scanner cross-platform application

<img src="https://raw.githubusercontent.com/AndreMiras/QrScan/develop/docs/images/play_feature_graphic.png" alt="Feature graphics">

## Install
```sh
make
```

## Run

### Linux
```sh
make run
```

### Android
Build, deploy and run on Android using buildozer:
```sh
buildozer android debug deploy run logcat
buildozer android adb -- logcat
```

## Tests
```sh
make test
```

## Credits

Icon made by [Pixel perfect](https://www.flaticon.com/authors/pixel-perfect) from [Flaticon.com](https://www.flaticon.com/) and licensed by [Creative Commons 3.0](http://creativecommons.org/licenses/by/3.0/).
