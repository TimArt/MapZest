--  ============================================================================
--  MapZest PostgreSQL Database Initialization : Test Data Insertions for Debug
--  ============================================================================

-- Connect to MapZest DB
\c mapzest

-- Create Users
CALL create_user ('tim@tim', 'abc', 'abc');
CALL create_user ('lolz@lolz', 'abc', 'abc');
CALL create_user ('wut@wut', 'abc', 'abc');
CALL create_user ('okay@okay', 'abc', 'abc');
CALL create_user ('omg@omg', 'abc', 'abc');
CALL create_user ('jk@jk', 'abc', 'abc');
CALL create_user ('kk@kk', 'abc', 'abc');
CALL create_user ('jam@jam', 'abc', 'abc');
CALL create_user ('mc@mc', 'abc', 'abc');
CALL create_user ('swag@swag', 'abc', 'abc');
CALL create_user ('yo@yo', 'abc', 'abc');
CALL create_user ('tx@tx', 'abc', 'abc');
CALL create_user ('um@um', 'abc', 'abc');
CALL create_user ('jank@jank', 'abc', 'abc');
CALL create_user ('lit@lit', 'abc', 'abc');

-- Show all Users
SELECT * FROM users;

-- Test Friend "Get" methods before making friends
SELECT get_user_friend_requests ('fake');
SELECT get_user_friend_requests ('swag@swag');
SELECT get_user_friend_requests ('yo@yo');
SELECT get_user_friend_requests ('tim@tim');
SELECT get_user_friend_requests ('lit@lit');
SELECT get_user_friend_requests ('kk@kk');

SELECT get_user_friends ('fake');
SELECT get_user_friends ('swag@swag');
SELECT get_user_friends ('yo@yo');
SELECT get_user_friends ('tim@tim');
SELECT get_user_friends ('lit@lit');
SELECT get_user_friends ('kk@kk');

SELECT get_user_potential_friends ('fake');
SELECT get_user_potential_friends ('swag@swag');
SELECT get_user_potential_friends ('yo@yo');
SELECT get_user_potential_friends ('tim@tim');
SELECT get_user_potential_friends ('lit@lit');
SELECT get_user_potential_friends ('kk@kk');


-- Add Friends
-- send friend requests . . .
CALL set_user_friend_status ('fake', 'lit@lit', 'accepted');
CALL set_user_friend_status ('yo@yo', 'dank', 'accepted');
CALL set_user_friend_status ('tim@tim', 'lit@lit', 'accepted');
CALL set_user_friend_status ('yo@yo', 'lolz@lolz', 'accepted');
CALL set_user_friend_status ('lolz@lolz', 'yo@yo', 'rejected');
CALL set_user_friend_status ('tim@tim', 'lolz@lolz', 'accepted');
CALL set_user_friend_status ('tim@tim', 'jam@jam', 'accepted');
CALL set_user_friend_status ('tim@tim', 'mc@mc', 'accepted');
CALL set_user_friend_status ('tx@tx', 'tim@tim', 'accepted');
CALL set_user_friend_status ('kk@kk', 'omg@omg', 'accepted');
CALL set_user_friend_status ('kk@kk', 'lit@lit', 'accepted');
CALL set_user_friend_status ('yo@yo', 'lit@lit', 'accepted');
CALL set_user_friend_status ('um@um', 'lit@lit', 'accepted');
CALL set_user_friend_status ('kk@kk', 'lit@lit', 'rejected');
CALL set_user_friend_status ('kk@kk', 'lit@lit', 'rejected');
CALL set_user_friend_status ('kk@kk', 'lit@lit', 'accepted');
CALL set_user_friend_status ('omg@omg', 'lit@lit', 'accepted');

-- reply to friend requests . . .
CALL set_user_friend_status ('jam@jam', 'tim@tim', 'accepted');
CALL set_user_friend_status ('lit@lit', 'tim@tim', 'rejected');
CALL set_user_friend_status ('mc@mc', 'tim@tim' 'accepted');
CALL set_user_friend_status ('mc@mc', 'tim@tim', 'rejected');
CALL set_user_friend_status ('mc@mc', 'tim@tim', 'rejected');
CALL set_user_friend_status ('lit@lit', 'kk@kk', 'accepted');
CALL set_user_friend_status ('lit@lit', 'kk@kk', 'rejected');
CALL set_user_friend_status ('lit@lit', 'kk@kk', 'accepted');
CALL set_user_friend_status ('lit@lit', 'yo@yo', 'accepted');
CALL set_user_friend_status ('lolz@lolz', 'tim@tim', 'accepted');



-- Test Friend "Get" methods after making friends
SELECT get_user_friend_requests ('fake');
SELECT get_user_friend_requests ('tim@tim');
SELECT get_user_friend_requests ('lolz@lolz');
SELECT get_user_friend_requests ('wut@wut');
SELECT get_user_friend_requests ('okay@okay');
SELECT get_user_friend_requests ('omg@omg');
SELECT get_user_friend_requests ('jk@jk');
SELECT get_user_friend_requests ('kk@kk');
SELECT get_user_friend_requests ('jam@jam');
SELECT get_user_friend_requests ('mc@mc');
SELECT get_user_friend_requests ('swag@swag');
SELECT get_user_friend_requests ('yo@yo');
SELECT get_user_friend_requests ('tx@tx');
SELECT get_user_friend_requests ('um@um');
SELECT get_user_friend_requests ('jank@jank');
SELECT get_user_friend_requests ('lit@lit');

SELECT get_user_friends ('fake');
SELECT get_user_friends ('tim@tim');
SELECT get_user_friends ('lolz@lolz');
SELECT get_user_friends ('wut@wut');
SELECT get_user_friends ('okay@okay');
SELECT get_user_friends ('omg@omg');
SELECT get_user_friends ('jk@jk');
SELECT get_user_friends ('kk@kk');
SELECT get_user_friends ('jam@jam');
SELECT get_user_friends ('mc@mc');
SELECT get_user_friends ('swag@swag');
SELECT get_user_friends ('yo@yo');
SELECT get_user_friends ('tx@tx');
SELECT get_user_friends ('um@um');
SELECT get_user_friends ('jank@jank');
SELECT get_user_friends ('lit@lit');

SELECT get_user_potential_friends ('fake');
SELECT get_user_potential_friends ('tim@tim');
SELECT get_user_potential_friends ('lolz@lolz');
SELECT get_user_potential_friends ('wut@wut');
SELECT get_user_potential_friends ('okay@okay');
SELECT get_user_potential_friends ('omg@omg');
SELECT get_user_potential_friends ('jk@jk');
SELECT get_user_potential_friends ('kk@kk');
SELECT get_user_potential_friends ('jam@jam');
SELECT get_user_potential_friends ('mc@mc');
SELECT get_user_potential_friends ('swag@swag');
SELECT get_user_potential_friends ('yo@yo');
SELECT get_user_potential_friends ('tx@tx');
SELECT get_user_potential_friends ('um@um');
SELECT get_user_potential_friends ('jank@jank');
SELECT get_user_potential_friends ('lit@lit');

