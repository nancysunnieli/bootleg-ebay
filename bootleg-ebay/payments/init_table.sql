-- for reference

DROP TABLE IF EXISTS `payment_card`;
CREATE TABLE `payment_card` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `card_number` int NOT NULL UNIQUE,
  `security_code` int NOT NULL,
  `expiration_date` DATE NOT NULL,
  PRIMARY KEY (`id`)
);