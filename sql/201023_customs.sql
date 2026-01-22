CREATE TABLE `customs_offices` (
	`custom_id` CHAR(36) NOT NULL DEFAULT '',
	`code` CHAR(32) DEFAULT '',
	`name` CHAR(255) NOT NULL DEFAULT '',
	`type` ENUM('land','maritime','air','inland') NOT NULL,
	`state` CHAR(64) NOT NULL DEFAULT '',
	`status` enum('active','inactive') NOT NULL DEFAULT 'active',
	`created_at` timestamp NOT NULL DEFAULT '2000-01-01 00:00:00',
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`custom_id`)
)  ENGINE=INNODB DEFAULT CHARSET=UTF8;

INSERT INTO `customs_offices` (`custom_id`, `code`, `name`, `type`, `state`) VALUES
('00', '00', 'No Aplica', 'land', '');