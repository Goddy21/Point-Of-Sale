import os

os.environ['KIVY_LOG_LEVEL'] = 'debug'


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from admin.admin import AdminWindow
from signin.signin import SigninWindow
from signup.signup import SignupWindow
from till_operator.till_operator import OperationWindow
from kivy.config import Config

Config.set('kivy', 'window', 'sdl2')


class MainWindow(BoxLayout):
    admin_widget = AdminWindow()
    signin_widget = SigninWindow()
    signup_widget = SignupWindow()
    operator_widget = OperationWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_signup.add_widget(self.signup_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)


class MainApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    MainApp().run()
