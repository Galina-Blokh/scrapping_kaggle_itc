CREATE TABLE 'teams' (
  'team_id' int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  'name'  varchar(256)
);

CREATE TABLE 'competition' (
  'competition_id' int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  'organizator_name' varchar(256),
  'description' text,
  'link' varchar(256),
  'teams_count' int,
  'headline' varchar(256),
  'entries_competition' int,
  'd_start' datetime,
  'd_end' datetime,
  'prize' int,
  'number_topics' int
);

CREATE TABLE 'leaderboard' (
  'competition_id' int,
  'team_id' int,
  'place_rank' int,
  'entries_leader' int,
  'score' float,
  'position_changed' int
);

CREATE TABLE 'tags' (
  'tag_id' int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  'tag' varchar(50)
);

CREATE TABLE 'competags' (
  'tag_id' int,
  'competition_id' int
);

ALTER TABLE 'leaderboard' ADD FOREIGN KEY ('competition_key') REFERENCES 'competition' ('competition_id');

ALTER TABLE 'leaderboard' ADD FOREIGN KEY ('team_key') REFERENCES 'teams' ('team_id');

ALTER TABLE 'competags' ADD FOREIGN KEY ('tag_key') REFERENCES 'tags' ('tag_id');

ALTER TABLE 'competags' ADD FOREIGN KEY ('competition_key') REFERENCES 'competition' ('competition_id');