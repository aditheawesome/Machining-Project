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

DROP TABLE IF EXISTS `request`;
DROP TABLE IF EXISTS `machine_request`;
DROP TABLE IF EXISTS `machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `request_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `customer_id_` int NOT NULL,
  -- `builder_id_` int NOT NULL,
  `due_date` date DEFAULT NULL,
  `description_` text DEFAULT NULL,
  `is_completed` tinyint DEFAULT 0,
  `is_started` tinyint DEFAULT 0,
  -- `cust_delete` tinyint DEFAULT '0',
  -- `build_delete` tinyint DEFAULT '0',
  -- PRIMARY KEY (`request_id`)
  -- UNIQUE KEY (`builder_id_`)
  -- UNIQUE KEY (`customer_id_`)
  -- CONSTRAINT `builder_id` FOREIGN KEY (`builder_id_`) REFERENCES `builder` (`builder_id`)
  CONSTRAINT `customer_id` FOREIGN KEY (`customer_id_`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE

);


CREATE TABLE `machine_request` (
  -- confluence
  `machine_request_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `request_id_` int NOT NULL,
  `machine_id_` int NOT NULL,
  
  -- PRIMARY KEY (`request_id_`, `machine_id_`)

  FOREIGN KEY (`machine_id_`) REFERENCES `machine` (`machine_id`) ON DELETE CASCADE 
  FOREIGN KEY (`request_id_`) REFERENCES `request` (`request_id`) ON DELETE CASCADE
);


CREATE TABLE `machine` (
  `machine_id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `machine_name` text NOT NULL,
  `machine_desc` text NOT NULL  

);


/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

-- LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;

-- starts auto incrementing at 1.
INSERT INTO machine values (NULL, "cnc", "The CNC Mill is a super precise machine, which allows for high accuracy when cutting metal and other parts."); 

INSERT INTO machine values (NULL, "dremel", "Well rounded power tool that cuts lexan and metal. This is a great choice if you want to cut a piece of a c-channel off."); 

INSERT INTO machine values (NULL, "3d-printer", "3d printers are useful for a multitude of things. As the name implies, they are constructive, building items from the ground up. There is a wide range of colors that your project may be built in, just be sure to leave your preference in the description!");

-- future: make the machine name unique...??
-- INSERT INTO machine_request values (20, 1); -- request id, then machine id.
-- INSERT INTO machine_request values (20, 2);

-- INSERT INTO machine_request values (21, 2);
-- INSERT INTO machine_request values (21, 3);

-- INSERT INTO machine_request values (22, 3); 

-- SELECT * FROM machine_request;

-- SELECT machine_name FROM machine, machine_request WHERE request_id_ = 20 and machine_id_ = machine_id;

-- SELECT c.request_id_, m.machine_id, m.machine_name, m.machine_desc FROM machine m, machine_request c WHERE m.machine_id = c.machine_id_ and c.request_id_ = 21;

-- SELECT m.machine_id, m.machine_name, m.machine_desc FROM machine m, machine_request c;

-- SELECT * FROM machine;
-- SELECT * from request;
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
