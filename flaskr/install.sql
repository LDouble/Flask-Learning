DROP  TABLE  IF EXISTS entries;
CREATE  TABLE entries(
id INTEGER PRIMARY KEY  autoincrement,
title text not NULL,
content text not NULL
);
CREATE  TABLE cet(
id INTEGER PRIMARY KEY  autoincrement,
xq text not NULL,
js text not NULL,
lx text not NULL,
kch text NOT  NULL
)