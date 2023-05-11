DROP TABLE IF EXISTS requires;

CREATE TABLE requires(id SERIAL PRIMARY KEY, email TEXT NOT NULL, name TEXT NOT NULL,phone_number TEXT NOT NULL,direction TEXT,days INT);