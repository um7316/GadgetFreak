BEGIN;
--
-- Rename field img1 on device to img_1
--
ALTER TABLE "gadgetfreak_web_device" RENAME TO "gadgetfreak_web_device__old";
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "img_1" varchar(100) NOT NULL, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img2" varchar(100) NOT NULL, "img3" varchar(100) NOT NULL, "img4" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"));
INSERT INTO "gadgetfreak_web_device" ("author_id", "img_1", "description", "title", "img3", "img2", "id", "img4") SELECT "author_id", "img1", "description", "title", "img3", "img2", "id", "img4" FROM "gadgetfreak_web_device__old";
DROP TABLE "gadgetfreak_web_device__old";
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
--
-- Remove field img2 from device
--
ALTER TABLE "gadgetfreak_web_device" RENAME TO "gadgetfreak_web_device__old";
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img_1" varchar(100) NOT NULL, "img3" varchar(100) NOT NULL, "img4" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"));
INSERT INTO "gadgetfreak_web_device" ("img_1", "description", "title", "img3", "author_id", "id", "img4") SELECT "img_1", "description", "title", "img3", "author_id", "id", "img4" FROM "gadgetfreak_web_device__old";
DROP TABLE "gadgetfreak_web_device__old";
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
--
-- Remove field img3 from device
--
ALTER TABLE "gadgetfreak_web_device" RENAME TO "gadgetfreak_web_device__old";
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img_1" varchar(100) NOT NULL, "img4" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"));
INSERT INTO "gadgetfreak_web_device" ("img_1", "description", "title", "author_id", "id", "img4") SELECT "img_1", "description", "title", "author_id", "id", "img4" FROM "gadgetfreak_web_device__old";
DROP TABLE "gadgetfreak_web_device__old";
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
--
-- Remove field img4 from device
--
ALTER TABLE "gadgetfreak_web_device" RENAME TO "gadgetfreak_web_device__old";
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img_1" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"));
INSERT INTO "gadgetfreak_web_device" ("img_1", "description", "title", "author_id", "id") SELECT "img_1", "description", "title", "author_id", "id" FROM "gadgetfreak_web_device__old";
DROP TABLE "gadgetfreak_web_device__old";
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
--
-- Add field img_2 to device
--
ALTER TABLE "gadgetfreak_web_device" RENAME TO "gadgetfreak_web_device__old";
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img_1" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"), "img_2" varchar(100) NULL);
INSERT INTO "gadgetfreak_web_device" ("img_1", "description", "img_2", "title", "author_id", "id") SELECT "img_1", "description", NULL, "title", "author_id", "id" FROM "gadgetfreak_web_device__old";
DROP TABLE "gadgetfreak_web_device__old";
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
--
-- Add field img_3 to device
--
ALTER TABLE "gadgetfreak_web_device" RENAME TO "gadgetfreak_web_device__old";
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img_1" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"), "img_2" varchar(100) NULL, "img_3" varchar(100) NULL);
INSERT INTO "gadgetfreak_web_device" ("img_1", "description", "img_3", "img_2", "title", "author_id", "id") SELECT "img_1", "description", NULL, "img_2", "title", "author_id", "id" FROM "gadgetfreak_web_device__old";
DROP TABLE "gadgetfreak_web_device__old";
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
--
-- Add field img_4 to device
--
ALTER TABLE "gadgetfreak_web_device" RENAME TO "gadgetfreak_web_device__old";
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img_1" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"), "img_2" varchar(100) NULL, "img_3" varchar(100) NULL, "img_4" varchar(100) NULL);
INSERT INTO "gadgetfreak_web_device" ("img_4", "img_1", "description", "img_3", "img_2", "title", "author_id", "id") SELECT NULL, "img_1", "description", "img_3", "img_2", "title", "author_id", "id" FROM "gadgetfreak_web_device__old";
DROP TABLE "gadgetfreak_web_device__old";
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
--
-- Add field img_thumb to device
--
ALTER TABLE "gadgetfreak_web_device" RENAME TO "gadgetfreak_web_device__old";
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img_1" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"), "img_2" varchar(100) NULL, "img_3" varchar(100) NULL, "img_4" varchar(100) NULL, "img_thumb" varchar(100) NULL);
INSERT INTO "gadgetfreak_web_device" ("img_4", "img_1", "description", "img_3", "img_2", "title", "img_thumb", "author_id", "id") SELECT "img_4", "img_1", "description", "img_3", "img_2", "title", NULL, "author_id", "id" FROM "gadgetfreak_web_device__old";
DROP TABLE "gadgetfreak_web_device__old";
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
--
-- Add field score to device
--
ALTER TABLE "gadgetfreak_web_device" RENAME TO "gadgetfreak_web_device__old";
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img_1" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"), "img_2" varchar(100) NULL, "img_3" varchar(100) NULL, "img_4" varchar(100) NULL, "img_thumb" varchar(100) NULL, "score" decimal NOT NULL);
INSERT INTO "gadgetfreak_web_device" ("img_4", "img_1", "description", "img_3", "img_2", "title", "score", "img_thumb", "author_id", "id") SELECT "img_4", "img_1", "description", "img_3", "img_2", "title", '0.0', "img_thumb", "author_id", "id" FROM "gadgetfreak_web_device__old";
DROP TABLE "gadgetfreak_web_device__old";
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
COMMIT;
