import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import DBFunctions as DatabaseFunctions
from concurrent.futures import ThreadPoolExecutor
import requests


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("media/design.ui", self)
        self.pushButton.clicked.connect(self.generate_books)
        self.fetched_books = []  # store fetched books data

    @staticmethod
    def fetch_book_data(Id):
        # fetch data for a book from an API
        url = "https://books-api7.p.rapidapi.com/books/get/random/"
        headers = {
            "X-RapidAPI-Key": "5337ed38a4mshe1182bf071f2012p1ada89jsnc47b13b0ac26",
            "X-RapidAPI-Host": "books-api7.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print(f"Successfully fetched data for product {Id}")
            data = response.json()
            author_first_name = data.get('author', {}).get('first_name', '')
            author_last_name = data.get('author', {}).get('last_name', '')
            title = data.get('title', '')
            pages = data.get('pages', 0)
            genres = data.get('genres', [])
            return {
                'author_first_name': author_first_name,
                'author_last_name': author_last_name,
                'title': title,
                'pages': pages,
                'genres': genres
            }
        else:
            print(f"Failed to fetch data for product {Id}. Status code: {response.status_code}")
            return None

    def generate_books(self):
        number_of_books = self.number_of_books.value()

        # clear fetched_books list whenever the number of books changes
        if len(self.fetched_books) != number_of_books:
            self.fetched_books.clear()

        if not self.fetched_books:  # fetch books only if not fetched already
            number_of_books = self.number_of_books.value()
            with ThreadPoolExecutor() as thread:
                self.fetched_books = list(thread.map(self.fetch_book_data, range(1, number_of_books + 1)))

        # create SQLite database table
        table_name = 'books_table'
        props_for_table = {
            'first_name': 'TEXT',
            'last_name': 'TEXT',
            'title': 'TEXT',
            'pages_number': 'INTEGER',
            'description': 'TEXT',
            'genres': 'TEXT'
        }
        DatabaseFunctions.create_database_table(table_name, props_for_table)

        output_message = ""
        for data in self.fetched_books:
            if data is not None:
                book_props = (data['author_first_name'],
                              data['author_last_name'],
                              data['title'],
                              data['pages'],
                              "",
                              ', '.join(data['genres']))
                if DatabaseFunctions.check_book_exists(table_name='books_table',
                                                       title=data['title'],
                                                       first_name=data['author_first_name'],
                                                       last_name=data['author_last_name']):
                    continue
                else:
                    DatabaseFunctions.add_one('books_table', book_props)

        wish_index = self.wish.currentIndex()
        wish_options = {
            0: self.get_average_pages_num,
            1: self.get_max_page_book,
            2: self.get_min_page_book
        }

        if wish_index in wish_options:
            output_message = wish_options[wish_index](table_name)

        self.label_4.setText(output_message)

    # get output messages
    @staticmethod
    def get_average_pages_num(table_name):
        items = DatabaseFunctions.get_avg_pages(table_name)
        average_pages = items[0][0] if items and items[0][0] is not None else 0
        return f'Average Number Of Pages\n{int(average_pages)} pages'


    @staticmethod
    def get_max_page_book(table_name):
        row = DatabaseFunctions.get_max_page(table_name)
        max_book = row[0][0]
        max_pages = row[0][1]
        return f'Book With Maximum Number Of Pages\n{max_book}, {max_pages} pages'

    @staticmethod
    def get_min_page_book(table_name):
        row = DatabaseFunctions.get_min_page(table_name)
        min_book = row[0][0]
        min_pages = row[0][1]
        return f'Book With Minimum Number Of Pages\n{min_book}, {min_pages} pages'


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setFixedSize(800, 600)
    window.setWindowTitle("Books Generator | GE")
    window.setWindowIcon(QIcon('media/icon.png'))
    window.show()
    sys.exit(app.exec_())
