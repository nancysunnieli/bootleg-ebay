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
INSERT INTO `payments` VALUES (1,1,7063310325632092,141,'2023-02-01'),(2,2,7165837211852426,594,'2025-04-01'),(3,3,9264932924998386,940,'2022-08-01'),(4,4,3286332758271912,914,'2024-06-01'),(5,5,9959890766289836,713,'2026-10-01'),(6,6,9348961890374584,625,'2024-01-01'),(7,7,5397520285640890,180,'2023-02-01'),(8,8,8947223578778917,450,'2023-12-01'),(9,9,9949129517063461,565,'2026-09-01'),(10,10,1451212647669734,775,'2025-12-01'),(11,11,2667231481963179,616,'2026-04-01'),(12,12,8576359036491333,774,'2022-12-01'),(13,13,1173550847010276,390,'2024-12-01'),(14,14,4500111455437390,611,'2024-10-01'),(15,15,6423228979242831,418,'2024-05-01'),(16,16,9388474104406049,505,'2023-03-01'),(17,17,7048490584499804,388,'2023-09-01'),(18,18,6045479749764356,169,'2022-09-01'),(19,19,5766366282690578,451,'2022-03-01'),(20,20,6647008257642889,452,'2025-11-01'),(21,21,1647084651564969,163,'2023-09-01'),(22,22,9147043452457811,284,'2024-08-01'),(23,23,6583048939943900,995,'2026-06-01'),(24,24,4693808366862780,894,'2024-03-01'),(25,25,3441750656108229,284,'2023-10-01'),(26,26,9627861918107899,434,'2024-03-01'),(27,27,1960091202410630,527,'2023-11-01'),(28,28,9326802786841108,915,'2022-01-01'),(29,29,3479320120918505,844,'2025-09-01'),(30,30,1532301338739886,370,'2024-11-01');
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

-- Dump completed on 2021-11-12  7:12:43
