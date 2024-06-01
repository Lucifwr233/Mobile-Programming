import flet
import json
from flet import *

# login page
class MyLogin(UserControl):
    def __init__(self):
        super(MyLogin, self).__init__()
        self.username = TextField(label="username")
        self.password = TextField(label="password", password=True)

    def build(self):
        return Container(
            bgcolor="yellow200",
            padding=10,
            content=Column([
                Text("Login Account", size=30),
                self.username,
                self.password,
                ElevatedButton(
                    "Login Now",
                    bgcolor="blue",
                    color="white",
                    on_click=self.loginbtn
                ),
                ElevatedButton(
                    "Register",
                    bgcolor="blue",
                    color="white",
                    on_click=self.registerbtn
                ),
            ])
        )

    def registerbtn(self, e):
        self.page.go("/register")
        self.page.update()

    def loginbtn(self, e):
        try:
            with open("login-test/login.json", "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {"users": []}

                username = self.username.value
                password = self.password.value

                user_found = False
                for user in data["users"]:
                    if user["username"] == username and user["password"] == password:
                        user_found = True
                        break

                if user_found:
                    print("Login Success")

                    datalogin = {
                        "value": True,
                        "username": self.username.value
                    }

                    self.page.session.set("login", datalogin)
                    self.page.go("/privatepage")
                    self.page.update()
                else:
                    print("Login Failed")
                    self.page.snack_bar = SnackBar(
                        Text("Login Failed", size=30),
                        bgcolor="red"
                    )
                    self.page.snack_bar.open = True
                    self.page.update()
        except Exception as ex:
            print(f"Error: {ex}")
            self.page.snack_bar = SnackBar(
                Text("Error occurred while logging in", size=30),
                bgcolor="red"
            )
            self.page.snack_bar.open = True
            self.page.update()

class PrivatePage(UserControl):
    def __init__(self):
        super(PrivatePage, self).__init__()

    def build(self):
        return Container(
            bgcolor="blue",
            content=Column([
                Text("Welcome to the main page", size=30),
                ElevatedButton("Logout", bgcolor="red", color="white", on_click=self.logoutbtn)
            ])
        )

    def logoutbtn(self, e):
        self.page.session.clear()
        self.page.go("/")
        self.page.update()

class MyRegister(UserControl):
    def __init__(self):
        super(MyRegister, self).__init__()
        self.username = TextField(label="username")
        self.password = TextField(label="password", password=True)

    def build(self):
        return Container(
            bgcolor="green",
            padding=10,
            content=Column([
                Text("Register", size=30),
                self.username,
                self.password,
                ElevatedButton("Register", on_click=self.registerprocess)
            ])
        )

    def registerprocess(self, e):
        new_user = {
            "username": self.username.value,
            "password": self.password.value,
        }

        try:
            try:
                with open("login-test/login.json", "r") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {"users": []}

            data["users"].append(new_user)

            with open("login-test/login.json", "w") as f:
                json_string = json.dumps(data, indent=4)
                f.write(json_string)

            self.page.go("/")
            self.page.update()
        except Exception as ex:
            print(f"Error: {ex}")
            self.page.snack_bar = SnackBar(
                Text("Error occurred while registering", size=30),
                bgcolor="red"
            )
            self.page.snack_bar.open = True
            self.page.update()

def main(page: Page):
    mylogin = MyLogin()
    privatepage = PrivatePage()
    registerpage = MyRegister()

    def myroute(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(View("/", [mylogin]))
        elif page.route == "/privatepage":
            if page.session.get("login") is None:
                page.go("/")
            else:
                page.views.append(View("/privatepage", [privatepage]))
        elif page.route == "/register":
            page.views.append(View("/register", [registerpage]))
        page.update()

    page.on_route_change = myroute
    page.go(page.route)

flet.app(target=main)

