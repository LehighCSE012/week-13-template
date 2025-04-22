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


def test_update_item_value_success_and_verify(db_path):
    """
    Test 6: Verifies updating an item's value. Checks return value and data change.
            Also tests updating a non-existent item returns False.
    """
    # Add an item
    item_name = "Shield +1"
    original_value = 1200
    item_id = adventure.record_new_loot(db_path, item_name, "Armor", original_value, "Uncommon", "Castle")
    assert item_id is not None, "Failed to record item for update test."

    # Update the value
    new_value = 1500
    update_result = adventure.update_item_value(db_path, item_id, new_value)

    # Assertions for successful update
    assert update_result is True, f"update_item_value should return True for successful update of ID {item_id}."

    # Verify the change using inspect_loot_item
    updated_item_details = adventure.inspect_loot_item(db_path, item_id)
    assert updated_item_details is not None, "Item disappeared after update."
    assert updated_item_details[3] == new_value, f"Item value was not updated correctly. Expected {new_value}, got {updated_item_details[3]}."

    # Verify the change using direct DB query
    db_data = query_db(db_path, "SELECT value_gp FROM loot WHERE id = ?", (item_id,))
    assert len(db_data) == 1, "Direct DB query couldn't find item after update."
    assert db_data[0][0] == new_value, f"Direct DB query shows incorrect value {db_data[0][0]} after update, expected {new_value}."

    # Test updating a non-existent item
    non_existent_id = 999
    update_fail_result = adventure.update_item_value(db_path, non_existent_id, 5000)
    assert update_fail_result is False, f"update_item_value should return False for non-existent ID {non_existent_id}."

