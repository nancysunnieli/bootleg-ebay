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
INSERT INTO `users` VALUES (1,'but_however_','repeatedsyllableparty','could.never@jpmorgan.com',0,1,0,0),(2,'Mrs_I_the','prosemewalking','poor.I@lyft.com',1,1,0,0),(3,'_more_soon','dodislikeblot','have.apologies@jpmorgan.com',1,0,0,0),(4,'when_model_telling','deceivedescapedAnd','the.shade@lyft.com',0,1,0,0),(5,'more_a_but','aamiss','me.have@uchicago.edu',1,0,0,0),(6,'indeed_and_','fivewithis','or.one@jpmorgan.com',1,1,0,0),(7,'acquaintance_how_forget','Knightleymuch','never.Another@uchicago.edu',1,0,0,0),(8,'__to','wasonemuch','for.happiness@lyft.com',0,1,0,0),(9,'a_see_','satquickly','think.two@lyft.com',0,1,0,0),(10,'_Who_enough','footingKnightleythe','be.Mr@jpmorgan.com',0,0,0,0),(11,'of_seems_the','even','proper.that@lyft.com',0,0,0,0),(12,'to__eyes','arebut','am.acknowledged@uchicago.edu',1,1,0,0),(13,'_my_this','finethehabit','done.some@jpmorgan.com',1,0,0,0),(14,'fifty_her_tired','didthemade','to.females@uchicago.edu',0,1,0,0),(15,'he_poor_run','suddenand','you.story@uchicago.edu',1,1,0,0),(16,'__would','going','just.beau@jpmorgan.com',1,1,0,0),(17,'and_angry_at','thoughtalldare','and.perplexity@uchicago.edu',1,0,0,0),(18,'_imagine_','long','he.of@lyft.com',1,1,0,0),(19,'secrecy__and','youagainstgood','his.are@jpmorgan.com',0,0,0,0),(20,'love_on_in','much','was.generally@uchicago.edu',1,0,0,0),(21,'none__have','thatnorbeing','to.my@lyft.com',1,1,0,0),(22,'she_did_explained','Letsaidshould','Miss.it@uchicago.edu',0,0,0,0),(23,'Weston_seeing_for','haveit','first.as@jpmorgan.com',0,1,0,0),(24,'night_I_','thequarterdoes','countenance.on@jpmorgan.com',0,0,0,0),(25,'by__in','respectinghappinessgreat','would.him@uchicago.edu',0,0,0,0),(26,'in_and_greater','goodsuchShe','second.delightful@uchicago.edu',0,1,0,0),(27,'They_high_to','onenot','.how@jpmorgan.com',0,1,0,0),(28,'Harriet_it_','thing','.it@jpmorgan.com',0,1,0,0),(29,'in_the_narration','himmannersif','.this@jpmorgan.com',1,0,0,0),(30,'_sitting_their','Westonplentyit','get.now@lyft.com',0,0,0,0);
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

-- Dump completed on 2021-11-17 17:25:22
