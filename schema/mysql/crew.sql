CREATE TABLE `crew` (
    `ship_id` int(11) NOT NULL,
    `sailor_id` varchar(128) NOT NULL,
    PRIMARY KEY (`ship_id`, `sailor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
