# MapZest : User Management Web Application

This application allows users to sign up, log in, view other users' names,
make friend requests, accept friend requests, and remove friends.

## Development

### CRAP I think WSGI is an alternative to the CGI stuff we are doing, not sure if allowed
### Local Dev
To get going with development on a local machine we will use the Python package
mod_wsgi to run Apache.

First, install mod_wsgi
```bash
pip install mod-wsgi
```

After installation, you now have access to the `mod_wsgi-express` program. Run
this to launch the server:
```bash
mod_wsgi-express start-server
```
Now go to `http://localhost:8000/` in your browser and you should see a super
weird landing page with some snakes in a bottle of yellow liquid and something
about malt whiskey. Super weird defualt page, I know.

But we want this Apache server to run our own Python CGI script. To do this, run
the command in the `/user_management_web_app` directory:
```bash
mod_wsgi-express start-server main.py
```



### Web Server Dev
We gotta figure this part out . . .
