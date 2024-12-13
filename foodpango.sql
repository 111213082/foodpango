-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-13 10:10:19
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
  `password` varchar(50) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `verification` tinyint(1) NOT NULL,
  `bank` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `cID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `card` varchar(20) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `address` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

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
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `restaurant`
--

CREATE TABLE `restaurant` (
  `rID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` text NOT NULL,
  `license` varchar(50) NOT NULL,
  `bank` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `announcement` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

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
  ADD PRIMARY KEY (`bID`);

--
-- 資料表索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`cID`);

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
  ADD KEY `rID` (`rID`);

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
  ADD PRIMARY KEY (`rID`);

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
  MODIFY `bID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `cID` int(11) NOT NULL AUTO_INCREMENT;

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
  MODIFY `rID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `star`
--
ALTER TABLE `star`
  MODIFY `sID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `food`
--
ALTER TABLE `food`
  ADD CONSTRAINT `food_ibfk_1` FOREIGN KEY (`rID`) REFERENCES `restaurant` (`rID`);

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
