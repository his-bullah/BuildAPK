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
            try:
                from jnius import autoclass
                
                # Android activity context edukkuroam
                mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
                
                # Buildozer generate pannuna Java Service class-a edukkurom
                # Format: <package.domain>.<package.name>.Service<ServiceName>
                # Unga spec file padi idhu dhaan correct-aana name:
                ServiceClass = autoclass('org.test.foregroundapp.ServiceMyservice')
                
                # Direct-a service-a start pandrom (Arguments: context, custom string)
                ServiceClass.start(mActivity, "Foreground service started from app!")
                
                print("Foreground Service Started Successfully!")
            except Exception as e:
                print(f"Service start pandrappo error: {e}")
        else:
            print("Service can only be started on an Android device!")


if __name__ == '__main__':
    ForegroundApp().run()
