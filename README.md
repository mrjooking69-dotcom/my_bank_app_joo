[app]
title = My Bank App
package.name = mybankapp
package.domain = org.joo
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True
[buildozer]
log_level = 2
warn_on_root = 1
