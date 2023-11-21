/*
 Navicat Premium Data Transfer

 Source Server         : 111
 Source Server Type    : MySQL
 Source Server Version : 80028 (8.0.28)
 Source Host           : 127.0.0.1:3306
 Source Schema         : music__

 Target Server Type    : MySQL
 Target Server Version : 80028 (8.0.28)
 File Encoding         : 65001

 Date: 21/11/2023 15:44:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('73114713dfa0');

-- ----------------------------
-- Table structure for email_captcha
-- ----------------------------
DROP TABLE IF EXISTS `email_captcha`;
CREATE TABLE `email_captcha`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `captcha` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of email_captcha
-- ----------------------------
INSERT INTO `email_captcha` VALUES (2, '1943583024@qq.com', '2932');
INSERT INTO `email_captcha` VALUES (3, '1943583024@qq.com', '6605');
INSERT INTO `email_captcha` VALUES (4, '1943583024@qq.com', '3262');

-- ----------------------------
-- Table structure for 下单
-- ----------------------------
DROP TABLE IF EXISTS `下单`;
CREATE TABLE `下单`  (
  `OrderID` int NOT NULL,
  `MusicID` int NOT NULL,
  PRIMARY KEY (`OrderID`, `MusicID`) USING BTREE,
  INDEX `MusicID`(`MusicID` ASC) USING BTREE,
  CONSTRAINT `下单_ibfk_1` FOREIGN KEY (`MusicID`) REFERENCES `音乐` (`MusicID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `下单_ibfk_2` FOREIGN KEY (`OrderID`) REFERENCES `订单` (`OrderID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 下单
-- ----------------------------

-- ----------------------------
-- Table structure for 广告
-- ----------------------------
DROP TABLE IF EXISTS `广告`;
CREATE TABLE `广告`  (
  `AdvertisingID` int NOT NULL AUTO_INCREMENT,
  `Abstract` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `title` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `ReleaseTime` datetime NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `Picture` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`AdvertisingID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 广告
-- ----------------------------

-- ----------------------------
-- Table structure for 榜单
-- ----------------------------
DROP TABLE IF EXISTS `榜单`;
CREATE TABLE `榜单`  (
  `ChartID` int NOT NULL AUTO_INCREMENT,
  `ChartType` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`ChartID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 榜单
-- ----------------------------

-- ----------------------------
-- Table structure for 歌手
-- ----------------------------
DROP TABLE IF EXISTS `歌手`;
CREATE TABLE `歌手`  (
  `SingerID` int NOT NULL AUTO_INCREMENT,
  `Singer` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `SingerSex` enum('男','女') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`SingerID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 歌手
-- ----------------------------
INSERT INTO `歌手` VALUES (1, '周杰伦', '男');

-- ----------------------------
-- Table structure for 演唱
-- ----------------------------
DROP TABLE IF EXISTS `演唱`;
CREATE TABLE `演唱`  (
  `SingerID` int NOT NULL,
  `MusicID` int NOT NULL,
  PRIMARY KEY (`SingerID`, `MusicID`) USING BTREE,
  INDEX `MusicID`(`MusicID` ASC) USING BTREE,
  CONSTRAINT `演唱_ibfk_1` FOREIGN KEY (`MusicID`) REFERENCES `音乐` (`MusicID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `演唱_ibfk_2` FOREIGN KEY (`SingerID`) REFERENCES `歌手` (`SingerID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 演唱
-- ----------------------------
INSERT INTO `演唱` VALUES (1, 1);
INSERT INTO `演唱` VALUES (1, 2);
INSERT INTO `演唱` VALUES (1, 3);

-- ----------------------------
-- Table structure for 用户
-- ----------------------------
DROP TABLE IF EXISTS `用户`;
CREATE TABLE `用户`  (
  `UserID` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Password` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UserName` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sex` enum('男','女') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ContactNumber` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`UserID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 用户
-- ----------------------------
INSERT INTO `用户` VALUES ('11111111111', '12345678', '111', '女', '1943583024@qq.com', '18800710156');

-- ----------------------------
-- Table structure for 登榜
-- ----------------------------
DROP TABLE IF EXISTS `登榜`;
CREATE TABLE `登榜`  (
  `MusicID` int NOT NULL,
  `ChartID` int NOT NULL,
  `SongRanking` int NOT NULL,
  PRIMARY KEY (`MusicID`, `ChartID`) USING BTREE,
  INDEX `ChartID`(`ChartID` ASC) USING BTREE,
  CONSTRAINT `登榜_ibfk_1` FOREIGN KEY (`ChartID`) REFERENCES `音乐` (`MusicID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `登榜_ibfk_2` FOREIGN KEY (`MusicID`) REFERENCES `音乐` (`MusicID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 登榜
-- ----------------------------

-- ----------------------------
-- Table structure for 管理员
-- ----------------------------
DROP TABLE IF EXISTS `管理员`;
CREATE TABLE `管理员`  (
  `AdmID` int NOT NULL AUTO_INCREMENT,
  `AdmName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Aassword` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`AdmID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 管理员
-- ----------------------------

-- ----------------------------
-- Table structure for 类型
-- ----------------------------
DROP TABLE IF EXISTS `类型`;
CREATE TABLE `类型`  (
  `ClassID` int NOT NULL AUTO_INCREMENT,
  `TypeName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`ClassID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 类型
-- ----------------------------
INSERT INTO `类型` VALUES (1, '爱情');

-- ----------------------------
-- Table structure for 订单
-- ----------------------------
DROP TABLE IF EXISTS `订单`;
CREATE TABLE `订单`  (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `UserID` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `OrderTime` datetime NOT NULL,
  `DownloadStatus` enum('0','1') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`OrderID`) USING BTREE,
  INDEX `UserID`(`UserID` ASC) USING BTREE,
  CONSTRAINT `订单_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `用户` (`UserID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 订单
-- ----------------------------

-- ----------------------------
-- Table structure for 评论
-- ----------------------------
DROP TABLE IF EXISTS `评论`;
CREATE TABLE `评论`  (
  `CommentID` int NOT NULL AUTO_INCREMENT,
  `Content` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `CommentTime` datetime NOT NULL,
  `MusicID` int NULL DEFAULT NULL,
  `UserID` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`CommentID`) USING BTREE,
  INDEX `MusicID`(`MusicID` ASC) USING BTREE,
  INDEX `UserID`(`UserID` ASC) USING BTREE,
  CONSTRAINT `评论_ibfk_1` FOREIGN KEY (`MusicID`) REFERENCES `音乐` (`MusicID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `评论_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `用户` (`UserID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 评论
-- ----------------------------

-- ----------------------------
-- Table structure for 音乐
-- ----------------------------
DROP TABLE IF EXISTS `音乐`;
CREATE TABLE `音乐`  (
  `MusicID` int NOT NULL AUTO_INCREMENT,
  `ClassID` int NULL DEFAULT NULL,
  `MusicName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Intro` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `price` decimal(10, 2) NOT NULL,
  `StorageLocation` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `IssueTime` datetime NOT NULL,
  `Cover` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`MusicID`) USING BTREE,
  INDEX `ClassID`(`ClassID` ASC) USING BTREE,
  CONSTRAINT `音乐_ibfk_1` FOREIGN KEY (`ClassID`) REFERENCES `类型` (`ClassID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of 音乐
-- ----------------------------
INSERT INTO `音乐` VALUES (1, 1, '爱在西元前', '1', 1.00, '../static/musics/周杰伦 - 爱在西元前.mp3', '2023-11-13 16:02:32', NULL);
INSERT INTO `音乐` VALUES (2, 1, '安静', '1', 1.00, 'D:\\桌面\\数据库课设\\音乐网站\\musics\\周杰伦 - 安静.mp3', '2023-11-22 16:04:10', NULL);
INSERT INTO `音乐` VALUES (3, 1, '半岛铁盒', '1', 1.00, 'D:\\桌面\\数据库课设\\音乐网站\\musics\\周杰伦 - 半岛铁盒.mp3', '2023-11-15 22:38:36', NULL);

SET FOREIGN_KEY_CHECKS = 1;
