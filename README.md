# Books Generator

Books Generator is a Python application that fetches book data from an API, stores it in a SQLite database, and provides functionalities to analyze the fetched books.

## Features

- Fetches book data (author name, title, number of pages, genres) from an external API.
- Stores fetched book data in a SQLite database.
- Provides options to analyze the fetched books:
  - Calculate the average number of pages among the fetched books.
  - Identify the book with the maximum number of pages.
  - Identify the book with the minimum number of pages.

## Requirements

- Python 3.x
- PyQt5
- requests
- DBFunctions (custom module for interacting with SQLite database)
- concurrent.futures (for concurrent execution of tasks)
- additional packages as specified in `requirements.txt`

## Usage

1. Run the application:
- python main.py

2. The application window will open. Adjust the number of books to generate using the input field.
3. Click the "Generate" button to fetch and analyze the books.
4. Choose an analysis option from the dropdown menu to see the corresponding result.

## Structure

- `main.py`: Main Python script containing the PyQt5 application.
- `DBFunctions.py`: Module for interacting with the SQLite database.
- `media/`: Directory containing UI files and icons.

>Gvantsa