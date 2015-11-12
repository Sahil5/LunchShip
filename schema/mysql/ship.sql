CREATE TABLE `ship` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `captain_id` varchar(128) NOT NULL,
    `time_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `departure_time` timestamp NOT NULL,
    `destination` varchar(64),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
