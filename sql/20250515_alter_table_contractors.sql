ALTER TABLE `contractors` ADD `repse` char(32) not null default '' AFTER `tax_regime_id`;
ALTER TABLE `contractors` ADD `notes` varchar(2048) not null default '' AFTER `references`;
