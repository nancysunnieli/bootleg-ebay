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
INSERT INTO `users` VALUES (1,'sometimes_woman_','thickwhich','her.must@jpmorgan.com',0,0,0,0),(2,'might_and_on','hehad','fine.@lyft.com',1,1,0,0),(3,'could_was_good','notasshe','.@uchicago.edu',0,0,0,0),(4,'could__time','doestoany','being.could@lyft.com',1,0,0,0),(5,'_a_not','knewgivinga','dies.quite@jpmorgan.com',1,0,0,0),(6,'or_you_He','forwalksay','.as@jpmorgan.com',1,1,0,0),(7,'clever__','additionneither','.She@lyft.com',1,1,0,0),(8,'of_to_between','fromIcame','no.subjection@lyft.com',1,0,0,0),(9,'in__','anyall','surprize.she@jpmorgan.com',1,1,0,0),(10,'__Harriet','forbelow','.and@jpmorgan.com',0,1,0,0),(11,'not_quite_','newsthe','.eligible@uchicago.edu',0,0,0,0),(12,'made_proof_Jane','allThereguilt','was.her@lyft.com',0,0,0,0),(13,'in_kind_','smistakenFrank','it.grew@lyft.com',1,0,0,0),(14,'say__to','wellMrbe','that.way@uchicago.edu',0,0,0,0),(15,'down_She_man','havewereit','obviate.@lyft.com',0,1,0,0),(16,'_of_Harriet','treatssurehowever','the.her@uchicago.edu',1,0,0,0),(17,'and_She_not','intos','are.as@uchicago.edu',1,0,0,0),(18,'_is_such','thepreciousMr','some.@uchicago.edu',1,0,0,0),(19,'possessed_think_are','youforHe','now.@uchicago.edu',0,0,0,0),(20,'to_any_','myherincrease','her.on@lyft.com',0,1,0,0),(21,'induced_in_it','towill','me.to@lyft.com',1,1,0,0),(22,'have_to_her','writingwith','I.Miss@jpmorgan.com',1,1,0,0),(23,'in_true_Miss','slightlyveryand','not.far@uchicago.edu',1,0,0,0),(24,'days_comfortable_being','sointentionsherself','smile.leg@uchicago.edu',1,1,0,0),(25,'for_probably_','lessdreadson','How.claim@jpmorgan.com',1,0,0,0),(26,'of_resolution_than','it','so.am@uchicago.edu',0,1,0,0),(27,'_her_as','fatherbe','herself.@jpmorgan.com',1,1,0,0),(28,'thing_heard_satisfactorily','circumstancefor','her.were@uchicago.edu',0,1,0,0),(29,'the_eager_opinions','ashehave','worthy.taken@lyft.com',0,1,0,0),(30,'silly_our_s','andwasall','announcing.such@jpmorgan.com',0,1,0,0);
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

-- Dump completed on 2021-11-12  7:03:34
