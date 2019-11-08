from lib.Route import *

Route.view ("/", "login.html")
Route.view ("/login", "login.html")
Route.post ("/login", "login.py")
