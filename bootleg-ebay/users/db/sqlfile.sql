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
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `suspended` tinyint(1) DEFAULT '0',
  `is_admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'no__very','friendsyoubut','you.@lyft.com',1,1),(2,'and_measuring_feelings','partmustwidower','fact.good@uchicago.edu',0,1),(3,'watching_every_Her','Campbellsdoor','likes.@uchicago.edu',0,0),(4,'notions__the','toaccount','her.presumption@jpmorgan.com',0,1),(5,'how_takes_of','offbethe','period.that@jpmorgan.com',0,1),(6,'better_on_be','tothingsyou','happy.not@jpmorgan.com',0,1),(7,'_to_event','thatneverin','been.all@jpmorgan.com',1,1),(8,'so__reproached','theminebeing','.to@uchicago.edu',1,0),(9,'clearness_she_putting','theyouword','particulars.sad@uchicago.edu',0,1),(10,'Miss_watched_what','FranksofteningChurchills','I.herself@uchicago.edu',0,0),(11,'__and','topoint','Elton.well@jpmorgan.com',1,0),(12,'two_Mr_as','promisesfor','and.the@lyft.com',0,1),(13,'one_eligibly_it','ofcriedof','.visibly@lyft.com',0,0),(14,'expeditious_not_not','andattentiona','not.he@lyft.com',1,1),(15,'there_heard_bounds','brightexplanation','running.may@uchicago.edu',1,0),(16,'be__had','deeplatestdissipated','.feelings@jpmorgan.com',1,1),(17,'domestic_It_that','The','.that@lyft.com',0,0),(18,'was_and_not','in','yesterday.in@uchicago.edu',1,1),(19,'any_And_to','pleasuresthey','in.@uchicago.edu',1,1),(20,'moment_give_believe','thatevery','of.Mrs@jpmorgan.com',0,1),(21,'must_on_else','bepleased','Mrs.@lyft.com',1,0),(22,'home_had_','onthehave','most.young@uchicago.edu',1,1),(23,'of_Angry_own','fortoAnd','I.one@jpmorgan.com',0,1),(24,'profit_bring_no','inonly','His.had@uchicago.edu',1,1),(25,'neighbourhood_he_long','ofbaroucheI','Miss.And@jpmorgan.com',1,1),(26,'astonished_as_very','firessay','enter.than@jpmorgan.com',0,1),(27,'I__','itthat','Emma.@lyft.com',0,0),(28,'to__and','thoughtherrecollect','and.Knightley@lyft.com',0,1),(29,'to_know_and','notyouwill','on.but@lyft.com',1,1),(30,'and_self_door','tothathe','yet.bad@lyft.com',0,1);
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

-- Dump completed on 2021-11-04  2:02:07
