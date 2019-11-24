--  ============================================================================
--  MapZest PostgreSQL Database Initialization : Procedures
--  ============================================================================

-- Connect to MapZest DB
\c mapzest

/* Procedures and Functions ****************************************************
 ******************************************************************************/

/** Create User
 *
 *  Tables Modified: users
 *
 *  Errors:
 *      - row with email already exists
 *          : duplicate key value
 */
CREATE OR REPLACE PROCEDURE create_user
(
    IN p_email VARCHAR (345),
    IN p_password BYTEA,
    IN p_email_verification_code BYTEA -- 64 Bytes
)
LANGUAGE SQL
AS $$
    INSERT INTO users (email, password, email_verification_code, created_at)
        VALUES (p_email, p_password, p_email_verification_code, CURRENT_TIMESTAMP);
$$;


/** Get User Password Hash
 *
 *  Tables Modified: none
 */
CREATE OR REPLACE FUNCTION get_user_password_hash
(
    IN p_email VARCHAR (345)
)
RETURNS BYTEA
LANGUAGE SQL
AS $$
    SELECT password FROM users WHERE email = p_email LIMIT 1;
$$;


/** Get User ID
 *
 *  Tables Modified: none
 */
CREATE OR REPLACE FUNCTION get_user_id
(
    IN p_email VARCHAR (345)
)
RETURNS INTEGER
LANGUAGE SQL
AS $$
    SELECT user_id FROM users WHERE email = p_email LIMIT 1;
$$;


/** Set User Auth Token
 *
 *  Tables Modified: user_auth_tokens
 */
CREATE OR REPLACE PROCEDURE set_user_auth_token
(
    IN p_email VARCHAR (345),
    IN p_auth_token BYTEA
)
LANGUAGE SQL
AS $$
    -- If row already exists, update it
    INSERT INTO user_auth_tokens (user_id, auth_token, created_at)
        VALUES (get_user_id (p_email), p_auth_token, CURRENT_TIMESTAMP)
        ON CONFLICT (user_id) DO
            UPDATE SET auth_token = p_auth_token, created_at = CURRENT_TIMESTAMP
            WHERE user_auth_tokens.user_id = get_user_id (p_email);
$$;


/** Does User Auth Token Exist
 *
 *  Tables Modified: none
 */
CREATE OR REPLACE FUNCTION does_user_auth_token_exist
    (p_email VARCHAR (345), p_token BYTEA)
    RETURNS BOOLEAN
AS $$
    SELECT EXISTS (SELECT FROM user_auth_tokens WHERE user_id = get_user_id(p_email)
        AND auth_token = p_token
        AND (CURRENT_TIMESTAMP - created_at) < INTERVAL '10 minutes'
        LIMIT 1);
$$  LANGUAGE SQL;


/** Verify User Email
 *
 *  Tables Modified: users
 *
 *  Errors:
 *      - row with email already exists
 *          : duplicate key value
 */
CREATE OR REPLACE PROCEDURE verify_user_email
(
    IN p_email VARCHAR (345),
    IN p_email_verification_code BYTEA -- 64 Bytes
)
LANGUAGE SQL
AS $$
    UPDATE users SET email_verified_at=CURRENT_TIMESTAMP WHERE email=p_email
        AND EXISTS (
            SELECT FROM users WHERE email=p_email
                AND email_verification_code=p_email_verification_code
                AND email_verified_at IS NULL
        );
$$;


/** Get User Friends
 *
 *  Tables Modified: none
 */
CREATE OR REPLACE FUNCTION get_user_friends
(
    IN p_email VARCHAR (345)
)
RETURNS TABLE (
    user_id users.user_id%TYPE,
    email users.email%TYPE,
    latitude locations.latitude%TYPE,
    longitude locations.longitude%TYPE
)
LANGUAGE SQL
AS $$

    SELECT u.user_id, u.email, COALESCE (l.latitude, 0.0),
        COALESCE (l.longitude, 0.0) FROM users AS u
        JOIN
        (
            -- All friends where this user is user_1_id
            (SELECT user_2_id AS user_id FROM friends
                WHERE user_1_id = get_user_id (p_email)
                AND user_1_status = 'accepted'
                AND user_2_status = 'accepted')
            UNION
            -- All friends where this user is listed second
            (SELECT user_1_id AS user_id FROM friends
                WHERE user_2_id = get_user_id (p_email)
                AND user_1_status = 'accepted'
                AND user_2_status = 'accepted')
        ) AS f
        ON u.user_id = f.user_id
        LEFT JOIN locations AS l ON u.user_id = l.user_id;
$$;


/** Get User Friends
 *
 *  Tables Modified: none
 */
CREATE OR REPLACE FUNCTION get_user_friend_requests
(
    IN p_email VARCHAR (345)
)
RETURNS TABLE (
    user_id users.user_id%TYPE,
    email users.email%TYPE
)
LANGUAGE SQL
AS $$

    SELECT u.user_id, u.email FROM users AS u
        NATURAL JOIN
        (
            -- All friends where this user is user_1_id
            (SELECT user_2_id AS user_id FROM friends
                WHERE user_1_id = get_user_id (p_email)
                AND user_1_status = 'unspecified'
                AND user_2_status = 'accepted')
            UNION
            -- All friends where this user is listed second
            (SELECT user_1_id AS user_id FROM friends
                WHERE user_2_id = get_user_id (p_email)
                AND user_1_status = 'accepted'
                AND user_2_status = 'unspecified')
        ) AS f;
$$;


/** Get User Potential Friends
 *
 *  Returns 5 random potential friends for the specified user.
 *
 *  Tables Modified: none
 */
CREATE OR REPLACE FUNCTION get_user_potential_friends
(
    IN p_email VARCHAR (345)
)
RETURNS TABLE (
    user_id users.user_id%TYPE,
    email users.email%TYPE
)
LANGUAGE SQL
AS $$

    SELECT u.user_id, u.email FROM users AS u NATURAL JOIN
    (
        -- Grab all possible user_ids which are not this user except the ones
        -- the user is already friends with
        SELECT user_id FROM users WHERE email != p_email AND NOT EXISTS
            (
                (SELECT user_1_id AS user_id FROM friends WHERE user_1_id = get_user_id (p_email)
                    OR user_2_id = get_user_id (p_email))
                UNION
                (SELECT user_2_id AS user_id FROM friends WHERE user_1_id = get_user_id (p_email)
                    OR user_2_id = get_user_id (p_email))
            )
    ) AS pf
    -- Ensure the following user actually exists and don't return
    -- data if that user doesn't exist
    WHERE EXISTS (SELECT user_id FROM users WHERE email = p_email)
    ORDER BY random()
    LIMIT 10;
$$;


/** Set User Friend Status
 *
 *  Tables Modified: friends
 *
 *  Errors:
 *      - null value in column "user_id" violates not-null constraint
 *          : means no user exists with that email
 */
CREATE OR REPLACE PROCEDURE set_user_friend_status
(
    IN p_this_user_email VARCHAR (345),
    IN p_other_user_email VARCHAR (345),
    IN p_this_user_status friend_status
)
LANGUAGE SQL
AS $$
    -- If row already exists, update it
    INSERT INTO friends AS f (user_1_id, user_2_id, user_1_status, user_2_status, updated_at)
        VALUES (LEAST (get_user_id (p_this_user_email), get_user_id (p_other_user_email)),
                GREATEST (get_user_id (p_this_user_email), get_user_id (p_other_user_email)),

                CASE WHEN get_user_id (p_this_user_email)
                        = LEAST (get_user_id (p_this_user_email), get_user_id (p_other_user_email))
                THEN p_this_user_status
                ELSE 'unspecified'
                END,

                CASE WHEN get_user_id (p_this_user_email)
                        = GREATEST (get_user_id (p_this_user_email), get_user_id (p_other_user_email))
                THEN p_this_user_status
                ELSE 'unspecified'
                END,
                CURRENT_TIMESTAMP)

        ON CONFLICT (user_1_id, user_2_id) DO

            UPDATE SET
            user_1_status = CASE WHEN get_user_id (p_this_user_email)
                                    = LEAST (get_user_id (p_this_user_email), get_user_id (p_other_user_email))
                            THEN p_this_user_status
                            ELSE
                                (
                                SELECT user_1_status FROM friends AS f WHERE
                                f.user_1_id
                                    = LEAST (get_user_id (p_this_user_email), get_user_id (p_other_user_email))
                                AND
                                f.user_2_id
                                    = GREATEST (get_user_id (p_this_user_email), get_user_id (p_other_user_email))
                                LIMIT 1
                                )
                            END,

            user_2_status = CASE WHEN get_user_id (p_this_user_email)
                                    = GREATEST (get_user_id (p_this_user_email), get_user_id (p_other_user_email))
                            THEN p_this_user_status
                            ELSE
                                (
                                SELECT user_2_status FROM friends AS f WHERE
                                f.user_1_id
                                    = LEAST (get_user_id (p_this_user_email), get_user_id (p_other_user_email))
                                AND
                                f.user_2_id
                                    = GREATEST (get_user_id (p_this_user_email), get_user_id (p_other_user_email))
                                LIMIT 1
                                )
                            END,

            updated_at = CURRENT_TIMESTAMP

            WHERE
            (f.user_1_id = get_user_id (p_this_user_email) AND
             f.user_2_id = get_user_id (p_other_user_email))
            OR
            (f.user_1_id = get_user_id (p_other_user_email) AND
             f.user_2_id = get_user_id (p_this_user_email))
            ;
$$;


/** Set User's Current Location
 *
 *  Tables Modified: locations
 *
 *  Errors:
 *      - null value in column "user_id" violates not-null constraint
 *          : means no user exists with that email
 */
CREATE OR REPLACE PROCEDURE set_user_active_location
(
    IN p_email VARCHAR (345),
    IN p_latitude REAL,
    IN p_longitude REAL
)
LANGUAGE SQL
AS $$
    INSERT INTO locations (user_id, latitude, longitude, created_at)
        VALUES (get_user_id (p_email), p_latitude, p_longitude, CURRENT_TIMESTAMP)
        ON CONFLICT DO NOTHING;
$$;


/** Get User Current Location
 *
 *  Tables Modified: none
 */
CREATE OR REPLACE FUNCTION get_user_active_location (p_email VARCHAR (345))
   RETURNS TABLE (
      latitude locations.latitude%TYPE,
      longitude locations.longitude%TYPE,
      created_at locations.created_at%TYPE
    )
AS $$
   SELECT latitude, longitude, created_at FROM locations WHERE created_at = (
        SELECT MAX (l.created_at) FROM locations AS l JOIN users AS u ON
            l.user_id = u.user_id
            WHERE u.email = p_email
    ) LIMIT 1;
$$  LANGUAGE SQL;
