-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : dim. 19 mai 2024 à 17:27
-- Version du serveur : 10.4.28-MariaDB
-- Version de PHP : 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `db_botnet`
--

-- --------------------------------------------------------

--
-- Structure de la table `interface_servers`
--

CREATE TABLE `interface_servers` (
  `id` int(11) NOT NULL,
  `server_id` text NOT NULL,
  `ipv4` text NOT NULL,
  `proxy_port` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `owner_token` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `tasks`
--

CREATE TABLE `tasks` (
  `id` int(11) NOT NULL,
  `task_type` text NOT NULL,
  `task_id` text NOT NULL,
  `task_args` text NOT NULL,
  `task_status` int(11) NOT NULL,
  `task_date` date NOT NULL,
  `owner_token` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `tasks`
--

INSERT INTO `tasks` (`id`, `task_type`, `task_id`, `task_args`, `task_status`, `task_date`, `owner_token`) VALUES
(1, 'distributed_denial_of_service', 'randomid123', '{\"destination\":\"www.google.com\",\"power\":\"1000\"}', 1, '2024-04-09', '');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `token` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `victims`
--

CREATE TABLE `victims` (
  `id` int(11) NOT NULL,
  `computer_name` text NOT NULL,
  `ipv4` text NOT NULL,
  `port` int(11) NOT NULL,
  `status` text NOT NULL,
  `country` text NOT NULL,
  `session_id` int(11) NOT NULL,
  `latency_ms` int(11) NOT NULL,
  `first_connection` date NOT NULL,
  `owner_token` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `victims`
--

INSERT INTO `victims` (`id`, `computer_name`, `ipv4`, `port`, `status`, `country`, `session_id`, `latency_ms`, `first_connection`, `owner_token`) VALUES
(1, 'james', '192.168.100.1', 4444, 'connected', 'FR', 12, 109, '2024-04-02', ''),
(2, 'test', '212121', 4444, '1', 'FR', 1212, 100, '2024-04-03', '');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `interface_servers`
--
ALTER TABLE `interface_servers`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `victims`
--
ALTER TABLE `victims`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `interface_servers`
--
ALTER TABLE `interface_servers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `victims`
--
ALTER TABLE `victims`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
