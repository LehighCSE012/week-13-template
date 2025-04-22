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


def test_inspect_non_existent_item(db_path):
    """
    Test 3: Verifies that inspecting a non-existent item ID returns None.
    """
    non_existent_id = 999
    retrieved_item = adventure.inspect_loot_item(db_path, non_existent_id)

    assert retrieved_item is None, f"inspect_loot_item should return None for non-existent ID {non_existent_id}."

