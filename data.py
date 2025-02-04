import datadotworld as dw
import numpy as np
import pandas as pd

################################################################################
################################################################################
                            ## HELPER FUNCTIONS ##
################################################################################
################################################################################

def weekday_name(integer):
    """Convert integer from 0-6 to return corresponding weekday name.

    Function takes an integer from dayofweek value for timestamp and
    returns the name of the day of the week. For example: a day of
    week value of 0 returns 'Monday'

    Parameters
    ----------
    integer:    int  (valid values range 0 to 6)

    Returns
    -------
    Str:        Returns the name of the day of the week.

    Example
    -------
    >>> weekday_name(3)  # returns Thursday
    """
    day_names = ("Monday","Tuesday","Wednesday","Thursday",
                 "Friday","Saturday","Sunday")
    return day_names[integer]


def month_name(integer):
    """Convert integer from timestamp month to return corresponding
    month name.

    Function takes integer from month value for timestamp and returns
    corresponding name of month in calendar year (zero indexed) as a
    string.  For example, a timestamp with datetime.month value of 3
    returns April.

    Parameters
    ----------
    integer:  int (timestamp.month)

    Returns
    -------
    Str:    Name of month at correspnding place in list of months
            zero indexed and in caldenar year order.

    Example
    -------
    >>> month_name(12)  # returns December
    """
    month_names = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    return month_names[integer-1]



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
    Pandas Series: Series or column containing data for 4 digit number
                   representing fiscal year.

    Examples
    --------
    >>> get_fiscalyear(df['request_date']) # assumes July fiscal year start

    >>> get_fiscalyear(df['request_date'], fiscalyear_start=3) # assumes March
        fiscal year start

    >>> get_fiscalyear(df['request_date'], 10) # October fiscal year start
    """

    fiscal_year = [date.year + 1 if date.month >= fiscalyear_start
                   else date.year for date in column]

    return fiscal_year




class ValueNotTypeFloatIntListSetStr(ValueError):
    pass

def valid_instance(value):
    """Checks whether a value is instance of float,int,list,set or str and returns Boolean.

    Parameters
    ----------
    value:     float int list set or str
            Any value passed to function such as 8, '8', [8,'8'], 8.0 or set([8,'8'])

    Returns
    -------
    Boolean:   True if value parameter is of type float, int, list set or str,
               and returns False otherwise.

    Example:
    --------
    >>>       valid_instance("I'm good!") # returns True

    >>>       valid_instance({'name':'Joe Budden'}) # raises Error
    """

    if (isinstance(value, float)  or
        isinstance(value, int)    or
        isinstance(value, list)   or
        isinstance(value, set)    or
        isinstance(value, str)):

        return True
    else:
        ### Valid value types include: [str, int, list, float]
        raise ValueNotTypeFloatIntListSetStr(value)




def container_hasvalue(container, value):
    """Checks whether or not a value appears in a column and returns Boolean.

    Parameters
    ----------
    container:    Pandas Series or list
                A dataframe column or list of values.

    value:        Valid values include Int, Str, Float
                A value for against which the list or series object can be searched
                to determine its existence.

    Returns
    -------
    Boolean:    Returns True if value is in container object, False otherwise

    """
    if valid_instance(value):

        container = list(container)
        container = set(container)

        if value in container:
            return True
        else:
            return False

    else:
        return False



class ValueNotTypeInt(ValueError):
    pass

def valid_fiscalyear(series, year):
    """Checks whether or not a fiscalyear value appears in a column.

    Parameters
    ----------
    series:    Pandas Series object
            A dataframe column against which a check will be performed to determine
            existence of a particular year value.

    year:      Int
            A 4 digit fiscal year representing the value that will be searched for
            in the series.

    Returns
    --------
    Boolean:  Returns True if year is in series, False if not.

    Example
    -------
    >>> valid_fiscalyear(series=requestDate, year=2017) # returns True if 2017 is in
                                                          requestDate column

    >>> valid_fiscalyear(requestDate, '2030') # returns ValueNotTypeInt error

    """
    if isinstance(year, int):
        return container_hasvalue(series, year)
    else:
        ### year parameter expects value of type int
        raise ValueNotTypeInt(year)




def filter_fiscalyear(dframe, column, fiscalyear):
    """Return filtered dataframe with a view of data for a single fiscalyear.

    Function uses a fiscalyear parameter to slice a dataframe and provide
    a dataset that excludes data for all fiscalyears except the one passed. It
    accepts an integer representing a  4-digit year present in the target column.

    Parameters
    ----------
    dframe:      Pandas Dataframe

    column:      Str
            Column name or Pandas Series containing the fiscalyear data. Expects a 
            column with values similar in format to what is passed to the fiscalyear
            parameter. For example, a series with values: [2015,2018,2016,2016,2016...]

    fiscalyear:  Int
            4 digit year of one of the fiscalyears present in target column.

    Returns
    -------
    Pandas Dataframe

    Example
    -------
    >>> filter_fiscalyear(dframe, 'fy_completed')

    >>> filter_fiscalyear(dframe, 'FYear_Requested', 2015)
    """

    if valid_fiscalyear(series=dframe[column], year=fiscalyear):

        try:
            dataframe = dframe[(dframe[column] == fiscalyear)]
            return dataframe

        except Exception as e:
            print(e)  # convert to log

    else:

        print('Function failed to return filtered dataframe. Exited false vailid_fiscalyear')


    #validated_year = validate_fiscalyear(dframe[column], fiscalyear)

#     if validated_year:
#         try:
#             dataframe = dframe[(dframe[column] == fiscalyear)]
#             return dataframe
#         except Exception as e:
#             print(e)  # convert to log
#     else:
#         return validated_year




def null_nonexistent(series):
    """Performs check to see if a column has null values and returns boolean.

    Parameters
    ----------
    series:      Pandas Series
            The column name of a dataframe

    Returns
    -------
    Boolean:  Returns True if there are no null values in column, False otherwise.

    Example
    -------
    >>> null_nonexistent(dataframe.index) # returns True

    """
    if series.isnull().sum() > 0:
        return False
    else:
        return True


def ontime(dframe, problemtype_column='prob_type', duration_column='duration'):
    """Get information by type, on count, average duration and percentage of workorders
    closed ontime.

    Returns tupple of 3 Pandas Series objects with information on the percentage of
    workorders on time for each problem type. Information returned at each position in
    tupple is: 1) number of requests by problem type, 2) mean duration by problem type
    3) percentage of workorders ontime by problem type.

    Tupple allows for unpacking for elements required to create charts on workorders
    closed ontime. For example, values for x, y and size of a scatter plot can be passed
    as x = ontime(dframe)[0], y = ontime(dframe)[1], size = ontime(dframe)[2]

    Parameters
    ----------
    dframe:              Pandas Dataframe
                Expects a dataframe that has had all open workorders removed.
                Filtering out open workorders removes null values from completion
                and duration columns to support calculation of groupby and average
                taking on dataframe.

    problemtype_column:  Str
                Name of column containing data on the workorder type category.

    duration_column:     Str
                Name of datetime type column containing duration for each workorder.

    Returns
    -------
    Tupple:   Return object has 3 items in tupple:
             (total_volume_bytype, avg_duration_bytype, percentage_ontime)

    Example
    -------
    >>> ontime(df,'prob_type','duration') # if duration has no null values returns tupple

    >>> ontime(df, 'ptypes', 'drtn') # if null values present returns string:
                                       'Check "drtn" column, ensure there are no null values.'
    """
    if null_nonexistent(dframe[duration_column]):
        try:
            dframe['days_integer'] = dframe[duration_column].dt.days.astype(int)
            dframe['average_duration'] = dframe.groupby(problemtype_column)['days_integer'].transform('mean')
            dframe['ontime'] = np.where(dframe['days_integer'] <= dframe['average_duration'], 1, 0)

            avg_duration_bytype = dframe.groupby(problemtype_column)['average_duration'].mean()
            number_ontime_bytype = dframe.groupby(problemtype_column)['ontime'].sum()
            total_volume_bytype = dframe.groupby(problemtype_column)['ontime'].count()
            percentage_ontime = (number_ontime_bytype / total_volume_bytype) * 100

            return (total_volume_bytype, avg_duration_bytype, percentage_ontime)

        except Exception as e:
            print(e) # convert to log
    else:
        return 'Check "{}" column, ensure there are no null values.'.format(duration_column)



def remove_open_workorders(dframe, column='date_completed'):
    """Return filtered dataframe removing workorder data missing completion dates.

    Parameters
    ----------
    dframe:   Pandas Dataframe

    column:   Str
            Name of datetime object column containing dates of work order
            completion.
    Returns
    -------
    Pandas Dataframe

    Example
    -------
    >>> remove_open_workorders(dframe)
    """

    dataframe = dframe[(dframe[column].notnull())]
    return dataframe






################################################################################
################################################################################
                            ## REQUEST DATA ##
################################################################################
################################################################################

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
    '''Perform reindexing, cleaning and feature generation on dataframe for
    dashboard.

    Parameters
    ----------
    dframe:   Pandas Dataframe
            Expects pandas dataframe returned from the get_data function. The
            data.py module structure separates the request from the preparation
            of the data into two functions: get_data and this clean_data

    Returns
    -------
    Pandas Dataframe:  Returns a new dataframe with releveant Series converted
                       to datetime objects, adds relevant features for duration
                       and resets the index.

    Example
    -------
    >>> data = get_data(dataset_name='performance_indicators',
                        dataframe_name='public_safety')

        clean_data(dframe=data)

    '''
    target_columns = (['wo_id','date_completed','prob_type','bl_id',
                        'completed_by','date_requested','time_completed',
                        'time_start','time_end'])

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


def make_map_dframe(dframe, excelfile, skipnrows=6):
    """Generate dataframe for mapping charts with archibus data.

    Parameters
    ----------
    dframe:     pandas dataframe
            the dataframe returned from the clean_data function
            in the data.py module

    excelfile:  file object
            excel file with the latitude and longitude data required
            to identify the location of markers for archibus data.

    skipnrows:  int
            the number of rows to skip when reading in excel sheet
            for conversion to pandas dataframe.

    Returns
    -------
    Pandas Dataframe

    Example
    -------
    >>> make_map_dframe(dframe=df, excelfile='file.xlsx', skipnrows=5)

    """

    df = pd.read_excel(excelfile, skiprows=skipnrows)
    df.columns = ['bl_id','name','addr','site_id','latitude','longitude']
    geo_dict = {}
    for bld in df['bl_id'].unique():
        geo_dict[bld] = {'latitude': df.loc[df['bl_id'] == bld]['latitude'].values[0],
                        'longitude': df.loc[df['bl_id'] == bld]['longitude'].values[0],
                        'bld_name': df.loc[df['bl_id'] == bld]['name'].values[0]}

    dframe['latitude'] = dframe['bl_id'].apply(lambda x: geo_dict[x]['latitude'])
    dframe['longitude'] = dframe['bl_id'].apply(lambda x: geo_dict[x]['longitude'])
    dframe['bld_name'] = dframe['bl_id'].apply(lambda x: geo_dict[x]['bld_name'])

    return dframe

################################################################################
################################################################################
                            ## MODULE VARIABLES ##
################################################################################
################################################################################

data = get_data(
    dataset_name='dgs-kpis/fmd-maintenance',
    dataframe_name='archibus_maintenance_data')

dframe = clean_data(data)

map_dframe = make_map_dframe(
    dframe=dframe, excelfile='data/building_lat_longs.xlsx')


preventative_types = ['PREVENTIVE MAINT','HVAC|PM']
corrective_types = ['BOILER','CHILLERS','COOLING TOWERS','HVAC',
                   'HVAC INFRASTRUCTURE','HVAC|REPAIR']

hvac_types = ['PREVENTIVE MAINT','HVAC|PM','BOILER','CHILLERS',
              'COOLING TOWERS','HVAC','HVAC INFRASTRUCTURE',
              'HVAC|REPAIR' ]
