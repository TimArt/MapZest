--  ============================================================================
--  MapZest PostgreSQL Database Initialization
--
--  Runs MySQL scripts for database creation, procedure creation, and any
--  default insertions.
--  ============================================================================

-- Include Table and Procedure scripts.
\i mapzest-postgresql-db-init_tables.sql
\i mapzest-postgresql-db-init_procedures.sql;
-- \i mapzest-postgresql-db-init_insertions.sql;
