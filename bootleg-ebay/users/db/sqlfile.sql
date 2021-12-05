-- MySQL dump 10.13  Distrib 8.0.27, for Linux (x86_64)
--
-- Host: localhost    Database: users
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `suspended` tinyint(1) DEFAULT '0',
  `is_admin` tinyint(1) DEFAULT '0',
  `total_rating` int unsigned DEFAULT '0',
  `number_of_ratings` int unsigned DEFAULT '0',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'it__s','quitenever','looking.Emma@uchicago.edu',0,0,0,0),(2,'couple_and_wonder','of','manner.compose@lyft.com',0,0,0,0),(3,'_before_you','weIthis','.@jpmorgan.com',0,0,0,0),(4,'beginning_shoes_to','notdidthought','resisting.@uchicago.edu',1,0,0,0),(5,'speak__of','howwill','of.betrayed@jpmorgan.com',0,1,0,0),(6,'_I_','hashimshe','accompanied.rather@jpmorgan.com',1,1,0,0),(7,'and_I_and','beforerepastspare','with.did@uchicago.edu',1,1,0,0),(8,'and_Campbell_making','thatwasthe','again.@uchicago.edu',1,0,0,0),(9,'was__himself','very','.my@jpmorgan.com',0,0,0,0),(10,'Mr_the_decided','intowilllook','more.could@jpmorgan.com',0,1,0,0),(11,'silent__The','shouldSerleman','here.@lyft.com',1,0,0,0),(12,'_replied_few','aupI','.as@uchicago.edu',0,0,0,0),(13,'spend_of_and','ofwifereverie','sort.@lyft.com',0,0,0,0),(14,'__minutes','asof','.and@lyft.com',0,0,0,0),(15,'_John_think','thelooking','do.Cole@uchicago.edu',0,1,0,0),(16,'Then__this','afterandbe','that.pleasant@lyft.com',0,1,0,0),(17,'wait_Take_whether','MysteryMrsthough','the.had@jpmorgan.com',0,0,0,0),(18,'happy_it_The','foundwithSo','.@lyft.com',1,0,0,0),(19,'Emma_his_any','Emmahison','.decided@lyft.com',1,1,0,0),(20,'to_The_and','beforesayingwould','for.it@jpmorgan.com',0,0,0,0),(21,'and_and_the','formadesatisfies','Perhaps.Fairfax@lyft.com',1,0,0,0),(22,'_be_marry','atand','a.not@jpmorgan.com',0,0,0,0),(23,'should__before','verythought','of.found@jpmorgan.com',1,0,0,0),(24,'doubt_altogether_she','thewould','lent.Wingfield@lyft.com',1,0,0,0),(25,'the_staid_','amthinkingdesirable','.mind@lyft.com',0,1,0,0),(26,'to_pay_s','nonefirst','which.@uchicago.edu',0,0,0,0),(27,'not__her','everdonecan','.what@jpmorgan.com',1,0,0,0),(28,'should_to_deceived','Exactlyshould','was.me@lyft.com',1,1,0,0),(29,'_already_','asnotconsent','what.@uchicago.edu',0,1,0,0),(30,'already_place_of','overanever','.@jpmorgan.com',1,1,0,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-05 21:22:52
