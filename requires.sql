DROP TABLE IF EXISTS requires;

CREATE TABLE requires(id SERIAL PRIMARY KEY, email TEXT NOT NULL, name TEXT NOT NULL,phone_number TEXT NOT NULL,startlocation TEXT,endlocation TEXT,partysize INT,budget INT,days INT,today TEXT);
