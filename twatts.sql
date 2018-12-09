CREATE TABLE twatts (
  id SERIAL PRIMARY KEY,
  username_id INTEGER REFERENCES userInfo(id),
  twatt VARCHAR NOT NULL
);

SELECT username, twatt FROM userInfo JOIN twatts ON twatts.username_id = userInfo.id;

INSERT INTO twatts (username_id, twatt) VALUES (1, 'hello world');

INSERT INTO twatts (username_id, twatt) VALUES (2, 'hello dude');
