DROP TABLE IF EXISTS tour;

CREATE TABLE tour(id SERIAL PRIMARY KEY, name TEXT NOT NULL,price INT,filename TEXT);

INSERT INTO tour(name, price) VALUES
    ('Sydeny & Surrounding', 39),
    ('Melbourne & Surrounding', 45);