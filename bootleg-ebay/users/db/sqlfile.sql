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
INSERT INTO `users` VALUES (1,'_a_She','occasionHenceforwardalert','it.possible@jpmorgan.com',0,1,0,0),(2,'matter_own_','Mrtalkstation','from.for@jpmorgan.com',1,0,0,0),(3,'no_keeping_unexamined','degreeguess','.was@uchicago.edu',0,0,0,0),(4,'that_make_all','twoMrsmeant','.a@uchicago.edu',1,1,0,0),(5,'looked_the_so','timea','Jane.The@lyft.com',0,1,0,0),(6,'_been_Mrs','jokewasof','Mrs.morning@lyft.com',0,0,0,0),(7,'they__bathing','andthatsuited','.means@lyft.com',0,0,0,0),(8,'madam_chosen_must','wesaid','my.detained@lyft.com',0,1,0,0),(9,'as__','Thebeingexpressive','.and@jpmorgan.com',1,0,0,0),(10,'I_from_of','blushingwasits','how.chose@uchicago.edu',0,0,0,0),(11,'sure_but_shall','satisfieddid','.Yorkshire@jpmorgan.com',0,1,0,0),(12,'workbags_cannot_another','butorwe','.doubt@lyft.com',1,0,0,0),(13,'direct__Martin','extentthe','Dear.We@uchicago.edu',1,1,0,0),(14,'poor_We_are','andmeaningit','her.my@jpmorgan.com',1,0,0,0),(15,'after_England_dare','wasto','body.consent@jpmorgan.com',1,1,0,0),(16,'cheerfully_comfort_to','gainingpointperceived','momentary.she@lyft.com',1,1,0,0),(17,'there_again_','thenimagineabout','to.line@jpmorgan.com',0,0,0,0),(18,'watching_of_utmost','inshetwo','greater.@jpmorgan.com',1,0,0,0),(19,'thing_safe_to','CHURCHILLparishpropose','.no@lyft.com',1,0,0,0),(20,'the__proposals','isto','been.is@jpmorgan.com',0,0,0,0),(21,'for_She_','ittalk','Emma.@uchicago.edu',1,0,0,0),(22,'and_Indifferent_attendance','felicitysucceedairy','.@uchicago.edu',1,1,0,0),(23,'South__likeness','objectspeakvery','I.Mrs@lyft.com',0,0,0,0),(24,'wife_real_nothing','too','satin.being@lyft.com',1,0,0,0),(25,'been_are_think','hercompliment','I.Emma@jpmorgan.com',1,1,0,0),(26,'and_a_to','notthatHe','eager.own@uchicago.edu',1,1,0,0),(27,'_remained_','mentionedwhich','.given@uchicago.edu',1,1,0,0),(28,'every_deserve_catching','behimwhat','time.did@lyft.com',1,0,0,0),(29,'was_very_to','hisme','we.@jpmorgan.com',0,0,0,0),(30,'_unless_One','waswerebe','Emma.@uchicago.edu',1,0,0,0);
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

-- Dump completed on 2021-11-12 20:28:28
