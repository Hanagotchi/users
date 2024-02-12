CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.users (
    id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL
);

INSERT INTO
    dev.users (name)
VALUES ('Agus'),
    ('Pach'),
    ('Sofi'),
    ('Violeta');