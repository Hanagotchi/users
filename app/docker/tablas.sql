CREATE SCHEMA IF NOT EXISTS users_service;

CREATE TABLE IF NOT EXISTS users_service.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    gender VARCHAR(20),
    photo VARCHAR(255),
    birthdate DATE,
    location JSONB,
    nickname VARCHAR(30),
    biography VARCHAR(255)
);

INSERT INTO
    users_service.users (name, email, birthdate, location)
VALUES ('Agus', 'agus@fi.uba.ar', TO_DATE('1999-01-29', 'YYYY-MM-DD'), '{"lat": 20, "long": 100}'),
    ('Pach', 'pach@fi.uba.ar', TO_DATE('1999-08-06', 'YYYY-MM-DD'), '{"lat": 10, "long": 200}'),
    ('Sofi', 'sofi@fi.uba.ar', TO_DATE('1998-04-26', 'YYYY-MM-DD'), '{"lat": 1190, "long": 500}'),
    ('Violeta', 'violeta@fi.uba.ar', TO_DATE('1998-05-12', 'YYYY-MM-DD'), '{"lat": 330, "long": 2333}');