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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'there_to_and','Knightleymyselfpleasant','change.pleasant@jpmorgan.com',1,0,0,0),(2,'that_of_','Shedemandingor','of.were@lyft.com',1,0,0,0),(3,'Mrs_This_','manwas','he.@jpmorgan.com',1,0,0,0),(4,'immediately_nor_to','Churchillinto','last.not@jpmorgan.com',1,0,0,0),(5,'have__in','Sheof','no.and@jpmorgan.com',0,0,0,0),(6,'an_well_not','oftheformed','having.He@jpmorgan.com',1,1,0,0),(7,'_at_have','lastthoughEmma','.though@uchicago.edu',0,0,0,0),(8,'the_together_to','keepoccasionconstitution','I.We@uchicago.edu',1,0,0,0),(9,'hand_there_opinion','thescold','of.valuable@uchicago.edu',0,1,0,0),(10,'to__have','thinkfor','condescension.open@uchicago.edu',1,0,0,0),(11,'we_to_its','knowingbeen','something.are@lyft.com',0,1,0,0),(12,'to_amazement_wretched','forthey','something.will@uchicago.edu',1,1,0,0),(13,'_Mrs_handsomest','ittiredwould','thoroughly.@jpmorgan.com',0,0,0,0),(14,'Mr_saying_said','Mrswas','.@uchicago.edu',1,0,0,0),(15,'not_to_','am','said.free@lyft.com',1,1,0,0),(16,'but__unreasonable','awould','You.faults@uchicago.edu',0,0,0,0),(17,'air_in_than','theyventuresay','and.hair@lyft.com',0,1,0,0),(18,'and_acquainted_the','offeelings','Jane.surprized@lyft.com',1,0,0,0),(19,'_Mr_and','theyofColonel','my.all@jpmorgan.com',1,1,0,0),(20,'Woodhouse__','middledeep','conveyance.been@uchicago.edu',1,1,0,0),(21,'fire_surprized_','goingais','made.@jpmorgan.com',0,0,0,0),(22,'Frank_rather_cross','grandmotherandparty','I.understand@jpmorgan.com',1,1,0,0),(23,'She_half_address','Fairfaxdayher','In.I@uchicago.edu',0,1,0,0),(24,'again_observe_feeling','adviceama','angel.under@lyft.com',0,0,0,0),(25,'most__I','anotherhow','known.about@lyft.com',0,0,0,0),(26,'and_to_them','degreechanged','.can@lyft.com',1,1,0,0),(27,'intimation__to','guessingwell','reaching.directions@uchicago.edu',1,0,0,0),(28,'no_or_dinner','wellherher','disappointed.@jpmorgan.com',1,1,0,0),(29,'principal_had_mean','spaciousthey','the.some@jpmorgan.com',0,1,0,0),(30,'parties_distressed_to','Woodhousesuchin','.poor@lyft.com',0,1,0,0);
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

-- Dump completed on 2021-11-16 23:18:20
