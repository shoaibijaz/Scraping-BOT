/*
Navicat PGSQL Data Transfer

Source Server         : Local
Source Server Version : 90404
Source Host           : localhost:5432
Source Database       : gumtree
Source Schema         : public

Target Server Type    : PGSQL
Target Server Version : 90404
File Encoding         : 65001

Date: 2017-01-29 23:10:20
*/


-- ----------------------------
-- Table structure for app_websites
-- ----------------------------
DROP TABLE IF EXISTS "public"."app_websites";
CREATE TABLE "public"."app_websites" (
"id" int4 DEFAULT nextval('app_websites_id_seq'::regclass) NOT NULL,
"name" text COLLATE "default",
"url" text COLLATE "default",
"function" text COLLATE "default",
"search_url" text COLLATE "default",
"country" text COLLATE "default",
"comment_url" text COLLATE "default",
"order" int4
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Records of app_websites
-- ----------------------------
INSERT INTO "public"."app_websites" VALUES ('1', 'Gumtree Singapore', 'https://www.gumtree.sg/', 'gumtree_1', 'https://www.gumtree.sg/s-{search}/page-{page}/v1q0p{page}', 'Singapore', 'https://www.gumtree.sg/rui-api/page/reply/model/en_SG', '1');
INSERT INTO "public"."app_websites" VALUES ('2', 'Gumtree Ireland', 'https://www.gumtree.ie/', 'gumtree_1', 'https://www.gumtree.ie/s-{search}/page-{page}/v1q0p{page}', 'Ireland', 'https://www.gumtree.ie/rui-api/page/reply/model/en_IE', '2');
INSERT INTO "public"."app_websites" VALUES ('3', 'Gumtree South Africa', 'https://www.gumtree.co.za/', 'gumtree_1', 'https://www.gumtree.co.za/s-{search}/page-{page}/v1q0p{page}', 'South Africa', 'https://www.gumtree.co.za/rui-api/page/reply/model/en_ZA', '3');
INSERT INTO "public"."app_websites" VALUES ('4', 'Gumtree UK', 'https://www.gumtree.com/', 'gumtree_2', 'https://www.gumtree.com/search?search_category=all&search_location=uk&q={search}&page={page}', 'UK', null, '5');
INSERT INTO "public"."app_websites" VALUES ('5', 'Gumtree Australia', 'http://www.gumtree.com.au/', 'gumtree_3', 'http://www.gumtree.com.au/s-search/page-{page}/k0?categoryRedirected=true', 'Australia', null, '4');
INSERT INTO "public"."app_websites" VALUES ('6', 'Locanto Singapore', 'http://singapore.locanto.sg/q', 'locanto', '{url}/?query={search}&page={page}', 'Singapore', null, '6');

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table app_websites
-- ----------------------------
ALTER TABLE "public"."app_websites" ADD PRIMARY KEY ("id");
