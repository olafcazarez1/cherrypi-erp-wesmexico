-- /*!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.6.18-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: wesmexico
-- ------------------------------------------------------
-- Server version	10.6.18-MariaDB-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `measures`
--

DROP TABLE IF EXISTS `measures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measures` (
  `measure_id` char(36) NOT NULL,
  `external_reference` char(36) NOT NULL DEFAULT '',
  `code` char(32) NOT NULL DEFAULT '',
  `name` char(32) NOT NULL DEFAULT '',
  `weight` int(3) unsigned NOT NULL DEFAULT 99,
  `created_at` timestamp NOT NULL DEFAULT '2000-01-01 08:00:00',
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` enum('active','inactive') NOT NULL DEFAULT 'active',
  PRIMARY KEY (`measure_id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `name` (`name`),
  KEY `status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measures`
--

LOCK TABLES `measures` WRITE;
/*!40000 ALTER TABLE `measures` DISABLE KEYS */;
INSERT INTO `measures` VALUES ('1217b2a4-8e81-40e1-a54d-763875b5cf84','0ec01dc6-516b-11e8-a542-66d4b3ba2dec','0004','KILO',0,'2018-01-15 18:44:22','2024-09-21 19:36:59','active'),('2880e637-9931-411a-aa22-c609a891ccbc','0e10f16d-516b-11e8-a542-66d4b3ba2dec','0001','PIEZA',0,'2018-01-15 17:33:01','2024-09-21 19:36:59','active'),('2c104815-86ed-4989-b497-d3c097fc7926','1097cc39-516b-11e8-a542-66d4b3ba2dec','0012','PAQUETE',0,'2018-02-25 21:34:42','2024-09-21 19:36:59','active'),('2fa1f61b-ee55-4ace-9145-cd4c561d0e5d','0f38257f-516b-11e8-a542-66d4b3ba2dec','0010','MILILITROS',0,'2018-02-25 19:20:04','2024-09-21 19:36:59','active'),('3d567b2a-7034-493f-8172-0edf8a26b9fd','0e229b3d-516b-11e8-a542-66d4b3ba2dec','0018','HORA',0,'2018-02-27 03:55:09','2024-09-21 19:36:59','active'),('41198f9f-86d6-41c3-9c56-4424aa590e19','10a143a6-516b-11e8-a542-66d4b3ba2dec','0006','ROLLO',0,'2018-02-24 21:55:22','2024-09-21 19:36:59','active'),('63f8deb3-272a-42eb-97d9-3de4030c6999','1088d941-516b-11e8-a542-66d4b3ba2dec','0017','NO APLICA',0,'2018-02-27 03:53:08','2024-09-21 19:36:59','active'),('6999f29e-105a-4d9f-9062-a55d98bc8c20','0f42b342-516b-11e8-a542-66d4b3ba2dec','0014','METRO CUBICO',0,'2018-02-25 23:01:56','2024-09-21 19:36:59','active'),('832778c5-c1b6-4307-af11-20b95a8e6cb5','0c36804a-516b-11e8-a542-66d4b3ba2dec','0016','GALON',0,'2018-02-25 23:02:36','2024-09-21 19:36:59','active'),('84adbc9e-5e35-4f1a-871f-374a5671d74e','0d1f75c0-516b-11e8-a542-66d4b3ba2dec','0022','SERVICIO',0,'2018-05-30 23:24:15','2024-09-21 19:36:59','active'),('8a45de1f-8f58-41df-a794-8c8c2260a60b','0e10f16d-516b-11e8-a542-66d4b3ba2dec','0003','TRAMO',0,'2018-01-15 18:44:02','2024-09-21 19:36:59','active'),('9633a98f-59c5-4662-a98c-508e2328477d','10a43be1-516b-11e8-a542-66d4b3ba2dec','0007','SACO',0,'2018-02-25 19:07:20','2024-09-21 19:36:59','active'),('a3545958-b162-43dc-9176-b680a923b700','0fee42cc-516b-11e8-a542-66d4b3ba2dec','0015','JUEGO',0,'2018-02-25 23:02:11','2024-09-21 19:36:59','active'),('a71271d6-9875-4d2d-9cd1-aaedc90900db','10837bd3-516b-11e8-a542-66d4b3ba2dec','0021','LOTE',0,'2018-03-07 02:24:12','2024-09-21 19:36:59','active'),('b258e3dc-fad3-4fb6-b200-ec5116e3e955','0f008cb4-516b-11e8-a542-66d4b3ba2dec','0002','METRO LINEAL',0,'2018-01-15 17:51:23','2024-09-21 19:36:59','active'),('b2bb151d-e566-43f6-8142-f128b276186f','0f429652-516b-11e8-a542-66d4b3ba2dec','0013','METRO CUADRADO',0,'2018-02-25 23:01:41','2024-09-21 19:36:59','active'),('b3f4810e-a3a8-47d3-b3c6-d65a43e60142','0efb4ca6-516b-11e8-a542-66d4b3ba2dec','0019','JORNADA',0,'2018-03-28 17:57:30','2024-09-21 19:36:59','active'),('bbe8b608-83c6-46cc-bf48-a703ba97e567','1087df08-516b-11e8-a542-66d4b3ba2dec','0011','BOLSA',0,'2018-02-25 19:28:02','2024-09-21 19:36:59','active'),('bfacd294-bb01-41fd-9ad8-5d85bd40ae0c','0dd881ba-516b-11e8-a542-66d4b3ba2dec','0009','GRAMOS',0,'2018-02-25 19:13:11','2024-09-21 19:36:59','active'),('c6458f96-db9b-49a5-86be-e953cca6ce0b','104ea458-516b-11e8-a542-66d4b3ba2dec','0005','CAJA',0,'2018-01-24 19:03:14','2024-09-21 19:36:59','active'),('c78fd151-3deb-48a8-8bca-8a3cf6ea878a','0f019d13-516b-11e8-a542-66d4b3ba2dec','0008','LITRO',0,'2018-02-25 19:10:31','2024-09-21 19:36:59','active'),('f7ae11dc-f66e-43a9-b19d-091e4b281758','0cff4a2c-516b-11e8-a542-66d4b3ba2dec','0020','DIA',0,'2018-02-27 04:31:11','2024-09-21 19:36:59','active');
/*!40000 ALTER TABLE `measures` ENABLE KEYS */;
INSERT INTO `series` VALUES ('c78ff377-75ab-11ef-91ab-df44b6c4b437', 'general', 'measures', '', 22, '', '2024-09-10 16:16:04', '2024-09-10 16:16:04');

UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-21 12:41:03
