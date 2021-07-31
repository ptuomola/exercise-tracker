from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_login import current_user
from flask_bs4.nav import BootstrapRenderer
from dominate import tags

nav = Nav()

def main_nav():

    if not current_user.is_authenticated:
        return Navbar(
            View("Exercise Tracker", "main.index"), 
            View("Login", "auth.login"), 
            View("Sign up", "auth.signup"), 
        )

    if current_user.superuser: 
        return Navbar(
            View("Exercise Tracker", "main.index"), 
            View("Users", "admin.list_users"),
            View("Profile", "main.profile"), 
            View("Logout", "auth.logout")
        )

    return Navbar(
        View("Exercise Tracker", "main.index"), 
        View("My exercises", "exercises.list_exercises", user_id = current_user.id),
        View("Profile", "main.profile"), 
        View("Logout", "auth.logout")
    )

nav.register_element("main_nav", main_nav)

# Custom renderer to fix the colors for the navbar
class MyBootstrapRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        nav_root = BootstrapRenderer.visit_Navbar(self, node)
        nav_root["class"] = "navbar navbar-expand-lg navbar-light"
        nav_root["style"] = "background-color: #426fa1"
        return nav_root