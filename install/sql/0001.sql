BEGIN;
--
-- Create model Device
--
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img1" varchar(100) NOT NULL, "img2" varchar(100) NOT NULL, "img3" varchar(100) NOT NULL, "img4" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"));
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
COMMIT;
