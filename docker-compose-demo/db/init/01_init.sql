CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INT NOT NULL,
    date_of_birth DATE NOT NULL
);

INSERT INTO users (first_name, last_name, age, date_of_birth) VALUES
('Marko', 'Marković', 28, '1996-03-12'),
('Jelena', 'Petrović', 34, '1990-08-25'),
('Nikola', 'Jovanović', 22, '2002-01-05');
