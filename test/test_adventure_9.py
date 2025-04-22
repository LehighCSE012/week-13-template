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

# Test 6: Function find_heavy_deep_artifacts - Combined Criteria
def test_find_heavy_deep_artifacts_basic(sample_df):
    """
    Tests find_heavy_deep_artifacts with minimum weight and depth,
    expecting rows that meet both criteria.
    """
    min_weight = 5.0
    min_depth = 8.0
    result_df = adventure.find_heavy_deep_artifacts(sample_df, min_weight, min_depth)

    # Manually find rows meeting Weight >= 5.0 AND Depth >= 8.0
    expected_data = {
        'ArtifactID': ['AZM002', 'AZM012', 'AZM019'],
        'Type': ['Statue Head', 'Statue Base', 'Statue Head'],
        'Material': ['Marble', 'Marble', 'Marble'],
        'Weight_kg': [8.2, 150.0, 7.5],
        'EstValue': [1500, 5000, 1300],
        'Depth_m': [8.0, 12.0, 8.5],
        'Description': ['Head of a deity?', 'Massive stone base', 'Weathered features'],
        'Sector': ['West', 'Central', 'West']
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df.index = result_df.index # Align indices

    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True), check_dtype=True)
