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
SELECT the_function_identifier (param_1, param_2, param_3);
```

In summary, stored procedures are generally used for inserting or updating new
information into the database, while stored functions are generally used for
getting data from the database. Make sure to use the correct syntax between the
two above for either a procedure or a function.


