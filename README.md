# QrScan
QR Code &amp; Barcode scanner cross-platform application


## Install
```
make
```
Also [compile & install OpenCV](https://github.com/AndreMiras/garden.zbarcam/blob/develop/OpenCV.md).


## Run

### Linux
```
./src/main.py --debug
```
The `--debug` flag is required if you want to see errors printed in your console.
Otherwise the exception will be only sent to Sentry.

### Android
Build, deploy and run on Android using buildozer:
```
buildozer android debug deploy run logcat
buildozer android adb -- logcat
```

## Tests
```
python -m unittest discover --start-directory=src/
```


## Credits

Icon made by [Pixel perfect](https://www.flaticon.com/authors/pixel-perfect) from [Flaticon.com](https://www.flaticon.com/) and licensed by [Creative Commons 3.0](http://creativecommons.org/licenses/by/3.0/).
