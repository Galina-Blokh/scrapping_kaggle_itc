CREATE TABLE `link` (
  `id` int PRIMARY KEY NOT NULL,
  `competition_id` int,
  `link` varchar(256)
);

CREATE TABLE `competition` (
  `id` int PRIMARY KEY NOT NULL,
  `organizator_id` int,
  `teams_count` int,
  `entries` int,
  `d_start` datetime,
  `d_end` datetime,
  `prize` varchar(50),
  `headline` varchar(256)
);

CREATE TABLE `organizator` (
  `id` int PRIMARY KEY NOT NULL,
  `name` varchar(50)
);

CREATE TABLE `description` (
  `id` int PRIMARY KEY NOT NULL,
  `competition_id` int,
  `text` varchar(256)
);

ALTER TABLE `link` ADD FOREIGN KEY (`competition_id`) REFERENCES `competition` (`id`);

ALTER TABLE `competition` ADD FOREIGN KEY (`organizator_id`) REFERENCES `organizator` (`id`);

ALTER TABLE `description` ADD FOREIGN KEY (`competition_id`) REFERENCES `competition` (`id`);
