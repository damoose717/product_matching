import pandas as pd
import numpy as np


def develop_matching_features(extracted_data_path: str) -> pd.DataFrame:
    """This function takes the path of the exctracted_data csv file as a string 
    and returns the matching_features as a Pandas dataframe."""
    
    # read in dataframe
    extracted_data = pd.read_csv(extracted_data_path)
    
    # get price from price_value_blended
    extracted_data['price'] = extracted_data['price_value_blended']
    
    # get package from package_value
    extracted_data['package'] = extracted_data['package_value']
    
    # get thc_weight from cannabinoid_thc_value and adding units of mg
    extracted_data['thc_weight'] = extracted_data.apply(
        lambda x: float('nan')
            if np.isnan(x['cannabinoid_thc_value'])
            else str(int(x['cannabinoid_thc_value'])) + 'mg'
        , axis = 1)
    
    # get cbd_weight from cannabinoid_cbd_value and adding units of mg
    extracted_data['cbd_weight'] = extracted_data.apply(
        lambda x: float('nan')
            if np.isnan(x['cannabinoid_cbd_value'])
            else str(int(x['cannabinoid_cbd_value'])) + 'mg'
        , axis = 1)
    
    # get id_product from brand_name and flavor_ingestibles 
    extracted_data['id_product'] = (extracted_data['brand_name'] + 
                                    '-' + 
                                    extracted_data['flavor_ingestibles']
                                   ).str.replace(' ', '-').str.replace('\'', '')
    
    # remove hyphens from brand_name
    extracted_data['brand_name'] = extracted_data['brand_name'].str.replace('-', '')
    # replace nan with smokiez TODO FIX THIS
    extracted_data['brand_name'] == np.where(
        extracted_data['brand_name'].isna()
        , 'smokiez'
        , extracted_data['brand_name']
    )
    # rename stiiizy to stiizy 
    extracted_data['brand_name'] = extracted_data['brand_name'].str.replace(
        'stiiizy', 'stiizy')
    # rename smokiez edibles to smokiez 
    extracted_data['brand_name'] = extracted_data['brand_name'].str.replace(
        'smokiez edibles', 'smokiez')
    
    # flavor_ingestibles fixes
    extracted_data['flavor_ingestibles'] = extracted_data['flavor_ingestibles'].str.replace(
        'ñ', 'n')
    extracted_data['flavor_ingestibles'] = extracted_data['flavor_ingestibles'].str.replace(
        'sour blue raspberry', 'blue raspberry')
    extracted_data['flavor_ingestibles'] = extracted_data['flavor_ingestibles'].str.replace(
        'root beer float', 'rootbeer float')    
    extracted_data['flavor_ingestibles'] = extracted_data['flavor_ingestibles'].str.replace(
        'assorted', 'assorted flavors') 
    extracted_data['flavor_ingestibles'] = extracted_data['flavor_ingestibles'].str.replace(
        'cocoa banana cream pie', 'banana cream pie') 
    extracted_data['flavor_ingestibles'] = extracted_data['flavor_ingestibles'].str.replace(
        'tropical fruit', 'tropical') 
    extracted_data['flavor_ingestibles'] = extracted_data['flavor_ingestibles'].str.replace(
        'sour blackberry', 'blackberry') 
    extracted_data['flavor_ingestibles'] = extracted_data['flavor_ingestibles'].str.replace(
        'rainbow sorbet', 'rainbow sherbet') 
    extracted_data['flavor_ingestibles'] = extracted_data['flavor_ingestibles'].str.replace(
        'plum', 'indica plum') 
    extracted_data['flavor_ingestibles'] = extracted_data['flavor_ingestibles'].str.replace(
        'chile lime', 'mango & chile lime') 
    
    # reorder columns
    extracted_data = extracted_data[['_id'
                                      , 'brand_name'
                                      , 'flavor_ingestibles'
                                      , 'thc_weight'
                                      , 'cbd_weight'
                                      , 'cannabis_strain_type'
                                      , 'price'
                                      , 'package'
                                      , 'day_report_date'
                                      , 'data_source_name'
                                      , 'product_slug'
                                      , 'id_product']]
    
    return extracted_data
    
    
def develop_matched_data(matching_features_path: str) -> pd.DataFrame:
    """This function takes the path of the matching_features csv file as a string 
    and returns the matched_data as a Pandas dataframe."""
    
    # read in dataframe
    matching_features = pd.read_csv(matching_features_path)
    
    # rename columns 
    matching_features['brand'] = matching_features['brand_name']
    matching_features['flavor'] = matching_features['flavor_ingestibles']
    matching_features['strain_type'] = matching_features['cannabis_strain_type']

    # set product_name_line column to NaN
    matching_features['product_name_line'] = np.nan
    
    matching_features['cbd_weight'] = matching_features['cbd_weight'] + ' cbd'
    matching_features['thc_weight'] = matching_features['thc_weight'] + ' thc'

    # get id_product_match from brand_name and flavor_ingestibles 
    matching_features['_id_product_match'] = (matching_features['brand_name'] + 
                                    '-' + 
                                    matching_features['flavor_ingestibles']
                                   ).str.replace(' ', '-').str.replace('\'', '')
    # assign a unique numerical value to each value of _id_product_match
    id_product_match_dict = {x: i for i, x in 
                             enumerate(set(matching_features['_id_product_match']))}
    matching_features = matching_features.replace({'_id_product_match': 
                                                   id_product_match_dict})

    # reorder columns 
    matching_features = matching_features[['_id'
                                           , '_id_product_match'
                                           , 'brand'
                                           , 'flavor'
                                           , 'thc_weight'
                                           , 'cbd_weight'
                                           , 'strain_type'
                                           , 'day_report_date'
                                           , 'product_slug'
                                           , 'price'
                                           , 'data_source_name'
                                           , 'product_name_line']]
   
    return matching_features
    
    
