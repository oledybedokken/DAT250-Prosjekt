-- MySQL:

create database "Nettbank"
use "Nettbank"

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

CREATE TABLE IF NOT EXISTS 'brukere' (
    'id' int(5) NOT NULL AUTO_INCREMENT,
    'email' varchar(32)) NOT NULL,
    'etternavn' varchar(32) NOT NULL,
    'fornavn' varchar(32) NOT NULL,
    'bruker_nr' varchar(16) NOT NULL,
    'dagly_transaksjon_limit' varchar(8) NOT NULL,      -- daglig transaksjons limit. 8 siffer
    'mengde_overfor_hoy' varchar(6) NOT NULL,           -- TRENGER AUTHENTICATION KONFIRMATION, MAKS 10'000'000
    'mengde_overfor_lav' varchar(5) NOT NULL,           -- antall sendt over (log), MAKS 10'0000
    'antall_fra_deg' varchar(10) NOT NULL,              -- Antall briler har gitt
    'antall_fra_andre' varchar(10) NOT NULL,            -- Antall bruker har fått
    'brukskonto' varchar(7) NOT NULL,                   -- MAKS 10'000'000
    UNIQUE KEY 'bruker_nr' ('bruker_nr'),
    UNIQUE KEY 'email' ('email'),
    PRIMARY KEY ('id')
)

CREATE TABLE IF NOT EXISTS `kunder` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `fornavn` varchar(32) NOT NULL,
  `etternavn` varchar(32) NOT NULL,
  `fodselsdato` varchar(6) NOT NULL,               -- 310100 som betyr DD/MM/ÅÅ
  `tlf_nummer` varchar(8) NOT NULL,                -- 82 74 82 42 59
  `email` varchar(32) NOT NULL,
  `passord` varchar(32) NOT NULL,
  `authentication` varchar(5) NOT NULL,            -- Authentication kode, random
  `konto_nr` varchar(16) NOT NULL,
  `by` varchar(16) NOT NULL,
  'fylke' varchar(16) NOT NULL,
  `post` varchar(3) NOT NULL,
  `post_kode` varchar(5) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `konto_nr` (`konto_nr`),
  UNIQUE KEY `email` (`email`)
)

SELECT * FROM 'brukere'
