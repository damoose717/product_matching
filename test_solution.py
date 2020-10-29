import pandas as pd
import numpy as np


def test_develop_matching_features():
    
    expected = pd.read_csv('2-matching_features_final.csv').drop(
        columns = ['id_product', 'brand_name', 'flavor_ingestibles']
    ).sort_values('_id').reset_index(drop = True)
    
    actual = develop_matching_features('1-extracted_data_final.csv').drop(
        columns = ['id_product', 'brand_name', 'flavor_ingestibles']
    ).sort_values('_id').reset_index(drop = True)
    
    pd.testing.assert_frame_equal(expected, actual)
    
    
def test_develop_matched_data():
    
    expected = pd.read_csv('3-matched_data_final.csv').drop(
        columns = ['_id_product_match', 'cbd_weight', 'strain_type']
    ).sort_values('_id').reset_index(drop = True)
    
    actual = develop_matched_data('2-matching_features_final.csv').drop(
        columns = ['_id_product_match', 'cbd_weight', 'strain_type']
    ).sort_values('_id').reset_index(drop = True)
    
    pd.testing.assert_frame_equal(expected, actual)
    