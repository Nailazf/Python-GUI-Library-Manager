-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 13 Jul 2025 pada 16.16
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `perpustakaan`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `anggota`
--

CREATE TABLE `anggota` (
  `id` int(11) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `tanggal_daftar` date DEFAULT curdate(),
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `anggota`
--

INSERT INTO `anggota` (`id`, `nama`, `email`, `phone`, `alamat`, `tanggal_daftar`, `status`, `created_at`, `updated_at`) VALUES
(1, 'Ahmad Fauzi', 'ahmad.fauzi@email.com', '08123456789', 'Jl. Merdeka No. 123, Jakarta', '2025-07-13', 'active', '2025-07-13 11:55:28', '2025-07-13 11:55:28'),
(2, 'Siti Nurhaliza', 'siti.nurhaliza@email.com', '08234567890', 'Jl. Sudirman No. 456, Bandung', '2025-07-13', 'active', '2025-07-13 11:55:28', '2025-07-13 11:55:28'),
(3, 'Budi Santoso', 'budi.santoso@email.com', '08345678901', 'Jl. Thamrin No. 789, Surabaya', '2025-07-13', 'active', '2025-07-13 11:55:28', '2025-07-13 11:55:28'),
(4, 'Dewi Sartika', 'dewi.sartika@email.com', '08456789012', 'Jl. Diponegoro No. 321, Yogyakarta', '2025-07-13', 'active', '2025-07-13 11:55:28', '2025-07-13 11:55:28'),
(5, 'Rizki Pratama', 'rizki.pratama@email.com', '08567890123', 'Jl. Gatot Subroto No. 654, Medan', '2025-07-13', 'active', '2025-07-13 11:55:28', '2025-07-13 11:55:28');

-- --------------------------------------------------------

--
-- Struktur dari tabel `buku`
--

CREATE TABLE `buku` (
  `id` int(11) NOT NULL,
  `judul` varchar(255) NOT NULL,
  `pengarang` varchar(255) NOT NULL,
  `kategori` varchar(100) DEFAULT NULL,
  `deskripsi` text DEFAULT NULL,
  `jumlah_total` int(11) DEFAULT 1,
  `jumlah_tersedia` int(11) DEFAULT 1,
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `buku`
--

INSERT INTO `buku` (`id`, `judul`, `pengarang`, `kategori`, `deskripsi`, `jumlah_total`, `jumlah_tersedia`, `status`, `created_at`, `updated_at`) VALUES
(1, 'The Great Gatsby', 'F.SCOTT FITZGERald', 'Fiction', 'Mengisahkan Jay Gatsby, seorang jutawan misterius yang terobsesi dengan cinta masa lalunya, Daisy Buchanan.', 3, 2, 'active', '2025-07-13 12:32:26', '2025-07-13 12:33:45'),
(2, 'Harper lee to kill a mockingbird', 'harper lee', 'Fiction', 'Novel sejarah pembunuhan', 2, 1, 'active', '2025-07-13 12:32:26', '2025-07-13 12:33:45'),
(3, '1984', 'George Orwell', 'Technology', 'Buku pembelajaran algoritma', 4, 4, 'active', '2025-07-13 12:32:26', '2025-07-13 14:12:58'),
(4, 'Sejarah Indonesia Modern', 'Dr. Sartono Kartodirdjo', 'Thriller', 'Buku ini adalah peringatan tentang bahaya otoritarianisme, pengawasan massal, dan manipulasi kebenasan.', 1, 1, 'active', '2025-07-13 12:32:26', '2025-07-13 14:13:03'),
(5, 'Pride and Prejudice', 'Jane auten', 'Romantic', 'Novel Romansa remaja', 2, 2, 'active', '2025-07-13 12:32:26', '2025-07-13 12:32:26'),
(6, 'The catcher in the rye', 'J.D. salinger', 'Literature', 'Kumpulan sastra Indonesia', 2, 2, 'active', '2025-07-13 12:32:26', '2025-07-13 12:32:26'),
(7, 'Little women', 'Louise may allcot', 'Education', 'edukasi terhadap para wanita', 4, 4, 'active', '2025-07-13 12:32:26', '2025-07-13 12:32:26'),
(8, 'Rich dad poor dad', 'Robert T. kiyosaki', 'Bussiness', 'pentingnya kewirausahaan', 0, 0, 'active', '2025-07-13 12:32:26', '2025-07-13 12:32:26'),
(9, 'Atomic Habits', 'James Clear', 'Psychology', 'Buku ini mengajarkan cara memahami dan merancang kebiasaan Anda untuk mencapai tujuan', 2, 2, 'active', '2025-07-13 12:32:26', '2025-07-13 12:32:26'),
(10, 'A brief history of humankind', 'Yuval Noah Harari', 'sains', 'Sebuah eksplorasi ambisius tentang sejarah umat manusia, dari awal mula Homo Sapiens hingga masa kini, dan bahkan meramalkan masa depan', 0, 0, 'active', '2025-07-13 12:32:26', '2025-07-13 12:32:26');

-- --------------------------------------------------------

--
-- Struktur dari tabel `denda`
--

CREATE TABLE `denda` (
  `id` int(11) NOT NULL,
  `loan_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `status` enum('unpaid','paid') DEFAULT 'unpaid',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `loans`
--

CREATE TABLE `loans` (
  `id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `tanggal_pinjam` date NOT NULL,
  `tanggal_kembali` date NOT NULL,
  `tanggal_dikembalikan` date DEFAULT NULL,
  `status` enum('dipinjam','dikembalikan','terlambat') DEFAULT 'dipinjam',
  `denda` decimal(10,2) DEFAULT 0.00,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `loans`
--

INSERT INTO `loans` (`id`, `book_id`, `member_id`, `tanggal_pinjam`, `tanggal_kembali`, `tanggal_dikembalikan`, `status`, `denda`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2025-07-01', '2025-07-08', NULL, 'dipinjam', 0.00, '2025-07-13 12:33:19', '2025-07-13 12:33:19'),
(2, 2, 2, '2025-07-05', '2025-07-12', NULL, 'dipinjam', 0.00, '2025-07-13 12:33:19', '2025-07-13 12:33:19'),
(3, 3, 3, '2025-06-20', '2025-06-27', NULL, 'dikembalikan', 0.00, '2025-07-13 12:33:19', '2025-07-13 12:33:19'),
(4, 4, 4, '2025-07-10', '2025-07-17', NULL, 'dikembalikan', 0.00, '2025-07-13 12:33:19', '2025-07-13 14:13:03'),
(5, 5, 5, '2025-06-15', '2025-06-22', NULL, 'dikembalikan', 0.00, '2025-07-13 12:33:19', '2025-07-13 12:33:19'),
(6, 3, 4, '2025-07-16', '2025-07-20', NULL, 'dikembalikan', 0.00, '2025-07-13 14:12:38', '2025-07-13 14:12:58');

-- --------------------------------------------------------

--
-- Stand-in struktur untuk tampilan `v_active_loans`
-- (Lihat di bawah untuk tampilan aktual)
--
CREATE TABLE `v_active_loans` (
`id` int(11)
,`tanggal_pinjam` date
,`tanggal_kembali` date
,`status` enum('dipinjam','dikembalikan','terlambat')
,`judul` varchar(255)
,`pengarang` varchar(255)
,`kategori` varchar(100)
,`nama_peminjam` varchar(255)
,`email` varchar(255)
,`phone` varchar(20)
,`status_keterlambatan` varchar(20)
,`hari_terlambat` int(7)
);

-- --------------------------------------------------------

--
-- Stand-in struktur untuk tampilan `v_available_books`
-- (Lihat di bawah untuk tampilan aktual)
--
CREATE TABLE `v_available_books` (
`id` int(11)
,`judul` varchar(255)
,`pengarang` varchar(255)
,`kategori` varchar(100)
,`deskripsi` text
,`jumlah_total` int(11)
,`jumlah_tersedia` int(11)
,`status` enum('active','inactive')
,`created_at` timestamp
,`updated_at` timestamp
,`available_count` bigint(22)
);

-- --------------------------------------------------------

--
-- Struktur untuk view `v_active_loans`
--
DROP TABLE IF EXISTS `v_active_loans`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_active_loans`  AS SELECT `l`.`id` AS `id`, `l`.`tanggal_pinjam` AS `tanggal_pinjam`, `l`.`tanggal_kembali` AS `tanggal_kembali`, `l`.`status` AS `status`, `b`.`judul` AS `judul`, `b`.`pengarang` AS `pengarang`, `b`.`kategori` AS `kategori`, `m`.`nama` AS `nama_peminjam`, `m`.`email` AS `email`, `m`.`phone` AS `phone`, CASE WHEN `l`.`tanggal_kembali` < curdate() THEN 'Terlambat' WHEN `l`.`tanggal_kembali` = curdate() THEN 'Jatuh Tempo Hari Ini' ELSE 'Normal' END AS `status_keterlambatan`, to_days(curdate()) - to_days(`l`.`tanggal_kembali`) AS `hari_terlambat` FROM ((`loans` `l` join `buku` `b` on(`l`.`book_id` = `b`.`id`)) join `anggota` `m` on(`l`.`member_id` = `m`.`id`)) ;

-- --------------------------------------------------------

--
-- Struktur untuk view `v_available_books`
--
DROP TABLE IF EXISTS `v_available_books`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_available_books`  AS SELECT `b`.`id` AS `id`, `b`.`judul` AS `judul`, `b`.`pengarang` AS `pengarang`, `b`.`kategori` AS `kategori`, `b`.`deskripsi` AS `deskripsi`, `b`.`jumlah_total` AS `jumlah_total`, `b`.`jumlah_tersedia` AS `jumlah_tersedia`, `b`.`status` AS `status`, `b`.`created_at` AS `created_at`, `b`.`updated_at` AS `updated_at`, `b`.`jumlah_total`- coalesce(`active_loans`.`count`,0) AS `available_count` FROM (`buku` `b` left join (select `loans`.`book_id` AS `book_id`,count(0) AS `count` from `loans` where `loans`.`status` = 'dipinjam' group by `loans`.`book_id`) `active_loans` on(`b`.`id` = `active_loans`.`book_id`)) WHERE `b`.`status` = 'active' ;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `anggota`
--
ALTER TABLE `anggota`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_members_email` (`email`);

--
-- Indeks untuk tabel `buku`
--
ALTER TABLE `buku`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_books_status` (`status`);

--
-- Indeks untuk tabel `denda`
--
ALTER TABLE `denda`
  ADD PRIMARY KEY (`id`),
  ADD KEY `loan_id` (`loan_id`);

--
-- Indeks untuk tabel `loans`
--
ALTER TABLE `loans`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_id` (`book_id`),
  ADD KEY `member_id` (`member_id`),
  ADD KEY `idx_loans_status` (`status`),
  ADD KEY `idx_loans_dates` (`tanggal_pinjam`,`tanggal_kembali`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `anggota`
--
ALTER TABLE `anggota`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `buku`
--
ALTER TABLE `buku`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT untuk tabel `denda`
--
ALTER TABLE `denda`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `loans`
--
ALTER TABLE `loans`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `denda`
--
ALTER TABLE `denda`
  ADD CONSTRAINT `denda_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`id`);

--
-- Ketidakleluasaan untuk tabel `loans`
--
ALTER TABLE `loans`
  ADD CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `buku` (`id`),
  ADD CONSTRAINT `loans_ibfk_2` FOREIGN KEY (`member_id`) REFERENCES `anggota` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
