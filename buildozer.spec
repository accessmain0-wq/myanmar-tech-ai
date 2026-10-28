[app]
title = Flashlight Hacker
package.name = flashlighthacker
package.domain = com.techshare
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,pyjnius,android
orientation = portrait
fullscreen = 1
android.permissions = CAMERA,FLASHLIGHT,FOREGROUND_SERVICE,POST_NOTIFICATIONS,WAKE_LOCK
android.api = 33
android.minapi = 24
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1