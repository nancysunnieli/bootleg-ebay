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
INSERT INTO `users` VALUES (1,'think_as_s','toWoodhousefor','again.terms@uchicago.edu',1,1,0,0),(2,'when_Bath_Elton','beingbe','mounted.no@uchicago.edu',0,1,0,0),(3,'their__Martin','youbasketsnice','their.that@lyft.com',1,1,0,0),(4,'_still_which','anditor','and.had@jpmorgan.com',0,1,0,0),(5,'case_Mrs_was','thoughtdemure','the.@lyft.com',0,1,0,0),(6,'all_every_try','totheand','and.They@uchicago.edu',0,1,0,0),(7,'my_hours_which','sharpits','time.it@lyft.com',1,0,0,0),(8,'a_Elton_have','Shepassed','be.the@uchicago.edu',1,0,0,0),(9,'a_could_not','havebeenthe','of.I@jpmorgan.com',1,1,0,0),(10,'God_excuse_','Andnor','been.he@jpmorgan.com',0,0,0,0),(11,'and_what_your','minevoicedone','but.vigorously@jpmorgan.com',1,0,0,0),(12,'and_or_not','apopinterest','struggle.can@jpmorgan.com',1,0,0,0),(13,'suspect_him_the','youtoThe','have.@lyft.com',1,0,0,0),(14,'attending_of_s','hisandno','to.o@uchicago.edu',0,0,0,0),(15,'his_and_are','Mrsseeingup','.Elton@lyft.com',0,1,0,0),(16,'often_does_the','talkedyoung','perhaps.day@lyft.com',0,1,0,0),(17,'mind_and_','thehecarefully','but.@uchicago.edu',1,1,0,0),(18,'was_condescension_s','itinevitablebeen','she.be@uchicago.edu',0,0,0,0),(19,'how_other_','toand','.pounds@lyft.com',1,0,0,0),(20,'the__to','aswithhad','to.envy@lyft.com',1,0,0,0),(21,'doubt_and_trying','werestill','from.and@uchicago.edu',0,1,0,0),(22,'He_labours_Donwell','anasay','when.@jpmorgan.com',0,0,0,0),(23,'the_belonged_was','isif','the.not@uchicago.edu',1,1,0,0),(24,'class_admitted_allow','infinitelysoher','an.it@jpmorgan.com',1,1,0,0),(25,'__of','itand','at.afterwards@jpmorgan.com',0,1,0,0),(26,'_did_consequence','nevernow','years.change@jpmorgan.com',0,0,0,0),(27,'strong_change_hear','Ohmustit','.@jpmorgan.com',1,1,0,0),(28,'heart_went_least','hadcouldany','to.ready@lyft.com',1,0,0,0),(29,'Knightley__Tell','looked','I.imagine@uchicago.edu',0,1,0,0),(30,'move_body_longing','hardlybetterEmma','Plain.he@uchicago.edu',1,0,0,0);
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

-- Dump completed on 2021-11-17  2:03:51
