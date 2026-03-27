[app]

title = Shadow

package.name = shadow

package.domain = shadow.bridge

source.dir = .

source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,pyjnius,android,requests

orientation = portrait

fullscreen = 0

android.permissions = FOREGROUND_SERVICE, WAKE_LOCK, POST_NOTIFICATIONS, INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, RECORD_AUDIO, FOREGROUND_SERVICE_MICROPHONE, SYSTEM_ALERT_WINDOW, QUERY_ALL_PACKAGES

android.api = 33

android.minapi = 26

android.archs = arm64-v8a

android.allow_backup = True

services = myservice:service.py:foreground:sticky

[buildozer]

log_level = 2

warn_on_root = 1
