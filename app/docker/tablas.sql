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
    biography VARCHAR(255),
    device_token VARCHAR(255)
);

INSERT INTO
    users_service.users (name, email, birthdate, location)
VALUES ('Agus', 'agus@fi.uba.ar', TO_DATE('1999-01-29', 'YYYY-MM-DD'), '{"lat": 20, "long": 100}'),
    ('Pach', 'pach@fi.uba.ar', TO_DATE('1999-08-06', 'YYYY-MM-DD'), '{"lat": 10, "long": 200}'),
    ('Sofi', 'sofi@fi.uba.ar', TO_DATE('1998-04-26', 'YYYY-MM-DD'), '{"lat": 1190, "long": 500}'),
    ('Violeta', 'violeta@fi.uba.ar', TO_DATE('1998-05-12', 'YYYY-MM-DD'), '{"lat": 330, "long": 2333}');


-- Para users con device_token
-- INSERT INTO
--     users_service.users (name, email, birthdate, location, device_token)
-- VALUES ('Agus', 'agus@fi.uba.ar', TO_DATE('1999-01-29', 'YYYY-MM-DD'), '{"lat": 20, "long": 100}', 'FEFEF'),
--     ('Pach', 'pach@fi.uba.ar', TO_DATE('1999-08-06', 'YYYY-MM-DD'), '{"lat": 10, "long": 200}', 'ASDASD'),
--     ('Sofi', 'sofi@fi.uba.ar', TO_DATE('1998-04-26', 'YYYY-MM-DD'), '{"lat": 1190, "long": 500}', 'QWEQWE'),
--     ('Violeta', 'violeta@fi.uba.ar', TO_DATE('1998-05-12', 'YYYY-MM-DD'), '{"lat": 330, "long": 2333}', 'ZXZXZX');

DROP TABLE IF EXISTS users_service.alarms CASCADE;

CREATE TABLE IF NOT EXISTS users_service.alarms (
    id SERIAL PRIMARY KEY,
    id_user INT NOT NULL REFERENCES users_service.users(id) ON DELETE CASCADE,
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    content VARCHAR(128) NOT NULL
);
CREATE INDEX idx_alarms_date_time ON users_service.alarms(date_time);

INSERT INTO
    users_service.alarms (id_user, date_time, content)
VALUES (1, '2024-04-30 00:50:00-03', 'Wake up 1!'),
    (1, '2024-04-30 00:50:00-03', 'Wake up 2!'),
    (1, '2024-04-30 00:50:00-03', 'Wake up 3!'),
    (1, '2024-04-30 00:50:00-03', 'Wake up 4!');

-- SELECT users_service.alarms.id, users_service.alarms.content, users_service.users.device_token
-- FROM users_service.alarms 
-- INNER JOIN users_service.users ON users_service.alarms.id_user = users_service.users.id 
-- WHERE users_service.alarms.datetime = '2024-04-29 02:15:00-03';