BEGIN;
--
-- Create model TechnicalSpecification
--
CREATE TABLE "gadgetfreak_web_technicalspecification" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "value" varchar(100) NOT NULL, "device_id" integer NOT NULL REFERENCES "gadgetfreak_web_device" ("id"));
CREATE INDEX "gadgetfreak_web_technicalspecification_9379346c" ON "gadgetfreak_web_technicalspecification" ("device_id");
COMMIT;
