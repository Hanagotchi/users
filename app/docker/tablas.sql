CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    genre VARCHAR(20),
    photo VARCHAR(255)
);

INSERT INTO
    dev.users (name, email)
VALUES ('Agus', 'agus@fi.uba.ar'),
    ('Pach', 'pach@fi.uba.ar'),
    ('Sofi', 'sofi@fi.uba.ar'),
    ('Violeta', 'violeta@fi.uba.ar');