CREATE DATABASE IF NOT EXISTS `fuzzy_modul1` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `fuzzy_modul1`;

DROP TABLE IF EXISTS `usia_bayi`;
CREATE TABLE `usia_bayi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usia_min` double NOT NULL,
  `usia_max` double NOT NULL,
  `nilai_fuzzy` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_bayi` (`usia_min`,`usia_max`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usia_bayi` (`id`, `usia_min`, `usia_max`, `nilai_fuzzy`) VALUES
(1, 0, 2.5, 'fungsi_bayi_naik'),
(2, 2.5, 5, 'fungsi_bayi_turun'),
(3, 5, 150, '0');

DROP TABLE IF EXISTS `usia_anak`;
CREATE TABLE `usia_anak` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usia_min` double NOT NULL,
  `usia_max` double NOT NULL,
  `nilai_fuzzy` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_anak` (`usia_min`,`usia_max`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usia_anak` (`id`, `usia_min`, `usia_max`, `nilai_fuzzy`) VALUES
(1, 0, 5, '0'),
(2, 5, 8.5, 'fungsi_anak_naik'),
(3, 8.5, 11, 'fungsi_anak_turun'),
(4, 11, 150, '0');

DROP TABLE IF EXISTS `usia_remaja`;
CREATE TABLE `usia_remaja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usia_min` double NOT NULL,
  `usia_max` double NOT NULL,
  `nilai_fuzzy` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_remaja` (`usia_min`,`usia_max`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usia_remaja` (`id`, `usia_min`, `usia_max`, `nilai_fuzzy`) VALUES
(1, 0, 10, '0'),
(2, 10, 14.5, 'fungsi_remaja_naik'),
(3, 14.5, 19, 'fungsi_remaja_turun'),
(4, 19, 150, '0');

DROP TABLE IF EXISTS `usia_pemuda`;
CREATE TABLE `usia_pemuda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usia_min` double NOT NULL,
  `usia_max` double NOT NULL,
  `nilai_fuzzy` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_pemuda` (`usia_min`,`usia_max`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usia_pemuda` (`id`, `usia_min`, `usia_max`, `nilai_fuzzy`) VALUES
(1, 0, 15, '0'),
(2, 15, 19.5, 'fungsi_pemuda_naik'),
(3, 19.5, 24, 'fungsi_pemuda_turun'),
(4, 24, 150, '0');

DROP TABLE IF EXISTS `usia_dewasa`;
CREATE TABLE `usia_dewasa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usia_min` double NOT NULL,
  `usia_max` double NOT NULL,
  `nilai_fuzzy` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_dewasa` (`usia_min`,`usia_max`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usia_dewasa` (`id`, `usia_min`, `usia_max`, `nilai_fuzzy`) VALUES
(1, 0, 20, '0'),
(2, 20, 42.5, 'fungsi_dewasa_naik'),
(3, 42.5, 65, 'fungsi_dewasa_turun'),
(4, 65, 150, '0');

DROP TABLE IF EXISTS `usia_lansia`;
CREATE TABLE `usia_lansia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usia_min` double NOT NULL,
  `usia_max` double NOT NULL,
  `nilai_fuzzy` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_lansia` (`usia_min`,`usia_max`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usia_lansia` (`id`, `usia_min`, `usia_max`, `nilai_fuzzy`) VALUES
(1, 0, 60, '0'),
(2, 60, 70, 'fungsi_lansia_naik'),
(3, 70, 80, 'fungsi_lansia_turun'),
(4, 80, 150, '0');

