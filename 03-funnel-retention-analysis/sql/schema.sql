-- SQLite schema. Import data/users.csv into users and data/events.csv into events.
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  user_id TEXT PRIMARY KEY,
  first_seen_date TEXT NOT NULL,
  signup_date TEXT,
  signup_week TEXT,
  device TEXT NOT NULL,
  region TEXT NOT NULL,
  acquisition_channel TEXT NOT NULL
);
CREATE TABLE events (
  event_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  event_name TEXT NOT NULL,
  event_ts TEXT NOT NULL,
  week_since_signup INTEGER,
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);
CREATE INDEX idx_events_name_user ON events(event_name, user_id);
CREATE INDEX idx_events_user_ts ON events(user_id, event_ts);
CREATE INDEX idx_users_segments ON users(device, region, signup_week);
