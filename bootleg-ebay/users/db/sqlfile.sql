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
INSERT INTO `users` VALUES (1,'to_expectation_too','Heremet','time.but@jpmorgan.com',1,0,0,0),(2,'wife_Woodhouse_','buthad','down.doing@uchicago.edu',1,1,0,0),(3,'can_did_throat','beforespeech','Cooper.getting@jpmorgan.com',1,0,0,0),(4,'__Not','amHighbury','spring.had@jpmorgan.com',0,1,0,0),(5,'_what_bearing','Randallssensible','to.ensued@jpmorgan.com',0,1,0,0),(6,'papa_from_found','himwhilehad','make.a@lyft.com',0,0,0,0),(7,'I_her_Presently','mythem','not.as@jpmorgan.com',1,1,0,0),(8,'I_suspicion_','oflittlesmiles','ever.look@uchicago.edu',1,0,0,0),(9,'of_spot_She','atmancorner','him.to@uchicago.edu',0,0,0,0),(10,'herself_and_','indeedto','meeting.sure@jpmorgan.com',1,0,0,0),(11,'them_great_a','Tuesday','as.of@uchicago.edu',1,0,0,0),(12,'_to_Harriet','stayson','of.Her@lyft.com',0,1,0,0),(13,'_Mr_he','fartherfirst','hand.consent@lyft.com',0,0,0,0),(14,'to_his_though','someduewould','the.his@jpmorgan.com',0,1,0,0),(15,'Knightley__','keptperhapscompliments','time.always@lyft.com',1,1,0,0),(16,'_wants_it','ofinformationEmma','I.could@lyft.com',0,1,0,0),(17,'stay_resuming_','theastime','.not@uchicago.edu',0,1,0,0),(18,'indeed_there_going','Mrandvery','not.to@uchicago.edu',1,1,0,0),(19,'at_and_have','hadbetternecessary','good.very@uchicago.edu',0,1,0,0),(20,'_harbour_with','IChurchill','has.you@lyft.com',0,0,0,0),(21,'he_resisting_by','Knightley','can.it@jpmorgan.com',0,0,0,0),(22,'it_will_where','situationof','.mind@lyft.com',0,0,0,0),(23,'_been_immense','toTheI','wanted.his@lyft.com',1,0,0,0),(24,'it__happy','friendsheVery','visitings.early@jpmorgan.com',1,1,0,0),(25,'as_have_done','onto','was.Mrs@uchicago.edu',1,0,0,0),(26,'into_leave_an','veryorthe','to.He@uchicago.edu',0,1,0,0),(27,'attention_himself_soon','Sheherand','disrespect.how@uchicago.edu',1,1,0,0),(28,'in_the_her','ofany','that.Smith@jpmorgan.com',1,0,0,0),(29,'him_which_','moveLetabout','.have@jpmorgan.com',1,0,0,0),(30,'as_with_so','admiredto','was.his@jpmorgan.com',1,1,0,0);
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

-- Dump completed on 2021-11-10 23:48:38
