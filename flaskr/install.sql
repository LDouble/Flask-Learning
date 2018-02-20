DROP  TABLE  IF EXISTS entries;
CREATE  TABLE entries(
id INTEGER PRIMARY KEY  autoincrement,
title text not NULL,
content text not NULL
)