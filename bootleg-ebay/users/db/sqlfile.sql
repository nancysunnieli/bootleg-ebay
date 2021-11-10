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
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'XGN3AMS2XSBIBQ0','123','jinli7255@gmail.com',0,0,0,0),(2,'4LEIGLJDMMCXAQO','123','jinli7255@gmail.com',0,0,0,0),(5,'E209X7FPUB0OZ1A','123','jinli7255@gmail.com',0,0,0,0),(6,'E209X7FPUB0OZ1As','123','jinli7255@gmail.com',0,0,0,0),(7,'E209X7FPUB0OZ1Ass','123','jinli7255@gmail.com',0,0,22,5),(10,'RXG8TGNI1VCTRIZ','new_password','email',0,0,2,1),(12,'The_way_to','yousuggestionsnot','ordered.@lyft.com',1,0,0,0),(13,'_manner_income','nobutHe','Weston.entreaties@lyft.com',1,0,0,0),(14,'_a_very','himselfwe','Mr.be@uchicago.edu',0,0,0,0),(15,'hope_exceedingly_tenderness','beMrsobservations','in.belonged@uchicago.edu',0,1,0,0),(16,'the_we_gets','areperhapsreport','I.@uchicago.edu',1,0,0,0),(17,'_without_do','jokes','away.your@uchicago.edu',1,1,0,0),(18,'_that_the','andrespectablethink','could.brother@jpmorgan.com',1,0,0,0),(19,'to_schemes_','nottooattraction','Emma.@jpmorgan.com',1,0,0,0),(20,'he_more_of','asmanner','you.done@lyft.com',1,0,0,0),(21,'me_her_','handmostI','some.of@lyft.com',0,0,0,0),(22,'Bates_Randalls_as','Emmamanintentions','to.had@lyft.com',0,1,0,0),(23,'_her_what','hadgoing','And.them@jpmorgan.com',0,0,0,0),(24,'on_be_know','andhe','engaging.Emma@lyft.com',1,1,0,0),(25,'assured_as_questions','tohold','.thought@lyft.com',0,0,0,0),(26,'than_I_Mrs','Coxesathe','charming.love@lyft.com',0,0,0,0),(27,'Mrs_had_','benot','not.Hawkins@lyft.com',1,1,0,0),(28,'their_ma_of','anyallwhich','deal.detail@lyft.com',1,0,0,0),(29,'_and_','attheBaronne','a.manner@lyft.com',1,1,0,0),(30,'all_to_degree','painsjudge','introductions.any@lyft.com',0,1,0,0),(31,'impossibility_his_one','cut','three.still@uchicago.edu',0,1,0,0),(32,'weather_a_I','Westonsetof','I.a@lyft.com',1,0,0,0),(33,'_nodding_to','livednicely','delicate.@uchicago.edu',0,1,0,0),(34,'and_and_the','ofshepower','.One@uchicago.edu',0,0,0,0),(35,'always_may_brother','ceasedthanknow','with.had@uchicago.edu',1,0,0,0),(36,'fear_sense_for','plan','do.use@uchicago.edu',0,0,0,0),(37,'consequence__friends','interest','her.@jpmorgan.com',0,1,0,0),(38,'into_he_','whichinto','Emma.Bateses@lyft.com',0,0,0,0),(39,'medium__to','thannotAnd','it.@jpmorgan.com',0,1,0,0),(40,'_and_a','amshe','I.pain@lyft.com',1,1,0,0),(41,'question__herself','oflonger','precious.you@jpmorgan.com',1,1,0,0);
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

-- Dump completed on 2021-11-10 16:27:22
