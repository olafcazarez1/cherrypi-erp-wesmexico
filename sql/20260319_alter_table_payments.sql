ALTER TABLE `sales_documents_payments` ADD `serie` int(10) unsigned DEFAULT 0 AFTER `code`;
ALTER TABLE `sales_documents_payments` ADD UNIQUE KEY ( `document_id`, `serie` );