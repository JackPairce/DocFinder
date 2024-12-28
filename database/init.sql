-- Books table
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    issued DATE,
    title TEXT NOT NULL,
    language TEXT,
    authors TEXT[],
    subjects TEXT[],
    cover_url TEXT,
);

-- Vectors table
CREATE TABLE books_vectors (
    id INT PRIMARY KEY REFERENCES books(id),
    subject_vector FLOAT8[],
    content_vector FLOAT8[]
);
