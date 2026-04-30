
CREATE TABLE `assets` (
	`asset_id` CHAR(36) NOT NULL DEFAULT '',
	`name` CHAR(64) NOT NULL DEFAULT '',
	`caption` CHAR(128) NOT NULL DEFAULT '',
	`path` VARCHAR(1024) DEFAULT '',
	`type` CHAR(64) NOT NULL DEFAULT '',
	`height` int UNSIGNED DEFAULT 0,
	`width` int UNSIGNED DEFAULT 0,
	`size` bigint UNSIGNED DEFAULT 0,
	`status` ENUM('active', 'inactive', 'deleted') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`asset_id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `images_and_documents` (
	`transaction_id` CHAR(36) NOT NULL,
	`document_id` CHAR(64) NOT NULL,
	`origin` CHAR(64) NOT NULL,
	`path` VARCHAR(1024) NOT NULL DEFAULT '',
	`index` int NOT NULL DEFAULT 0,
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`transaction_id`, `document_id`),
	KEY `document_id` (`document_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `series` (
	`serie_id` CHAR(128) PRIMARY KEY,
	`reference` CHAR(128) NOT NULL DEFAULT '',
	`key` CHAR(36) NOT NULL DEFAULT '',
	`prefix` CHAR(10) NOT NULL DEFAULT '',
	`index` int NOT NULL DEFAULT 0,
	`description` CHAR(64) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	INDEX (`reference`, `serie_id`),
	UNIQUE KEY (`reference`, `key`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `users` (
	`user_id` char(36) NOT NULL DEFAULT '',
	`name` char(127) NOT NULL DEFAULT '',
	`email` char(127) NOT NULL DEFAULT '',
	`password` char(32) NOT NULL DEFAULT '',
	`type` char(32) NOT NULL DEFAULT 'admin',
	`is_verified` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`status` enum('active', 'inactive') not null default 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`user_id`),
	UNIQUE KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `users_tokens` (
	`user_id` char(36) NOT NULL DEFAULT '',
	`token_id` char(36) NOT NULL DEFAULT '',
	`status` enum('active', 'inactive') not null default 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`user_id`, `token_id`),
	FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `verification_codes` (
	`secure_id` char(36) NOT NULL DEFAULT '',
	`user_id` char(36) NOT NULL DEFAULT '',
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`secure_id`),
	KEY `user_id` (`user_id`,`secure_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `customs_offices` (
	`custom_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(255) NOT NULL DEFAULT '',
	`type` ENUM('land','maritime','air','inland') NOT NULL,
	`state` CHAR(64) NOT NULL DEFAULT '',
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`custom_id`),
	UNIQUE KEY (`code`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `categories` (
	`category_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(128) NOT NULL DEFAULT '',
	`type` ENUM('products', 'services', 'work-position', 'work-area', 'clients', 'contractors', 'suppliers', 'department') NOT NULL DEFAULT 'products',
	`weight` int(5) DEFAULT 0,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`category_id`),
	UNIQUE KEY (`type`, `code`),
	UNIQUE KEY (`type`, `name`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `subcategories` (
	`category_id` CHAR(36) NOT NULL DEFAULT '',
	`subcategory_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(128) NOT NULL DEFAULT '',
	`weight` int(5) DEFAULT 0,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`category_id`, `subcategory_id`),
	UNIQUE KEY (`category_id`, `code`),
	UNIQUE KEY (`category_id`, `name`),
	FOREIGN KEY (`category_id`) REFERENCES `categories`(`category_id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `companies` (
	`company_id` char(36) PRIMARY KEY,
	`tax_regime_id` CHAR(36) NOT NULL DEFAULT '',
	`code` char(32) default '',
	`legal_name` char(120) NOT NULL default '',
	`trade_name` char(120) NOT NULL default '',
	`serie` char(4) NOT NULL DEFAULT '',
	`address_street` char(60) not null,
	`address_external_number` char(10) not null,
	`address_internal_number` char(10) not null,
	`neighborhood` char(60) not null,
	`state_id` char(36) not null,
	`municipality_id` char(36) not null,
	`locality_id` char(36) not null,
	`zip` int(10) NOT NULL DEFAULT '0',
	`taxpayer_id` char(14) not null default '',
	`phone` char(10) NOT NULL DEFAULT '',
	`logo` VARCHAR(1024) NOT NULL DEFAULT '',
	`timezone` char(64) NOT NULL DEFAULT '',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	FOREIGN KEY ( `state_id`, `municipality_id`, `locality_id`) REFERENCES `localities`( `state_id`, `municipality_id`, `locality_id`),
	INDEX `status` (`status`),
	unique key(`code`),
	unique key(`legal_name`),
	unique key(`taxpayer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `branch_offices` (
	`company_id` char(36) NOT NULL DEFAULT '',
	`branch_id` char(36) PRIMARY KEY,
	`code` char(32) default '',
	`name` char(120) NOT NULL default '',
	`type` enum('main','office') NOT NULL DEFAULT 'main',
	`serie` char(4) NOT NULL DEFAULT '',
	`address_street` char(60) not null,
	`address_external_number` char(10) not null,
	`address_internal_number` char(10) not null,
	`neighborhood` char(60) not null,
	`state_id` char(36) not null,
	`municipality_id` char(36) not null,
	`locality_id` char(36) not null,
	`zip` int(10) NOT NULL DEFAULT '0',
	`taxpayer_id` char(14) not null default '',
	`phone` char(10) NOT NULL DEFAULT '',
	`timezone` char(64) NOT NULL DEFAULT '',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	INDEX `status` (`status`),
	unique key(`company_id`, `code`),
	unique key(`company_id`, `name`),
	FOREIGN KEY (`company_id`) REFERENCES `companies`(`company_id`),
	FOREIGN KEY ( `state_id`, `municipality_id`, `locality_id`) REFERENCES `localities`( `state_id`, `municipality_id`, `locality_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table `bank_accounts` (
	`bank_account_id` char(36) PRIMARY KEY NOT NULL DEFAULT '',
	`associated_id` char(36) NOT NULL DEFAULT '',
	`code` char(32) not null default '',
	`associated_with` ENUM('company', 'contractor', 'client', 'supplier', 'employee', 'division') default 'company',
	`internal_code` char(5) not null default '',
	`bank_id` char(36) NOT NULL DEFAULT '',
	`bank_code` char(36) NOT NULL DEFAULT '',
	`bank_name` char(255) NOT NULL DEFAULT '',
	`description` char(128) not null default '',
	`currency` char(3) not null default 'mxn',
	`account_number` char(18) NOT NULL DEFAULT '',
	`card_number` char(16) NOT NULL DEFAULT '',
	`interbank_key` char(18) NOT NULL DEFAULT '',
	`reference` char(10) NOT NULL DEFAULT '',
	`balance` double not null default 0.00,
	`type` ENUM('generic', 'virtual') NOT NULL DEFAULT 'generic',
	`is_default` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	UNIQUE KEY (`associated_with`, `associated_id`, `code`),
	INDEX (`associated_with`, `associated_id`)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `employees` (
	`company_id` char(36) NOT NULL DEFAULT '',
	`branch_id` char(36) NOT NULL DEFAULT '',
	`employee_id` char(36) PRIMARY KEY,
	`code` char(32) default '',
	`internal_code` char(32) default '',
	`names` char(120) NOT NULL default '',
	`first_last_name` char(60) NOT NULL default '',
	`second_last_name` char(60) NOT NULL default '',
	`birthday` DATE NOT NULL DEFAULT '1900-01-01',
	`gender` ENUM('male', 'female') NOT NULL DEFAULT 'male',
	`blood_type` ENUM("NA", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-") NOT NULL DEFAULT 'NA',
	`marital_status` ENUM("single", "married", "divorced", "widowed", "separated", "concubinage") NOT NULL DEFAULT 'single',
	`education_level` enum('none','primary','secondary','high_school','associate','bachelor','master','doctorate') NOT NULL DEFAULT 'none',
	`taxpayer_id` char(32) default '',
	`federal_id` char(32) default '',
	`ssn` char(32) default '',
	`department_id` char(36) NOT NULL DEFAULT '',
	`work_area_id` char(36) NOT NULL default '',
	`work_position_id` char(36) NOT NULL default '',
	`email` char(127) NOT NULL default '',
	`phone` char(10) NOT NULL DEFAULT '',
	`cell_phone` char(10) NOT NULL DEFAULT '',
	`address_street` char(60) not null,
	`address_external_number` char(10) not null,
	`address_internal_number` char(10) not null,
	`neighborhood` char(60) not null,
	`state_id` char(36) not null,
	`municipality_id` char(36) not null,
	`locality_id` char(36) not null,
	`zip` int(10) NOT NULL DEFAULT 0,
	`has_license` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`has_medical_insurance` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`has_infonavit_credit` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`has_fonacot_credit` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`has_alergies` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`alergies` TEXT NOT NULL DEFAULT (""),
	`has_medical_conditions` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`medical_conditions` TEXT NOT NULL DEFAULT (""),
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	unique key(`code`),
	INDEX `status` (`status`),
	FOREIGN KEY (`company_id`) REFERENCES `companies`(`company_id`),
	FOREIGN KEY (`branch_id`) REFERENCES `branch_offices`(`branch_id`),
	FOREIGN KEY ( `department_id`) REFERENCES `categories`( `category_id`),
	FOREIGN KEY ( `work_position_id`) REFERENCES `categories`( `category_id`),
	FOREIGN KEY ( `work_area_id`) REFERENCES `categories`( `category_id`),
	FOREIGN KEY ( `state_id`, `municipality_id`, `locality_id`) REFERENCES `localities`( `state_id`, `municipality_id`, `locality_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `employees_driving_licenses` (
	`employee_id` char(36) PRIMARY KEY NOT NULL DEFAULT '',
	`type` char(10) NOT NULL DEFAULT '',
	`number` char(20) NOT NULL DEFAULT '',
	`issuing_agency` char(64) NOT NULL DEFAULT '',
	`place_of_issue` char(64) NOT NULL DEFAULT '',
	`document` VARCHAR(1024) NOT NULL DEFAULT '',
	`expedition_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`expiration_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (`employee_id`) REFERENCES `employees`( `employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `employees_medicals_insurances` (
	`employee_id` char(36) PRIMARY KEY NOT NULL DEFAULT '',
	`number` char(20) NOT NULL DEFAULT '',
	`hospital` VARCHAR(512) NOT NULL DEFAULT '',
	`document` VARCHAR(1024) NOT NULL DEFAULT '',
	`withdrawal` ENUM('na', 'resignation', 'dismissal') NOT NULL DEFAULT 'na',
	`start_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`leave_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`reason_for_withdrawal` VARCHAR(1024) not null default '',
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (`employee_id`) REFERENCES `employees`( `employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `employees_infonavit_credits` (
	`employee_id` char(36) PRIMARY KEY NOT NULL DEFAULT '',
	`reference` char(20) NOT NULL DEFAULT '',
	`amount` double not null default 0.00,
	`document` VARCHAR(1024) NOT NULL DEFAULT '',
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (`employee_id`) REFERENCES `employees`( `employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `employees_fonacot_credits` (
	`employee_id` char(36) PRIMARY KEY NOT NULL DEFAULT '',
	`reference` char(20) NOT NULL DEFAULT '',
	`amount` double not null default 0.00,
	`document` VARCHAR(1024) NOT NULL DEFAULT '',
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (`employee_id`) REFERENCES `employees`( `employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `employees_relatives` (
	`employee_id` char(36) PRIMARY KEY,
	`relative_id` char(36) NOT NULL DEFAULT '',
	`names` char(120) NOT NULL default '',
	`first_last_name` char(60) NOT NULL default '',
	`second_last_name` char(60) NOT NULL default '',
	`cell_phone` char(10) NOT NULL DEFAULT '',
	`relation` char(60) not null DEFAULT 'na',
	`emergency` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,	
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (`employee_id`) REFERENCES `employees`( `employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `users_employees` (
	`user_id` char(36) PRIMARY KEY,
	`employee_id` char(36) NOT NULL DEFAULT '',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (`user_id`) REFERENCES `users`( `user_id`),
	FOREIGN KEY (`employee_id`) REFERENCES `employees`( `employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `warehouses` (
	`warehouse_id` char(36) NOT NULL,
	`code` char(32) not null default '',
	`name` char(120) NOT NULL,
	`image` VARCHAR(1024) NOT NULL DEFAULT '',
	`type` enum('main','store','mobile','virtual') NOT NULL DEFAULT 'main',
	`weight` int(5) DEFAULT 0,
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	PRIMARY KEY (`warehouse_id`),
	unique key(`code`),
	unique key( `name` ),
	KEY `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table `branch_offices_warehouses` (
	`branch_id` char(36) not null default '',
	`warehouse_id` char(36) not null default '',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	primary key(`branch_id`, `warehouse_id`),
	FOREIGN KEY(`branch_id`) REFERENCES `branch_offices`(`branch_id`),
	FOREIGN KEY(`warehouse_id`) REFERENCES `warehouses`(`warehouse_id`)
) engine=innodb default CHARSET=utf8;

create table `clients`(
	`client_id` char(36) primary key,
	`category_id` char(36) NOT NULL DEFAULT '',
	`code` char(32) default '',
	`legal_name`char(120) not null,
	`trade_name` char(120) not null,
	`address_street` char(60) not null,
	`address_external_number` char(10) not null,
	`address_internal_number` char(10) not null,
	`neighborhood` char(60) default '',
	`state_id` char(36) default '',
	`municipality_id` char(36) default '',
	`locality_id` char(36) not null,
	`zip` int(10) not null default 0,
	`taxpayer_id` char(14) not null default '',
	`tax_regime_id` CHAR(36) NOT NULL DEFAULT '',
	`email` char(127) not null default '',
	`phone` char(10) not null default '',
	`cell_phone` char(10) NOT NULL DEFAULT '',
	`references` VARCHAR(512) not null default '',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	`status` enum('active', 'inactive') not null default 'active',
	unique key(`code`),
	-- unique key(`taxpayer_id`),
	index (`status`),
	FOREIGN KEY ( `category_id` ) REFERENCES `categories`( `category_id` ),
	FOREIGN KEY ( `state_id`, `municipality_id`, `locality_id`) REFERENCES `localities`( `state_id`, `municipality_id`, `locality_id`)	
) engine=innodb default CHARSET=utf8;

CREATE TABLE `clients_contacts` (
	`client_id` char(36) NOT NULL DEFAULT '',
	`contact_id` char(36) NOT NULL DEFAULT '',
	`code` char(32) default '',
	`name` char(120) NOT NULL,
	`position` char(120) NOT NULL,
	`email` char(127) NOT NULL,
	`phone` char(10) NOT NULL DEFAULT "",
	`extension` char(5) NOT NULL DEFAULT  "",
	`cell_phone` char(10) NOT NULL DEFAULT "",
	`updated_by` char(64) not null default '',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	PRIMARY KEY(`client_id`, `contact_id`),
	FOREIGN KEY(`client_id`) REFERENCES `clients`(`client_id`) ON DELETE CASCADE,
	INDEX `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table `suppliers`(
	`supplier_id` char(36) primary key,
	`category_id` char(36) NOT NULL DEFAULT '',
	`code` char(32) default '',
	`legal_name`char(120) not null,
	`trade_name` char(120) not null,
	`address_street` char(60) not null,
	`address_external_number` char(10) not null,
	`address_internal_number` char(10) not null,
	`neighborhood` char(60) default '',
	`state_id` char(36) default '',
	`municipality_id` char(36) default '',
	`locality_id` char(36) not null,
	`zip` int(10) not null default 0,
	`taxpayer_id` char(14) not null default '',
	`tax_regime_id` CHAR(36) NOT NULL DEFAULT '',
	`email` char(127) not null default '',
	`phone` char(10) not null default '',
	`cell_phone` char(10) NOT NULL DEFAULT '',
	`references` VARCHAR(512) not null default '',
	`status` enum('active', 'inactive') not null default 'active',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	unique key(`code`),
	unique key(`taxpayer_id`),
	index (`status`),
	FOREIGN KEY ( `category_id` ) REFERENCES `categories`( `category_id` ),
	FOREIGN KEY ( `state_id`, `municipality_id`, `locality_id`) REFERENCES `localities`( `state_id`, `municipality_id`, `locality_id`)	
) engine=innodb default CHARSET=utf8;

CREATE TABLE `suppliers_contacts` (
	`supplier_id` char(36) NOT NULL DEFAULT '',
	`contact_id` char(36) NOT NULL DEFAULT '',
	`code` char(32) default '',
	`name` char(120) NOT NULL,
	`position` char(120) NOT NULL,
	`email` char(127) NOT NULL,
	`phone` char(10) NOT NULL DEFAULT "",
	`extension` char(5) NOT NULL DEFAULT  "",
	`cell_phone` char(10) NOT NULL DEFAULT "",
	`updated_by` char(64) not null default '',
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	PRIMARY KEY(`supplier_id`, `contact_id`),
	FOREIGN KEY(`supplier_id`) REFERENCES `suppliers`(`supplier_id`) ON DELETE CASCADE,
	INDEX `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `suppliers_settings` (
	`supplier_id` char(36) PRIMARY KEY NOT NULL DEFAULT '',
	`freight_included` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`notes` VARCHAR(2048) NOT NULL DEFAULT '',
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (`supplier_id`) REFERENCES `suppliers`( `supplier_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table `contractors`(
	`contractor_id` char(36) primary key,
	`category_id` char(36) NOT NULL DEFAULT '',
	`code` char(32) default '',
	`legal_name`char(120) not null,
	`trade_name` char(120) not null,
	`address_street` char(60) not null,
	`address_external_number` char(10) not null,
	`address_internal_number` char(10) not null,
	`neighborhood` char(60) default '',
	`state_id` char(36) default '',
	`municipality_id` char(36) default '',
	`locality_id` char(36) not null,
	`zip` int(10) not null default 0,
	`taxpayer_id` char(14) not null default '',
	`tax_regime_id` CHAR(36) NOT NULL DEFAULT '',
	`email` char(127) not null default '',
	`phone` char(10) not null default '',
	`cell_phone` char(10) NOT NULL DEFAULT '',
	`references` VARCHAR(512) not null default '',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	`status` enum('active', 'inactive') not null default 'active',
	unique key(`code`),
	unique key(`taxpayer_id`),
	index (`status`),
	FOREIGN KEY ( `category_id` ) REFERENCES `categories`( `category_id` ),
	FOREIGN KEY ( `state_id`, `municipality_id`, `locality_id`) REFERENCES `localities`( `state_id`, `municipality_id`, `locality_id`)	
) engine=innodb default CHARSET=utf8;

CREATE TABLE `contractors_contacts` (
	`contractor_id` char(36) NOT NULL DEFAULT '',
	`contact_id` char(36) NOT NULL DEFAULT '',
	`code` char(32) default '',
	`name` char(120) NOT NULL,
	`position` char(120) NOT NULL,
	`email` char(127) NOT NULL,
	`phone` char(10) NOT NULL DEFAULT "",
	`extension` char(5) NOT NULL DEFAULT  "",
	`cell_phone` char(10) NOT NULL DEFAULT "",
	`updated_by` char(64) not null default '',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	PRIMARY KEY(`contractor_id`, `contact_id`),
	FOREIGN KEY(`contractor_id`) REFERENCES `contractors`(`contractor_id`) ON DELETE CASCADE,
	INDEX `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table `companies_bank_accounts` (
	`company_id` char(36) NOT NULL DEFAULT '',
	`bank_account_id` char(36) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY(`company_id`, `bank_account_id`),
	UNIQUE(`bank_account_id`),
	FOREIGN KEY (`company_id`) REFERENCES `companies`(`company_id`),
	FOREIGN KEY (`bank_account_id`) REFERENCES `bank_accounts`(`bank_account_id`)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table `contractors_bank_accounts` (
	`contractor_id` char(36) NOT NULL DEFAULT '',
	`bank_account_id` char(36) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY(`contractor_id`, `bank_account_id`),
	UNIQUE(`bank_account_id`),
	FOREIGN KEY (`contractor_id`) REFERENCES `contractors`(`contractor_id`),
	FOREIGN KEY (`bank_account_id`) REFERENCES `bank_accounts`(`bank_account_id`)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table `clients_bank_accounts` (
	`client_id` char(36) NOT NULL DEFAULT '',
	`bank_account_id` char(36) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY(`client_id`, `bank_account_id`),
	UNIQUE(`bank_account_id`),
	FOREIGN KEY (`client_id`) REFERENCES `clients`(`client_id`),
	FOREIGN KEY (`bank_account_id`) REFERENCES `bank_accounts`(`bank_account_id`)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table `employees_bank_accounts` (
	`employee_id` char(36) NOT NULL DEFAULT '',
	`bank_account_id` char(36) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY(`employee_id`, `bank_account_id`),
	UNIQUE(`bank_account_id`),
	FOREIGN KEY (`employee_id`) REFERENCES `employees`(`employee_id`),
	FOREIGN KEY (`bank_account_id`) REFERENCES `bank_accounts`(`bank_account_id`)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table `suppliers_bank_accounts` (
	`supplier_id` char(36) NOT NULL DEFAULT '',
	`bank_account_id` char(36) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY(`supplier_id`, `bank_account_id`),
	UNIQUE(`bank_account_id`),
	FOREIGN KEY (`supplier_id`) REFERENCES `suppliers`(`supplier_id`),
	FOREIGN KEY (`bank_account_id`) REFERENCES `bank_accounts`(`bank_account_id`)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `measures` (
	`measure_id` CHAR(36) PRIMARY KEY,
	`external_reference` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) NOT NULL DEFAULT '',
	`name` CHAR(32) NOT NULL DEFAULT '',
	`weight` int(3) unsigned NOT NULL DEFAULT 99,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	unique key(`code`),
	unique index( `name` ),
	KEY `status` (`status`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `taxes` (
	`tax_id` CHAR(36) PRIMARY KEY,
	`code` CHAR(32) NOT NULL DEFAULT '',
	`name` CHAR(32) NOT NULL DEFAULT '',
	`percent` DOUBLE NOT NULL DEFAULT 0.0,
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	unique key(`code`),
	unique index( `name` ),
	KEY `status` (`status`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `brands` (
	`brand_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(128) NOT NULL DEFAULT '',
	`type` enum('product','car') NOT NULL DEFAULT 'product',
	`weight` int(5) DEFAULT 0,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`brand_id`),
	UNIQUE KEY `name` (`type`,`name`),
	UNIQUE KEY `code` (`type`,`code`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `models` (
	`brand_id` CHAR(36) NOT NULL DEFAULT '',
	`model_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(128) NOT NULL DEFAULT '',
	`weight` int(5) DEFAULT 0,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`brand_id`, `model_id`),
	UNIQUE KEY (`brand_id`, `code`),
	UNIQUE KEY (`brand_id`, `name`),
	FOREIGN KEY (`brand_id`) REFERENCES `brands`(`brand_id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `versions` (
	`brand_id` CHAR(36) NOT NULL DEFAULT '',
	`model_id` CHAR(36) NOT NULL DEFAULT '',
	`version_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(128) NOT NULL DEFAULT '',
	`weight` int(5) DEFAULT 0,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`brand_id`, `model_id`, `version_id`),
	UNIQUE KEY (`brand_id`, `model_id`, `code`),
	UNIQUE KEY (`brand_id`, `model_id`, `name`),
	FOREIGN KEY (`brand_id`, `model_id`) REFERENCES `models`(`brand_id`, `model_id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;


CREATE TABLE `products` (
	`product_id` CHAR(36) PRIMARY KEY,
	`brand_id` CHAR(36) NOT NULL DEFAULT '',
	`model_id` CHAR(36) NOT NULL DEFAULT '',
	`category_id` CHAR(36) NOT NULL DEFAULT '',
	`subcategory_id` CHAR(36) NOT NULL DEFAULT '',
	`external_reference` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) NOT NULL DEFAULT '',
	`name` VARCHAR(512) NOT NULL DEFAULT '',
	`short_name` CHAR(128) NOT NULL DEFAULT '',
	`description` VARCHAR(1048) NOT NULL DEFAULT '',
	`image` VARCHAR(1024) NOT NULL DEFAULT '',
	`currency` CHAR(3) NOT NULL DEFAULT 'mxn',
	`type` ENUM( 'product', 'service', 'material' ) NOT NULL DEFAULT 'product',
	`has_units` tinyint(1) NOT NULL DEFAULT 0,
	`is_imported` tinyint(1) NOT NULL DEFAULT 0,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	UNIQUE KEY `code`(`type`, `code`),
	UNIQUE KEY `name`(`type`, `name` ),
	FOREIGN KEY( `category_id`, `subcategory_id`) REFERENCES `subcategories`(`category_id`, `subcategory_id`),
	FOREIGN KEY( `brand_id`, `model_id`) REFERENCES `models`(`brand_id`, `model_id`),
	index (`status`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

create table `products_measures` (
	`product_id` char(36) not null default '',
	`measure_id` char(36) not null default '',
	`external_reference` CHAR(36) NOT NULL DEFAULT '',
	`equivalence` int(5) unsigned not null default 1,
	`default` int(1) unsigned not null default 0,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	primary key(`product_id`, `measure_id`),
	FOREIGN KEY(`product_id`) REFERENCES `products`(`product_id`),
	FOREIGN KEY(`measure_id`) REFERENCES `measures`(`measure_id`)
) engine=innodb default CHARSET=utf8;

create table `products_taxes` (
	`product_id` char(36) not null default '',
	`tax_id` char(36) not null default '',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	primary key(`product_id`, `tax_id`),
	FOREIGN KEY(`product_id`) REFERENCES `products`(`product_id`),
	FOREIGN KEY(`tax_id`) REFERENCES `taxes`(`tax_id`)
) engine=innodb default CHARSET=utf8;

create table `products_related` (
	`product_id` char(36) not null default '',
	`item_id` char(36) not null default '',
	`measure_id` char(36) not null default '',
	`quantity` int unsigned not null default 1,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	primary key(`product_id`, `item_id`, `measure_id`),
	FOREIGN KEY(`product_id`) REFERENCES `products`(`product_id`),
	FOREIGN KEY(`item_id`) REFERENCES `products`(`product_id`),
	FOREIGN KEY(`measure_id`) REFERENCES `measures`(`measure_id`)
) engine=innodb default CHARSET=utf8;

CREATE TABLE `products_units` (
	`product_id` CHAR(36) NOT NULL DEFAULT '',
	`unit_id` CHAR(36) NOT NULL DEFAULT '',
	`company_id` CHAR(36) NOT NULL DEFAULT '',
	`department_id` CHAR(36) NOT NULL DEFAULT '',
	`brand_id` CHAR(36) NOT NULL DEFAULT '',
	`model_id` CHAR(36) NOT NULL DEFAULT '',
	`version_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) NOT NULL DEFAULT '',
	`serie` CHAR(64) NOT NULL DEFAULT '',
	`reference` CHAR(64) NOT NULL DEFAULT '',
	`uid` CHAR(64) NOT NULL DEFAULT '',
	`description` VARCHAR(1024) NOT NULL DEFAULT '',
	`importation_number` char(20) not null default '',
	`importation_date` timestamp not null default '1980-01-01 00:00:00',
	`custom_id`  char(36) not null default '00',
	`status` enum('active','damage','assigned','sold','delivered','disposal','inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY (`product_id`, `unit_id`),
	UNIQUE KEY `code`(`product_id`, `code`),
	UNIQUE KEY `uid`(`product_id`, `uid` ),
	FOREIGN KEY(`product_id`) REFERENCES `products`(`product_id`),
	FOREIGN KEY(`company_id`) REFERENCES `companies`(`company_id`),
	FOREIGN KEY( `brand_id`, `model_id`, `version_id`) REFERENCES `versions`(`brand_id`, `model_id`, `version_id`),
	FOREIGN KEY (`company_id`) REFERENCES `companies`(`company_id`),
	FOREIGN KEY ( `department_id`) REFERENCES `categories`( `category_id`),
	index (`status`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

create table `stocks` (
	`warehouse_id` char(36) not null,
	`product_id` char(36) not null,
	`measure_id` char(36) not null,
	`price` double not null default 0.00,
	`discount` double not null default 0.00,
	`quantity` double not null default 0.00,
	`status` enum('active', 'inactive') not null default 'active',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	primary key ( `warehouse_id`, `product_id`, `measure_id` ),
	foreign key (`warehouse_id`) references `warehouses`(`warehouse_id`),
	foreign key (`product_id`, `measure_id`) references `products_measures`(`product_id`, `measure_id`)
) engine=innodb default CHARSET=utf8;

create table `stocks_io` (
	`stock_io_id` char(36) primary key not null default '',
	`user_id` char(36) not null default '',
	`employee_id` char(36) not null default '',
	`company_id` char(36) not null default '',
	`branch_id` char(36) not null default '',
	`warehouse_id` char(36) not null default '',
	`supplier_id` char(36) not null default '',
	`code` char(32) not null default '',
	`reference` char(36) not null default '',
	`transaction_type` enum('credit', 'cash') DEFAULT 'cash',
	`document_type` enum( 'sale_note', 'sale_invoice' ) default 'sale_note',
	`currency` char(4) not null default 'mxn',
	`exchange_rate` double not null default 0.00,
	`amount` double not null default 0.00,
	`discount` double not null default 0.00,
	`tax` double not null default 0.00, 
	`subtotal` double not null default 0.00,
	`total` double not null default 0.00,
	`purchase_origin` enum( 'national', 'international' ) default 'national',
	`importation_number` char(20) not null default '',
	`importation_date` timestamp not null default '1980-01-01 00:00:00',
	`custom_id`  char(36) not null default '00',
	`type` enum( 'purchases', 'input', 'output', 'declines', 'losses' ) default 'purchases',
	`transaction_date` timestamp not null default '2000-01-01 00:00:00',
	`payment_type` char(36) not null default '',
	`payment_method` char(36) not null default '',
	`tax_receipt` char(36) not null default '',
	`notes` VARCHAR(1024) not null default '',
	`status` enum('active', 'canceled') not null default 'active',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	unique key(`supplier_id`, `type`, `reference`),
	unique key(`code`),
	foreign key (`user_id`) references `users`(`user_id`),
	foreign key (`employee_id`) references `employees`(`employee_id`),
	FOREIGN KEY (`supplier_id`) REFERENCES `suppliers`(`supplier_id`),   
	foreign key (`company_id`) references `companies`(`company_id`),
	foreign key (`branch_id`) references `branch_offices`(`branch_id`),
	foreign key (`warehouse_id`) references `warehouses`(`warehouse_id`),
	foreign key (`custom_id`) references `customs_offices`(`custom_id`),
	index (`status`)
) engine=innodb default CHARSET=utf8;

CREATE TABLE `stocks_io_products_taxes` (
	`stock_io_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`tax_id` CHAR(36) NOT NULL,
	`percent` DOUBLE NOT NULL DEFAULT '0',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`stock_io_id`, `product_id`, `tax_id`),
	KEY `product_id` (`product_id`),
	KEY `tax_id` (`tax_id`),
	FOREIGN KEY (`stock_io_id`) REFERENCES `stocks_io` (`stock_io_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `tax_id`) REFERENCES `products_taxes` (`product_id`, `tax_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

create table `stocks_io_details` (
	`stock_io_id` char(36),
	`product_id` char(36) not null,
	`measure_id` char(36) not null,
	`currency` char(4) not null default 'mxn',
	`quantity` double not null default 0.00,
	`price` DOUBLE NOT NULL DEFAULT 0.00,
	`subtotal` DOUBLE NOT NULL DEFAULT 0.00,
	`discount` DOUBLE NOT NULL DEFAULT 0.00,
	`tax` DOUBLE NOT NULL DEFAULT 0.00,
	`total` DOUBLE NOT NULL DEFAULT 0.00,
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	primary key ( `stock_io_id`, `product_id`, `measure_id` ),
	foreign key (`stock_io_id`) references `stocks_io`(`stock_io_id`),
	foreign key (`product_id`) references `products`(`product_id`),
	foreign key (`measure_id`) references `measures`(`measure_id`)
) engine=innodb default charset=utf8;

create table `stocks_io_products_units` (
	`stock_io_id` char(36) not null default "",
	`product_id` char(36) not null default "",
	`measure_id` char(36) not null default "",
	`unit_id` char(36) not null default "",
	`uid` CHAR(64) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	primary key ( `stock_io_id`, `product_id`, `measure_id`,`unit_id` ),
	foreign key (`stock_io_id`, `product_id`, `measure_id`) references `stocks_io_details`(`stock_io_id`, `product_id`, `measure_id`),
	foreign key (`product_id`, `unit_id`) references `products_units`(`product_id`, `unit_id`),
	foreign key (`measure_id`) references `measures`(`measure_id`)
) engine=innodb default charset=utf8;


CREATE TABLE `quotes_documents` (
	`quote_id` CHAR(36) NOT NULL,
	`company_id` CHAR(36) NOT NULL,
	`branch_id` CHAR(36) NOT NULL,
	`warehouse_id` CHAR(36) NOT NULL,
	`client_id` CHAR(36) NOT NULL,
	`user_id` CHAR(36) NOT NULL,
	`seller_id` CHAR(36) NOT NULL,
	`code` CHAR(32) DEFAULT '',
	`currency` CHAR(4) NOT NULL DEFAULT 'mxn',
	`exchange_rate` DOUBLE NOT NULL DEFAULT 1.00,
	`amount` DOUBLE NOT NULL DEFAULT 0.00,
	`discount` DOUBLE NOT NULL DEFAULT 0.00,
	`subtotal` DOUBLE NOT NULL DEFAULT 0.00,
	`taxes` DOUBLE NOT NULL DEFAULT 0.00,
	`total` DOUBLE NOT NULL DEFAULT 0.00,
	`transaction_method` ENUM('cash', 'debit_card', 'credit_card', 'mixed') DEFAULT 'cash',
	`transaction_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`notes` VARCHAR(2048) not null default '',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY (`quote_id`),
	UNIQUE KEY (`code`),
	FOREIGN KEY (`company_id`) REFERENCES `companies`(`company_id`),
	FOREIGN KEY (`branch_id`, `warehouse_id`) REFERENCES `branch_offices_warehouses`(`branch_id`, `warehouse_id`),
	FOREIGN KEY (`client_id`) REFERENCES `clients`(`client_id`),
	foreign key (`user_id`) REFERENCES `users`(`user_id`),
	foreign key (`seller_id`) REFERENCES `employees`(`employee_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `quotes_documents_products_taxes` (
	`quote_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`tax_id` CHAR(36) NOT NULL,
	`percent` DOUBLE NOT NULL DEFAULT '0',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`quote_id`, `product_id`, `tax_id`),
	KEY `product_id` (`product_id`),
	KEY `tax_id` (`tax_id`),
	FOREIGN KEY (`quote_id`) REFERENCES `quotes_documents` (`quote_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `tax_id`) REFERENCES `products_taxes` (`product_id`, `tax_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `quotes_documents_details` (
	`quote_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`measure_id` CHAR(36) NOT NULL,
	`currency` CHAR(4) NOT NULL DEFAULT 'mxn',
	`quantity` DOUBLE NOT NULL DEFAULT 0.00,
	`original_price` DOUBLE NOT NULL DEFAULT 0.00,
	`discount_factor` DOUBLE NOT NULL DEFAULT 0.00,
	`price` DOUBLE NOT NULL DEFAULT 0.00,
	`amount` DOUBLE NOT NULL DEFAULT 0.00,
	`subtotal` DOUBLE NOT NULL DEFAULT 0.00,
	`discount` DOUBLE NOT NULL DEFAULT 0.00,
	`taxes` DOUBLE NOT NULL DEFAULT 0.00,
	`total` DOUBLE NOT NULL DEFAULT 0.00,
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`quote_id`, `product_id`,`measure_id`),
	KEY `product_id` (`product_id`),
	KEY `measure_id` (`measure_id`),
	FOREIGN KEY (`quote_id`) REFERENCES `quotes_documents` (`quote_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `measure_id`) REFERENCES `products_measures` (`product_id`, `measure_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `sales_documents` (
	`document_id` CHAR(36) NOT NULL,
	`company_id` CHAR(36) NOT NULL,
	`branch_id` CHAR(36) NOT NULL,
	`warehouse_id` CHAR(36) NOT NULL,
	`seller_id` CHAR(36) NOT NULL,
	`client_id` CHAR(36) NOT NULL,
	`user_id` CHAR(36) NOT NULL,
	`code` CHAR(32) DEFAULT '',
	`currency` CHAR(4) NOT NULL DEFAULT 'mxn',
	`exchange_rate` DOUBLE NOT NULL DEFAULT 1.00,
	`amount` DOUBLE NOT NULL DEFAULT 0.00,
	`subtotal` DOUBLE NOT NULL DEFAULT 0.00,
	`discount` DOUBLE NOT NULL DEFAULT 0.00,
	`taxes` DOUBLE NOT NULL DEFAULT 0.00,
	`total` DOUBLE NOT NULL DEFAULT 0.00,
	`requires_invoice` TINYINT(1) NOT NULL DEFAULT 0,
	`payment_status` ENUM('pending','paid') NOT NULL DEFAULT 'pending',
	`payment_type_id` CHAR(36) NOT NULL DEFAULT 'PUE',
	`payment_method_id` CHAR(36) NOT NULL DEFAULT '99',
	`fiscal_use_id` CHAR(36) NOT NULL DEFAULT 'G03',
	`transaction_method` ENUM('cash', 'debit_card', 'credit_card', 'mixed') DEFAULT 'cash',
	`transaction_type` ENUM('full_payment', 'payment_in_installments') DEFAULT 'full_payment',
	`transaction_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`transaction_status` ENUM('pending', 'paid') DEFAULT 'pending',
	`is_signed` tinyint(1) NOT NULL DEFAULT 0,
	`notes` varchar(512) NOT NULL DEFAULT '',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY (`document_id`),
	UNIQUE KEY (`company_id`, `code`),
	FOREIGN KEY (`company_id`) REFERENCES `companies`(`company_id`),
	FOREIGN KEY (`branch_id`, `warehouse_id`) REFERENCES `branch_offices_warehouses`(`branch_id`, `warehouse_id`),
	FOREIGN KEY (`client_id`) REFERENCES `clients`(`client_id`),
	foreign key (`user_id`) REFERENCES `users`(`user_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `sales_documents_products_taxes` (
	`document_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`tax_id` CHAR(36) NOT NULL,
	`percent` DOUBLE NOT NULL DEFAULT '0',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`document_id`, `product_id`, `tax_id`),
	KEY `product_id` (`product_id`),
	KEY `tax_id` (`tax_id`),
	FOREIGN KEY (`document_id`) REFERENCES `sales_documents` (`document_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `tax_id`) REFERENCES `products_taxes` (`product_id`, `tax_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `sales_documents_details` (
	`document_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`measure_id` CHAR(36) NOT NULL,
	`currency` CHAR(4) NOT NULL DEFAULT 'mxn',
	`quantity` DOUBLE NOT NULL DEFAULT 0.00,
	`original_price` DOUBLE NOT NULL DEFAULT 0.00,
	`discount_factor` DOUBLE NOT NULL DEFAULT 0.00,
	`price` DOUBLE NOT NULL DEFAULT 0.00,
	`amount` DOUBLE NOT NULL DEFAULT 0.00,
	`subtotal` DOUBLE NOT NULL DEFAULT 0.00,
	`discount` DOUBLE NOT NULL DEFAULT 0.00,
	`taxes` DOUBLE NOT NULL DEFAULT 0.00,
	`total` DOUBLE NOT NULL DEFAULT 0.00,
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`document_id`, `product_id`,`measure_id`),
	KEY `product_id` (`product_id`),
	KEY `measure_id` (`measure_id`),
	FOREIGN KEY (`document_id`) REFERENCES `sales_documents` (`document_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `measure_id`) REFERENCES `products_measures` (`product_id`, `measure_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;


create table `sales_documents_products_units` (
	`document_id` char(36) not null default "",
	`product_id` char(36) not null default "",
	`measure_id` char(36) not null default "",
	`unit_id` char(36) not null default "",
	`uid` CHAR(64) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	primary key ( `document_id`, `product_id`, `measure_id`,`unit_id` ),
	foreign key (`document_id`) references `sales_documents`(`document_id`),
	foreign key (`product_id`, `unit_id`) references `products_units`(`product_id`, `unit_id`),
	foreign key (`measure_id`) references `measures`(`measure_id`)
) engine=innodb default charset=utf8;

create table `sales_documents_payments` (
	`payment_id` char(36) PRIMARY KEY,
	`document_id` char(36) NOT NULL,
	`branch_id` CHAR(36) NOT NULL,
	-- `register_id` CHAR(36) NOT NULL,
	`user_id` CHAR(36) NOT NULL,
	`reference` CHAR(32) DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`serie` int(10) unsigned DEFAULT 0,
	`payment_method` char(36) not null default '',
	`pay_with` DOUBLE NOT NULL DEFAULT 0.00,
	`change` DOUBLE NOT NULL DEFAULT 0.00,
	`previous_balance` double not null default 0.00,
	`amount` double not null default 0.00,
	`balance` double not null default 0.00,
	`currency` char(4) not null default 'mxn',
	`exchange_rate` double not null default 1.00,
	`transaction_date` timestamp not null default '2000-01-01 00:00:00',
	`is_signed` tinyint(1) NOT NULL DEFAULT 0,
	`status` enum('active', 'inactive') not null default 'active',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	UNIQUE KEY ( `code` ),
	UNIQUE KEY ( `document_id`, `serie` ),
	KEY (`document_id`, `payment_id`),
	FOREIGN KEY (`document_id`) REFERENCES `sales_documents` (`document_id`),
	FOREIGN KEY (`branch_id`) REFERENCES `branch_offices`(`branch_id`),
	FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
) engine=innodb default CHARSET=utf8;


CREATE TABLE `invoiced_documents` (
	`invoice_id` CHAR(36) NOT NULL,
	`company_id` char(36) NOT NULL,
	`branch_id` CHAR(36) NOT NULL,
	`warehouse_id` CHAR(36) NOT NULL,
	`client_id` CHAR(36) NOT NULL,
	`user_id` CHAR(36) NOT NULL,
	`payment_type_id` char(36) not null,
	`payment_method_id` char(36) not null,
	`receipt_type_id` char(36) not null,
	`code` CHAR(32) DEFAULT '',
	`currency` CHAR(4) NOT NULL DEFAULT 'mxn',
	`exchange_rate` DOUBLE NOT NULL DEFAULT 1.00,
	`amount` double NOT NULL DEFAULT 0,
	`subtotal` DOUBLE NOT NULL DEFAULT 0.00,
	`discount` DOUBLE NOT NULL DEFAULT 0.00,
	`taxes` DOUBLE NOT NULL DEFAULT 0.00,
	`total` DOUBLE NOT NULL DEFAULT 0.00,
	`transaction_method` ENUM('cash', 'credit_card', 'debit_card', 'transfer', 'other') DEFAULT 'cash',
	`transaction_type` ENUM('full_payment', 'payment_in_installments') DEFAULT 'full_payment',
	`transaction_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`transaction_status` ENUM('pending', 'paid') DEFAULT 'pending',
	`is_global` tinyint(1) NOT NULL DEFAULT 0,
	`status` ENUM('pending', 'signed', 'cancellation_requested', 'cancelled') NOT NULL DEFAULT 'pending',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY (`invoice_id`),
	UNIQUE KEY (`company_id`, `code`),
	FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`),
	FOREIGN KEY (`branch_id`, `warehouse_id`) REFERENCES `branch_offices_warehouses`(`branch_id`, `warehouse_id`),
	FOREIGN KEY (`client_id`) REFERENCES `clients`(`client_id`),
	foreign key (`user_id`) REFERENCES `users`(`user_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `invoiced_documents_products` (
	`invoice_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`measure_id` CHAR(36) NOT NULL,
	`currency` CHAR(4) NOT NULL DEFAULT 'mxn',
	`quantity` DOUBLE NOT NULL DEFAULT 0.00,
	`original_price` DOUBLE NOT NULL DEFAULT 0.00,
	`discount_factor` DOUBLE NOT NULL DEFAULT 0.00,
	`price` DOUBLE NOT NULL DEFAULT 0.00,
	`amount` double NOT NULL DEFAULT 0,
	`subtotal` DOUBLE NOT NULL DEFAULT 0.00,
	`discount` DOUBLE NOT NULL DEFAULT 0.00,
	`taxes` DOUBLE NOT NULL DEFAULT 0.00,
	`total` DOUBLE NOT NULL DEFAULT 0.00,
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`invoice_id`, `product_id`,`measure_id`),
	KEY `product_id` (`product_id`),
	KEY `measure_id` (`measure_id`),
	FOREIGN KEY (`invoice_id`) REFERENCES `invoiced_documents` (`invoice_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `measure_id`) REFERENCES `products_measures` (`product_id`, `measure_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `invoiced_documents_products_taxes` (
	`invoice_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`tax_id` CHAR(36) NOT NULL,
	`percent` DOUBLE NOT NULL DEFAULT '0',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`invoice_id`, `product_id`, `tax_id`),
	KEY `product_id` (`product_id`),
	KEY `tax_id` (`tax_id`),
	FOREIGN KEY (`invoice_id`) REFERENCES `invoiced_documents` (`invoice_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `tax_id`) REFERENCES `products_taxes` (`product_id`, `tax_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `documents_invoices` (
	`invoice_id` CHAR(36) NOT NULL,
	`document_id` CHAR(36) NOT NULL,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`invoice_id`, `document_id`),
	FOREIGN KEY (`invoice_id`) REFERENCES `invoiced_documents` (`invoice_id`),
	FOREIGN KEY (`document_id`) REFERENCES `sales_documents` (`document_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `divisions` (
	`division_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(128) NOT NULL DEFAULT '',
	`weight` int(5) DEFAULT 0,
	`value` double not null default 0.00,
	`is_global` tinyint(1) NOT NULL DEFAULT 0,
	`is_fixed` tinyint(1) NOT NULL DEFAULT 0,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`division_id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `subdivisions` (
	`division_id` CHAR(36) NOT NULL DEFAULT '',
	`subdivision_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(128) NOT NULL DEFAULT '',
	`weight` int(5) DEFAULT 0,
	`value` double not null default 0.00,
	`is_fixed` tinyint(1) NOT NULL DEFAULT 0,
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`division_id`, `subdivision_id`),
	UNIQUE KEY (`division_id`, `code`),
	UNIQUE KEY (`division_id`, `name`),
	FOREIGN KEY (`division_id`) REFERENCES `divisions`(`division_id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `concepts` (
	`division_id` CHAR(36) NOT NULL DEFAULT '',
	`subdivision_id` CHAR(36) NOT NULL DEFAULT '',
	`concept_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(128) NOT NULL DEFAULT '',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`concept_id`),
	FOREIGN KEY (`division_id`, `subdivision_id`) REFERENCES `subdivisions`(`division_id`, `subdivision_id`),
	UNIQUE KEY (`code`),
	UNIQUE KEY (`name`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `subconcepts` (
	`concept_id` CHAR(36) NOT NULL DEFAULT '',
	`subconcept_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(128) NOT NULL DEFAULT '',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`subconcept_id`),
	FOREIGN KEY (`concept_id`) REFERENCES `concepts`(`concept_id`),
	UNIQUE KEY (`concept_id`, `code`),
	UNIQUE KEY (`concept_id`, `name`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

create table `subconcepts_taxes` (
	`subconcept_id` char(36) not null default '',
	`tax_id` char(36) not null default '',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp not null default '2000-01-01 00:00:00',
	`updated_at` timestamp not null default current_timestamp on update current_timestamp ,
	primary key(`subconcept_id`, `tax_id`),
	FOREIGN KEY(`subconcept_id`) REFERENCES `subconcepts`(`subconcept_id`),
	FOREIGN KEY(`tax_id`) REFERENCES `taxes`(`tax_id`)
) engine=innodb default CHARSET=utf8;

CREATE TABLE `products_assignments` (
	`assignment_id` CHAR(36) NOT NULL,
	`user_id` CHAR(36) NOT NULL,
	-- `assigned_by` CHAR(36) NOT NULL,
	`company_id` char(36) not null default '',
	`branch_id` char(36) not null default '',
	`warehouse_id` char(36) not null default '',
	`employee_id` CHAR(36) NOT NULL,
	`department_id` char(36) NOT NULL DEFAULT '',
	`work_area_id` char(36) NOT NULL default '',
	`code` CHAR(32) DEFAULT '',
	`type` ENUM('assignment', 'return') DEFAULT 'assignment',
	`notes` VARCHAR(512) not null default '',
	`transaction_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY (`assignment_id`),
	UNIQUE KEY (`code`),
	FOREIGN KEY (`company_id`) REFERENCES `companies`(`company_id`),
	FOREIGN KEY (`branch_id`, `warehouse_id`) REFERENCES `branch_offices_warehouses`(`branch_id`, `warehouse_id`),
	FOREIGN KEY (`employee_id`) REFERENCES `employees`(`employee_id`),
	FOREIGN KEY ( `department_id`) REFERENCES `categories`( `category_id`),
	FOREIGN KEY ( `work_area_id`) REFERENCES `categories`( `category_id`),
	foreign key (`user_id`) REFERENCES `users`(`user_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

create table `products_assignments_items` (
	`assignment_id` char(36),
	`product_id` char(36) not null,
	`measure_id` char(36) not null,
	`quantity` double not null default 0.00,
	`type` ENUM('assignment', 'return') DEFAULT 'assignment',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	primary key ( `assignment_id`, `product_id`, `measure_id` ),
	foreign key (`assignment_id`) references `products_assignments`(`assignment_id`),
	foreign key (`product_id`) references `products`(`product_id`),
	foreign key (`measure_id`) references `measures`(`measure_id`)
) engine=innodb default charset=utf8;

CREATE TABLE `products_assignments_documents` (
	`assignment_id` CHAR(36) NOT NULL,
	`document_id` CHAR(36) NOT NULL,
	`path` VARCHAR(1024) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`assignment_id`, `document_id`),
	KEY `document_id` (`document_id`),
	FOREIGN KEY (`assignment_id`) REFERENCES `products_assignments` (`assignment_id`) ON DELETE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `products_units_assignments` (
	`assignment_id` CHAR(36) NOT NULL,
	`user_id` CHAR(36) NOT NULL,
	-- `warehouse_id` CHAR(36) NOT NULL,
	`employee_id` CHAR(36) NOT NULL,
	`department_id` char(36) NOT NULL DEFAULT '',
	`work_area_id` char(36) NOT NULL default '',
	`code` CHAR(32) DEFAULT '',
	`type` ENUM('assignment', 'return') DEFAULT 'assignment',
	`notes` VARCHAR(512) not null default '',
	`transaction_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY (`assignment_id`),
	UNIQUE KEY (`code`),
	FOREIGN KEY (`employee_id`) REFERENCES `employees`(`employee_id`),
	FOREIGN KEY ( `department_id`) REFERENCES `categories`( `category_id`),
	FOREIGN KEY ( `work_position_id`) REFERENCES `categories`( `category_id`),
	foreign key (`user_id`) REFERENCES `users`(`user_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `products_units_assignments_details` (
	`assignment_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`unit_id` CHAR(36) NOT NULL,
	`type` ENUM('assignment', 'return') DEFAULT 'assignment',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`assignment_id`, `product_id`, `unit_id`),
	KEY `product_id` (`product_id`, `unit_id`),
	FOREIGN KEY (`assignment_id`) REFERENCES `products_units_assignments` (`assignment_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `unit_id`) REFERENCES `products_units` (`product_id`, `unit_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `products_units_assignments_documents` (
	`assignment_id` CHAR(36) NOT NULL,
	`document_id` CHAR(36) NOT NULL,
	`path` VARCHAR(1024) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`assignment_id`, `document_id`),
	KEY `document_id` (`document_id`),
	FOREIGN KEY (`assignment_id`) REFERENCES `products_units_assignments` (`assignment_id`) ON DELETE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `employees_products` (
	`employee_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`measure_id` CHAR(36) NOT NULL,
	`quantity` DOUBLE NOT NULL DEFAULT 0.00,
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`employee_id`, `product_id`, `measure_id`),
	KEY `product_id` (`product_id`, `measure_id`),
	FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE CASCADE,
	foreign key (`product_id`) references `products`(`product_id`),
	foreign key (`measure_id`) references `measures`(`measure_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `products_units_assignments` (
	`assignment_id` CHAR(36) NOT NULL,
	`user_id` CHAR(36) NOT NULL,
	-- `warehouse_id` CHAR(36) NOT NULL,
	`employee_id` CHAR(36) NOT NULL,
	`department_id` char(36) NOT NULL DEFAULT '',
	`work_area_id` char(36) NOT NULL default '',
	`code` CHAR(32) DEFAULT '',
	`type` ENUM('assignment', 'return') DEFAULT 'assignment',
	`notes` VARCHAR(512) not null default '',
	`transaction_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY (`assignment_id`),
	UNIQUE KEY (`code`),
	FOREIGN KEY (`employee_id`) REFERENCES `employees`(`employee_id`),
	FOREIGN KEY ( `department_id`) REFERENCES `categories`( `category_id`),
	FOREIGN KEY ( `work_area_id`) REFERENCES `categories`( `category_id`),
	foreign key (`user_id`) REFERENCES `users`(`user_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `products_units_assignments_details` (
	`assignment_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`unit_id` CHAR(36) NOT NULL,
	`type` ENUM('assignment', 'return') DEFAULT 'assignment',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`assignment_id`, `product_id`, `unit_id`),
	KEY `product_id` (`product_id`, `unit_id`),
	FOREIGN KEY (`assignment_id`) REFERENCES `products_units_assignments` (`assignment_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `unit_id`) REFERENCES `products_units` (`product_id`, `unit_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `products_units_assignments_documents` (
	`assignment_id` CHAR(36) NOT NULL,
	`document_id` CHAR(36) NOT NULL,
	`path` VARCHAR(1024) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`assignment_id`, `document_id`),
	KEY `document_id` (`document_id`),
	FOREIGN KEY (`assignment_id`) REFERENCES `products_units_assignments` (`assignment_id`) ON DELETE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=UTF8;


CREATE TABLE `employees_products_units` (
	`employee_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`unit_id` CHAR(36) NOT NULL,
	`status` ENUM('assigned', 'returned') DEFAULT 'assigned',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`employee_id`, `product_id`, `unit_id`),
	KEY `product_id` (`product_id`, `unit_id`),
	FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `unit_id`) REFERENCES `products_units` (`product_id`, `unit_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `products_units_invoices` (
	`product_id` CHAR(36) NOT NULL DEFAULT '',
	`unit_id` CHAR(36) NOT NULL DEFAULT '',
	`folio` char(16) NOT NULL DEFAULT '',
	`agency` char(128) NOT NULL DEFAULT '',
	`client` char(128) NOT NULL DEFAULT '',
	`taxpayer_id` char(20) NOT NULL DEFAULT '',
	`total` DOUBLE NOT NULL DEFAULT 0.00,
	`document` VARCHAR(1024) NOT NULL DEFAULT '',
	`expedition_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`product_id`, `unit_id`),
	FOREIGN KEY(`product_id`) REFERENCES `products`(`product_id`),
	FOREIGN KEY(`product_id`, `unit_id`) REFERENCES `products_units`(`product_id`, `unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `products_units_specs` (
	`product_id` CHAR(36) NOT NULL DEFAULT '',
	`unit_id` CHAR(36) NOT NULL DEFAULT '',
	`spec_id` CHAR(36) NOT NULL DEFAULT '',
	`index` INT UNSIGNED NOT NULL DEFAULT 0,
	`reference` char(64) NOT NULL DEFAULT '',
	`value` char(128) NOT NULL DEFAULT '',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`product_id`, `unit_id`, `spec_id`),
	UNIQUE KEY (`unit_id`, `reference`),
	FOREIGN KEY(`product_id`) REFERENCES `products`(`product_id`),
	FOREIGN KEY(`product_id`, `unit_id`) REFERENCES `products_units`(`product_id`, `unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `products_units_notifications_configs` (
	`product_id` CHAR(36) NOT NULL DEFAULT '',
	`unit_id` CHAR(36) NOT NULL DEFAULT '',
	`per_mileage` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`mileage` DOUBLE NOT NULL DEFAULT 0.00,
	`per_days` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`days` DOUBLE NOT NULL DEFAULT 0.00,
	`per_hours` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
	`hours` DOUBLE NOT NULL DEFAULT 0.00,
	`status` CHAR(64) NOT NULL DEFAULT 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY(`unit_id`),
	INDEX(`product_id`, `unit_id`),
	FOREIGN KEY(`product_id`) REFERENCES `products`(`product_id`),
	FOREIGN KEY(`product_id`, `unit_id`) REFERENCES `products_units`(`product_id`, `unit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `units_maintenances` (
	`maintenance_id` CHAR(36) NOT NULL,
	`user_id` CHAR(36) NOT NULL,
	`employee_id` CHAR(36) NOT NULL,
	`supplier_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL DEFAULT '',
	`unit_id` CHAR(36) NOT NULL DEFAULT '',
	`brand_id` CHAR(36) NOT NULL DEFAULT '',
	`model_id` CHAR(36) NOT NULL DEFAULT '',
	`version_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`appointment_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`type` CHAR(64) NOT NULL DEFAULT 'undefined',
	`reason` CHAR(64) NOT NULL DEFAULT 'undefined',
	`tax` double not null default 0.00, 
	`subtotal` double not null default 0.00,
	`total` double not null default 0.00,
	`notes` VARCHAR(512) not null default '',
	`status` ENUM('todo', 'in-progress', 'done', 'cancelled', 'postponed') NOT NULL DEFAULT 'todo',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY (`maintenance_id`),
	UNIQUE KEY (`code`),
	FOREIGN KEY (`employee_id`) REFERENCES `employees`(`employee_id`),
	FOREIGN KEY (`supplier_id`) REFERENCES `suppliers`(`supplier_id`),
	FOREIGN KEY (`product_id`, `unit_id`) REFERENCES `products_units`(`product_id`, `unit_id`),
	foreign key (`user_id`) REFERENCES `users`(`user_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;



CREATE TABLE `sales_deliveries_orders` (
	`order_id` CHAR(36) NOT NULL,
	`document_id` CHAR(36) NOT NULL,
	`company_id` CHAR(36) NOT NULL,
	`branch_id` CHAR(36) NOT NULL,
	`warehouse_id` CHAR(36) NOT NULL,
	`client_id` CHAR(36) NOT NULL,
	`user_id` CHAR(36) NOT NULL,
	`worker_id` CHAR(36) NOT NULL,
	`code` CHAR(32) DEFAULT '',
	`transaction_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`notes` varchar(512) NOT NULL DEFAULT '',
	`status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
	PRIMARY KEY (`order_id`),
	UNIQUE KEY (`code`),
	FOREIGN KEY (`document_id`) REFERENCES `sales_documents`(`document_id`),	
	FOREIGN KEY (`company_id`) REFERENCES `companies`(`company_id`),
	FOREIGN KEY (`branch_id`, `warehouse_id`) REFERENCES `branch_offices_warehouses`(`branch_id`, `warehouse_id`),
	FOREIGN KEY (`client_id`) REFERENCES `clients`(`client_id`),
	FOREIGN KEY (`worker_id`) REFERENCES `employees`(`employee_id`),
	foreign key (`user_id`) REFERENCES `users`(`user_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `sales_deliveries_orders_products` (
	`order_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`measure_id` CHAR(36) NOT NULL,
	`ordered` DOUBLE NOT NULL DEFAULT 0.00,
	`delivered_before` DOUBLE NOT NULL DEFAULT 0.00,
	`quantity` DOUBLE NOT NULL DEFAULT 0.00,
	`remaining` DOUBLE NOT NULL DEFAULT 0.00,
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`order_id`, `product_id`,`measure_id`),
	KEY `product_id` (`product_id`),
	KEY `measure_id` (`measure_id`),
	FOREIGN KEY (`order_id`) REFERENCES `sales_deliveries_orders` (`order_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `measure_id`) REFERENCES `products_measures` (`product_id`, `measure_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

create table `sales_deliveries_orders_products_units` (
	`order_id` char(36) not null default "",
	`product_id` char(36) not null default "",
	`measure_id` char(36) not null default "",
	`unit_id` char(36) not null default "",
	`uid` CHAR(64) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	primary key ( `order_id`, `product_id`, `measure_id`,`unit_id` ),
	foreign key (`order_id`) references `sales_deliveries_orders`(`order_id`),
	foreign key (`product_id`, `unit_id`) references `products_units`(`product_id`, `unit_id`),
	foreign key (`measure_id`) references `measures`(`measure_id`)
) engine=innodb default charset=utf8;

CREATE TABLE `purchase_orders_documents` (
	`purchase_order_id` CHAR(36) NOT NULL,
	`company_id` CHAR(36) NOT NULL,
	`branch_id` CHAR(36) NOT NULL,
	`warehouse_id` CHAR(36) NOT NULL,
	`supplier_id` CHAR(36) NOT NULL,
	`user_id` CHAR(36) NOT NULL,
	`employee_id` CHAR(36) NOT NULL,
	`code` CHAR(32) DEFAULT '',
	`reference` VARCHAR(120) NOT NULL DEFAULT '',
	`priority` ENUM('low', 'medium', 'high', 'urgent') NOT NULL DEFAULT 'medium',
	`currency` CHAR(4) NOT NULL DEFAULT 'mxn',
	`exchange_rate` DOUBLE NOT NULL DEFAULT 1.00,
	`amount` DOUBLE NOT NULL DEFAULT 0.00,
	`discount` DOUBLE NOT NULL DEFAULT 0.00,
	`subtotal` DOUBLE NOT NULL DEFAULT 0.00,
	`taxes` DOUBLE NOT NULL DEFAULT 0.00,
	`total` DOUBLE NOT NULL DEFAULT 0.00,
	`transaction_date` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`is_approved` TINYINT(1) NOT NULL DEFAULT 0,
	`approved_by` CHAR(36) NOT NULL DEFAULT '',
	`status` ENUM('new', 'in_process', 'done', 'cancelled') NOT NULL DEFAULT 'new',
	`approved_at` TIMESTAMP NULL,
	`notes` VARCHAR(2048) NOT NULL DEFAULT '',
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`purchase_order_id`),
	UNIQUE KEY (`code`),
	KEY `supplier_id` (`supplier_id`),
	KEY `employee_id` (`employee_id`),
	FOREIGN KEY (`company_id`) REFERENCES `companies`(`company_id`),
	FOREIGN KEY (`branch_id`, `warehouse_id`) REFERENCES `branch_offices_warehouses`(`branch_id`, `warehouse_id`),
	FOREIGN KEY (`supplier_id`) REFERENCES `suppliers`(`supplier_id`),
	FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`),
	FOREIGN KEY (`employee_id`) REFERENCES `employees`(`employee_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `purchase_orders_documents_products_taxes` (
	`purchase_order_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`tax_id` CHAR(36) NOT NULL,
	`percent` DOUBLE NOT NULL DEFAULT 0,
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`purchase_order_id`, `product_id`, `tax_id`),
	KEY `product_id` (`product_id`),
	KEY `tax_id` (`tax_id`),
	FOREIGN KEY (`purchase_order_id`) REFERENCES `purchase_orders_documents` (`purchase_order_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `tax_id`) REFERENCES `products_taxes` (`product_id`, `tax_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;

CREATE TABLE `purchase_orders_documents_details` (
	`purchase_order_id` CHAR(36) NOT NULL,
	`product_id` CHAR(36) NOT NULL,
	`measure_id` CHAR(36) NOT NULL,
	`currency` CHAR(4) NOT NULL DEFAULT 'mxn',
	`quantity` DOUBLE NOT NULL DEFAULT 0.00,
	`original_price` DOUBLE NOT NULL DEFAULT 0.00,
	`discount_factor` DOUBLE NOT NULL DEFAULT 0.00,
	`price` DOUBLE NOT NULL DEFAULT 0.00,
	`amount` DOUBLE NOT NULL DEFAULT 0.00,
	`subtotal` DOUBLE NOT NULL DEFAULT 0.00,
	`discount` DOUBLE NOT NULL DEFAULT 0.00,
	`taxes` DOUBLE NOT NULL DEFAULT 0.00,
	`total` DOUBLE NOT NULL DEFAULT 0.00,
	`created_at` TIMESTAMP NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`purchase_order_id`, `product_id`, `measure_id`),
	KEY `product_id` (`product_id`),
	KEY `measure_id` (`measure_id`),
	FOREIGN KEY (`purchase_order_id`) REFERENCES `purchase_orders_documents` (`purchase_order_id`) ON DELETE CASCADE,
	FOREIGN KEY (`product_id`, `measure_id`) REFERENCES `products_measures` (`product_id`, `measure_id`)
) ENGINE=INNODB DEFAULT CHARSET=UTF8;


CREATE VIEW `v_branch_offices_warehouses` AS 
SELECT
`branch_offices_warehouses`.`branch_id`,
`branch_offices_warehouses`.`warehouse_id`,
`warehouses`.`code`,
`warehouses`.`name`,
`warehouses`.`type`,
`warehouses`.`weight`,
`branch_offices_warehouses`.`status`,
`branch_offices_warehouses`.`created_at`,
`branch_offices_warehouses`.`updated_at`
FROM
`branch_offices_warehouses`
INNER JOIN
`warehouses`
ON
`branch_offices_warehouses`.`warehouse_id` = `warehouses`.`warehouse_id`; 


CREATE VIEW `v_products_measures` AS 
SELECT
`products_measures`.`product_id` AS `product_id`,
`products_measures`.`measure_id` AS `measure_id`,
`products_measures`.`external_reference` AS `external_reference`,
`measures`.`code` AS `code`,
`measures`.`name` AS `name`,
`products_measures`.`equivalence` AS `equivalence`,
`products_measures`.`default` AS `default`,
`measures`.`weight` AS `weight`,
`products_measures`.`status` AS `status`,
`products_measures`.`created_at` AS `created_at`,
`products_measures`.`updated_at` AS `updated_at`
FROM
`products_measures` 
INNER JOIN
`measures`
ON
`products_measures`.`measure_id` = `measures`.`measure_id`;

CREATE VIEW `v_products_cars` AS 
SELECT 
`products_units`.`product_id` AS `product_id`,
`products_units`.`unit_id` AS `unit_id`,
`products_units`.`company_id` AS `company_id`,
`products_units`.`department_id` AS `department_id`,
`products_units`.`brand_id` AS `brand_id`,
`products_units`.`model_id` AS `model_id`,
`products_units`.`version_id` AS `version_id`,
`products_units`.`code` AS `code`,
`products_units`.`serie` AS `serie`,
`products_units`.`reference` AS `reference`,
`products_units`.`uid` AS `uid`,
`products_units`.`description` AS `description`,
`products_units`.`status` AS `status`,
`products_units`.`created_at` AS `created_at`,
`products_units`.`updated_at` AS `updated_at`,
cast(`products_units`.`uid` as unsigned) AS `num_uid` 
FROM `products_units`;


INSERT INTO `categories` VALUES
('67b3744f-12b4-4d93-b6c9-0544152ad007','0001','Generica','work-position',0,'active','2024-09-06 17:31:50','2024-09-06 17:31:50'),
('b0311ae9-e710-47ca-a91a-16e36006c32e','0001','Generica','work-area',0,'active','2024-09-06 17:31:58','2024-09-06 17:31:58'),
('ed77e6e8-2c99-43e4-b4a4-a945e9afd444','0001','Conocido','department',0,'active','2024-09-06 17:36:16','2024-09-06 17:36:16'),
('ff828219-7cd1-44b1-b90c-6a98567b2f4c', '0001', 'Generico', 'clients', 0, 'active', '2024-09-10 16:16:04', '2024-09-10 16:16:04'); 


INSERT INTO `series` VALUES
('2fe285f2-91d1-4729-8858-ca6b8562a697','general','category_of_department','',1,'','2024-09-06 17:36:16','2024-09-06 17:36:16'),
('3f412848-3675-479a-994d-62d95bb67d7a','general','category_of_work-position','',1,'','2024-09-06 17:31:50','2024-09-06 17:31:50'),
('d129a570-522e-4046-9da2-21d6c069d82d','general','category_of_work-area','',1,'','2024-09-06 17:31:58','2024-09-06 17:31:58'),
('c9697e0a-2d8b-4a94-abc7-6366cc59b80e', 'general', 'category_of_clients', '', 1, '', '2024-09-10 16:16:04', '2024-09-10 16:16:04');

INSERT INTO `suppliers` SET `supplier_id` = "f4538ac1-a9c5-11ed-9f14-809133bea1e5", `category_id` = "ea07e6bb-6ef6-4562-898d-bdc5f2b1ad16", `code` = "0000", `legal_name` = "Sistema", `trade_name` = "Sistema", `address_street` = "Conocido", `address_external_number` = "SN", `address_internal_number` = "", `neighborhood` = "Conocido", `state_id` = "03", `municipality_id` = "003", `locality_id` = "0001", `zip` = "0", `taxpayer_id` = "ND", `tax_regime_id` = "", `email` = "noreply@wesmexico.com", `phone` = "0000000000", `cell_phone` = "6121416994", `references` = "", `created_at` = "2022-03-22 04:20:16", `updated_at` = "2022-03-23 18:06:28", `status` = "inactive";
