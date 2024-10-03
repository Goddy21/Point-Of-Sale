import hashlib
import os
from pymongo import MongoClient
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.config import Config

# Ensure Kivy logs for debugging
os.environ['KIVY_LOG_LEVEL'] = 'debug'

Config.set('kivy', 'window', 'sdl2')

Builder.load_file('signup/signup.kv')

class SignupWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def register_user(self):
        # MongoDB client setup
        client = MongoClient()
        db = client.silverpos
        users = db.users

        # Get the user input from the TextInput fields
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        uname = self.ids.username_field.text
        designation = self.ids.designation_field.text
        passw = self.ids.pwd_field.text
        confirm_passw = self.ids.confirm_pwd_field.text
        info = self.ids.info

        # Clear fields after grabbing the values
        self.ids.first_name.text = ''
        self.ids.last_name.text = ''
        self.ids.username_field.text = ''
        self.ids.designation_field.text = ''
        self.ids.pwd_field.text = ''
        self.ids.confirm_pwd_field.text = ''

        # Validate inputs
        if not all([first_name, last_name, uname, designation, passw, confirm_passw]):
            info.text = "[color=#FF0000]All fields are required[/color]"
            return

        if passw != confirm_passw:
            info.text = "[color=#FF0000]Passwords do not match[/color]"
            return

        # Check if username already exists
        if users.find_one({'user_name': uname}):
            info.text = "[color=#FF0000]Username already exists[/color]"
            return

        # Hash the password for storage
        hashed_passw = hashlib.sha256(passw.encode()).hexdigest()

        # Insert new user into the database
        new_user = {
            'first_name': first_name,
            'last_name': last_name,
            'user_name': uname,
            'designation': designation,
            'password': hashed_passw
        }

        users.insert_one(new_user)
        info.text = "[color=#00FF00]User registered successfully[/color]"
        self.go_to_signin()


    def go_to_signin(self):
        self.parent.parent.current = 'scrn_si'


class SignupApp(App):
    def build(self):
        return SignupWindow()


if __name__ == "__main__":
    SignupApp().run()

