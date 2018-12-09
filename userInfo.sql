CREATE TABLE userInfo (
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL,
  email VARCHAR UNIQUE,
  username VARCHAR UNIQUE,
  password VARCHAR NOT NULL,
  bio VARCHAR DEFAULT '',
  followers INTEGER DEFAULT 0,
  following INTEGER DEFAULT 0,
  noTwatt INTEGER DEFAULT 0
);

INSERT INTO userInfo (username, password) VALUES ('michelle', 'haha');
INSERT INTO userInfo (username, password) VALUES ('mitchell', 'hehe');

ALTER TABLE userInfo ADD noTwatts INTEGER DEFAULT 0;
ALTER TABLE userInfo ADD email

DELETE FROM userInfo;
ALTER SEQUENCE userInfo_id_seq RESTART WITH 1;
-- to reset the id back to 1

