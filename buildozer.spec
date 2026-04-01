[app]

title = TTLock Root Exploit
package.name = ttlockroot
package.domain = org.grok4dev
source.dir = .
source.include_exts = py
version = 1.0

# 核心修复：添加 typing_extensions（解决 bleak 导入报错 ModuleNotFoundError）
requirements = python3,kivy==2.3.0,bleak,tqdm,cython==0.29.36,typing_extensions,pillow,jnius

orientation = portrait
fullscreen = 0

# TTLock 蓝牙所需完整权限（已优化）
android.permissions = INTERNET,BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,BLUETOOTH_ADVERTISE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FOREGROUND_SERVICE

android.api = 33
android.minapi = 24
android.archs = armeabi-v7a,arm64-v8a   # 增加 armeabi-v7a 兼容更多手机

android.accept_sdk_license = True
warn_on_root = 0

p4a.bootstrap = sdl2

[buildozer]

log_level = 2
warn_on_root = 0   # 强制关闭 root 警告
