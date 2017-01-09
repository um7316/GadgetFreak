BEGIN;
--
-- Create model ForumTopic
--
CREATE TABLE "gadgetfreak_web_forumtopic" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "topic_type" varchar(1) NOT NULL, "image" varchar(100) NULL, "score" decimal NULL, "contents" text NOT NULL, "date" datetime NOT NULL, "device_id" integer NOT NULL REFERENCES "gadgetfreak_web_device" ("id"));
CREATE INDEX "gadgetfreak_web_forumtopic_9379346c" ON "gadgetfreak_web_forumtopic" ("device_id");
COMMIT;
