-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 27, 2024 at 09:48 AM
-- Server version: 10.1.29-MariaDB
-- PHP Version: 7.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mp_uas`
--

-- --------------------------------------------------------

--
-- Table structure for table `pembeli`
--

CREATE TABLE `pembeli` (
  `id_pembeli` int(11) NOT NULL,
  `nama_pembeli` varchar(50) NOT NULL,
  `jk_pembeli` enum('pria','wanita') NOT NULL,
  `alamat` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pembeli`
--

INSERT INTO `pembeli` (`id_pembeli`, `nama_pembeli`, `jk_pembeli`, `alamat`) VALUES
(1, 'Ran', 'pria', 'Kudus'),
(3, 'Rin', 'wanita', 'Kudus'),
(4, 'Ren', 'pria', 'Pati'),
(5, 'Ris', 'wanita', 'Sukolilo');

-- --------------------------------------------------------

--
-- Table structure for table `penjualan`
--

CREATE TABLE `penjualan` (
  `id_penjualan` int(5) NOT NULL,
  `tanggal` date NOT NULL,
  `kasir` varchar(30) NOT NULL,
  `id_pembeli` int(5) NOT NULL,
  `id_sembako` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `penjualan`
--

INSERT INTO `penjualan` (`id_penjualan`, `tanggal`, `kasir`, `id_pembeli`, `id_sembako`) VALUES
(1, '2024-06-19', 'Mas Andre', 1, 2),
(2, '2024-06-27', 'Mas Kasir', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `sembako`
--

CREATE TABLE `sembako` (
  `id_sembako` int(10) NOT NULL,
  `nama_sembako` varchar(20) NOT NULL,
  `harga` int(10) NOT NULL,
  `quantity` int(5) NOT NULL,
  `satuan` enum('Kg','L') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sembako`
--

INSERT INTO `sembako` (`id_sembako`, `nama_sembako`, `harga`, `quantity`, `satuan`) VALUES
(1, 'Minyak', 20000, 4, 'L'),
(2, 'Beras', 10000, 1, 'Kg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pembeli`
--
ALTER TABLE `pembeli`
  ADD PRIMARY KEY (`id_pembeli`);

--
-- Indexes for table `penjualan`
--
ALTER TABLE `penjualan`
  ADD PRIMARY KEY (`id_penjualan`),
  ADD KEY `id_pembeli` (`id_pembeli`),
  ADD KEY `id_sembako` (`id_sembako`);

--
-- Indexes for table `sembako`
--
ALTER TABLE `sembako`
  ADD PRIMARY KEY (`id_sembako`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pembeli`
--
ALTER TABLE `pembeli`
  MODIFY `id_pembeli` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `penjualan`
--
ALTER TABLE `penjualan`
  MODIFY `id_penjualan` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sembako`
--
ALTER TABLE `sembako`
  MODIFY `id_sembako` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `penjualan`
--
ALTER TABLE `penjualan`
  ADD CONSTRAINT `penjualan_ibfk_1` FOREIGN KEY (`id_pembeli`) REFERENCES `pembeli` (`id_pembeli`),
  ADD CONSTRAINT `penjualan_ibfk_2` FOREIGN KEY (`id_sembako`) REFERENCES `sembako` (`id_sembako`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
