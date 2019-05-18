import datadotworld as dw
import numpy as np
import pandas as pd

#############################################################
                ## HELPER FUNCTIONS ##
#############################################################

def get_fiscalyear(column, fiscalyear_start=7):
    """Create conversion column that reads dates and returns fiscal year. 
    
    Function takes a datetime series object or column and produces a 
    list with the corresponding fiscal year as a four digit year for 
    each date in the original series.

    The function's default value is based on the Maryland Govt fiscal 
    year which runs from July 1st (month 7) to June 30th.  It returns 
    a list that is the same size as the original column making it easy  
    to simply use the return from the function call as a new column
    for the same dataframe, adding data for fiscal year. The 
    fiscalyear_start parameter allows for generation of fiscal year data 
    for various months.
    
    Parameters
    -----------
    column:             pandas Series
                    a column of data type datetime. 
    
    fiscalyear_start:   int
                    a number representing the numerical value for month of 
                    the year to be used as the start of the fiscal year.
                    
    Returns
    --------
    Pandas Series: Series or column containing data for 4 digit number representing fiscal year.
    
    Examples
    --------
    >>> get_fiscalyear(df['request_date']) # assumes July fiscal year start
    
    >>> get_fiscalyear(df['request_date'], fiscalyear_start=3) # assumes March fiscal year start
    
    >>> get_fiscalyear(df['request_date'], 10) # assumes October fiscal year start
    """
    fiscal_year = np.where(column.month >= fiscalyear_start,
                           column.year+1, column.year)
    return fiscal_year


#############################################################
                ## REQUEST DATA ##
#############################################################

def get_data(dataset_name, dataframe_name):
    """Request data from datadotworld API, and returns pandas dataframe.
    
    Additional information on the datadotworld api can be found at the 
    following site: https://apidocs.data.world/api 
    
    Parameters
    ----------
    dataset_name:     str
                    name assigned to the desired dataset stored with 
                    datadotworld service.
    
    dataframe_name:   str
                    name of the key associated with the datadotworld
                    dataset which stores objects within the dataset within
                    a dictionary of dataframes in key value pair. 
                    
    Returns
    -------
    Pandas Dataframe
    
    Examples
    --------
    >>> get_data(dataset_name='census2020', dataframe_name='Kansas')
    
    >>> get_data('performance_indicators', 'public_safety')
    """
    dataworld_obj = dw.load_dataset(dataset_name)
    dataframe = dataworld_obj.dataframes[dataframe_name]
    
    return dataframe


def clean_data(dframe):
    '''

    '''
    target_columns = (['wo_id','date_completed','prob_type','bl_id','completed_by',
                        'date_requested','time_completed','time_start','time_end'])
    
    if isinstance(dframe, pd.core.frame.DataFrame):
        try:
            dframe = dframe[target_columns][(dframe['prob_type'] != 'TEST(DO NOT USE)')]
            dframe['date_completed'] = pd.to_datetime(dframe['date_completed'])
            dframe['date_requested'] = pd.to_datetime(dframe['date_requested'])
            dframe.set_index('date_requested', inplace=True)
            dframe['duration'] = dframe['date_completed'] - dframe.index
            dframe['fiscal_year_requested'] = get_fiscalyear(dframe.index)
            dframe['fiscal_year_completed'] = get_fiscalyear(dframe['date_completed'])
            dframe.sort_index(inplace=True)
            
            status = 'Pass'
        except Exception as e:
            status = 'Fail'
            # log event if failed 
    else:
        print('Function requires pandas dataframe object but received type: {}.'
             .format(type(dframe)))
        
    return dframe


data = get_data(dataset_name='dgs-kpis/fmd-maintenance',
                dataframe_name='archibus_maintenance_data')
dframe = clean_data(data)

