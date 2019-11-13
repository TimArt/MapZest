from lib.Route import *
from lib.Auth import *
from controllers.LoginController import *
from controllers.IndexController import *

Route.get ("/", IndexController.get, [Auth.run])
Route.view ("/login", "login.html")
Route.post ("/login", LoginController.login)
