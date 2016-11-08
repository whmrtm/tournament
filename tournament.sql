drop database if exists tournament
create database tournament
\c tournament

create table player
(
p_id SERIAL,
name TEXT NOT NULL,
primary key(p_id)
);

create table match
(
match_id SERIAL,
win_id INT NOT NULL references player(p_id),
lost_id INT NOT NULL references player(p_id),
primary key(match_id)
);


