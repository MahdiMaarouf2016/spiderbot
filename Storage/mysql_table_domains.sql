

CREATE TABLE feedspider.domains ( `url` VARCHAR(100) NOT NULL , `name` VARCHAR(100) NOT NULL , `description` TEXT NOT
NULL, `roletype` VARCHAR(30)NOT NULL, `title` VARCHAR(100)NOT NULL, `image` VARCHAR(200)NOT NULL, `keywords` TEXT NOT
NULL, `icon` VARCHAR(200)NOT NULL, `language` VARCHAR(15)NOT NULL, `robots` TEXT NOT NULL, `starturl` VARCHAR(200)
NOT NULL, PRIMARY KEY(`url`))ENGINE = MyISAM;