-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 28, 2026 at 06:07 AM
-- Server version: 8.4.7
-- PHP Version: 8.5.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tugas_2_fuzzy`
--

-- --------------------------------------------------------

--
-- Table structure for table `domain_kategori_usia`
--

DROP TABLE IF EXISTS `domain_kategori_usia`;
CREATE TABLE IF NOT EXISTS `domain_kategori_usia` (
  `id_kategori` int NOT NULL AUTO_INCREMENT,
  `nama_kategori` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rentang_usia` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `param_a` double NOT NULL,
  `param_b` double NOT NULL,
  `param_c` double NOT NULL,
  `param_d` double NOT NULL,
  PRIMARY KEY (`id_kategori`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `domain_kategori_usia`
--

INSERT INTO `domain_kategori_usia` (`id_kategori`, `nama_kategori`, `rentang_usia`, `param_a`, `param_b`, `param_c`, `param_d`) VALUES
(1, 'Bayi / Anak Usia Dini', '0-5 tahun', 0, 2, 3, 5),
(2, 'Anak-anak', '6-11 tahun', 6, 8, 9, 11),
(3, 'Remaja', '10-19 tahun', 10, 14, 15, 19),
(4, 'Pemuda', '15-24 tahun', 15, 19, 20, 24),
(5, 'Dewasa', '20-65 tahun', 20, 42, 43, 65),
(6, 'Lanjut Usia', '60-80 tahun', 60, 69.5, 70.5, 80);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
