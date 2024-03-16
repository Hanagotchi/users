CREATE SCHEMA IF NOT EXISTS users_service;

CREATE TABLE IF NOT EXISTS users_service.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    gender VARCHAR(20),
    photo VARCHAR(255)
);

INSERT INTO
    users_service.users (name, email)
VALUES ('Agus', 'agus@fi.uba.ar'),
    ('Pach', 'pach@fi.uba.ar'),
    ('Sofi', 'sofi@fi.uba.ar'),
    ('Violeta', 'violeta@fi.uba.ar');