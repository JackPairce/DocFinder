-- Books table
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    issued DATE,
    title TEXT NOT NULL,
    language TEXT,
    authors TEXT[],
    subjects TEXT[],
    bookshelve TEXT[]
);

-- Categories table
CREATE TABLE bookshelves (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Vectors table
CREATE TABLE books_vectors (
    id INT PRIMARY KEY REFERENCES books(id),
    subject_vector FLOAT8[],
    content_vector FLOAT8[]
);
