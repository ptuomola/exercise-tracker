from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_login import current_user

nav = Nav()

def main_nav():
    if current_user.is_authenticated:
        return Navbar(
            View("Home", "main.index"), 
            View("Profile", "main.profile"), 
            View("Logout", "auth.logout")
        )
    else:
        return Navbar(
            View("Home", "main.index"), 
            View("Login", "auth.login"), 
            View("Sign up", "auth.signup"), 
        )

nav.register_element("main_nav", main_nav)