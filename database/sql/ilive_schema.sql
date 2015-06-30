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

-- 国家
CREATE TABLE `country` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `country` VARCHAR(255) NOT NULL,
    `zh_cn` VARCHAR(255) DEFAULT NULL,
    `zh_hk` VARCHAR(255) DEFAULT NULL,
    `en_us` VARCHAR(255) DEFAULT NULL,
    KEY (`country`),
    KEY (`zh_cn`),
    KEY (`zh_hk`),
    KEY (`en_us`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 省份
CREATE TABLE `province` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `province` VARCHAR(255) NOT NULL,
    `govern_no` VARCHAR(255) NOT NULL,
    `zh_cn` VARCHAR(255) DEFAULT NULL,
    `zh_hk` VARCHAR(255) DEFAULT NULL,
    `en_us` VARCHAR(255) DEFAULT NULL,
    `country_id` INTEGER NOT NULL,
    KEY (`province`, `country_id`),
    KEY (`govern_no`, `country_id`),
    KEY (`zh_cn`),
    KEY (`zh_hk`),
    KEY (`en_us`),
    KEY `country_id` (`country_id`),
    CONSTRAINT `prvc_country_id_fk` FOREIGN KEY (`country_id`) REFERENCES `country` (`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 城市
CREATE TABLE `city` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `city` VARCHAR(255) NOT NULL,
    `govern_no` VARCHAR(255) NOT NULL,
    `zh_cn` VARCHAR(255) DEFAULT NULL,
    `zh_hk` VARCHAR(255) DEFAULT NULL,
    `en_us` VARCHAR(255) DEFAULT NULL,
    `province_id` INTEGER NOT NULL,
    KEY (`city`, `province_id`),
    KEY (`govern_no`, `province_id`),
    KEY (`zh_cn`),
    KEY (`zh_hk`),
    KEY (`en_us`),
    KEY `province_id` (`province_id`),
    CONSTRAINT `ct_province_id_fk` FOREIGN KEY (`province_id`) REFERENCES `province` (`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 区
CREATE TABLE `district` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `district` VARCHAR(255) NOT NULL,
    `govern_no` VARCHAR(255) NOT NULL,
    `zh_cn` VARCHAR(255) DEFAULT NULL,
    `zh_hk` VARCHAR(255) DEFAULT NULL,
    `en_us` VARCHAR(255) DEFAULT NULL,
    `city_id` INTEGER NOT NULL,
    KEY (`district`, `city_id`),
    KEY (`govern_no`, `city_id`),
    KEY (`zh_cn`),
    KEY (`zh_hk`),
    KEY (`en_us`),
    KEY `city_id` (`city_id`),
    CONSTRAINT `dst_city_id_fk` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 街道
CREATE TABLE `street` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `street` VARCHAR(255) NOT NULL,
    `govern_no` VARCHAR(255) NOT NULL,
    `zh_cn` VARCHAR(255) DEFAULT NULL,
    `zh_hk` VARCHAR(255) DEFAULT NULL,
    `en_us` VARCHAR(255) DEFAULT NULL,
    `pinyin` VARCHAR(255) DEFAULT NULL,
    `district_id` INTEGER NOT NULL,
    KEY (`street`, `district_id`),
    KEY (`govern_no`, `district_id`),
    KEY (`zh_cn`),
    KEY (`zh_hk`),
    KEY (`en_us`),
    KEY (`pinyin`),
    KEY `district_id` (`district_id`),
    CONSTRAINT `st_district_id_fk` FOREIGN KEY (`district_id`) REFERENCES `district` (`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 用户
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


-- 收货地址
CREATE TABLE `delivery_address` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `user_id` INTEGER NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `telephone` VARCHAR(255) NOT NULL,
    `country` VARCHAR(255) NOT NULL,
    `province` VARCHAR(255) NOT NULL,
    `city` VARCHAR(255) NOT NULL,
    `district` VARCHAR(255) NOT NULL,
    `street` VARCHAR(255) NOT NULL,
    `full_address` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    KEY `user_id` (`user_id`),
    CONSTRAINT `da_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 营养素
CREATE TABLE `nutrient` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 食材
CREATE TABLE `food_material` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `hash` CHAR(32) NOT NULL,
    `classification` VARCHAR(255) DEFAULT NULL,
    `category` VARCHAR(255) DEFAULT NULL,
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


-- 食材营养价值
CREATE TABLE `food_material_nutrient` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `material_id` INTEGER NOT NULL,
    `nutrient_id` INTEGER NOT NULL,
    `content_amount` VARCHAR(255) DEFAULT NULL,
    `content_unit` VARCHAR(255) DEFAULT NULL,
    `content_unit_readable` VARCHAR(255) DEFAULT NULL,
    `content_readable` VARCHAR(255) DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    KEY `material_id` (`material_id`),
    KEY `nutrient_id` (`nutrient_id`),
    CONSTRAINT `fmn_material_id_fk` FOREIGN KEY (`material_id`) REFERENCES `food_material` (`id`),
    CONSTRAINT `fmn_nutrient_id_fk` FOREIGN KEY (`nutrient_id`) REFERENCES `nutrient` (`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 用户喜欢食材
CREATE TABLE `user_like_material` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `user_id` INTEGER NOT NULL,
    `material_id` INTEGER NOT NULL,
    KEY `user_id` (`user_id`),
    KEY `material_id` (`material_id`),
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    CONSTRAINT `ulm_material_id_fk` FOREIGN KEY (`material_id`) REFERENCES `food_material` (`id`),
    CONSTRAINT `ulm_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 用户收藏食材


-- 食谱
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


-- 食谱食材构成
CREATE TABLE `food_recipe_material` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `recipe_id` INTEGER NOT NULL,
    `material_id` INTEGER NOT NULL,
    `dosage_amount` VARCHAR(255) DEFAULT NULL,
    `dosage_unit` VARCHAR(255) DEFAULT NULL,
    `dosage_unit_readable` VARCHAR(255) DEFAULT NULL,
    `dosage_readable` VARCHAR(255) DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    KEY `recipe_id` (`recipe_id`),
    KEY `material_id` (`material_id`),
    CONSTRAINT `frm_recipe_id_fk` FOREIGN KEY (`recipe_id`) REFERENCES `food_recipe` (`id`),
    CONSTRAINT `frm_material_id_fk` FOREIGN KEY (`material_id`) REFERENCES `food_material` (`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 用户喜欢食谱
CREATE TABLE `user_like_recipe` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `user_id` INTEGER NOT NULL,
    `recipe_id` INTEGER NOT NULL,
    KEY `recipe_id` (`recipe_id`),
    KEY `user_id` (`user_id`),
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    CONSTRAINT `ulr_recipe_id_fk` FOREIGN KEY (`recipe_id`) REFERENCES `food_recipe` (`id`),
    CONSTRAINT `ulr_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 用户收藏食谱


-- 中医体质
CREATE TABLE `tcm_consitution` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 中医药材
CREATE TABLE `tcm_material` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `alias` VARCHAR(255) DEFAULT NULL,
    `efficacy` VARCHAR(255) DEFAULT NULL,
    `toxicity` VARCHAR(255) DEFAULT NULL,
    `tropism` VARCHAR(255) DEFAULT NULL,
    `property` VARCHAR(255) DEFAULT NULL,
    `taste` VARCHAR(255) DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 中医症状
CREATE TABLE `tcm_symptom` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 中医功效
CREATE TABLE `tcm_efficacy` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
