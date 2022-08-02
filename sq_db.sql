CREATE TABLE IF NOT EXISTS mainmenu(
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);
CREATE TABLE IF NOT EXISTS posts(
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
prise text NOT NULL,
description text NOT NULL
);
CREATE TABLE IF NOT EXISTS users(
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
password text NOT NULL,
email email NOT NULL,
avatar BLOB DEFAULT NULL
);