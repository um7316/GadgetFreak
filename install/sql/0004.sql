BEGIN;
--
-- Create model UserProfile
--
CREATE TABLE "gadgetfreak_web_userprofile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "profile_img" varchar(100) NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id"));
COMMIT;
