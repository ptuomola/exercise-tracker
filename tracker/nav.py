from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()

nav.register_element("main", Navbar(
    View("Home", "main.index"), 
    View("Profile", "main.profile"), 
    View("Login", "auth.login"), 
    View("Sign up", "auth.signup"), 
    View("Logout", "auth.logout")
))