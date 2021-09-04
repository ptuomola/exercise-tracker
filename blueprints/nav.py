from hashlib import sha1
from dominate import tags

from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_login import current_user
from flask_bs4.nav import BootstrapRenderer

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
            View("My exercises", "exercises.list_exercises", user_id=current_user.id),
            View("Users", "users.list_users"),
            View("Activities", "activities.list_activities"),
            View("Profile", "users.detail", user_id=current_user.id),
            View("Logout", "auth.logout"),
        )

    return Navbar(
        View("Exercise Tracker", "main.index"),
        View("My exercises", "exercises.list_exercises", user_id=current_user.id),
        View("Profile", "users.detail", user_id=current_user.id),
        View("Logout", "auth.logout"),
    )


nav.register_element("main_nav", main_nav)

# Custom based on code from flash-bs4: needed to change the colors for the navbar
# and to fix a bug in flash-bs4 lib's navbar dropdown
class MyBootstrapRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        # create a navbar id that is somewhat fixed, but do not leak any
        # information about memory contents to the outside
        # This is broken in Flash-bs4 as it creates IDs starting with integer
        # which are not allowed by CSS
        node_id = self.id or "a" + sha1(str(id(node)).encode()).hexdigest()

        nav_root = tags.nav() if self.html5 else tags.div(role='navigation')
        nav_root["class"] = "navbar navbar-expand-lg navbar-light"
        nav_root["style"] = "background-color: #426fa1"

        root = tags.div(_class="container-fluid")

        # title may also have a 'get_url()' method, in which case we render
        # a brand-link
        if node.title is not None:
            if hasattr(node.title, 'get_url'):
                root.add(tags.a(node.title.text, _class='navbar-brand',
                                href=node.title.get_url()))
            else:
                root.add(tags.span(node.title, _class='navbar-brand'))

        btn = root.add(tags.button())
        btn['class'] = 'navbar-toggler'
        btn['type'] = 'button'
        btn['data-bs-toggle'] = 'collapse'
        btn['data-bs-target'] = '#' + node_id
        btn['aria-controls'] = node_id
        btn['aria-expanded'] = 'false'
        btn['aria-label'] = 'Toogle Navigation'

        btn.add(tags.span(_class='navbar-toggler-icon'))

        navbar = root.add(tags.div(
            _class='navbar-collapse collapse',
            id=node_id,
        ))

        bar_list = navbar.add(tags.ul(_class='navbar-nav mr-auto'))

        for item in node.items:
            bar_list.add(self.visit(item))

        nav_root.add(root)
        return nav_root
