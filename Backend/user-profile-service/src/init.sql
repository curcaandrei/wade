CREATE DATABASE users;
USE users;


CREATE TABLE users_data (
    user_id  varchar(30)  NOT NULL ,
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
    id integer  NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
  PRIMARY KEY (id)
);
INSERT INTO skills
  (name)
VALUES
  ('Java'),
    ('Photoshop'),
  ('Web');

CREATE TABLE cities (
    id integer  NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
  PRIMARY KEY (id)
);
INSERT INTO cities
  (name)
VALUES
  ('Iasi'),
    ('Bucharest'),
  ('Cluj');
CREATE TABLE companies(
    id integer  NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
  PRIMARY KEY (id)
);
INSERT INTO companies
  (name)
VALUES
  ('Apple'),
    ('Microsoft'),
  ('Profi');