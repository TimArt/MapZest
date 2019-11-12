from lib.Route import *
from controllers.LoginController import *

Route.view ("/", "login.html")
Route.view ("/login", "login.html")
Route.post ("/login", LoginController.login)
