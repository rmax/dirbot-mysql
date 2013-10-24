DROP TABLE IF EXISTS website;
CREATE TABLE website (
  guid CHAR(32) PRIMARY KEY,
  name TEXT,
  description TEXT,
  url TEXT,
  updated DATETIME
) DEFAULT CHARSET=utf8;

