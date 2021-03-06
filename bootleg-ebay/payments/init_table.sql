-- for reference

DROP TABLE IF EXISTS `payments`;
CREATE TABLE `payments` (
  `payment_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL UNIQUE,
  `card_number` BIGINT unsigned NOT NULL UNIQUE,
  `security_code` int NOT NULL,
  `expiration_date` DATE NOT NULL,
  PRIMARY KEY (`payment_id`)
);


DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `transaction_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `payment_id` int unsigned NOT NULL,
  `item_id` varchar(100) NOT NULL,
  `money` float NOT NULL,
  `quantity` int unsigned NOT NULL, 
  PRIMARY KEY (`transaction_id`)
);