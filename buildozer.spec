[app]
title = Fractal Clock
package.name = fractalclock
package.domain = com.snuq
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec,ini
version = 1.0
requirements = python3,kivy
#presplash.filename = %(source.dir)s/data/presplash.png
#icon.filename = %(source.dir)s/data/icon.png
orientation = landscape
fullscreen = 1
#android.presplash_color = #FFFFFF
android.permissions = WAKE_LOCK
#android.permissions = android.permission.INTERNET, (name=android.permission.WRITE_EXTERNAL_STORAGE;maxSdkVersion=18)
#android.api = 31
#android.minapi = 21
#android.sdk = 20
#android.ndk = 23b
#android.ndk_api = 21
android.wakelock = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
android.archs = arm64-v8a, armeabi-v7a


[buildozer]
log_level = 2
warn_on_root = 0
