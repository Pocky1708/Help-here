
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.text import LabelBase
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
import mysql.connector

LabelBase.register(name="default_font", fn_regular="assets/Poppins-Regular.ttf")

class FirstWindow(ScreenManager):
    pass

class MainApp(MDApp):
    global screen_manager
    screen_manager = ScreenManager()

    def build(self):
        self.title = "ATC Technology"
        self.theme_cls.theme_style = "Light"

        screen_manager.add_widget(Builder.load_file("splashScreen.kv"))
        screen_manager.add_widget(Builder.load_file("Sign.kv"))

        return screen_manager
    
    def on_start(self):
        Clock.schedule_once(self.change_screen, 10)
    def change_screen(self, dt):
        screen_manager.current = "log_win"

class LoginWindow(Screen):
    def build(self):
        self.title = "ATC Technology"
        self.theme_cls.theme_style = "Light"
    
        my_db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "MySQLgo%321x!",
            database = "project_db",
            auth_plugin='mysql_native_password',
        )

        c = my_db.cursor()
        c.execute("CREATE DATABASE IF NOT EXISTS project_db")

        my_db.commit()
        my_db.close()

    def check_info(self):
        my_db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "MySQLgo%321x!",
            database = "project_db",
            auth_plugin='mysql_native_password',
        )

        c = my_db.cursor()

        U_name = self.ids.Name.text
        U_passwd = self.ids.passWord.text

        c.execute("SELECT * FROM Users WHERE name = %s AND password = %s", (U_name, U_passwd))

        find_data = c.fetchall()

        if find_data:
            self.manager.current = "main"
        else:
            self.error_login = MDDialog(
                title="Error", text="Access Failed\nPlease check your username and password"
                )
            self.error_login.open()

class RegisterWindow(Screen):
    def check_data(self):
        my_db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "MySQLgo%321x!",
            database = "project_db",
            auth_plugin='mysql_native_password',
        )

        c = my_db.cursor()

        name = self.ids.F_Name.text
        pasw = self.ids.F_passWord.text

        c.execute("SELECT * FROM Users WHERE name = %s", (name,))

        result = c.fetchone()
        if result:
            self.dialog_error_name = MDDialog(
                text="This Username already exists"
            )
            self.dialog_error_name.open()
        else:
            if name != "" and name != " " and pasw != "" and pasw != " ":
                value_name = (self.ids.F_Name.text) 
                value_pass = (self.ids.F_passWord.text)

                c.execute("INSERT INTO Users (name, password) VALUES (%s, %s)", (value_name, value_pass))
                my_db.commit()
                self.success_regis = MDDialog(
                    title="Successful!",
                    text="You have been registered",
                    auto_dismiss = False,
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: self.success_regis.dismiss()
                            )
                        ]
                    )
                self.success_regis.open()
            else:
                self.dialog_error_passw = MDDialog(text="Please fill the username and password")
                self.dialog_error_passw.open()
        c.close()

class MainWindow(Screen):
    pass


if __name__ == "__main__":
    MainApp().run()