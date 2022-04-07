-- MySQL dump 10.13  Distrib 5.7.36, for Linux (x86_64)
--
-- Host: localhost    Database: myproject01
-- ------------------------------------------------------
-- Server version	5.7.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add user profile',7,'add_userprofile'),(26,'Can change user profile',7,'change_userprofile'),(27,'Can delete user profile',7,'delete_userprofile'),(28,'Can view user profile',7,'view_userprofile'),(29,'Can add item profile',8,'add_itemprofile'),(30,'Can change item profile',8,'change_itemprofile'),(31,'Can delete item profile',8,'delete_itemprofile'),(32,'Can view item profile',8,'view_itemprofile'),(33,'Can add vendor profile',9,'add_vendorprofile'),(34,'Can change vendor profile',9,'change_vendorprofile'),(35,'Can delete vendor profile',9,'delete_vendorprofile'),(36,'Can view vendor profile',9,'view_vendorprofile'),(37,'Can add history order',10,'add_historyorder'),(38,'Can change history order',10,'change_historyorder'),(39,'Can delete history order',10,'delete_historyorder'),(40,'Can view history order',10,'view_historyorder'),(41,'Can add favor item',11,'add_favoritem'),(42,'Can change favor item',11,'change_favoritem'),(43,'Can delete favor item',11,'delete_favoritem'),(44,'Can view favor item',11,'view_favoritem');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(11,'items','favoritem'),(8,'items','itemprofile'),(6,'sessions','session'),(10,'users','historyorder'),(7,'users','userprofile'),(9,'users','vendorprofile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2022-02-17 10:27:08.835956'),(2,'auth','0001_initial','2022-02-17 10:27:08.895771'),(3,'admin','0001_initial','2022-02-17 10:27:09.021061'),(4,'admin','0002_logentry_remove_auto_add','2022-02-17 10:27:09.053606'),(5,'admin','0003_logentry_add_action_flag_choices','2022-02-17 10:27:09.059830'),(6,'contenttypes','0002_remove_content_type_name','2022-02-17 10:27:09.094719'),(7,'auth','0002_alter_permission_name_max_length','2022-02-17 10:27:09.114327'),(8,'auth','0003_alter_user_email_max_length','2022-02-17 10:27:09.133708'),(9,'auth','0004_alter_user_username_opts','2022-02-17 10:27:09.143637'),(10,'auth','0005_alter_user_last_login_null','2022-02-17 10:27:09.160983'),(11,'auth','0006_require_contenttypes_0002','2022-02-17 10:27:09.162604'),(12,'auth','0007_alter_validators_add_error_messages','2022-02-17 10:27:09.169862'),(13,'auth','0008_alter_user_username_max_length','2022-02-17 10:27:09.188453'),(14,'auth','0009_alter_user_last_name_max_length','2022-02-17 10:27:09.207636'),(15,'auth','0010_alter_group_name_max_length','2022-02-17 10:27:09.226053'),(16,'auth','0011_update_proxy_permissions','2022-02-17 10:27:09.232689'),(17,'sessions','0001_initial','2022-02-17 10:27:09.242176'),(18,'users','0001_initial','2022-02-17 10:27:09.259368'),(20,'users','0002_auto_20220217_1842','2022-02-17 10:42:27.951234'),(22,'users','0003_auto_20220218_0954','2022-02-18 01:54:34.143945'),(26,'items','0001_initial','2022-02-18 02:53:29.568376'),(27,'items','0002_auto_20220218_1054','2022-02-18 02:54:47.808497'),(28,'users','0004_auto_20220218_1512','2022-02-18 07:13:01.925029'),(29,'users','0005_remove_vendorprofile_contact_phone','2022-02-18 07:21:55.242284'),(30,'users','0006_remove_vendorprofile_contact_email','2022-02-18 07:22:41.674565'),(31,'users','0007_auto_20220222_0945','2022-02-22 01:45:15.615856'),(32,'users','0008_auto_20220222_1350','2022-02-22 05:51:00.626662'),(33,'users','0009_auto_20220222_1612','2022-02-22 08:12:29.586933');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items_item_profile`
--

DROP TABLE IF EXISTS `items_item_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items_item_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_name` varchar(50) NOT NULL,
  `item_num` varchar(6) NOT NULL,
  `price` int(11) NOT NULL,
  `pic` varchar(100) NOT NULL,
  `item_class` varchar(6) NOT NULL,
  `score` int(11) NOT NULL,
  `vendor` varchar(50) NOT NULL,
  `item_amount` int(11) NOT NULL,
  `create_time` date NOT NULL,
  `upload_time` date NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items_item_profile`
--

LOCK TABLES `items_item_profile` WRITE;
/*!40000 ALTER TABLE `items_item_profile` DISABLE KEYS */;
INSERT INTO `items_item_profile` VALUES (1,'【美津濃MIZUNO】長袖大學T恤(黑)','000001',880,'item_pic/000001_1633417248.jpg','長袖',0,'TESTVENDOR',99,'2022-02-23','2022-02-23',1);
/*!40000 ALTER TABLE `items_item_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_favor_items`
--

DROP TABLE IF EXISTS `users_favor_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_favor_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `upload_time` date NOT NULL,
  `active` tinyint(1) NOT NULL,
  `item_name_id` int(11) NOT NULL,
  `username_id` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `D_users_favor_items_item_name_id_09b65a41_fk__items_i` (`item_name_id`),
  KEY `D_users_favor_items_username_id_add566f7_fk_users_us` (`username_id`),
  CONSTRAINT `D_users_favor_items_item_name_id_09b65a41_fk__items_i` FOREIGN KEY (`item_name_id`) REFERENCES `items_item_profile` (`id`),
  CONSTRAINT `D_users_favor_items_username_id_add566f7_fk_users_us` FOREIGN KEY (`username_id`) REFERENCES `users_user_profile` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_favor_items`
--

LOCK TABLES `users_favor_items` WRITE;
/*!40000 ALTER TABLE `users_favor_items` DISABLE KEYS */;
INSERT INTO `users_favor_items` VALUES (1,'2022-02-23',1,1,'test1'),(2,'2022-02-23',1,1,'test2');
/*!40000 ALTER TABLE `users_favor_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_history_order`
--

DROP TABLE IF EXISTS `users_history_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_history_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_num` varchar(12) NOT NULL,
  `item_name` varchar(50) NOT NULL,
  `item_price` int(11) NOT NULL,
  `item_num` int(11) NOT NULL,
  `total_amount` int(11) NOT NULL,
  `create_time` date NOT NULL,
  `ordername_id` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `users_history_order_ordername_id_b93575df_fk_users_use` (`ordername_id`),
  CONSTRAINT `users_history_order_ordername_id_b93575df_fk_users_use` FOREIGN KEY (`ordername_id`) REFERENCES `users_user_profile` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_history_order`
--

LOCK TABLES `users_history_order` WRITE;
/*!40000 ALTER TABLE `users_history_order` DISABLE KEYS */;
INSERT INTO `users_history_order` VALUES (1,'199205000001','黑色西裝外套',1999,1,1999,'2022-02-22','test1'),(2,'199205000002','黑色毛衣',3999,1,3999,'2022-02-23','test2');
/*!40000 ALTER TABLE `users_history_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_profile`
--

DROP TABLE IF EXISTS `users_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_user_profile` (
  `username` varchar(16) NOT NULL,
  `userpwd` varchar(32) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `addr` varchar(100) NOT NULL,
  `amount` int(11) NOT NULL,
  `permission` varchar(7) NOT NULL,
  `create_time` date NOT NULL,
  `upload_time` date NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_profile`
--

LOCK TABLES `users_user_profile` WRITE;
/*!40000 ALTER TABLE `users_user_profile` DISABLE KEYS */;
INSERT INTO `users_user_profile` VALUES ('test1','25f9e794323b453885f5181f1b624d0b','test1@gmail.com','0987654321','台北市南港區中坡北路',0,'manager','2022-02-18','2022-02-22',1),('test2','25d55ad283aa400af464c76d713c07ad','test2@gmail.com','0912345678','尚無設定地址',0,'user','2022-02-21','2022-02-21',1);
/*!40000 ALTER TABLE `users_user_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_vendor_profile`
--

DROP TABLE IF EXISTS `users_vendor_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_vendor_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(50) NOT NULL,
  `company_num` varchar(8) NOT NULL,
  `contact_name` varchar(10) NOT NULL,
  `contact_tel` varchar(20) NOT NULL,
  `create_time` date NOT NULL,
  `upload_time` date NOT NULL,
  `active` tinyint(1) NOT NULL,
  `contactor_id` varchar(16) NOT NULL,
  `contact_email` varchar(254) NOT NULL,
  `contact_phone` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `contactor_id` (`contactor_id`),
  CONSTRAINT `users_vendor_profile_contactor_id_9e16b5b3_fk_users_use` FOREIGN KEY (`contactor_id`) REFERENCES `users_user_profile` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_vendor_profile`
--

LOCK TABLES `users_vendor_profile` WRITE;
/*!40000 ALTER TABLE `users_vendor_profile` DISABLE KEYS */;
INSERT INTO `users_vendor_profile` VALUES (1,'TESTVENDOR','12345678','王帥小胖','02-2626-1688','2022-02-23','2022-02-23',1,'test2','test2@gmail.com','0912345678');
/*!40000 ALTER TABLE `users_vendor_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-24 17:19:16
