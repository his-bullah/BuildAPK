from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class ForegroundApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        start_btn = Button(text="Start Foreground Service", font_size=20)
        start_btn.bind(on_press=self.start_service)
        
        layout.add_widget(start_btn)
        return layout

    def start_service(self, instance):
        instance.text = "Service Running..."
        try:
            from jnius import autoclass
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            ServiceClass = autoclass('org.test.foregroundapp.ServiceMyservice')
            ServiceClass.start(mActivity, "Foreground service started from app!")
            print("Foreground Service Started Successfully!")
        except Exception as e:
            instance.text = f"Error Through: {e}"
            print(f"Service start pandrappo error: {e}")


ForegroundApp().run()
