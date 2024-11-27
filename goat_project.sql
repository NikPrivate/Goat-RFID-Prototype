-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 27, 2024 at 02:53 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `goat_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `name`, `email`, `password`) VALUES
(1, 'admin', 'admin@gmail.com', 'admin123'),
(2, 'admin2', 'admin2@gmail.com', 'admin123');

-- --------------------------------------------------------

--
-- Table structure for table `breeding`
--

CREATE TABLE `breeding` (
  `uid` varchar(255) NOT NULL,
  `partner_uid` varchar(255) NOT NULL,
  `program_date` datetime NOT NULL,
  `pregnancy_check_date` datetime NOT NULL,
  `expected_birth_date` datetime NOT NULL,
  `breeding_method` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `farmer`
--

CREATE TABLE `farmer` (
  `Id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `date_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `farmer`
--

INSERT INTO `farmer` (`Id`, `name`, `email`, `password`, `date_time`) VALUES
(9, 'ahmad', 'ahmad@gmail.com', 'ahmad123', '2024-09-09 11:02:00'),
(10, 'farmer5', 'farmer5@gmail.com', 'farmer123', '2024-09-12 11:27:00'),
(11, 'farmer7', 'farmer7@gmail.com', 'farmer7123', '2024-09-13 10:36:00');

-- --------------------------------------------------------

--
-- Table structure for table `feed_price`
--

CREATE TABLE `feed_price` (
  `Id` int(255) NOT NULL,
  `time` datetime NOT NULL,
  `total_spend` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feed_price`
--

INSERT INTO `feed_price` (`Id`, `time`, `total_spend`) VALUES
(13, '2024-08-01 15:19:00', 4000),
(14, '2024-08-21 15:20:00', 3000),
(15, '2024-09-07 15:20:00', 2500),
(17, '2024-06-05 15:21:00', 3000);

-- --------------------------------------------------------

--
-- Table structure for table `goat`
--

CREATE TABLE `goat` (
  `uid` varchar(255) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `image_path` varchar(255) NOT NULL,
  `breed` varchar(255) NOT NULL,
  `age` int(255) NOT NULL,
  `weight` int(255) NOT NULL,
  `register_time` datetime NOT NULL,
  `birth_date` datetime NOT NULL,
  `health_status` varchar(255) NOT NULL,
  `vaccine_type` varchar(255) NOT NULL,
  `treatment_time` datetime NOT NULL,
  `next_vaccine_time` datetime NOT NULL,
  `rfid_scan_time` datetime NOT NULL,
  `mom_uid` varchar(255) DEFAULT NULL,
  `dad_uid` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `goat`
--

INSERT INTO `goat` (`uid`, `gender`, `image_path`, `breed`, `age`, `weight`, `register_time`, `birth_date`, `health_status`, `vaccine_type`, `treatment_time`, `next_vaccine_time`, `rfid_scan_time`, `mom_uid`, `dad_uid`) VALUES
('4D E1 45 43', 'Male', 'static/baby_goat.jpeg', 'Alpine', 13, 6, '2024-10-09 12:49:00', '2024-10-02 12:49:00', 'healthy', '', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '2024-10-15 16:23:17', 'BD 14 7B 42', '8D 65 AD 42'),
('5D 6A 8B 43', 'Female', 'static/female_goat_2.jpg', 'Alpine', 69, 53, '2024-10-09 13:05:00', '2024-08-01 13:05:00', 'healthy', 'CD&T (Clostridial Diseases & Tetanus)', '2024-11-09 00:00:00', '2025-11-08 16:00:00', '2024-10-15 10:50:55', NULL, NULL),
('6D 6D 6F 42', 'Female', 'static/baby_goat_2.jpg', 'Boer', 9, 6, '2024-10-09 13:02:00', '2024-10-05 13:02:00', 'healthy', '', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '2024-10-15 10:52:38', '5D 6A 8B 43', '8D 65 AD 42'),
('8D 65 AD 42', 'Male', 'static/goat_image.jpg', 'Alpine', 0, 70, '2024-10-08 22:15:00', '2024-09-01 22:15:00', 'healthy', 'CD&T (Clostridial Diseases & Tetanus)', '1970-01-01 00:00:00', '1970-12-31 16:30:00', '2024-10-15 16:22:35', NULL, NULL),
('BD 14 7B 42', 'Female', 'static/female_goat.jpg', 'Boer', 69, 50, '2024-10-09 12:40:00', '2024-08-01 12:40:00', 'healthy', 'CD&T (Clostridial Diseases & Tetanus)', '1970-01-01 00:00:00', '1970-12-31 16:30:00', '2024-10-14 22:58:19', NULL, NULL),
('BD 18 26 43', 'Female', 'static/baby_goat3.jpg', 'Alpine', 4, 4, '2024-10-15 10:24:00', '2024-10-11 10:24:00', '', '', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '2024-10-15 10:50:45', '6D 6D 6F 42', '4D E1 45 43'),
('FD 92 B9 4B', 'Male', 'static/baby_goat_4.jpg', 'Alpine', 4, 1, '2024-10-15 10:48:00', '2024-10-11 10:48:00', '', '', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '2024-10-15 10:50:34', '6D 6D 6F 42', '4D E1 45 43');

-- --------------------------------------------------------

--
-- Table structure for table `health_tracker`
--

CREATE TABLE `health_tracker` (
  `uid` varchar(255) NOT NULL,
  `treatment_form` varchar(255) NOT NULL,
  `vaccination_form` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `health_tracker`
--

INSERT INTO `health_tracker` (`uid`, `treatment_form`, `vaccination_form`) VALUES
('BD 14 7B 42', '', ''),
('4D E1 45 43', '', ''),
('6D 6D 6F 42', '', ''),
('5D 6A 8B 43', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `slaughter`
--

CREATE TABLE `slaughter` (
  `uid` varchar(255) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `register_time` datetime NOT NULL,
  `weight` int(255) NOT NULL,
  `sold_amount` int(255) NOT NULL,
  `buyer` varchar(255) NOT NULL,
  `cause_of_death` varchar(255) NOT NULL,
  `slaughter_cost` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `slaughter`
--

INSERT INTO `slaughter` (`uid`, `gender`, `register_time`, `weight`, `sold_amount`, `buyer`, `cause_of_death`, `slaughter_cost`) VALUES
('4D E1 45 43', 'Female', '2024-09-06 10:29:00', 60, 7000, 'abu', 'slaughter', 1000),
('5D 6A 8B 43', 'Male', '2024-09-11 16:42:00', 70, 5000, 'abu', 'slaugher', 700);

-- --------------------------------------------------------

--
-- Table structure for table `vet`
--

CREATE TABLE `vet` (
  `Id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `date_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vet`
--

INSERT INTO `vet` (`Id`, `name`, `email`, `password`, `date_time`) VALUES
(26, 'olaf', 'olaf@gmail.com', 'olaf123', '2024-09-09 15:45:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `farmer`
--
ALTER TABLE `farmer`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `feed_price`
--
ALTER TABLE `feed_price`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `goat`
--
ALTER TABLE `goat`
  ADD PRIMARY KEY (`uid`),
  ADD KEY `mom_uid` (`mom_uid`),
  ADD KEY `dad_uid` (`dad_uid`);

--
-- Indexes for table `slaughter`
--
ALTER TABLE `slaughter`
  ADD PRIMARY KEY (`uid`);

--
-- Indexes for table `vet`
--
ALTER TABLE `vet`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `farmer`
--
ALTER TABLE `farmer`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `feed_price`
--
ALTER TABLE `feed_price`
  MODIFY `Id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `vet`
--
ALTER TABLE `vet`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `goat`
--
ALTER TABLE `goat`
  ADD CONSTRAINT `goat_ibfk_1` FOREIGN KEY (`mom_uid`) REFERENCES `goat` (`uid`),
  ADD CONSTRAINT `goat_ibfk_2` FOREIGN KEY (`dad_uid`) REFERENCES `goat` (`uid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
