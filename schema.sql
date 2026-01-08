-- This is the logic used to create your FIFA database
CREATE TABLE IF NOT EXISTS player (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    team TEXT NOT NULL,
    played INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0,
    goals_for INTEGER DEFAULT 0,
    goals_against INTEGER DEFAULT 0,
    goal_diff INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS match (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    home_player_id INTEGER,
    away_player_id INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    is_played BOOLEAN DEFAULT 0,
    FOREIGN KEY(home_player_id) REFERENCES player(id),
    FOREIGN KEY(away_player_id) REFERENCES player(id)
);