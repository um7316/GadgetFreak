BEGIN;
--
-- Remove field img_thumb from device
--
ALTER TABLE "gadgetfreak_web_device" RENAME TO "gadgetfreak_web_device__old";
CREATE TABLE "gadgetfreak_web_device" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "img_1" varchar(100) NOT NULL, "author_id" integer NULL REFERENCES "auth_user" ("id"), "img_2" varchar(100) NULL, "img_3" varchar(100) NULL, "img_4" varchar(100) NULL, "score" decimal NOT NULL);
INSERT INTO "gadgetfreak_web_device" ("img_4", "img_1", "description", "img_3", "img_2", "title", "score", "author_id", "id") SELECT "img_4", "img_1", "description", "img_3", "img_2", "title", "score", "author_id", "id" FROM "gadgetfreak_web_device__old";
DROP TABLE "gadgetfreak_web_device__old";
CREATE INDEX "gadgetfreak_web_device_4f331e2f" ON "gadgetfreak_web_device" ("author_id");
COMMIT;
