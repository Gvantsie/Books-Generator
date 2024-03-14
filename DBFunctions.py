import sqlite3


def create_database_table(name, props):
    conn = sqlite3.connect("books")
    c = conn.cursor()

    c.execute(f"""CREATE TABLE IF NOT EXISTS {name} (
        {', '.join([f'{column} {datatype}' for column, datatype in props.items()])}
    )""")

    conn.commit()
    conn.close()


def add_one(table_name, props):
    conn = sqlite3.connect("books")
    c = conn.cursor()

    c.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in range(len(props))])})", props)

    conn.commit()
    conn.close()


def show_all(table_name):
    conn = sqlite3.connect("books")
    c = conn.cursor()

    c.execute(f"SELECT rowid, * FROM {table_name}")
    items = c.fetchall()

    for item in items:
        print(item)

    conn.close()


def check_book_exists(table_name, title, first_name, last_name):
    conn = sqlite3.connect("books")
    c = conn.cursor()

    select_query = f"SELECT * FROM {table_name} WHERE first_name=? AND last_name=? AND title=?"
    props = (first_name, last_name, title)
    c.execute(select_query, props)
    existing_row = c.fetchone()
    conn.close()

    if existing_row is not None:
        return True
    else:
        return False


def get_avg_pages(table_name):
    conn = sqlite3.connect("books")
    c = conn.cursor()

    c.execute(f"SELECT AVG(pages_number) FROM {table_name}")
    items = c.fetchall()
    conn.close()

    return items


def get_max_page(table_name):
    conn = sqlite3.connect("books")
    c = conn.cursor()

    c.execute(f"SELECT rowid, * FROM {table_name} ORDER BY pages_number DESC LIMIT 1")
    row = c.fetchall()
    conn.close()

    return row


def get_min_page(table_name):
    conn = sqlite3.connect("books")
    c = conn.cursor()

    c.execute(f"SELECT rowid, * FROM {table_name} ORDER BY pages_number ASC LIMIT 1")
    row = c.fetchall()
    conn.close()

    return row
