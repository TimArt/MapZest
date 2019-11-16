--  ============================================================================
--  MapZest PostgreSQL Database Initialization : Tables
--  ============================================================================

/* Create Database *************************************************************
*******************************************************************************/
CREATE DATABASE mapzest ENCODING 'UTF8';
    -- LC_COLLATE 'en_US.UTF-8'
    -- LC_CTYPE 'en_US.UTF-8';


-- Connect to MapZest DB
\c mapzest

/* Create Tables ***************************************************************
*******************************************************************************/

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR (345) UNIQUE NOT NULL, -- Unique is automatically indexed
    password VARCHAR (255) NOT NULL, -- Salt + Hash of user's password
    -- User must verify their email before using their account
    -- This is NULL when the user is not verified and a timestamp when they are
    email_verification_code BYTEA NOT NULL, -- 64 Bytes
    email_verified_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);


CREATE TABLE user_auth_tokens (
    user_id INTEGER UNIQUE NOT NULL,
    auth_token BYTEA NOT NULL, -- 64 Bytes
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


/*  user_password_reset_codes

    A table of temporary password reset codes that are sent to User's
    via email allowing them to reset their password.

    I'm storing the requested_at as opposed to an expiration time since
    this makes it easy for my application to decide how long until a code
    expires instead of the database itself.
*/
CREATE TABLE user_password_reset_codes (
    user_id INTEGER UNIQUE NOT NULL,
    password_reset_code BYTEA NOT NULL, -- 64 Bytes
    requested_at TIMESTAMP WITH TIME ZONE NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,

    -- Are foreign Key Refs are automatically indexed by Postgresql?
    FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


CREATE TYPE friend_status AS ENUM ('unspecified', 'rejected', 'accepted');

CREATE TABLE friends (
    -- The lower user id of two users will always be user_1,
    -- the higher user id of the two will always be user_2.
    user_1_id INTEGER NOT NULL,
    user_2_id INTEGER NOT NULL,
    user_1_status friend_status NOT NULL DEFAULT 'unspecified',
    user_2_status friend_status NOT NULL DEFAULT 'unspecified',
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,

    PRIMARY KEY (user_1_id, user_2_id),

    -- Are foreign Key Refs are automatically indexed by Postgresql?
    FOREIGN KEY (user_1_id) REFERENCES users (user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (user_2_id) REFERENCES users (user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
