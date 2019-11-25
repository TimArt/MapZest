# MapZest
Source code for MapZest system.

## Database Setup
_Requires PostgreSQL 11 or Higher_

### Setup of Database

1. Make sure PostgreSQL is running using the associated Linux command
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

### Using the Database

#### Resetting the Database
If anything ever goes wrong and you need to start fresh, make sure you are in the
database directory and have the `psql` CLI open, then run:
```bash
\i mapzest-postgresql-db-teardown.sql
\i mapzest-postgresql-db-init.sql
```

#### Queries for this Database
You most likely will not need to use raw queries when using our database since
I have written stored procedures and functions for us to use.

Reasons I chose to do this:
1. Stored Procedures / Functions can be more secure
2. Queries are simplified and functionalized
3. We will not need to rewrite the same queries for the Python and the C server,
instead we can just use the stored procedures

#### Running Stored Procedures and Functions
So how do you use stored procedures / functions?

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


