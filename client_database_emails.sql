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
-- Table structure for table `emails`
--

DROP TABLE IF EXISTS `emails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emails` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `mFrom` varchar(128) NOT NULL DEFAULT 'machining.millburn@gmail.com',
  `mTo` varchar(128) NOT NULL,
  `mSubject` varchar(256) DEFAULT NULL,
  `mBody` text,
  `email_sent` tinyint DEFAULT '0',
  `time_sent` datetime DEFAULT NULL
  -- PRIMARY KEY (`id`)
  -- UNIQUE KEY (`id`)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emails`
--

-- LOCK TABLES `emails` WRITE;
/*!40000 ALTER TABLE `emails` DISABLE KEYS */;
-- INSERT INTO `emails` VALUES (4,'machining.millburn@gmail.com','sahm.rahman@gmail.com','test','testing 123',1,'2021-11-23 10:39:19'),(5,'machining.millburn@gmail.com','sahm.rahman@gmail.com','New Request','A new request has been received.',1,'2021-11-23 10:41:23'),(6,'machining.millburn@gmail.com','sahm.rahman@gmail.com','New Update','Something has been updated.',1,'2021-11-23 10:44:59'),(9,'machining.millburn@gmail.com','sahm.rahman@gmail.com','test','testing 123',1,'2021-11-23 10:50:27'),(10,'machining.millburn@gmail.com','sahm.rahman@gmail.com','test','testing 123',1,'2021-11-23 10:52:33'),(11,'machining.millburn@gmail.com','sahm.rahman@gmail.com','test','testing 123',1,'2021-11-23 14:01:29'),(12,'machining.millburn@gmail.com','sahm.rahman@gmail.com','test','testing 123',1,'2021-11-24 09:46:43'),(13,'machining.millburn@gmail.com','sahm.rahman@gmail.com','test','testing 123',1,'2021-11-24 10:45:00'),(14,'machining.millburn@gmail.com','sahm.rahman@gmail.com','test','testing 123',1,'2021-11-24 10:45:00'),(15,'machining.millburn@gmail.com','sahm.rahman@gmail.com','test','testing 123',1,'2021-11-24 10:45:00'),(16,'machining.millburn@gmail.com','sahm.rahman@gmail.com','New Request','A new request has been received.',1,'2021-11-24 11:09:46'),(17,'machining.millburn@gmail.com','sahm.rahman@gmail.com','New Update','Something has been updated.',1,'2021-11-29 21:06:11'),(18,'machining.millburn@gmail.com','sahm.rahman@gmail.com','New Builder','A new builder has been assigned to your request.',1,'2021-11-29 21:06:11');

SELECT * FROM emails;
/*!40000 ALTER TABLE `emails` ENABLE KEYS */;
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
