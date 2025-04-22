# test_adventure.py
import pytest
import sqlite3
import os
import adventure # Assumes student code is in adventure.py

# --- Fixture for Test Database ---

@pytest.fixture
def db_path(tmp_path):
    """
    Pytest fixture to create a temporary database for each test function.
    Initializes the ledger using the student's function.
    Yields the path to the database file.
    """
    # Create a unique path within the temporary directory provided by pytest
    db = tmp_path / "test_dm_ledger.db"
    db_file_path = str(db)

    # Ensure the database starts clean for the test
    if os.path.exists(db_file_path):
        os.remove(db_file_path)

    # Use the student's function to initialize the database and table
    adventure.initialize_ledger(db_file_path)

    # Provide the path to the test function
    yield db_file_path

    # Clean up the database file after the test runs (optional, tmp_path often handles it)
    # if os.path.exists(db_file_path):
    #     os.remove(db_file_path)

# --- Helper Function for Direct DB Verification ---

def query_db(db_path, sql, params=()):
    """Helper to run a SELECT query and fetch all results."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Direct DB Query Error: {e}")
        return None # Indicate error
    finally:
        if conn:
            conn.close()

# --- Test Functions (7 Tests) ---

def test_initialize_ledger_creates_table(db_path):
    """
    Test 1: Verifies that initialize_ledger creates the 'loot' table
            with the correct schema.
    Relies on the db_path fixture already calling initialize_ledger.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='loot';")
        result = cursor.fetchone()
        assert result is not None, "The 'loot' table was not created."
        assert result[0] == 'loot', "Table name should be 'loot'."

        # Check table schema (column names and types)
        cursor.execute("PRAGMA table_info(loot);")
        columns_info = cursor.fetchall()
        # cid, name, type, notnull, dflt_value, pk
        expected_schema = {
            'id': ('INTEGER', 1), # name: (type, pk_flag)
            'item_name': ('TEXT', 0),
            'item_type': ('TEXT', 0),
            'value_gp': ('INTEGER', 0),
            'rarity': ('TEXT', 0),
            'found_in_dungeon': ('TEXT', 0)
        }
        assert len(columns_info) == len(expected_schema), f"Expected {len(expected_schema)} columns, found {len(columns_info)}"

        for col in columns_info:
            col_name = col[1]
            col_type = col[2]
            col_pk = col[5]
            assert col_name in expected_schema, f"Unexpected column '{col_name}' found."
            assert col_type == expected_schema[col_name][0], \
                   f"Column '{col_name}' has wrong type '{col_type}', expected '{expected_schema[col_name][0]}'."
            assert col_pk == expected_schema[col_name][1], \
                   f"Column '{col_name}' has wrong primary key flag '{col_pk}', expected '{expected_schema[col_name][1]}'."

    except sqlite3.Error as e:
        pytest.fail(f"Database error during schema check: {e}")
    finally:
        if conn:
            conn.close()
