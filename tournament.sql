create table player
(
p_id SERIAL,
name TEXT NOT NULL,
primary key(p_id)
);

create table match
(
match_id SERIAL,
win_id INT NOT NULL,
lost_id INT NOT NULL,
primary key(match_id)
);
