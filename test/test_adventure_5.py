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


def test_record_and_inspect_single_item(db_path):
    """
    Test 2: Verifies recording a new loot item and then inspecting it.
            Checks return value of record_new_loot and inspect_loot_item.
    """
    item_name = "Scroll of Fireball"
    item_type = "Scroll"
    value = 150
    rarity = "Uncommon"
    location = "Wizard's Tower"

    # Record the item using the student's function
    new_id = adventure.record_new_loot(db_path, item_name, item_type, value, rarity, location)

    # Assertions for record_new_loot
    assert isinstance(new_id, int), "record_new_loot should return an integer ID."
    assert new_id > 0, "record_new_loot should return a positive ID."

    # Inspect the item using the student's function
    retrieved_item = adventure.inspect_loot_item(db_path, new_id)

    # Assertions for inspect_loot_item
    assert isinstance(retrieved_item, tuple), "inspect_loot_item should return a tuple."
    assert len(retrieved_item) == 6, "inspect_loot_item tuple should have 6 elements."
    # Expected tuple: (id, item_name, item_type, value_gp, rarity, found_in_dungeon)
    expected_tuple = (new_id, item_name, item_type, value, rarity, location)
    assert retrieved_item == expected_tuple, f"Retrieved item data {retrieved_item} does not match expected {expected_tuple}."

    # Optional: Direct DB verification
    db_data = query_db(db_path, "SELECT * FROM loot WHERE id = ?", (new_id,))
    assert len(db_data) == 1, "Direct DB query did not find the inserted item."
    assert db_data[0] == expected_tuple, "Direct DB data does not match expected tuple."
