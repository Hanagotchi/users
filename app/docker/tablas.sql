CREATE SCHEMA IF NOT EXISTS users_service;

CREATE TABLE IF NOT EXISTS users_service.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    gender VARCHAR(20),
    photo VARCHAR(255),
    location JSONB
);

INSERT INTO
    users_service.users (name, email, location)
VALUES ('Agus', 'agus@fi.uba.ar', '{"lat": 20, "long": 100}'),
    ('Pach', 'pach@fi.uba.ar','{"lat": 10, "long": 200}'),
    ('Sofi', 'sofi@fi.uba.ar', '{"lat": 1190, "long": 500}'),
    ('Violeta', 'violeta@fi.uba.ar', '{"lat": 330, "long": 2333}');