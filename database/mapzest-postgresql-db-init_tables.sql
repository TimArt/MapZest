--  ============================================================================
--  MapZest PostgreSQL Database Initialization : Tables
--  ============================================================================

/* Create Database *************************************************************
*******************************************************************************/
CREATE DATABASE MapZest
    WITH USER 'postgres'
    ENCODING 'UTF8'
    LC_COLLATE 'en_US.UTF-8'
    LC_CTYPE 'en_US.UTF-8';


-- Connect to MapZest DB
\c MapZest

/* Create Tables ***************************************************************
*******************************************************************************/

CREATE TABLE Users (
    userId INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR (345) UNIQUE NOT NULL, -- Unique is automatically indexed
    password VARCHAR (255) NOT NULL, -- Salt + Hash of user's password
    mostRecentLocationId INT UNSIGNED DEFAULT NULL,

    -- User must verify their email before using their account
    -- This is NULL when the user is not verified and a timestamp when they are
    emailVerifiedAt TIMESTAMP WITH TIME ZONE DEFAULT NULL,

    createdAt TIMESTAMP WITH TIME ZONE NOT NULL,

    -- Are foreign Key Refs are automatically indexed by Postgresql?
    FOREIGN KEY (mostRecentLocationId) REFERENCES Locations (locationId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

/*  UserEmailVerificationCodes

    A table of temporary email verification codes that are sent to User's
    via email allowing them to click a link to verify their User account.
*/
CREATE TABLE UserEmailVerificationCodes (
    userId INT UNSIGNED UNIQUE NOT NULL,
    emailVerificationCode VARCHAR (64) NOT NULL,

    FOREIGN KEY (userId) REFERENCES Users (userId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


/*  UserPasswordResetCodes

    A table of temporary password reset codes that are sent to User's
    via email allowing them to reset their password.

    I'm storing the requestedAt as opposed to an expiration time since
    this makes it easy for my application to decide how long until a code
    expires instead of the database itself.
*/
CREATE TABLE UserPasswordResetCodes (
    userId INT UNSIGNED UNIQUE NOT NULL,
    passwordResetCode VARCHAR (64) NOT NULL,
    requestedAt TIMESTAMP WITH TIME ZONE NOT NULL,

    FOREIGN KEY (userId) REFERENCES Users (userId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


CREATE TABLE Locations (
    locationId INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    userId INT UNSIGNED NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    createdAt TIMESTAMP WITH TIME ZONE NOT NULL,

    -- Are foreign Key Refs are automatically indexed by Postgresql?
    FOREIGN KEY (userId) REFERENCES Users (userId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


CREATE TYPE FRIEND_STATUS AS ENUM ('unspecified', 'rejected', 'accepted');

CREATE TABLE Friends (
    user1Id INT UNSIGNED UNIQUE NOT NULL,
    user2Id INT UNSIGNED UNIQUE NOT NULL,
    user1Status FRIEND_STATUS NOT NULL DEFAULT 'unspecified',
    user2Status FRIEND_STATUS NOT NULL DEFAULT 'unspecified',
    lastUpdate TIMESTAMP WITH TIME ZONE NOT NULL,

    -- Are foreign Key Refs are automatically indexed by Postgresql?
    FOREIGN KEY (user1Id) REFERENCES Users (userId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (user2Id) REFERENCES Users (userId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
