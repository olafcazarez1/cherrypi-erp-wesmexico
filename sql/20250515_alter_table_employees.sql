ALTER TABLE `employees` ADD `internal_code` char(32) default '' AFTER `code`;

ALTER TABLE `employees` ADD `blood_type` ENUM("NA", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-") NOT NULL DEFAULT 'NA' AFTER `gender`;
ALTER TABLE `employees` ADD `marital_status` ENUM("single", "married", "divorced", "widowed", "separated", "concubinage") NOT NULL DEFAULT 'single' AFTER `blood_type`;
ALTER TABLE `employees` ADD `education_level` ENUM("none", "primary", "secondary", "high_school", "associate", "bachelor", "master", "doctorate") NOT NULL DEFAULT 'none' AFTER `marital_status`;

ALTER TABLE `employees` ADD `has_medical_insurance` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 AFTER `has_license`;
ALTER TABLE `employees` ADD `has_infonavit_credit` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 AFTER `has_medical_insurance`;
ALTER TABLE `employees` ADD `has_fonacot_credit` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 AFTER `has_infonavit_credit`;
ALTER TABLE `employees` ADD `has_alergies` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 AFTER `has_fonacot_credit`;
ALTER TABLE `employees` ADD `alergies` TEXT NOT NULL DEFAULT ("") AFTER `has_alergies`;
ALTER TABLE `employees` ADD `has_medical_conditions` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 AFTER `has_alergies`;
ALTER TABLE `employees` ADD `medical_conditions` TEXT NOT NULL DEFAULT ("") AFTER `has_medical_conditions`;

ALTER TABLE `employees`DROP KEY `employees_ibfk_3`;
ALTER TABLE `employees`DROP KEY `employees_ibfk_4`;
ALTER TABLE `employees`DROP KEY `employees_ibfk_5`;

ALTER TABLE `employees` CHANGE `department` `department_id` char(36) default '';
ALTER TABLE `employees` CHANGE `work_position` `work_position_id` char(36) default '';
ALTER TABLE `employees` CHANGE `work_area` `work_area_id` char(36) default '';

ALTER TABLE `employees` ADD FOREIGN KEY ( `department_id`) REFERENCES `categories`( `category_id`);
ALTER TABLE `employees` ADD FOREIGN KEY ( `work_position_id`) REFERENCES `categories`( `category_id`);
ALTER TABLE `employees` ADD FOREIGN KEY ( `work_area_id`) REFERENCES `categories`( `category_id`);

ALTER TABLE `employees` DROP `ssn`;
