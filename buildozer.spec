[app]
title = Mr Joo App
package.name = mrjooapp
package.domain = org.bassem
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المتطلبات دي هي اللي بتخلي البرنامج يشتغل صح على أندرويد
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, requests, certifi

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
