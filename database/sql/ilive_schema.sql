-- FileName:   ilive.sql
-- Author:     Chen Yanfei
-- @contact:   fasionchan@gmail.com
-- @version:   $Id$
--
-- Description:
--
-- Changelog:
--
--


CREATE TABLE `user` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL,
    `realname` VARCHAR(255) DEFAULT NULL,
    `nickname` VARCHAR(255) DEFAULT NULL,
    `email` VARCHAR(255) DEFAULT NULL,
    `telephone` VARCHAR(255) DEFAULT NULL,
    `birthday` DATE DEFAULT NULL,
    `sex` ENUM("男", "女") DEFAULT NULL,
    `tags` VARCHAR(255) DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    UNIQUE KEY (`username`),
    UNIQUE KEY (`email`),
    UNIQUE KEY (`telephone`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `nutrient` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `food_material` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `hash` CHAR(32) NOT NULL,
    `category` VARCHAR(255) NOT NULL,
    `alias` VARCHAR(255) DEFAULT NULL,
    `tags` VARCHAR(255) DEFAULT NULL,
    `image_hash` CHAR(32) DEFAULT NULL,
    `amount_rec` VARCHAR(255) DEFAULT NULL,
    `suit_crowds` VARCHAR(255) DEFAULT NULL,
    `avoid_crowds` VARCHAR(255) DEFAULT NULL,
    `suit_ctcms` VARCHAR(255) DEFAULT NULL,
    `avoid_ctcms` VARCHAR(255) DEFAULT NULL,
    `brief` TEXT DEFAULT NULL,
    `nutrient` TEXT DEFAULT NULL,
    `efficacy` TEXT DEFAULT NULL,
    `taboos` TEXT DEFAULT NULL,
    `suit_mix` TEXT DEFAULT NULL,
    `avoid_mix` TEXT DEFAULT NULL,
    `choose` TEXT DEFAULT NULL,
    `store` TEXT DEFAULT NULL,
    `tips` TEXT DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    UNIQUE KEY (`name`),
    UNIQUE KEY (`hash`),
    KEY (`category`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `food_recipe` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `hash` CHAR(32) NOT NULL,
    `area` VARCHAR(255) DEFAULT NULL,
    `tags` VARCHAR(255) DEFAULT NULL,
    `method` VARCHAR(255) NOT NULL,
    `difficulty` VARCHAR(255) NOT NULL,
    `amount` INTEGER NOT NULL,
    `taste` VARCHAR(255) NOT NULL,
    `setup_time` VARCHAR(255) DEFAULT NULL,
    `cook_time` VARCHAR(255) DEFAULT NULL,
    `sharer` VARCHAR(255) DEFAULT NULL,
    `primaries` TEXT NOT NULL,
    `accessories` TEXT NOT NULL,
    `procedure` TEXT NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    KEY (`name`),
    KEY (`hash`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `food_recipe_material` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `recipe_id` INTEGER NOT NULL,
    `material_id` INTEGER NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    KEY `recipe_id` (`recipe_id`),
    KEY `material_id` (`material_id`),
    CONSTRAINT `recipe_id_fk` FOREIGN KEY (`recipe_id`) REFERENCES `food_recipe` (`id`),
    CONSTRAINT `material_id_fk` FOREIGN KEY (`material_id`) REFERENCES `food_material` (`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 中医体质
CREATE TABLE `tcm_consitution` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `tcm_material` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `tcm_symptom` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `tcm_effect` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
