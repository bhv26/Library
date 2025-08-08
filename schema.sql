
CREATE TABLE Member (
  member_id   INTEGER PRIMARY KEY,
  full_name   TEXT,
  email       TEXT,
  join_date   DATE DEFAULT CURRENT_DATE
);

CREATE TABLE Staff (
  staff_id    INTEGER PRIMARY KEY,
  full_name   TEXT,
  role        TEXT,
  hire_date   DATE DEFAULT CURRENT_DATE
);

CREATE TABLE Book (
  book_id     INTEGER PRIMARY KEY,
  title       TEXT,
  author      TEXT,
  isbn        TEXT,
  genre       TEXT,
  copies_total  INTEGER DEFAULT 1,
  copies_available INTEGER DEFAULT 1
);

CREATE TABLE Loan (
  loan_id     INTEGER PRIMARY KEY,
  book_id     INTEGER,
  member_id   INTEGER,
  loan_date   DATE DEFAULT CURRENT_DATE,
  due_date    DATE,
  return_date DATE,
  FOREIGN KEY (book_id)  REFERENCES Book(book_id),
  FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

INSERT INTO Member (full_name, email) VALUES
 ('Avni Singh','avni@gmail.com'),
 ('Noah Stryker','noah@gmail.com');

INSERT INTO Staff (full_name, role) VALUES
 ('Brad Pitt','Librarian'),
 ('Chris Rock','Assistant');

INSERT INTO Book (title, author, ISBN, genre, copies_total, copies_available) VALUES
 ('Percy Jackson and the Olympians: The Lightning Thief','Rick Riordan','0120000156','Fantasy/Adventure',4,4),
 ('To All the Boys I''ve Loved Before','Jenny Han','1534427031
','Romance/YA',3,3),
 ('Harry Potter and the Sorcerer''s Stone','J.K. Rowling','1338878921','Fantasy Fiction',5,5);


