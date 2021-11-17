-- MySQL dump 10.13  Distrib 8.0.27, for Linux (x86_64)
--
-- Host: localhost    Database: payments
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
-- Table structure for table `payment_card`
--

DROP TABLE IF EXISTS `payment_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_card` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `card_number` int NOT NULL,
  `security_code` int NOT NULL,
  `expiration_date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card_number` (`card_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_card`
--

LOCK TABLES `payment_card` WRITE;
/*!40000 ALTER TABLE `payment_card` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `payment_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `card_number` bigint unsigned NOT NULL,
  `security_code` int NOT NULL,
  `expiration_date` date NOT NULL,
  PRIMARY KEY (`payment_id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `card_number` (`card_number`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (1,1,2743043601343954,561,'2022-08-01'),(2,2,1455095999391446,507,'2025-10-01'),(3,3,4264612610302845,283,'2022-07-01'),(4,4,9779287542213978,955,'2025-06-01'),(5,5,1435521408285040,308,'2022-02-01'),(6,6,7600501153654293,441,'2023-03-01'),(7,7,3623694879881736,339,'2026-10-01'),(8,8,1651999242138993,348,'2024-06-01'),(9,9,4910922829501355,330,'2023-08-01'),(10,10,3498952442983783,787,'2025-10-01'),(11,11,8377426952892513,319,'2024-04-01'),(12,12,8796018396995174,924,'2022-12-01'),(13,13,2970850985356875,844,'2022-06-01'),(14,14,6670867536139062,723,'2024-10-01'),(15,15,6702987058698696,915,'2025-08-01'),(16,16,2433705309821275,131,'2022-09-01'),(17,17,6623492637064842,520,'2024-10-01'),(18,18,4751643740459020,973,'2025-09-01'),(19,19,2750366550913004,431,'2026-02-01'),(20,20,1214424660473048,658,'2022-03-01'),(21,21,4318576244370528,323,'2024-10-01'),(22,22,3765983078993406,132,'2024-02-01'),(23,23,1719423331917541,527,'2025-11-01'),(24,24,1564558987598441,992,'2024-04-01'),(25,25,4812838798620641,674,'2026-05-01'),(26,26,5159753452188609,559,'2025-11-01'),(27,27,2319431748376549,226,'2026-09-01'),(28,28,7920081784718389,766,'2022-05-01'),(29,29,8679992264617199,279,'2022-05-01'),(30,30,1197818909040242,868,'2023-05-01');
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `payment_id` int unsigned NOT NULL,
  `item_id` varchar(100) NOT NULL,
  `money` float NOT NULL,
  `quantity` int unsigned NOT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
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
