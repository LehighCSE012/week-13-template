import pytest
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
import numpy as np
from io import StringIO

# Assuming the student's code is in 'adventure.py'
import adventure

# Sample CSV data mimicking expedition_data.csv for testing
CSV_DATA = """ArtifactID,Type,Material,Weight_kg,EstValue,Depth_m,Description,Sector
AZM001,Pottery Shard,Ceramic,0.5,50,2.5,Painted fragment,North
AZM002,Statue Head,Marble,8.2,1500,8.0,Head of a deity?,West
AZM003,Coin,Gold,0.1,800,1.5,Emperor Azmar inscription,North
AZM004,Amulet,Jade,0.2,1200,5.5,Scarab beetle design,South
AZM005,Spearhead,Bronze,1.5,300,4.0,,West
AZM006,Goblet,Gold,0.8,2500,6.2,Intricate carvings,Central
AZM007,Tablet,Clay,2.1,150,3.0,Cuneiform script fragment,North
AZM008,Necklace,Gold,0.4,1800,5.0,Embedded with gems,Central
AZM009,Pottery Shard,Ceramic,0.6,60,2.8,,North
AZM010,Figurine,Bronze,3.5,600,7.5,Animal figure,West
AZM011,Coin,Silver,0.05,200,1.8,Unknown ruler,North
AZM012,Statue Base,Marble,150.0,5000,12.0,Massive stone base,Central
AZM013,Amulet,Gold,0.3,1500,5.8,Eye symbol,South
AZM014,Sword Hilt,Bronze,0.9,,9.0,Decorated hilt,West
AZM015,Pottery Shard,Ceramic,0.4,40,2.2,Simple design,North
AZM016,Mask,Gold,2.5,10000,11.5,Funerary mask,Central
AZM017,Figurine,Ceramic,1.8,250,6.5,Humanoid shape,South
AZM018,Coin,Bronze,0.15,20,1.2,Worn features,North
AZM019,Statue Head,Marble,7.5,1300,8.5,Weathered features,West
AZM020,Goblet,Silver,0.6,900,6.0,Plain silver goblet,Central
"""

@pytest.fixture
def sample_df():
    """Provides a sample DataFrame loaded from the CSV_DATA string."""
    return pd.read_csv(StringIO(CSV_DATA))


# Test 2: Function summarize_artifact_types - Correct Counts and Sorting
def test_summarize_artifact_types_correctness(sample_df):
    """
    Tests summarize_artifact_types for accurate counts of each type,
    sorted in descending order.
    """
    result_series = adventure.summarize_artifact_types(sample_df)

    # Manually calculate expected counts and order from CSV_DATA
    expected_data = {
        'Pottery Shard': 3,
        'Coin': 3,
        'Statue Head': 2,
        'Amulet': 2,
        'Goblet': 2,
        'Figurine': 2,
        'Spearhead': 1,
        'Tablet': 1,
        'Statue Base': 1,
        'Sword Hilt': 1,
        'Mask': 1,
        'Necklace': 1 # Added Necklace based on sample data review
    }
    # Correcting expected data based on sample: Necklace was missing
    expected_data_corrected = {
        'Pottery Shard': 3, 'Coin': 3, 'Statue Head': 2, 'Amulet': 2,
        'Goblet': 2, 'Figurine': 2, 'Spearhead': 1, 'Tablet': 1,
        'Necklace': 1, 'Statue Base': 1, 'Sword Hilt': 1, 'Mask': 1
    }

    expected_series = pd.Series(expected_data_corrected, name='count').sort_values(ascending=False)
    # Ensure the name matches if value_counts() adds one
    if result_series.name:
         expected_series.name = result_series.name # Match name if present

    assert_series_equal(result_series, expected_series, check_dtype=True, check_names=False) # Check names False as default might differ


