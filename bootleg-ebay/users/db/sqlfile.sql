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
  `money` float DEFAULT '0',
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
INSERT INTO `users` VALUES (1,'your_them_wished','childrenwillwould','on.than@jpmorgan.com',622,0,0),(2,'Fairfax_had_Miss','sdiesI','uncle.but@lyft.com',222,1,0),(3,'round_had_Mr','ofnever','I.persuading@jpmorgan.com',1069,0,1),(4,'might_pleasure_so','shewhichabout','rather.should@lyft.com',488,1,0),(5,'event_she_my','easynominala','same.I@lyft.com',1176,0,0),(6,'_He_given','ofwehave','think.@jpmorgan.com',175,1,1),(7,'__did','continuedhe','and.so@uchicago.edu',969,0,0),(8,'business_be_','Ipopulousher','had.but@jpmorgan.com',1231,1,1),(9,'does_sure_it','sheMrsbe','himself.to@lyft.com',156,0,0),(10,'_joy_be','affectionshesurprize','.@uchicago.edu',1447,0,1),(11,'It_sell_to','tosagacitylady','it.unpleasant@lyft.com',1000,0,0),(12,'her__','happinessyou','No.Not@jpmorgan.com',1352,0,1),(13,'now_and_only','andfallenof','sure.do@uchicago.edu',790,1,0),(14,'to_the_that','youhousedefer','That.to@jpmorgan.com',1073,1,0),(15,'was__increase','environsexcitingshortness','Abbey.the@uchicago.edu',224,1,1),(16,'in_good_','disagreeableam','as.and@uchicago.edu',827,1,1),(17,'which__','waitingthankedThey','would.Her@jpmorgan.com',1757,1,1),(18,'sir_to_','particularlyourof','.long@lyft.com',404,1,1),(19,'_night_and','poorwhichbetween','those.may@jpmorgan.com',581,1,0),(20,'with_was_and','askedspecimen','idea.but@lyft.com',1583,0,1),(21,'Indifferent_I_persons','withoutmostthe','in.off@lyft.com',1046,1,0),(22,'_let_much','yourcould','months.for@lyft.com',1285,0,1),(23,'_day_You','IMisss','keep.@uchicago.edu',1856,0,1),(24,'had_and_or','herpursuitIf','In.bosom@jpmorgan.com',1739,0,1),(25,'not_side_more','Nothingto','they.five@uchicago.edu',1930,0,0),(26,'__a','childnothad','be.and@lyft.com',1795,1,1),(27,'But_such_Churchill','pointon','some.@lyft.com',1200,0,0),(28,'there_John_It','frontwhatand','in.her@jpmorgan.com',1674,1,1),(29,'his_her_The','hadIattachment','much.perhaps@jpmorgan.com',1889,1,0),(30,'consent_sudden_it','Howquestiona','it.@uchicago.edu',1599,1,0);
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

-- Dump completed on 2021-10-30 18:21:31
