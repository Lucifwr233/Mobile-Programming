from flet import *


#login page
class Mylogin(object):
    def __init__(self):
        super(Mylogin, self).__init__()
        self.username = TextField(label="username")
        self.password = TextField(label="password")

    def build(self):
        return Container(
            bgcolor="yellow200",
            padding=10,
            content=Column([
                Text("Login Account", size=30),
                self.username,
                self.password,
                ElevatedButton("Login Now", 
                    gcolor="blue",
                    color="white",
                    on_click=self.loginbtn
                    ),
                ElevatedButton("Register", 
                    gcolor="blue",
                    color="white",
                    on_click=self.registerbtn
                    ),
            ])
        )


    def registerbtn(self, e ):
        self.page.go("/register")
        self.page.update()
    
    def loginbtn(self, e):
        with open("login.json", "r") as f:
            data = json.load(f)
            username = self.username.value
            password = selft.password.value

            if user in data["users"]:
                if user["username"] == username and user["password"] == password:
                    print("Login Succes")

                    datalogin ={
                        value:True,
                        username:self.username.value
                    }

                    self.page.session.set("loginme", datalogin)
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


class PrivatePage(UserControl):
    def __init__(self):
        super(PrivatePage, self).__init__()
    
    def build(self):
        return Container(
            bgcolor="blue",
            content=Column([
                Text("Wellcome to the main page", size=30),
                ElevatedButton("Logout",
                bgcolor="red", color="white",
                on_click=self.logoutbtn)
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
        self.password = TextField(label="password")

    def build(self, e):
        return Container(
            bgcolor="green",
            padding=10,
            content= Column({
                Text("Register", size=30),
                self.username,
                self.password,
                ElevatedButton("Register", 
                on_click = self.registerprocces
                )

            })
        )

    def registerprocces(self, e):
        new_user = {
            "username":self.username.value,
            "password":self.password.value,
        }
        data= {"users":[]}

        data["users"].append(new_user)
        with open("login.json", "w") as f:
            json_string = json.dumps(data)
            f.write(json_string)


        self.page.go("/")
        self.page.update



def main(page:Page):

    mylogin = Mylogin()
    privatepage = PrivatePage()
    registerpage = MyRegister()

    def myroute(route):
        page.views.clear()
        
        page.views.append(
                View(
                    "/",[
                        mylogin
                        ]
                )
        )

        if page.route == "/privatepage":
            print(page.session.get("login"))
            if page.session.get("login") == None:
                page.go("/")
            else:
                page.views.append(
                    View(
                        "/privatepage",
                        [
                            privatepage
                        ]
                    )
                )
        elif page.route == "/register":
            



    page.add()



flet.app(target=main)