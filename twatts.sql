CREATE TABLE twatts (
  id SERIAL PRIMARY KEY,
  username_id INTEGER REFERENCES userInfo,
  twatt VARCHAR NOT NULL
);

SELECT username, password FROM userInfo JOIN twatts ON twatts.username_id = userInfo.id;
