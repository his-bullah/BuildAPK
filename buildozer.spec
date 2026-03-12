[app]

# (str) Title of your application
title = MyForegroundApp

# (str) Package name
package.name = foregroundapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements - IDHU ROMBA MUKKIYAM
requirements = python3,kivy,pyjnius,android,requests

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions - FOREGROUND SERVICE & NOTIFICATION PERMISSIONS
android.permissions = FOREGROUND_SERVICE, WAKE_LOCK, POST_NOTIFICATIONS, INTERNET

# (int) Target Android API, should be as high as possible.
# API 33 is good for Android 13/14 compatibility
android.api = 33

# (int) Minimum API your APK will support.
# API 26 is Android 8.0 (Foreground service changes started here)
android.minapi = 26

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (list) Android service to declare
# FORMAT: name:entry_point:foreground_or_background
# Idhu dhaan unga service-a foreground-la run panna vaikkum
services = myservice:service.py:foreground:sticky

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
