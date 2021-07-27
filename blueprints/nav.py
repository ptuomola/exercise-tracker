from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_login import current_user
from flask_bs4.nav import BootstrapRenderer
from dominate import tags

nav = Nav()

def main_nav():
    if current_user.is_authenticated:
        return Navbar(
            View("Exercise Tracker", "main.index"), 
            View("Profile", "main.profile"), 
            View("Logout", "auth.logout")
        )
    else:
        return Navbar(
            View("Exercise Tracker", "main.index"), 
            View("Login", "auth.login"), 
            View("Sign up", "auth.signup"), 
        )

nav.register_element("main_nav", main_nav)

class MyBootstrapRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        nav_root = BootstrapRenderer.visit_Navbar(self, node)
        nav_root["class"] = "navbar navbar-expand-lg navbar-light"
        nav_root["style"] = "background-color: #426fa1"
        return nav_root