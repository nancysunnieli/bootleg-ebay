-- for reference

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL UNIQUE,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `suspended` boolean DEFAULT 0,
  `is_admin` boolean DEFAULT 0,
  `total_rating` int unsigned DEFAULT 0,
  `number_of_ratings` int unsigned DEFAULT 0,
  PRIMARY KEY (`user_id`)
);