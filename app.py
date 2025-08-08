import sqlite3
from datetime import date, timedelta

DB_PATH = "library.db"

def connect_to_database():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection

def show_books():
    with connect_to_database() as db:
        books = db.execute("""
            SELECT book_id, title, author,
            genre, ISBN, copies_available,
            copies_total
            FROM Book
            ORDER BY title
        """)
        books = list(books)  

    print("Books:")
    if not books:
        print("No books found.")
    else:
        for book in books:
            print(f"[{book[0]}] {book[1]} by {book[2]} "
                  f"(Genre: {book[3] or 'No genre'}, ISBN: {book[4]}, "
                  f"{book[5]}/{book[6]} available)")

def add_book():
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    genre = input("Genre (optional): ").strip() or None
    copies = int(input("Number of copies (default 1): ") or "1")

    with connect_to_database() as db:
        db.execute("""
            INSERT INTO Book (title, author,
            genre, copies_total, copies_available)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, genre, copies, copies))

    print("Book's been added!")

def add_member():
    name = input("Member name: ").strip()
    email = input("Email (optional): ").strip() or None

    with connect_to_database() as db:
        res = db.execute("INSERT INTO Member (full_name, email) VALUES (?, ?)", (name, email))
        member_id = res.lastrowid  
    print(f"Member added with ID {member_id}")

def borrow_book():
    with connect_to_database() as db:
        members = list(db.execute("SELECT member_id, full_name FROM Member"))
        books   = list(db.execute("SELECT book_id, title FROM Book"))

    print("Members:")
    for m in members:
        print(f"{m[0]} - {m[1]}")
    print("Books:")
    for b in books:
        print(f"{b[0]} - {b[1]}")

    try:
        member_id = int(input("Enter Member ID: "))
        book_id = int(input("Enter Book ID: "))
    except ValueError:
        print("Please enter only number(s)")
        return

    due_date_str = str(date.today() + timedelta(days=21))  

    with connect_to_database() as db:
        copies_available = None
        for row in db.execute("SELECT copies_available FROM Book WHERE book_id=?", (book_id,)):
            copies_available = row[0]
            break

        if copies_available is None:
            print("Book not found.")
            return
        if copies_available < 1:
            print("No copies available.")
            return

        res = db.execute("""
            INSERT INTO Loan (book_id, member_id, due_date)
            VALUES (?, ?, ?)
        """, (book_id, member_id, due_date_str))
        loan_id = res.lastrowid

        db.execute("""
            UPDATE Book
            SET copies_available = copies_available - 1
            WHERE book_id=? AND copies_available > 0
        """, (book_id,))

    print(f"Loan created! Loan ID = {loan_id}. Due date: {due_date_str}")

def return_book():
    try:
        loan_id = int(input("Enter Loan ID: "))
    except ValueError:
        print("Please enter a number.")
        return

    with connect_to_database() as db:
        book_id = None
        return_date = None
        for row in db.execute("SELECT book_id, return_date FROM Loan WHERE loan_id=?", (loan_id,)):
            book_id, return_date = row[0], row[1]
            break

        if book_id is None:
            print("Loan not found.")
            return
        if return_date is not None:
            print("Book already returned.")
            return

        db.execute("UPDATE Loan SET return_date = DATE('now') WHERE loan_id=?", (loan_id,))
        db.execute("UPDATE Book SET copies_available = copies_available + 1 WHERE book_id=?", (book_id,))

    print("Book returned.")

def show_loans():
    with connect_to_database() as db:
        loans = list(db.execute("""
            SELECT l.loan_id, m.full_name, b.title,
            l.loan_date, l.due_date, l.return_date
            FROM Loan l
            JOIN Member m ON m.member_id = l.member_id
            JOIN Book   b ON b.book_id   = l.book_id
            ORDER BY CASE WHEN l.return_date IS NOT NULL THEN l.return_date ELSE l.due_date END
        """))  

    print("Loans:")
    if not loans:
        print("No loans found.")
    else:
        for loan in loans:
            status = f"Returned {loan[5]}" if loan[5] else f"Due {loan[4]}"
            print(f"[{loan[0]}] {loan[1]}, {loan[2]} (Loaned {loan[3]}, {status})")

def show_overdue():
    with connect_to_database() as db:
        overdue = list(db.execute("""
            SELECT m.full_name, b.title, l.due_date
            FROM Loan l
            JOIN Member m ON m.member_id = l.member_id
            JOIN Book   b ON b.book_id   = l.book_id
            WHERE l.return_date IS NULL AND l.due_date < DATE('now')
            ORDER BY l.due_date
        """))

    print("Overdue books:")
    if not overdue:
        print("None")
    else:
        for name, title, due in overdue:
            print(f"{name} - {title} (Due {due})")

def menu():
    actions = {
        "1": show_books,
        "2": add_book,
        "3": add_member,
        "4": borrow_book,
        "5": return_book,
        "6": show_loans,
        "7": show_overdue,
    }
    while True:
        print("""
==== Library ====
1) Show all books
2) Add a new book
3) Add a new member
4) Borrow a book
5) Return a book
6) List all loaned out books
7) List overdue books
0) Quit
""")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            break
        if choice in actions:
            try:
                actions[choice]()
            except Exception as e:
                print("Error:", e)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    menu()
