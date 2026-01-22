/*!999999\- enable the sandbox mode */ 
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
-- Table structure for table `states`
--

-- DROP TABLE IF EXISTS `states`;
-- /*!40101 SET @saved_cs_client     = @@character_set_client */;
-- /*!40101 SET character_set_client = utf8 */;
-- CREATE TABLE `states` (
--   `state_id` char(36) NOT NULL,
--   `name` char(128) NOT NULL DEFAULT '',
--   `last_update` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
--   PRIMARY KEY (`state_id`),
--   UNIQUE KEY `name` (`name`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
-- /*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `states`
--

LOCK TABLES `states` WRITE;
/*!40000 ALTER TABLE `states` DISABLE KEYS */;
INSERT INTO `states` VALUES ('00','Conocido','2017-10-28 19:41:08'),('01','Aguascalientes','2017-09-25 19:08:23'),('02','Baja California','2017-09-25 19:08:23'),('03','Baja California Sur','2017-09-25 19:08:23'),('04','Campeche','2017-09-25 19:08:23'),('05','Coahuila de Zaragoza','2017-09-25 19:08:23'),('06','Colima','2017-09-25 19:08:23'),('07','Chiapas','2017-09-25 19:08:23'),('08','Chihuahua','2017-09-25 19:08:23'),('09','Ciudad de México','2017-09-25 19:08:23'),('10','Durango','2017-09-25 19:08:23'),('11','Guanajuato','2017-09-25 19:08:23'),('12','Guerrero','2017-09-25 19:08:23'),('13','Hidalgo','2017-09-25 19:08:23'),('14','Jalisco','2017-09-25 19:08:23'),('15','México','2017-09-25 19:08:23'),('16','Michoacán de Ocampo','2017-09-25 19:08:23'),('17','Morelos','2017-09-25 19:08:23'),('18','Nayarit','2017-09-25 19:08:23'),('19','Nuevo León','2017-09-25 19:08:23'),('20','Oaxaca','2017-09-25 19:08:23'),('21','Puebla','2017-09-25 19:08:23'),('22','Querétaro','2017-09-25 19:08:23'),('23','Quintana Roo','2017-09-25 19:08:23'),('24','San Luis Potosí','2017-09-25 19:08:23'),('25','Sinaloa','2017-09-25 19:08:23'),('26','Sonora','2017-09-25 19:08:23'),('27','Tabasco','2017-09-25 19:08:23'),('28','Tamaulipas','2017-09-25 19:08:23'),('29','Tlaxcala','2017-09-25 19:08:23'),('30','Veracruz de Ignacio de la Llave','2017-09-25 19:08:23'),('31','Yucatán','2017-09-25 19:08:23'),('32','Zacatecas','2017-09-25 19:08:23');
/*!40000 ALTER TABLE `states` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-04 16:33:40
