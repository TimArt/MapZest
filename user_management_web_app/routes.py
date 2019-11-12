from lib.Route import *
from controllers.LoginController import *
from controllers.IndexController import *

Route.get ("/", IndexController.get)
Route.view ("/login", "login.html")
Route.post ("/login", LoginController.login)
