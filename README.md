# MapZest
Source code for MapZest system.

Here's a map of the various directories of the repository:
```
client -> unused folder
cybersec -> Java Client Source Code
database -> PostgreSQL Database Init Scripts
server -> unsued folder
user_management_web_app -> Python User Management App Source Code
CServer.c -> C Server file
```

## Setup

### Database Setup (PostgreSQL)
_Requires PostgreSQL 11 or Higher_

1. Make sure the PostgreSQL daemon is running using the associated Linux command
(Google this).

2. Change directory to the database directory inside this project folder.
```bash
cd database
```

2. Open the PostgreSQL command line interface `psql` using the following:
```bash
psql postgres
```

3. Once inside the CLI program, run the following command to import all database
tables and stored procedures/functions.
```bash
\i mapzest-postgresql-db-init.sql
```

### User Management Web App (Python App) Setup
We used the **mod_wsgi** WSGI Apache Module interface to communicate with Apache.
To install mod_wsgi on your system and get the app running, follow this tutorial:
https://modwsgi.readthedocs.io/en/develop/user-guides/quick-installation-guide.html

After downloading, and building mod_wsgi, setup the Apache configuration file
using the following lines outside of any virtual host config blocks:
```apache
# Setup site root to run the main application
WSGIScriptAlias / /path/to/MapZest/user_management_web_app/main.py

# Tell python the directory to search for other modules in
WSGIPythonPath "/path/to/MapZest/user_management_web_app:"

# Setup a Daemon Process to run the app and set current working directory app
# to be the project folder (the home option does this)
WSGIDaemonProcess website.com user=aUser group=aUser processes=2 threads=25 home=/path/to/MapZest/user_management_web_app
WSGIProcessGroup test.com
```

Lastly, ensure that the `user_management_web_app/lib/config.py` file gets filled
with your database credentials. Replace the line
```python
POSTGRES_DB_CONNECT = "dbname=mapzest user=timarterbury"
```
with your credentials:
```python
POSTGRES_DB_CONNECT = "dbname=mapzest user=myuser password=passwordstring"
```


## Usage

### Database Usage

#### Resetting the Database
If anything ever goes wrong and you need to start fresh, make sure you are in the
database directory and have the `psql` CLI open, then run:
```bash
\i mapzest-postgresql-db-teardown.sql
\i mapzest-postgresql-db-init.sql
```

#### Running Stored Procedures and Functions
1. Brefly read through the documentation of function/procedure names and
descriptions in the file `database/mapzest-postgresql-db-init_procedures.sql`.
This will give you an idea of the preset actions you can do without needing to
write out queries.

2. To call a stored **procedure** marked as `PROCEDURE` in the source code, run the
following in SQL:
```sql
CALL the_procedure_identifier (param_1, param_2, param_3);
```

3. To call a stored **function** marked as `FUNCTION` in the source code, run the
following in SQL:
```sql
SELECT * FROM the_function_identifier (param_1, param_2, param_3);
```

In summary, stored procedures are generally used for inserting or updating new
information into the database, while stored functions are generally used for
getting data from the database. Make sure to use the correct syntax between the
two above for either a procedure or a function.

#### Setting Up Test Data
If you need to insert test data, one easy way to do this is with a SQL script
which calls the stored procedures/functions needed to setup the state you want.

1. Make a new SQL file in the `database` directory called `mapzest-postgresql-db-init_debug_insertions_X.sql` where `X` is replaced with the
next number in the sequence of the files present in this directory.

2. Write out the stored procedures you want to call in the order you want to call
them. See `mapzest-postgresql-db-init_debug_insertions_1.sql` as an example of
some test data you could make.

3. Run the script to execute your test execution and add new content to the DB:
```bash
\i mapzest-postgresql-db-init_debug_insertions_X.sql
```

Here's a quick example which you could use to add a few users, make some friend
connections, and update locations:
```sql
-- Connect to MapZest DB
\c mapzest

-- Inserts users with dummy passwords. If you need to test hashing, this will
-- NOT work and you will need to use the python script for this.
CALL create_user ('tim@tim.com', 'abc', 'abc');
CALL create_user ('jeff@jeff.com', 'abc', 'abc');
CALL create_user ('maddie@maddie.com', 'abc', 'abc');
CALL create_user ('josh@josh.com', 'abc', 'abc');

-- Make users friends
CALL set_user_friend_status ('tim@tim.com', 'jeff@jeff.com', 'accepted');
CALL set_user_friend_status ('jeff@jeff.com', 'tim@tim.com', 'accepted');

CALL set_user_friend_status ('tim@tim.com', 'maddie@maddie.com', 'accepted');
CALL set_user_friend_status ('maddie@maddie.com', 'tim@tim.com', 'accepted');

CALL set_user_friend_status ('tim@tim.com', 'josh@josh.com', 'accepted');
CALL set_user_friend_status ('josh@josh.com', 'tim@tim.com', 'accepted');

-- Set some locations
CALL set_user_active_location ('tim@tim.com', 38.43, 483.24);
CALL set_user_active_location ('jeff@jeff.com', 23.2343, 24.24);
CALL set_user_active_location ('maddie@maddie.com', 54.43, 29.24);
CALL set_user_active_location ('josh@josh.com', 3.43, 462.43);
```

## User Management Web App (Python App) Usage
Using the web app is pretty simple. When you first visit the site, it will
redirect you to the `/login` page. Here you can signup or login. First create a
user with the signup dialog. You will need a username in the form of an email
and a password at least 8 characters long. If successful signup occurs, you will
be directed to a page that says your account was created and says it sent you
an email. The email functionality has been disabled, so do not worry about this.
Go back to the login page manually and attempt a login. If you successfuly login
you will see a new page with Friend Requests, Friends, and Potential Friends.
If you see nothing here, go create another user so you can friend them. When more
users are present you can then send them friend requests and they can accept those
requests. After this you will see them in your friend list along with their last
set location. Friends can be removed at anytime. You can log out of a certain user
by hitting the logout button.

