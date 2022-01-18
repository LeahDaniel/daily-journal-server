CREATE TABLE `Tag` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`subject` TEXT NOT NULL
);

CREATE TABLE `Mood` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label` TEXT NOT NULL
);

CREATE TABLE `Entry` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`mood_id`  INTEGER NOT NULL,
	`date` TEXT NOT NULL,
	`concept` TEXT NOT NULL,
	`entry` TEXT NOT NULL,
	FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `EntryTag` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`entry_id`  INTEGER NOT NULL,
	`tag_id`  INTEGER NOT NULL,
	FOREIGN KEY(`entry_id`) REFERENCES `Entry`(`id`),
	FOREIGN KEY(`tag_id`) REFERENCES `Tag`(`id`)
);

INSERT INTO Tag VALUES (null, "Python");
INSERT INTO Tag VALUES (null, "Django");
INSERT INTO Tag VALUES (null, "SQL");
INSERT INTO Tag VALUES (null, "React");

INSERT INTO Mood VALUES (null, "Frustrated");
INSERT INTO Mood VALUES (null, "Exhausted");
INSERT INTO Mood VALUES (null, "Proud");
INSERT INTO Mood VALUES (null, "Excited");

INSERT INTO Entry VALUES (null, 4, "01/04/2022", "Python basics", "akjdhfajksdhfkjbdasjkf");
INSERT INTO Entry VALUES (null, 1, "01/13/2022", "SQL database setup", "adfgadfhadfhsgbargeadv");

INSERT INTO EntryTag VALUES (null, 1, 1);
INSERT INTO EntryTag VALUES (null, 2, 1);
INSERT INTO EntryTag VALUES (null, 2, 3);