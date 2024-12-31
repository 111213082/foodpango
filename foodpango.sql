-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-27 06:14:56
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
  `bank` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `bro`
--

INSERT INTO `bro` (`bID`, `name`, `email`, `password`, `phone`, `bank`) VALUES
(1, '老李', '111@gmail.com', '*832EB84CB764129D05D498ED9CA7E5CE9B8F83EB', '0987654321', '(165)1783493189'),
(2, '老孫', '222@gmail.com', '*899ECD04E40F745BD52A4C552BE4A818AC65FAF8', '0912345678', '(666)2841047396');

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
(1, '小羊', 'baa@gmail.com', '*6F12ADE7E5EF3C0284DE0691A2E1188C1AEF28D1', '3789 1658 0642 6705', '0988888888', ''),
(2, '小魚', 'fish@gmail.com', '*E6D7C000DDB4A28666FA2509F5A1B68B2B081C7C', '1234 5678 9101 1121', '0942686318', '');

-- --------------------------------------------------------

--
-- 資料表結構 `detail`
--

CREATE TABLE `detail` (
  `dID` int(11) NOT NULL,
  `oID` int(11) NOT NULL,
  `fID` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 傾印資料表的資料 `detail`
--

INSERT INTO `detail` (`dID`, `oID`, `fID`, `quantity`, `price`) VALUES
(2, 1, 1, 1, 380),
(3, 1, 2, 1, 250);

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

--
-- 傾印資料表的資料 `food`
--

INSERT INTO `food` (`fID`, `rID`, `ID`, `name`, `price`, `is_vegetarian`, `description`, `is_available`) VALUES
(1, 1, 1, '綜合義式冷肉拼盤', 380, 0, '義式火腿、臘腸、起司拼盤', 1),
(2, 1, 1, '卡布里沙拉', 250, 1, '新鮮乳酪、番茄、羅勒', 1),
(3, 1, 1, '烤大蒜蝦', 300, 0, '鮮蝦搭配香料大蒜烘烤', 1),
(4, 1, 2, '番茄羅勒湯', 180, 1, '義大利經典番茄湯搭配羅勒', 1),
(5, 1, 2, '奶油南瓜湯', 200, 1, '濃郁奶油與香甜南瓜融合', 1),
(6, 1, 3, '卡邦尼義大利麵', 350, 0, '蛋黃、培根、帕瑪森起司的完美結合', 1),
(7, 1, 3, '羅勒青醬義大利麵', 320, 1, '新鮮羅勒、松子、橄欖油特製醬料', 1),
(8, 1, 3, '海鮮番茄義大利麵', 400, 0, '鮮蝦、蛤蜊與番茄醬的經典組合', 1),
(9, 1, 4, '瑪格麗特披薩', 300, 1, '番茄醬、乳酪、羅勒葉', 1),
(10, 1, 4, '義式香腸披薩', 400, 0, '手工香腸、番茄醬、辣椒粉', 1),
(11, 1, 5, '提拉米蘇', 220, 0, '義大利經典咖啡甜點', 1),
(12, 1, 5, '義式奶酪', 180, 0, '搭配新鮮莓果醬', 1),
(13, 1, 6, '義式濃縮咖啡', 80, 1, '香濃濃縮咖啡', 1),
(14, 1, 6, '卡布奇諾', 120, 1, '義大利咖啡搭配綿密奶泡', 1),
(15, 1, 6, '自製檸檬氣泡水', 100, 1, '清爽解膩的氣泡水', 1),
(16, 2, 7, '香草冰淇淋', 80, 0, '經典香草風味，入口即化', 1),
(17, 2, 7, '巧克力冰淇淋', 90, 0, '濃郁巧克力，適合甜點愛好者', 1),
(18, 2, 7, '草莓冰淇淋', 90, 0, '新鮮草莓製成，酸甜可口', 1),
(19, 2, 11, '抹茶冰淇淋', 100, 0, '日本宇治抹茶，清新微苦', 1),
(20, 2, 11, '焦糖海鹽冰淇淋', 110, 0, '焦糖甜中帶鹹，口感層次豐富', 1),
(21, 2, 11, '芒果冰淇淋', 120, 0, '熱帶芒果香氣，清爽消暑', 1),
(22, 2, 12, '巧克力聖代', 150, 0, '巧克力冰淇淋搭配巧克力醬、堅果碎', 1),
(23, 2, 12, '水果冰淇淋杯', 160, 0, '香草冰淇淋配上當季水果', 1),
(24, 2, 12, '奶昔冰品杯', 170, 0, '奶昔基底，搭配奶油與餅乾屑', 1),
(25, 2, 13, '熱帶水果冰沙', 130, 0, '芒果、鳳梨、西瓜清新混合', 1),
(26, 2, 13, '藍莓優格冰沙', 140, 0, '健康藍莓配優格，酸甜滋味', 1);

-- --------------------------------------------------------

--
-- 資料表結構 `order`
--

CREATE TABLE `order` (
  `oID` int(11) NOT NULL,
  `cID` int(11) NOT NULL,
  `rID` int(11) NOT NULL,
  `bID` int(11) NOT NULL,
  `status` enum('待確認','已接單','配送中','完成') DEFAULT '待確認',
  `totalPrice` int(10) NOT NULL,
  `note` text DEFAULT NULL,
  `address` text NOT NULL,
  `createdAt` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `prepareTime` int(11) NOT NULL,
  `deliverTime` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `order`
--

INSERT INTO `order` (`oID`, `cID`, `rID`, `bID`, `status`, `totalPrice`, `note`, `address`, `createdAt`, `prepareTime`, `deliverTime`) VALUES
(1, 1, 2, 1, '待確認', 630, NULL, '大草原', '2024-12-27 04:39:21', 20, 20);

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
  `bank` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `time` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `restaurant`
--

INSERT INTO `restaurant` (`rID`, `name`, `email`, `password`, `phone`, `address`, `bank`, `is_active`, `time`) VALUES
(1, 'spagett義', 'spagetti@gmail.com', '*23AE809DDACAF96AF0FD78ED04B6A265E05AA257', '0936409918', '南投縣大同市信義路159號-4\r\n', '(700)3489718757', 0, '本月公休日:19.20號'),
(2, '愛死cream', 'icecream@gmail.com', '*531E182E2F72080AB0740FE2F2D689DBE0146E04', '0982172649', '南投縣大同市大業路78號', '(713)7018095462', 0, '');

-- --------------------------------------------------------

--
-- 資料表結構 `star`
--

CREATE TABLE `star` (
  `sID` int(11) NOT NULL,
  `oID` int(11) NOT NULL,
  `rateR` int(1) NOT NULL,
  `rateB` int(1) NOT NULL,
  `commentR` text DEFAULT NULL,
  `commentB` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `star`
--

INSERT INTO `star` (`sID`, `oID`, `rateR`, `rateB`, `commentR`, `commentB`) VALUES
(1, 1, 5, 5, '好吃', '好快');

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
-- 資料表索引 `detail`
--
ALTER TABLE `detail`
  ADD PRIMARY KEY (`dID`),
  ADD KEY `detail_ibfk_2` (`fID`),
  ADD KEY `detail_ibfk_1` (`oID`);

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
  ADD KEY `order_ibfk_3` (`rID`);

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
  ADD KEY `oID` (`oID`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `bro`
--
ALTER TABLE `bro`
  MODIFY `bID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `categories`
--
ALTER TABLE `categories`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `cID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `detail`
--
ALTER TABLE `detail`
  MODIFY `dID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `food`
--
ALTER TABLE `food`
  MODIFY `fID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order`
--
ALTER TABLE `order`
  MODIFY `oID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `rID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `star`
--
ALTER TABLE `star`
  MODIFY `sID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `categories`
--
ALTER TABLE `categories`
  ADD CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`rID`) REFERENCES `restaurant` (`rID`);

--
-- 資料表的限制式 `detail`
--
ALTER TABLE `detail`
  ADD CONSTRAINT `detail_ibfk_1` FOREIGN KEY (`oID`) REFERENCES `order` (`oID`) ON DELETE CASCADE,
  ADD CONSTRAINT `detail_ibfk_2` FOREIGN KEY (`fID`) REFERENCES `food` (`fID`);

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
  ADD CONSTRAINT `order_ibfk_3` FOREIGN KEY (`rID`) REFERENCES `restaurant` (`rID`);

--
-- 資料表的限制式 `star`
--
ALTER TABLE `star`
  ADD CONSTRAINT `star_ibfk_4` FOREIGN KEY (`oID`) REFERENCES `order` (`oID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
