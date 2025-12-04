import json
import logging
from pathlib import Path

# ---------------- Logging Setup ----------------
logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- Book Class ----------------
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"


# ---------------- Inventory Manager ----------------
class LibraryInventory:
    def __init__(self, filename="books.json"):
        self.filename = Path(filename)
        self.books = []
        self.load_data()

    def load_data(self):
        try:
            if self.filename.exists():
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    for b in data:
                        self.books.append(Book(**b))
            logging.info("Book data loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading file: {e}")
            self.books = []

    def save_data(self):
        try:
            with open(self.filename, "w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
            logging.info("Book data saved successfully.")
        except Exception as e:
            logging.error(f"Error saving file: {e}")

    def add_book(self, book):
        self.books.append(book)
        self.save_data()

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return self.books


# ---------------- CLI ----------------
def menu():
    print("\n======= Library Inventory Manager =======")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")
    return input("Enter choice: ")


def main():
    inventory = LibraryInventory()

    while True:
        choice = menu()

        try:
            if choice == "1":
                title = input("Enter title: ")
                author = input("Enter author: ")
                isbn = input("Enter ISBN: ")

                book = Book(title, author, isbn)
                inventory.add_book(book)
                print("Book added successfully.")

            elif choice == "2":
                isbn = input("Enter ISBN to issue: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.issue():
                    inventory.save_data()
                    print("Book issued.")
                else:
                    print("Book not found or already issued.")

            elif choice == "3":
                isbn = input("Enter ISBN to return: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.return_book():
                    inventory.save_data()
                    print("Book returned.")
                else:
                    print("Book not found or already available.")

            elif choice == "4":
                print("\n--- All Books ---")
                for b in inventory.display_all():
                    print(b)

            elif choice == "5":
                title = input("Enter title to search: ")
                results = inventory.search_by_title(title)
                if results:
                    print("\n--- Search Results ---")
                    for b in results:
                        print(b)
                else:
                    print("No books found.")

            elif choice == "6":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            print("Error:", e)
            logging.error(f"Runtime error: {e}")


if __name__ == "__main__":
    main()