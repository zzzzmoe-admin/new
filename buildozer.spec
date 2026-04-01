[app]
title = TTLock Root Exploit
package.name = ttlockroot
package.domain = org.grok4dev
source.dir = .
source.include_exts = py
version = 1.0

requirements = python3,kivy==2.3.0,bleak,tqdm,cython==0.29.36,typing_extensions,pillow,jnius
orientation = portrait
fullscreen = 0

android.permissions = INTERNET,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,BLUETOOTH_ADVERTISE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FOREGROUND_SERVICE
android.api = 33
android.minapi = 24
android.archs = armeabi-v7a,arm64-v8a

android.accept_sdk_license = True
warn_on_root = 0
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 0
