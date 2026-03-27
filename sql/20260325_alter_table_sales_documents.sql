ALTER TABLE `sales_documents`
  CHANGE COLUMN `transaction_status` `payment_status` ENUM('pending','paid') NOT NULL DEFAULT 'pending',
  CHANGE COLUMN `transaction_type` `payment_type` CHAR(32) NOT NULL DEFAULT 'PUE',
  CHANGE COLUMN `transaction_method` `payment_method` CHAR(32) NOT NULL DEFAULT '99',
  ADD COLUMN `fiscal_use` CHAR(3) NOT NULL DEFAULT 'G03' AFTER `payment_type`;

UPDATE `sales_documents`
SET `payment_type` = CASE `payment_type`
  WHEN 'full_payment' THEN 'PUE'
  WHEN 'payment_in_installments' THEN 'PPD'
  ELSE 'PUE'
END;


UPDATE `sales_documents`
SET `payment_method` = CASE `payment_method`
  WHEN 'cash' THEN '01'
  WHEN 'transfer' THEN '03'
  WHEN 'debit_card' THEN '28'
  WHEN 'credit_card' THEN '04'
  WHEN 'mixed' THEN '99'
  ELSE '99'
END;


ALTER TABLE `invoiced_documents`
  CHANGE COLUMN `transaction_status` `payment_status` ENUM('pending','paid') NOT NULL DEFAULT 'pending'
  DROP `transaction_method`
  DROP `transaction_type`;


ALTER TABLE `invoiced_documents` DROP KEY `code`;
ALTER TABLE `invoiced_documents` ADD UNIQUE KEY (`company_id`, `code`);