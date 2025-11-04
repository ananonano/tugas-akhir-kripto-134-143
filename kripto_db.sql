-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 04, 2025 at 07:38 AM
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
-- Database: `kripto_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `timestamp` datetime NOT NULL,
  `action_type` varchar(255) NOT NULL,
  `encrypted_log_entry` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `history`
--

INSERT INTO `history` (`id`, `user_id`, `timestamp`, `action_type`, `encrypted_log_entry`) VALUES
(1, 2, '2025-11-04 00:53:35', 'Super Enkripsi', 0xddca4264bc12329fdab9d16f004a75c1b67d4971b18029e5b45b07bf594863996b917889ce54f0d076d658f11b5dcd920edb62d0d6353b41a5cd4fa769a03e39),
(2, 2, '2025-11-04 00:53:45', 'Super Enkripsi', 0xddca4264bc12329fdab9d16f004a75c1b67d4971b18029e5b45b07bf594863996b917889ce54f0d076d658f11b5dcd92de154fa85ce92225013c2620f6746704),
(3, 2, '2025-11-04 00:54:00', 'Super Enkripsi', 0xddca4264bc12329fdab9d16f004a75c1b67d4971b18029e5b45b07bf594863996b917889ce54f0d076d658f11b5dcd920edb62d0d6353b41a5cd4fa769a03e39),
(4, 2, '2025-11-04 00:54:21', 'Super Dekripsi', 0x5939b4ae522e2340735f0752f613b576bcf5d9ea153a549a5c2b4eda343fbb249049782dfc4f3b9aad17b7782e0b58bbe4a99f7b06efe40d27e071b978bcb75a2dd385deed164b19),
(5, 2, '2025-11-04 00:54:33', 'Super Enkripsi', 0xddca4264bc12329fdab9d16f004a75c1b67d4971b18029e5b45b07bf594863996b917889ce54f0d076d658f11b5dcd925cb7f31b51df1300013c2620f6746704),
(6, 2, '2025-11-04 00:56:58', 'Super Enkripsi', 0xddca4264bc12329fab3f02924c35b74d1efc7c9beb1f0e7ad0b567d4bf00cd368c4fd6aec022568a9789697afad605736c612608f14b74fb0a3a04d9c0262f52),
(7, 2, '2025-11-04 00:57:23', 'Super Dekripsi', 0x5939b4ae522e2340cdf4ae499e385e84d8eb5ab777155fa19049782dfc4f3b9aad17b7782e0b58bbe4a99f7b06efe40d2e5f005d1dc72bdff09c473926270b51013c2620f6746704),
(8, 2, '2025-11-04 00:58:44', 'LSB Hide', 0x500c46d8a5c58ef35f35f0a764686f85d94a595e9c8e32801e1c292428f5f6123dd57705eb9c5b6677122805fc96231ce6ff311eec200c00f0111861346c3da9d5abcdec55228da3e22cfa276087468cee250742909cc522559b87ffb8dc8f8cdbeae181ac5e2670),
(9, 2, '2025-11-04 00:59:15', 'LSB Reveal', 0x4d049818d891943e5441dad5b65c2dadbd67813afd7500a355980d19b2cb005a),
(10, 2, '2025-11-04 00:59:57', 'LSB Hide', 0x500c46d8a5c58ef36f59e7b6c94a00883e45ba50aa16db0ab17975ac9d0a4973e22cfa276087468cee250742909cc522559b87ffb8dc8f8cdbeae181ac5e2670),
(11, 2, '2025-11-04 01:00:13', 'LSB Reveal', 0x4d049818d891943e5441dad5b65c2dadbd67813afd7500a34e160b8d56149e39013c2620f6746704),
(12, 2, '2025-11-04 01:02:46', 'AES Enkripsi File', 0xbb9e72327913dac55c26420b2d58ece60856526d034dfc2753346a9e6ec731b852ff94224dcd955726db2790bc70dd912470b0c6b70b2e24),
(13, 2, '2025-11-04 01:03:22', 'AES Enkripsi File', 0xbb9e72327913dac55c26420b2d58ece60856526d034dfc2753346a9e6ec731b86d3fc1f33ea469c7fcfc7795936274fadfcdc5d73d8b8886),
(14, 2, '2025-11-04 01:03:34', 'AES Enkripsi File', 0xbb9e72327913dac55c26420b2d58ece60856526d034dfc2753346a9e6ec731b86d3fc1f33ea469c7fcfc7795936274fafcfc7795936274fadfcdc5d73d8b8886),
(15, 2, '2025-11-04 01:03:39', 'AES Enkripsi File', 0xbb9e72327913dac55c26420b2d58ece60856526d034dfc2753346a9e6ec731b86d3fc1f33ea469c7fcfc7795936274fafcfc7795936274fafcfc7795936274fadfcdc5d73d8b8886),
(16, 2, '2025-11-04 01:03:47', 'AES Enkripsi File', 0xbb9e72327913dac55c26420b2d58ece60856526d034dfc2753346a9e6ec731b86d3fc1f33ea469c7fcfc7795936274fafcfc7795936274fafcfc7795936274fadfcdc5d73d8b8886),
(17, 2, '2025-11-04 01:04:11', 'AES Enkripsi File', 0x4eecea242e0db154230b70d13eed7d5a21e5cc7bfe7d923afd79c36a23e149a9ed5d8312f23e43b1fcfc7795936274faf7974b6bc8d03ff80a3a04d9c0262f52),
(18, 2, '2025-11-04 01:04:30', 'AES Dekripsi File', 0x4eecea242e0db154230b70d13eed7d5a21e5cc7bfe7d923a33ed8738a33f30528dc35a42794e1da46d3fc1f33ea469c7fcfc7795936274fadfcdc5d73d8b8886),
(19, 2, '2025-11-04 01:05:13', 'AES Enkripsi File', 0x1531e0f2c467954c2a0007f0709e0c3c7d9086f97fbc23cd901bf2b46b9ab95e56c350c9943b7957bc2489c66e5fa34d6ca4061e8ca3094eb61bc8cf3b4c03b56cda87427b8ecdb84dc4616eddcba186770175e9f97a9a7f),
(20, 2, '2025-11-04 01:05:58', 'AES Dekripsi File', 0x1531e0f2c467954c2a0007f0709e0c3c7d9086f97fbc23cd901bf2b46b9ab95e56c350c9943b7957bc2489c66e5fa34d6ca4061e8ca3094ea15962062c487e8760c08290bf67cb7c4dc4616eddcba1864dc4616eddcba186013c2620f6746704),
(21, 1, '2025-11-04 01:23:51', 'CAST-128 Enkripsi File', 0x13e00482d7f90791226a8213cce761dcfce130b09eb0329689d7c41235f90e95512fd004f2037a93b49bcdc5cdf037f8abd512638c5a6de0ff3aa6265283867fcf47a69ddeacb1de86d2d45dc4c6d26d),
(22, 1, '2025-11-04 01:24:14', 'CAST-128 Dekripsi File', 0x13e00482d7f90791226a8213cce761dcfce130b09eb0329689d7c41235f90e95512fd004f2037a93e3b24bd311ef42d05dabf67968b301da12a67381d2db2116cf47a69ddeacb1de7e6c4a2ad53ca787);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`) VALUES
(1, 'aksa', '41dc66c544ec22b6542029be844aae228e503ad2'),
(2, 'danang', '6724326b3e1ef986e896cbb6ed1a86a828cfe11c');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `history`
--
ALTER TABLE `history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `history`
--
ALTER TABLE `history`
  ADD CONSTRAINT `history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
