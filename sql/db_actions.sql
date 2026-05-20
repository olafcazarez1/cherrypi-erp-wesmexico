CREATE DATABASE `cafe88` CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE USER 'cafe88_rw'@'localhost' IDENTIFIED BY '$Cafe88.';
GRANT ALL PRIVILEGES ON `cafe88`.* TO 'cafe88_rw'@'localhost';

USE `cafe88`;

FLUSH PRIVILEGES;

ALTER TABLE `products` ADD `brand_id` CHAR(36) NOT NULL DEFAULT '' AFTER `product_id`;
ALTER TABLE `products` ADD `model_id` CHAR(36) NOT NULL DEFAULT '' AFTER `brand_id`;
ALTER TABLE `products` ADD `short_name` CHAR(128) NOT NULL DEFAULT '' AFTER `name`;

ALTER TABLE `products` MODIFY `name` VARCHAR(512) NOT NULL DEFAULT '';
ALTER TABLE `products` MODIFY `description` VARCHAR(1024) NOT NULL DEFAULT '';

UPDATE `products` SET `short_name` = `name`;
UPDATE `products` SET `brand_id` = "cda520cb-0970-4162-b8e9-4a59814c8110", `model_id` = "eedcdfa3-48e8-4f83-b9bf-dcefe8083247";

ALTER TABLE `products` ADD FOREIGN KEY( `brand_id`, `model_id`) REFERENCES `models`(`brand_id`, `model_id`);

UPDATE `products` INNER JOIN `brands` ON `products`.`brand_id` = `brands`.`brand_id` INNER JOIN `models` ON `products`.`model_id` = `models`.`model_id`
SET `products`.`name` = CONCAT(`products`.`short_name`, " " , `brands`.`name`, " ", `models`.`name`);