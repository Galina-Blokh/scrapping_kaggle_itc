CREATE TABLE `teams` (
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` int
);

CREATE TABLE `competition` (
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `organizator_name` varchar(256),
  `description` varchar(256),
  `link` varchar(256),
  `teams_count` int,
  `headline` varchar(256),
  `entries_competit` int,
  `d_start` datetime,
  `d_end` datetime,
  `prize` int,
  `number_topics` int
);

CREATE TABLE `leaderboard` (
  `compet_id` int,
  `team_id` int,
  `place_rank` int,
  `entries_leader` int,
  `score` int,
  `position_changed` int
);

CREATE TABLE `tags` (
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `tag` varchar(50)
);

CREATE TABLE `competags` (
  `tag_id` int,
  `competition_id` int
);

ALTER TABLE `leaderboard` ADD FOREIGN KEY (`compet_id`) REFERENCES `competition` (`id`);

ALTER TABLE `leaderboard` ADD FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`);

ALTER TABLE `competags` ADD FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`);

ALTER TABLE `competags` ADD FOREIGN KEY (`competition_id`) REFERENCES `competition` (`id`);
