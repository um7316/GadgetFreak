BEGIN;
--
-- Create model Comment
--
CREATE TABLE "gadgetfreak_web_comment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "contents" text NOT NULL, "date" datetime NOT NULL, "author_id" integer NOT NULL REFERENCES "auth_user" ("id"), "forum_topic_id" integer NOT NULL REFERENCES "gadgetfreak_web_forumtopic" ("id"));
CREATE INDEX "gadgetfreak_web_comment_4f331e2f" ON "gadgetfreak_web_comment" ("author_id");
CREATE INDEX "gadgetfreak_web_comment_2716e151" ON "gadgetfreak_web_comment" ("forum_topic_id");
COMMIT;
