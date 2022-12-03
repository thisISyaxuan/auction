-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2022-12-03 07:30:25
-- 伺服器版本： 10.4.21-MariaDB
-- PHP 版本： 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫: `test`
--

-- --------------------------------------------------------

--
-- 資料表結構 `bid`
--

CREATE TABLE `bid` (
  `bID` int(11) NOT NULL,
  `uID` int(11) NOT NULL,
  `oID` int(11) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `bid`
--

INSERT INTO `bid` (`bID`, `uID`, `oID`, `price`) VALUES
(1, 0, 1, 10),
(2, 0, 1, 11),
(3, 0, 3, 5),
(4, 0, 2, 5),
(5, 0, 2, 7),
(6, 0, 2, 8),
(7, 0, 4, 9),
(8, 0, 3, 8),
(9, 0, 1, 110),
(10, 8, 3, 8),
(11, 0, 3, 120),
(12, 0, 3, 15),
(13, 0, 2, 9),
(14, 0, 6, 123),
(15, 1, 6, 1234),
(16, 1000, 7, 1000),
(17, 3, 7, 10000),
(18, 0, 7, 100000),
(19, 1, 9, 10000);

-- --------------------------------------------------------

--
-- 資料表結構 `object`
--

CREATE TABLE `object` (
  `oID` int(11) NOT NULL,
  `name` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `expire` datetime NOT NULL,
  `uID` int(11) NOT NULL,
  `text` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `object`
--

INSERT INTO `object` (`oID`, `name`, `expire`, `uID`, `text`) VALUES
(1, 'vase', '2022-11-29 06:11:57', 0, ''),
(2, 'Bowl', '2022-11-29 06:11:57', 0, ''),
(3, 'test', '2022-11-28 13:41:17', 1, ''),
(4, 'okokok', '2022-11-28 13:44:04', 0, ''),
(5, '1231221312', '2022-12-03 13:49:20', 0, '333'),
(6, '123122131211', '2022-12-03 13:59:52', 0, '333'),
(7, '123123', '2022-12-03 14:17:09', 0, '11'),
(8, 'last test', '2022-12-03 14:19:24', 0, '如題'),
(9, 'dog', '2022-12-03 14:23:06', 0, '123');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `bid`
--
ALTER TABLE `bid`
  ADD PRIMARY KEY (`bID`);

--
-- 資料表索引 `object`
--
ALTER TABLE `object`
  ADD PRIMARY KEY (`oID`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `bid`
--
ALTER TABLE `bid`
  MODIFY `bID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `object`
--
ALTER TABLE `object`
  MODIFY `oID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
