DROP DATABASE IF EXISTS KaggleITC;

CREATE DATABASE KaggleITC;

USE KaggleITC;


CREATE TABLE teams (
  team_id int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  name  varchar(256)
);



CREATE TABLE competitions (
  competition_id int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  organizator_name varchar(256),
  description text,
  link varchar(256),
  teams_count int,
  competitors int,
  header varchar(256),
  entries_competition int,
  competition_start datetime,
  competition_end datetime,
  prize int,
  number_topics int,
  got_by_api int,
  category varchar(256),
  maxDailySubmissions int
);

CREATE TABLE leaderboard (
  competition_id int,
  team_id int,
  place int,
  entries_leader int,
  score float,
  last_entry varchar(20)
);

CREATE TABLE tags (
  tag_id int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  tag varchar(50)
);

CREATE TABLE compet_tags (
  tag_id int,
  competition_id int
);

CREATE TABLE kernels (
  kernel_id int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  competition_id int,
  author varchar(250),
  name varchar(250),
  votes int
);


ALTER TABLE leaderboard ADD FOREIGN KEY (competition_id) REFERENCES competitions (competition_id);

ALTER TABLE leaderboard ADD FOREIGN KEY (team_id) REFERENCES teams (team_id);

ALTER TABLE compet_tags ADD FOREIGN KEY (tag_id) REFERENCES tags (tag_id);

ALTER TABLE compet_tags ADD FOREIGN KEY (competition_id) REFERENCES competitions (competition_id);

ALTER TABLE kernels ADD FOREIGN KEY (competition_id) REFERENCES competitions (competition_id);
