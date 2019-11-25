--  ============================================================================
--  MapZest PostgreSQL Database Initialization
--
--  Runs PostgreSQL scripts for database creation and procedure/function setup.
--
--  Requiurements:
--      - PostgreSQL 11 or Higher
--  ============================================================================

-- Include Table and Procedure scripts.
\i mapzest-postgresql-db-init_tables.sql;
\i mapzest-postgresql-db-init_procedures.sql;
--\i mapzest-postgresql-db-init_debug_insertions.sql;
