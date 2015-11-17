CREATE TABLE `ship` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `captain_id` TEXT NOT NULL,
    `time_created` DATETIME NOT NULL,
    `departure_time` DATETIME NOT NULL,
    `destination` TEXT
);
