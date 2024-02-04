CREATE DATABASE users;
USE users;


CREATE TABLE users_data (
    user_id  varchar(50)  NOT NULL ,
    user_name VARCHAR(50),
    email varchar(150),
  locale VARCHAR(50),
  city  varchar(50),
  company varchar(50),
  isKnown boolean default false,
  PRIMARY KEY (user_id)

);


INSERT INTO users_data
  (user_id, user_name, email, locale,city,company)
VALUES
  ('1', 'Johnny','johhnydeep23@gmail.com','ro','Iasi','Profi'),
  ('2', 'Johnny2','johhnydeep234@gmail.com','bg','Iasi','Lidl');

CREATE TABLE skills (
    id integer  NOT NULL,
    name VARCHAR(50),
  PRIMARY KEY (id)
);
INSERT INTO skills
  (id,name)
VALUES
  (123455,'Java'),
 (123444,'Photoshop'),
  (123456,'Web');

CREATE TABLE cities (
    id integer  NOT NULL,
    name VARCHAR(50),
  PRIMARY KEY (id)
);
INSERT INTO cities
  (id,name)
VALUES
  (12345,'Westeros'),
    (12344,'Valyria'),
  (75676,'Winterfell');
CREATE TABLE companies(
    id integer  NOT NULL,
    name VARCHAR(50),
  PRIMARY KEY (id)
);
INSERT INTO companies
  (id,name)
VALUES
  (12345,'Apple'),
    (12344,'Microsoft'),
  (56756,'Profi');

create table books(
book_id integer not null,
title varchar(500),
average_rating float,
image_url varchar(350),
primary key(book_id)

);

create table authors(
author_id integer not null,
name varchar(150),
primary key(author_id)
);

create table user_book_interaction(
id BIGINT not null AUTO_INCREMENT,
user_id varchar(50) ,
book_id integer,
rating double,
primary key(id),
FOREIGN KEY (user_id) REFERENCES users_data(user_id),
FOREIGN KEY (book_id) REFERENCES books(book_id)
);


create table similar_books(
id BIGINT not null AUTO_INCREMENT,
book_id integer,
similar_book_id integer,
primary key(id),
FOREIGN KEY (book_id) REFERENCES books(book_id),
FOREIGN KEY (similar_book_id) REFERENCES books(book_id)
);

create table book_author(
id BIGINT not null AUTO_INCREMENT,
book_id integer,
author_id integer,
primary key(id),
FOREIGN KEY (book_id) REFERENCES books(book_id),
FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

create table google_books(
user_id  varchar(50) not null,
data longtext,
primary key(user_id),
FOREIGN KEY (user_id) REFERENCES users_data(user_id)
);

create table spotify(
user_id varchar(50) not null,
data longtext,
primary key(user_id),
FOREIGN KEY (user_id) REFERENCES users_data(user_id)
);

create table users_mapping_ids(
id BIGINT not null AUTO_INCREMENT,
user_id  varchar(50),
user_id_long BIGINT,
primary key(id),
FOREIGN KEY (user_id) REFERENCES users_data(user_id)
);