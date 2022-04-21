-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: client_database
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request_archived`;
DROP TABLE IF EXISTS `machine_request_archived`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request_archived` (
  `request_id` INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0,
  `customer_id_` int NOT NULL,
  -- `builder_id_` int NOT NULL,
  `due_date` date DEFAULT NULL,
  `description_` varchar(100) DEFAULT NULL,
  `is_completed` tinyint DEFAULT 0
  -- `cust_delete` tinyint DEFAULT '0',
  -- `build_delete` tinyint DEFAULT '0',
  -- PRIMARY KEY (`request_id`)
  -- UNIQUE KEY (`builder_id_`)
  -- UNIQUE KEY (`customer_id_`)
  -- CONSTRAINT `builder_id` FOREIGN KEY (`builder_id_`) REFERENCES `builder` (`builder_id`)
);

CREATE TABLE `machine_request_archived`(
  `machine_request_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `request_id_` int NOT NULL,
  `machine_id_` int NOT NULL
  
);

-- DROP TABLE IF EXISTS `machine_request`

-- CREATE TABLE `machine_request` (
--   `machine_id` INTEGER PRIMARY KEY AUTOINCREMENT,
--   `request_id_` int NOT NULL, 
--   `m_description` text DEFAULT NULL

--   CONSTRAINT `request_id` FOREIGN KEY (`request_id_`) REFERENCES `request` (`request_id`) 
-- )
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

-- LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
-- INSERT INTO `request` VALUES (1,1,1,'2021-11-18','coaster','wood','metal','plastic',0,0,0),(2,1,2,'2021-11-18','coaster','wood','metal','plastic',0,0,0),(3,1,-1,'2021-11-18','coaster','wood','metal','plastic',0,0,0),(4,1,-1,'2021-11-18','coaster','kevlar','metal','plastic',0,0,0),(5,1,-1,'2021-11-18','coaster','wood','metal','plastic',0,0,0);

SELECT * from request_archived;
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
-- UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-02  8:24:09
