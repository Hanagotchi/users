CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.users (
    id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, mail VARCHAR(255) NOT NULL
);

INSERT INTO
    dev.users (name, mail)
VALUES ('Agus', 'agus@fi.uba.ar'),
    ('Pach', 'pach@fi.uba.ar'),
    ('Sofi', 'sofi@fi.uba.ar'),
    ('Violeta', 'violeta@fi.uba.ar');