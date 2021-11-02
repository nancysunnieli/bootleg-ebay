-- for reference

DROP TABLE IF EXISTS `payments`;
CREATE TABLE `payments` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL UNIQUE,
  `card_number` BIGINT unsigned NOT NULL UNIQUE,
  `security_code` int NOT NULL,
  `expiration_date` DATE NOT NULL,
  PRIMARY KEY (`id`)
);