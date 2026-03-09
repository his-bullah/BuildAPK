from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.utils import platform

class ForegroundApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        start_btn = Button(text="Start Foreground Service", font_size=20)
        start_btn.bind(on_press=self.start_service)
        
        layout.add_widget(start_btn)
        return layout

    def start_service(self, instance):
        if platform == 'android':
            from jnius import autoclass
            # Android activity context edukkuroam
            context = autoclass('org.kivy.android.PythonActivity').mActivity
            
            # App package name and service class name (buildozer la kudukkura name)
            service_name = str(context.getPackageName()) + '.ServiceMyservice'
            
            # Service start panna intent create pandrom
            service_intent = autoclass('android.content.Intent')()
            service_intent.setClassName(context, service_name)
            service_intent.putExtra("pythonServiceArgument", "Service Started!")
            
            # Android 8.0+ kku startForegroundService() theva
            context.startForegroundService(service_intent)
            print("Foreground Service Started!")
        else:
            print("Service can only be started on an Android device!")

if __name__ == '__main__':
    ForegroundApp().run()
