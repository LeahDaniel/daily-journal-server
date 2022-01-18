import sqlite3
import json
from models import Entry, Mood


def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.mood_id,
            e.date,
            e.concept,
            e.entry,
            m.label
        FROM Entry e
        JOIN Mood m 
            ON e.mood_id = m.id
        """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Entry class above.
            entry = Entry(row['id'], row['mood_id'],
                          row['date'], row['concept'], row['entry'])

            mood = Mood(row['mood_id'], row['label'])

            db_cursor.execute("""
                SELECT
                    et.tag_id
                FROM EntryTag et
                JOIN Entry e
                    ON et.entry_id = e.id
                WHERE et.entry_id = ?
                """, (row['id'], ))

            # Convert rows of data into a Python list
            tag_data = db_cursor.fetchall()

            tag_list = []

            for new_row in tag_data:
                tag_list.append(new_row['tag_id'])

            entry.tags = tag_list
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)


def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.mood_id,
            e.date,
            e.concept,
            e.entry,
            m.label
        FROM Entry e
        JOIN Mood m 
            ON e.mood_id = m.id
        WHERE e.id = ?
        """, (id, ))

        # Load the single result into memory
        row = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(row['id'], row['mood_id'],
                      row['date'], row['concept'], row['entry'])

        mood = Mood(row['mood_id'], row['label'])

        entry.mood = mood.__dict__

        return json.dumps(entry.__dict__)


def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entry
        WHERE id = ?
        """, (id, ))


def get_entries_by_search(search_term):

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.mood_id,
            a.date,
            a.concept,
            a.entry
        FROM Entry a
        WHERE a.entry LIKE ? OR a.concept LIKE ?
        """, (f'%{search_term}%', f'%{search_term}%'))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['mood_id'], row['date'],
                          row['concept'], row['entry'])
            entries.append(entry.__dict__)

    return json.dumps(entries)


def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
            ( mood_id, date, concept, entry)
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['mood_id'], new_entry['date'],
              new_entry['concept'], new_entry['entry']
              ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        entry_id = db_cursor.lastrowid

        # Add the `id` property to the entry dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = entry_id

        for tag_id in new_entry['tags']:

            db_cursor.execute("""
                INSERT INTO EntryTag
                    ( entry_id, tag_id)
                VALUES
                    ( ?, ?);
                """, (entry_id, tag_id))

    return json.dumps(new_entry)


def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                mood_id = ?,
                date = ?,
                concept = ?,
                entry = ?
        WHERE id = ?
        """, (new_entry['mood_id'], new_entry['date'], new_entry['concept'],
              new_entry['entry'], id))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
