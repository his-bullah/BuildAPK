from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock

class ForegroundApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        start_btn = Button(text="Start Foreground Service", font_size=20)
        start_btn.bind(on_press=self.start_service)
        layout.add_widget(start_btn)

        self.hide_btn = Button(text="Hide App Icon", font_size=18)
        self.hide_btn.bind(on_press=self.hide_icon_delay)
        layout.add_widget(self.hide_btn)

        return layout

    def start_service(self, instance):
        try:
            from jnius import autoclass
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            ServiceClass = autoclass('org.test.foregroundapp.ServiceMyservice')
            ServiceClass.start(mActivity, "Foreground service started from app!")
            instance.text = "Service Running..."
        except Exception as e:
            instance.text = f"Error: {e}"

    def hide_icon_delay(self, instance):
        instance.text = "Icon hiding in 5s..."
        Clock.schedule_once(self.disable_app, 5)

    def disable_app(self, dt):
        try:
            from jnius import autoclass

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            PackageManager = autoclass('android.content.pm.PackageManager')

            activity = PythonActivity.mActivity
            pm = activity.getPackageManager()
            package_name = activity.getPackageName()

            # 🔥 MAIN TRICK (works in buildozer)
            pm.setApplicationEnabledSetting(
                package_name,
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP
            )

            print("App icon hidden")

        except Exception as e:
            print("Error:", e)


ForegroundApp().run()