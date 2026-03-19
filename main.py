from kivy.app import App
from jnius import autoclass
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout    

class ForegroundApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical',padding=50,spacing=20)
        self.permissions_btn = Button(text="Give Permissions", font_size=25)
        self.permissions_btn.bind(on_press=self.get_permission)
        self.permissions_btn.disabled = False
        layout.add_widget(self.permissions_btn)
        self.start_btn = Button(text="Start Service", font_size=25)
        self.start_btn.bind(on_press=self.start_service)
        self.start_btn.disabled = True
        layout.add_widget(self.start_btn)
        self.disable_btn = Button(text="Disable Icon", font_size=25)
        self.disable_btn.bind(on_press=self.disable_icon)
        self.disable_btn.disabled = True
        layout.add_widget(self.disable_btn)
        return layout

    def get_permission(self,instance):
        try:
            instance.text = "Getting Permission..."
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            Settings = autoclass('android.provider.Settings')
            activity = PythonActivity.mActivity
            package_name = activity.getPackageName()
            intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
            uri = Uri.parse("package:" + package_name)
            intent.setData(uri)
            instance.text = "Redirecting..."
            activity.startActivity(intent)
            instance.text = "Permission Granded."
            self.permissions_btn.disabled = True
            self.start_btn.disabled = False
        except Exception as error:
            instance.text = f"Permission Getting Error: {error}"

    def start_service(self,instance):
        try:
            instance.text = "Stariting Service..."
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            ServiceClass = autoclass(f'{mActivity.getPackageName()}.ServiceMyservice')
            ServiceClass.start(mActivity, "Foreground service started!")
            instance.text = "Service Running..."
            self.start_btn.disabled = True
            self.disable_btn.disabled = False
        except Exception as error:
            instance.text = f"Starting Service Error: {error}"

    def disable_icon(self,instance):
        try:
            instance.text = "Icon Disabling..."
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            PackageManager = autoclass('android.content.pm.PackageManager')
            activity = PythonActivity.mActivity
            pm = activity.getPackageManager()
            package_name = activity.getPackageName()
            pm.setApplicationEnabledSetting(package_name,PackageManager.COMPONENT_ENABLED_STATE_DISABLED,PackageManager.DONT_KILL_APP)
            instance.text = "Icon Disabled."
            self.disable_btn.disabled = True
        except Exception as error:
            instance.text = f"Icon Disabling Error: {error}"

ForegroundApp().run()
