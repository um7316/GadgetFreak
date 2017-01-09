BEGIN;
--
-- Add field author to forumtopic
--
ALTER TABLE "gadgetfreak_web_forumtopic" RENAME TO "gadgetfreak_web_forumtopic__old";
CREATE TABLE "gadgetfreak_web_forumtopic" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "author_id" integer NOT NULL REFERENCES "auth_user" ("id"), "name" varchar(100) NOT NULL, "topic_type" varchar(1) NOT NULL, "image" varchar(100) NULL, "score" decimal NULL, "contents" text NOT NULL, "date" datetime NOT NULL, "device_id" integer NOT NULL REFERENCES "gadgetfreak_web_device" ("id"));
INSERT INTO "gadgetfreak_web_forumtopic" ("name", "image", "topic_type", "score", "date", "author_id", "id", "contents", "device_id") SELECT "name", "image", "topic_type", "score", "date", 1, "id", "contents", "device_id" FROM "gadgetfreak_web_forumtopic__old";
DROP TABLE "gadgetfreak_web_forumtopic__old";
CREATE INDEX "gadgetfreak_web_forumtopic_4f331e2f" ON "gadgetfreak_web_forumtopic" ("author_id");
CREATE INDEX "gadgetfreak_web_forumtopic_9379346c" ON "gadgetfreak_web_forumtopic" ("device_id");
COMMIT;
