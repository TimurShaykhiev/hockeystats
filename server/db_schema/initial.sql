CREATE DATABASE IF NOT EXISTS NHL_STATS
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS versions
(
  version SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
  applied DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS updates
(
  type SMALLINT UNSIGNED PRIMARY KEY NOT NULL,
  description VARCHAR(255),
  start DATE NOT NULL,
  end DATE NOT NULL,
  successful TINYINT(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS conferences
(
  id BIGINT(20) UNSIGNED PRIMARY KEY NOT NULL,
  name VARCHAR(100) NOT NULL,
  active TINYINT(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS divisions
(
  id BIGINT(20) UNSIGNED PRIMARY KEY NOT NULL,
  name VARCHAR(100) NOT NULL,
  conference_id BIGINT(20) UNSIGNED,
  active TINYINT(1) NOT NULL,
  CONSTRAINT divisions_conferences_id_fk FOREIGN KEY (conference_id) REFERENCES conferences (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS teams
(
  id BIGINT(20) UNSIGNED PRIMARY KEY NOT NULL,
  name VARCHAR(100) NOT NULL,
  abbreviation VARCHAR(5),
  location VARCHAR(100),
  venue_name VARCHAR(100),
  venue_city VARCHAR(100),
  division_id BIGINT(20) UNSIGNED,
  active TINYINT(1) NOT NULL,
  CONSTRAINT teams_divisions_id_fk FOREIGN KEY (division_id) REFERENCES divisions (id) ON UPDATE CASCADE
);

# weight in pounds, height in inches
CREATE TABLE IF NOT EXISTS players
(
  id BIGINT(20) UNSIGNED PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  birth_date DATE,
  birth_city VARCHAR(100),
  birth_state VARCHAR(100),
  birth_country VARCHAR(100),
  nationality VARCHAR(100),
  height TINYINT UNSIGNED,
  weight SMALLINT UNSIGNED,
  shoots_catches ENUM('left', 'right'),
  primary_pos ENUM('center', 'right wing', 'left wing', 'defenseman', 'goalie'),
  current_team_id BIGINT(20) UNSIGNED,
  CONSTRAINT players_teams_id_fk FOREIGN KEY (current_team_id) REFERENCES teams (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS seasons
(
  id BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
  start DATE NOT NULL,
  po_start DATE NOT NULL,
  end DATE NOT NULL,
  status ENUM('not_started', 'regular', 'play_off', 'finished') NOT NULL,
  current TINYINT(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS games
(
  id BIGINT(20) UNSIGNED PRIMARY KEY NOT NULL,
  date DATE NOT NULL,
  is_regular TINYINT(1) NOT NULL,
  win_type ENUM('regular', 'overtime', 'shootout') NOT NULL,
  home_team_id BIGINT(20) UNSIGNED NOT NULL,
  away_team_id BIGINT(20) UNSIGNED NOT NULL,
  home_goals TINYINT UNSIGNED NOT NULL,
  home_goals_period1 TINYINT UNSIGNED NOT NULL,
  home_goals_period2 TINYINT UNSIGNED NOT NULL,
  home_goals_period3 TINYINT UNSIGNED NOT NULL,
  home_shots TINYINT UNSIGNED NOT NULL,
  home_pp_goals TINYINT UNSIGNED NOT NULL,
  home_pp_opportunities TINYINT UNSIGNED NOT NULL,
  home_face_off_wins TINYINT UNSIGNED NOT NULL,
  home_blocked TINYINT UNSIGNED NOT NULL,
  home_hits TINYINT UNSIGNED NOT NULL,
  home_penalty_minutes TINYINT UNSIGNED NOT NULL,
  away_goals TINYINT UNSIGNED NOT NULL,
  away_goals_period1 TINYINT UNSIGNED NOT NULL,
  away_goals_period2 TINYINT UNSIGNED NOT NULL,
  away_goals_period3 TINYINT UNSIGNED NOT NULL,
  away_shots TINYINT UNSIGNED NOT NULL,
  away_pp_goals TINYINT UNSIGNED NOT NULL,
  away_pp_opportunities TINYINT UNSIGNED NOT NULL,
  away_face_off_wins TINYINT UNSIGNED NOT NULL,
  away_blocked TINYINT UNSIGNED NOT NULL,
  away_hits TINYINT UNSIGNED NOT NULL,
  away_penalty_minutes TINYINT UNSIGNED NOT NULL,
  face_off_taken TINYINT UNSIGNED NOT NULL,
  CONSTRAINT games_home_team_id_fk FOREIGN KEY (home_team_id) REFERENCES teams (id) ON UPDATE CASCADE,
  CONSTRAINT games_away_team_id_fk FOREIGN KEY (away_team_id) REFERENCES teams (id) ON UPDATE CASCADE
);

# time on ice in seconds
CREATE TABLE IF NOT EXISTS skater_stats
(
  player_id BIGINT(20) UNSIGNED NOT NULL,
  team_id BIGINT(20) UNSIGNED NOT NULL,
  game_id BIGINT(20) UNSIGNED NOT NULL,
  date DATE NOT NULL,
  assists TINYINT UNSIGNED NOT NULL,
  goals TINYINT UNSIGNED NOT NULL,
  shots TINYINT UNSIGNED NOT NULL,
  hits TINYINT UNSIGNED NOT NULL,
  pp_goals TINYINT UNSIGNED NOT NULL,
  pp_assists TINYINT UNSIGNED NOT NULL,
  penalty_minutes TINYINT UNSIGNED NOT NULL,
  face_off_wins TINYINT UNSIGNED NOT NULL,
  face_off_taken TINYINT UNSIGNED NOT NULL,
  takeaways TINYINT UNSIGNED NOT NULL,
  giveaways TINYINT UNSIGNED NOT NULL,
  sh_goals TINYINT UNSIGNED NOT NULL,
  sh_assists TINYINT UNSIGNED NOT NULL,
  blocked TINYINT UNSIGNED NOT NULL,
  plus_minus TINYINT NOT NULL,
  toi SMALLINT UNSIGNED NOT NULL,
  even_toi SMALLINT UNSIGNED NOT NULL,
  pp_toi SMALLINT UNSIGNED NOT NULL,
  sh_toi SMALLINT UNSIGNED NOT NULL,
  CONSTRAINT skater_stats_pk PRIMARY KEY (player_id, game_id),
  CONSTRAINT skater_players_fk FOREIGN KEY (player_id) REFERENCES players (id) ON UPDATE CASCADE,
  CONSTRAINT skater_teams_fk FOREIGN KEY (team_id) REFERENCES teams (id) ON UPDATE CASCADE,
  CONSTRAINT skater_games_fk FOREIGN KEY (game_id) REFERENCES games (id) ON UPDATE CASCADE
);

# time on ice in seconds
CREATE TABLE IF NOT EXISTS goalie_stats
(
  player_id BIGINT(20) UNSIGNED NOT NULL,
  team_id BIGINT(20) UNSIGNED NOT NULL,
  game_id BIGINT(20) UNSIGNED NOT NULL,
  date DATE NOT NULL,
  toi SMALLINT UNSIGNED NOT NULL,
  assists TINYINT UNSIGNED NOT NULL,
  goals TINYINT UNSIGNED NOT NULL,
  penalty_minutes TINYINT UNSIGNED NOT NULL,
  shots TINYINT UNSIGNED NOT NULL,
  saves TINYINT UNSIGNED NOT NULL,
  pp_saves TINYINT UNSIGNED NOT NULL,
  sh_saves TINYINT UNSIGNED NOT NULL,
  even_saves TINYINT UNSIGNED NOT NULL,
  sh_shots_against TINYINT UNSIGNED NOT NULL,
  even_shots_against TINYINT UNSIGNED NOT NULL,
  pp_shots_against TINYINT UNSIGNED NOT NULL,
  decision ENUM('winner', 'loser', 'none') NOT NULL,
  CONSTRAINT goalie_stats_pk PRIMARY KEY (player_id, game_id),
  CONSTRAINT goalie_players_fk FOREIGN KEY (player_id) REFERENCES players (id) ON UPDATE CASCADE,
  CONSTRAINT goalie_teams_fk FOREIGN KEY (team_id) REFERENCES teams (id) ON UPDATE CASCADE,
  CONSTRAINT goalie_games_fk FOREIGN KEY (game_id) REFERENCES games (id) ON UPDATE CASCADE
);

# period time in seconds
CREATE TABLE IF NOT EXISTS goals
(
  id BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
  team_id BIGINT(20) UNSIGNED NOT NULL,
  game_id BIGINT(20) UNSIGNED NOT NULL,
  date DATE NOT NULL,
  scorer_id BIGINT(20) UNSIGNED NOT NULL,
  assist1_id BIGINT(20) UNSIGNED,
  assist2_id BIGINT(20) UNSIGNED,
  secondary_type VARCHAR(50),
  empty_net TINYINT(1) NOT NULL,
  strength ENUM('even', 'ppg', 'shg') NOT NULL,
  period_num TINYINT UNSIGNED NOT NULL,
  period_time SMALLINT UNSIGNED NOT NULL,
  coord_x TINYINT,
  coord_y TINYINT,
  CONSTRAINT goals_scorer_fk FOREIGN KEY (scorer_id) REFERENCES players (id) ON UPDATE CASCADE,
  CONSTRAINT goals_assist1_fk FOREIGN KEY (assist1_id) REFERENCES players (id) ON UPDATE CASCADE,
  CONSTRAINT goals_assist2_fk FOREIGN KEY (assist2_id) REFERENCES players (id) ON UPDATE CASCADE,
  CONSTRAINT goals_teams_fk FOREIGN KEY (team_id) REFERENCES teams (id) ON UPDATE CASCADE,
  CONSTRAINT goals_games_fk FOREIGN KEY (game_id) REFERENCES games (id) ON UPDATE CASCADE
);

# period time in seconds
CREATE TABLE IF NOT EXISTS penalty
(
  id BIGINT(20) UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
  team_id BIGINT(20) UNSIGNED NOT NULL,
  game_id BIGINT(20) UNSIGNED NOT NULL,
  date DATE NOT NULL,
  penalty_on_id BIGINT(20) UNSIGNED NOT NULL,
  drew_by_id BIGINT(20) UNSIGNED,
  penalty_minutes TINYINT UNSIGNED NOT NULL,
  secondary_type VARCHAR(100),
  period_num TINYINT UNSIGNED NOT NULL,
  period_time SMALLINT UNSIGNED NOT NULL,
  coord_x TINYINT,
  coord_y TINYINT,
  CONSTRAINT penalty_penalty_on_fk FOREIGN KEY (penalty_on_id) REFERENCES players (id) ON UPDATE CASCADE,
  CONSTRAINT penalty_drew_by_fk FOREIGN KEY (drew_by_id) REFERENCES players (id) ON UPDATE CASCADE,
  CONSTRAINT penalty_teams_fk FOREIGN KEY (team_id) REFERENCES teams (id) ON UPDATE CASCADE,
  CONSTRAINT penalty_games_fk FOREIGN KEY (game_id) REFERENCES games (id) ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS team_sum_stats
(
  team_id BIGINT(20) UNSIGNED NOT NULL,
  season_id BIGINT(20) UNSIGNED NOT NULL,
  is_regular TINYINT(1) NOT NULL,
  goals_for SMALLINT UNSIGNED NOT NULL,
  goals_against SMALLINT UNSIGNED NOT NULL,
  shots SMALLINT UNSIGNED NOT NULL,
  pp_goals SMALLINT UNSIGNED NOT NULL,
  pp_opportunities SMALLINT UNSIGNED NOT NULL,
  sh_goals_against SMALLINT UNSIGNED NOT NULL,
  sh_opportunities SMALLINT UNSIGNED NOT NULL,
  face_off_wins SMALLINT UNSIGNED NOT NULL,
  face_off_taken SMALLINT UNSIGNED NOT NULL,
  blocked SMALLINT UNSIGNED NOT NULL,
  hits SMALLINT UNSIGNED NOT NULL,
  penalty_minutes SMALLINT UNSIGNED NOT NULL,
  games TINYINT UNSIGNED NOT NULL,
  win_regular TINYINT UNSIGNED NOT NULL,
  win_overtime TINYINT UNSIGNED NOT NULL,
  win_shootout TINYINT UNSIGNED NOT NULL,
  lose_regular TINYINT UNSIGNED NOT NULL,
  lose_overtime TINYINT UNSIGNED NOT NULL,
  lose_shootout TINYINT UNSIGNED NOT NULL,
  CONSTRAINT team_sum_stats_pk PRIMARY KEY (team_id, season_id, is_regular),
  CONSTRAINT team_sum_players_fk FOREIGN KEY (team_id) REFERENCES teams (id) ON UPDATE CASCADE,
  CONSTRAINT team_sum_seasons_fk FOREIGN KEY (season_id) REFERENCES seasons (id) ON UPDATE CASCADE
);

# time on ice in seconds
CREATE TABLE IF NOT EXISTS skater_sum_stats
(
  player_id BIGINT(20) UNSIGNED NOT NULL,
  season_id BIGINT(20) UNSIGNED NOT NULL,
  is_regular TINYINT(1) NOT NULL,
  assists SMALLINT UNSIGNED NOT NULL,
  goals SMALLINT UNSIGNED NOT NULL,
  shots SMALLINT UNSIGNED NOT NULL,
  hits SMALLINT UNSIGNED NOT NULL,
  pp_goals SMALLINT UNSIGNED NOT NULL,
  pp_assists SMALLINT UNSIGNED NOT NULL,
  penalty_minutes SMALLINT UNSIGNED NOT NULL,
  face_off_wins SMALLINT UNSIGNED NOT NULL,
  face_off_taken SMALLINT UNSIGNED NOT NULL,
  takeaways SMALLINT UNSIGNED NOT NULL,
  giveaways SMALLINT UNSIGNED NOT NULL,
  sh_goals SMALLINT UNSIGNED NOT NULL,
  sh_assists SMALLINT UNSIGNED NOT NULL,
  blocked SMALLINT UNSIGNED NOT NULL,
  plus_minus SMALLINT NOT NULL,
  toi MEDIUMINT UNSIGNED NOT NULL,
  even_toi MEDIUMINT UNSIGNED NOT NULL,
  pp_toi MEDIUMINT UNSIGNED NOT NULL,
  sh_toi MEDIUMINT UNSIGNED NOT NULL,
  games TINYINT UNSIGNED NOT NULL,
  CONSTRAINT skater_sum_stats_pk PRIMARY KEY (player_id, season_id, is_regular),
  CONSTRAINT skater_sum_players_fk FOREIGN KEY (player_id) REFERENCES players (id) ON UPDATE CASCADE,
  CONSTRAINT skater_sum_seasons_fk FOREIGN KEY (season_id) REFERENCES seasons (id) ON UPDATE CASCADE
);

# time on ice in seconds
CREATE TABLE IF NOT EXISTS goalie_sum_stats
(
  player_id BIGINT(20) UNSIGNED NOT NULL,
  season_id BIGINT(20) UNSIGNED NOT NULL,
  is_regular TINYINT(1) NOT NULL,
  toi MEDIUMINT UNSIGNED NOT NULL,
  assists SMALLINT UNSIGNED NOT NULL,
  goals SMALLINT UNSIGNED NOT NULL,
  penalty_minutes SMALLINT UNSIGNED NOT NULL,
  shots SMALLINT UNSIGNED NOT NULL,
  saves SMALLINT UNSIGNED NOT NULL,
  pp_saves SMALLINT UNSIGNED NOT NULL,
  sh_saves SMALLINT UNSIGNED NOT NULL,
  even_saves SMALLINT UNSIGNED NOT NULL,
  sh_shots_against SMALLINT UNSIGNED NOT NULL,
  even_shots_against SMALLINT UNSIGNED NOT NULL,
  pp_shots_against SMALLINT UNSIGNED NOT NULL,
  games TINYINT UNSIGNED NOT NULL,
  wins TINYINT UNSIGNED NOT NULL,
  shutout TINYINT UNSIGNED NOT NULL,
  CONSTRAINT goalie_sum_stats_pk PRIMARY KEY (player_id, season_id, is_regular),
  CONSTRAINT goalie_sum_players_fk FOREIGN KEY (player_id) REFERENCES players (id) ON UPDATE CASCADE,
  CONSTRAINT goalie_sum_seasons_fk FOREIGN KEY (season_id) REFERENCES seasons (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS player_trades
(
  player_id BIGINT(20) UNSIGNED NOT NULL,
  date DATE NOT NULL,
  from_team_id BIGINT(20) UNSIGNED NOT NULL,
  to_team_id BIGINT(20) UNSIGNED NOT NULL,
  CONSTRAINT player_trades_pk PRIMARY KEY (player_id, date),
  CONSTRAINT player_trades_from_team_id_fk FOREIGN KEY (from_team_id) REFERENCES teams (id) ON UPDATE CASCADE,
  CONSTRAINT player_trades_to_team_id_fk FOREIGN KEY (to_team_id) REFERENCES teams (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS player_team_season
(
  player_id BIGINT(20) UNSIGNED NOT NULL,
  season_id BIGINT(20) UNSIGNED NOT NULL,
  team_id BIGINT(20) UNSIGNED NOT NULL,
  CONSTRAINT player_team_season_pk PRIMARY KEY (player_id, season_id, team_id),
  CONSTRAINT player_team_season_pid_fk FOREIGN KEY (player_id) REFERENCES players (id) ON UPDATE CASCADE,
  CONSTRAINT player_team_season_sid_fk FOREIGN KEY (season_id) REFERENCES seasons (id) ON UPDATE CASCADE,
  CONSTRAINT player_team_season_tid_fk FOREIGN KEY (team_id) REFERENCES teams (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS translations
(
  resource_type ENUM('conf_name', 'div_name', 'team_name', 'team_abbr', 'team_venue_name', 'player_name') NOT NULL,
  resource_id BIGINT(20) UNSIGNED NOT NULL,
  ru VARCHAR(255),
  CONSTRAINT translations_pk PRIMARY KEY (resource_type, resource_id)
);
