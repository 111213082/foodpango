-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-22 08:26:33
-- 伺服器版本： 10.4.28-MariaDB
-- PHP 版本： 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `foodpango`
--

-- --------------------------------------------------------

--
-- 資料表結構 `bro`
--

CREATE TABLE `bro` (
  `bID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `verification` tinyint(1) NOT NULL,
  `bank` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `bro`
--

INSERT INTO `bro` (`bID`, `name`, `email`, `password`, `phone`, `verification`, `bank`) VALUES
(1, '老李', '111@gmail.com', '*832EB84CB764129D05D498ED9CA7E5CE9B8F83EB', '0987654321', 1, '0000111122223333');

-- --------------------------------------------------------

--
-- 資料表結構 `categories`
--

CREATE TABLE `categories` (
  `ID` int(11) NOT NULL,
  `rID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `categories`
--

INSERT INTO `categories` (`ID`, `rID`, `name`) VALUES
(1, 1, '前菜（Antipasti）'),
(2, 1, '湯品（Zuppe）'),
(3, 1, '義大利麵（Pasta）'),
(4, 1, '披薩（Pizza）'),
(5, 1, '甜點（Dolci）'),
(6, 1, '飲品（Bevande）'),
(7, 2, '經典冰淇淋 (Classic Ice Cream)'),
(11, 2, '特色冰淇淋 (Specialty Ice Cream)'),
(12, 2, '冰品杯/聖代 (Sundaes & Cups)'),
(13, 2, '冰沙 (Smoothies)');

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `cID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `card` varchar(20) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `address` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `customer`
--

INSERT INTO `customer` (`cID`, `name`, `email`, `password`, `card`, `phone`, `address`) VALUES
(1, '小羊', 'baa@gmail.com', '*6F12ADE7E5EF3C0284DE0691A2E1188C1AEF28D1', NULL, '0988888888', '');

-- --------------------------------------------------------

--
-- 資料表結構 `discount`
--

CREATE TABLE `discount` (
  `dID` int(11) NOT NULL,
  `name` varchar(10) NOT NULL,
  `description` text NOT NULL,
  `discountType` enum('fixed','percentage') NOT NULL,
  `amount` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `food`
--

CREATE TABLE `food` (
  `fID` int(11) NOT NULL,
  `rID` int(11) NOT NULL,
  `ID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `price` int(10) NOT NULL,
  `is_vegetarian` tinyint(1) NOT NULL,
  `description` text NOT NULL,
  `is_available` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `order`
--

CREATE TABLE `order` (
  `oID` int(11) NOT NULL,
  `cID` int(11) NOT NULL,
  `rID` int(11) NOT NULL,
  `bID` int(11) NOT NULL,
  `dID` int(11) NOT NULL,
  `status` enum('待確認','已接單','配送中','完成') DEFAULT '待確認',
  `totalPrice` int(10) NOT NULL,
  `note` text DEFAULT NULL,
  `address` text NOT NULL,
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `prepareTime` int(11) NOT NULL,
  `deliverTime` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `restaurant`
--

CREATE TABLE `restaurant` (
  `rID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` text NOT NULL,
  `license` varchar(50) NOT NULL,
  `bank` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `announcement` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `restaurant`
--

INSERT INTO `restaurant` (`rID`, `name`, `email`, `password`, `phone`, `address`, `license`, `bank`, `is_active`, `announcement`) VALUES
(1, 'spagett義', 'spagetti@gmail.com', '*23AE809DDACAF96AF0FD78ED04B6A265E05AA257', '0936409918', '南投縣大同市信義路159號-4\r\n', '579846157', '(700)3489718757', 0, '本月公休日:19.20號'),
(2, '愛死cream', 'icecream@gmail.com', '*531E182E2F72080AB0740FE2F2D689DBE0146E04', '0982172649', '南投縣大同市大業路78號', '721105489', '(713)7018095462', 0, '');

-- --------------------------------------------------------

--
-- 資料表結構 `star`
--

CREATE TABLE `star` (
  `sID` int(11) NOT NULL,
  `cID` int(11) NOT NULL,
  `rID` int(11) NOT NULL,
  `bID` int(11) NOT NULL,
  `rate` int(11) DEFAULT NULL CHECK (`rate` between 1 and 5),
  `comment` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `bro`
--
ALTER TABLE `bro`
  ADD PRIMARY KEY (`bID`),
  ADD UNIQUE KEY `email` (`email`);

--
-- 資料表索引 `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `rID` (`rID`);

--
-- 資料表索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`cID`),
  ADD UNIQUE KEY `email` (`email`);

--
-- 資料表索引 `discount`
--
ALTER TABLE `discount`
  ADD PRIMARY KEY (`dID`);

--
-- 資料表索引 `food`
--
ALTER TABLE `food`
  ADD PRIMARY KEY (`fID`),
  ADD KEY `rID` (`rID`),
  ADD KEY `ID` (`ID`);

--
-- 資料表索引 `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`oID`),
  ADD KEY `bID` (`bID`),
  ADD KEY `cID` (`cID`),
  ADD KEY `dID` (`dID`),
  ADD KEY `rID` (`rID`);

--
-- 資料表索引 `restaurant`
--
ALTER TABLE `restaurant`
  ADD PRIMARY KEY (`rID`),
  ADD UNIQUE KEY `email` (`email`);

--
-- 資料表索引 `star`
--
ALTER TABLE `star`
  ADD PRIMARY KEY (`sID`),
  ADD KEY `bID` (`bID`),
  ADD KEY `cID` (`cID`),
  ADD KEY `rID` (`rID`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `bro`
--
ALTER TABLE `bro`
  MODIFY `bID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `categories`
--
ALTER TABLE `categories`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `cID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `discount`
--
ALTER TABLE `discount`
  MODIFY `dID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `food`
--
ALTER TABLE `food`
  MODIFY `fID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order`
--
ALTER TABLE `order`
  MODIFY `oID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `rID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `star`
--
ALTER TABLE `star`
  MODIFY `sID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`rID`) REFERENCES `restaurant` (`rID`);

--
-- 資料表的限制式 `food`
--
ALTER TABLE `food`
  ADD CONSTRAINT `food_ibfk_1` FOREIGN KEY (`rID`) REFERENCES `restaurant` (`rID`),
  ADD CONSTRAINT `food_ibfk_2` FOREIGN KEY (`ID`) REFERENCES `categories` (`ID`);

--
-- 資料表的限制式 `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`bID`) REFERENCES `bro` (`bID`),
  ADD CONSTRAINT `order_ibfk_2` FOREIGN KEY (`cID`) REFERENCES `customer` (`cID`),
  ADD CONSTRAINT `order_ibfk_3` FOREIGN KEY (`dID`) REFERENCES `discount` (`dID`),
  ADD CONSTRAINT `order_ibfk_4` FOREIGN KEY (`rID`) REFERENCES `restaurant` (`rID`);

--
-- 資料表的限制式 `star`
--
ALTER TABLE `star`
  ADD CONSTRAINT `star_ibfk_1` FOREIGN KEY (`bID`) REFERENCES `bro` (`bID`),
  ADD CONSTRAINT `star_ibfk_2` FOREIGN KEY (`cID`) REFERENCES `customer` (`cID`),
  ADD CONSTRAINT `star_ibfk_3` FOREIGN KEY (`rID`) REFERENCES `food` (`fID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
