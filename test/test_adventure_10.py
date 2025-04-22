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



def test_remove_loot_item_success_and_verify(db_path):
    """
    Test 7: Verifies removing a loot item. Checks return value and data removal.
            Also tests removing a non-existent item returns False.
    """
    # Add items
    id_to_remove = adventure.record_new_loot(db_path, "Wand of Magic Missiles", "Wand", 750, "Uncommon", "Crypt")
    id_to_keep = adventure.record_new_loot(db_path, "Backpack", "Gear", 2, "Common", "General Store")
    assert id_to_remove is not None and id_to_keep is not None, "Failed to record items for remove test."

    # Remove one item
    remove_result = adventure.remove_loot_item(db_path, id_to_remove)

    # Assertions for successful removal
    assert remove_result is True, f"remove_loot_item should return True for successful removal of ID {id_to_remove}."

    # Verify removal using inspect_loot_item
    removed_item_details = adventure.inspect_loot_item(db_path, id_to_remove)
    assert removed_item_details is None, f"Item with ID {id_to_remove} should not be found after removal."

    # Verify removal using direct DB query
    db_data_removed = query_db(db_path, "SELECT * FROM loot WHERE id = ?", (id_to_remove,))
    assert len(db_data_removed) == 0, f"Direct DB query found item {id_to_remove} after it should have been removed."

    # Verify the other item still exists
    kept_item_details = adventure.inspect_loot_item(db_path, id_to_keep)
    assert kept_item_details is not None, f"Item {id_to_keep} that should have been kept was removed."
    db_data_kept = query_db(db_path, "SELECT * FROM loot WHERE id = ?", (id_to_keep,))
    assert len(db_data_kept) == 1, f"Direct DB query could not find item {id_to_keep} which should have been kept."

    # Test removing a non-existent item
    non_existent_id = 999
    remove_fail_result = adventure.remove_loot_item(db_path, non_existent_id)
    assert remove_fail_result is False, f"remove_loot_item should return False for non-existent ID {non_existent_id}."
