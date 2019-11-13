from lib.Route import *
from lib.Auth import *
from controllers.LoginController import *
from controllers.IndexController import *

Route.get ("/", IndexController.get, [Auth.run])
Route.get ("/login", LoginController.get)
Route.post ("/login", LoginController.post)
