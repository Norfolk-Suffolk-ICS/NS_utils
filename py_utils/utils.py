import pandas as pd
import math

# European standard population Dataframe
EUROPEAN_STANDARD_POP = {
    'AgeBand5yrs': ['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80-84','85-89', '90+'],
    'Standard_pop': [5000,5500,5500,5500,6000,6000,6500,7000,7000,7000,7000,6500,6000,5500,5000,4000,2500,1500,1000]
}
EU_STANDARD_DF = pd.DataFrame(EUROPEAN_STANDARD_POP)


def calculate_standardised_rates(input_df, age_band_column:str, population_column:str, group_columns:list[str], count_column:str):
    """
    Calculates standardized rates based on EU Standard Population.
    
    Paremeters
    ----------
    input_df: dataframe
    age_band_column: column in the df with age bands  (0-4,5-9,10-14 and so on)
    population_column: column in the df with total population
    group_columns: List of column you want to group by and sum
    count_column: column in df with counts of a subset from the population column 
    
    Returns
    -------
    Dataframe containing Standard rates per 100k as a new column

    """

    df_ = input_df.loc[:,[age_band_column, population_column, count_column] + group_columns].copy()

    if age_band_column != 'AgeBand5yrs':
        df_ = df_.rename(columns={age_band_column : 'AgeBand5yrs'})
    df_ = pd.merge(df_, EU_STANDARD_DF, on='AgeBand5yrs', how='outer')
    df_[population_column] = df_[population_column].fillna(0)

    # Calculating the  Heart Failure Crude rates per 1000 people, in each age band
    df_['crude_rate'] = df_[count_column] / df_[population_column]
   
    # Calculating the Heart Failure Standardized rates
    df_['expected_events_in_std_subpopulation'] = (df_['crude_rate'] * df_['Standard_pop'])
    
    df_ = (df_
           .groupby(group_columns)
           .sum(numeric_only=True)
           .drop(columns=['crude_rate', 'Standard_pop'])
           .rename(columns={'expected_events_in_std_subpopulation': f'{count_column}_std_per_100k'})
           .reset_index()
           )
     
    return df_



def calculate_axis_lim(column , is_both_lim=True, is_max=True):
    """
    Calculates the axis limits and round them off based on:
     - If value is less than 10, round to nearest 10
     - If between 10 and 100, round off to nearest 100
     - If between 100 and 1000, round off to nearest 1000

    Parameters
    ----------
    column: Name of column whose Max & Min axis-lims needs to be known
    is_both_lim: A boolean value to confirm if both Max & Min axis-lims required
    is_max: A boolean, set to False if you only need Min-lim otherwise no input needed

    Returns
    -------
    if is_both_lim = False : a single INT value
    if is_both_lim = True  : Tuple with max and min lims

    """
    max = column.max()
    if (max < 10):
        round_max = math.ceil(max/1) * 1
    elif (max > 10 and max < 100):
        round_max = math.ceil(max/10) * 10
    elif (max > 100 and max < 1000):
        round_max = math.ceil(max/100) * 100
    else:
        round_max = math.ceil(max/1000) * 1000

    min = column.min()
    if (min < 10):
        round_min = math.ceil(min/1) * 1
    elif (min > 10 and min < 100):
        round_min = math.floor(min/10) * 10
    elif (min > 100 and min < 1000):
        round_min = math.floor(min/100) * 100
    else:
        round_min = math.floor(min/1000) * 1000

    if is_both_lim == True:
        return round_min , round_max
    else:
        if is_max == True:
            round_min = 0
            return round_max
        else:
            return round_min
        


def get_fiscal_year(date):
    """
    Calculates and return the fiscal year for a given date.

    Parameters
    ----------
    date: datetime.datetime
    A datetime object representing the date for which the fiscal year is to be determined

    Returns 
    -------
    Fiscal_year : Object
    An object representing the fiscal year

    Note
    ----
    The function assumed a fiscal year starts in April and ends in March

    USAGE
    -----
    DF['Fiscal_year'] = DF['Date'].map(get_fiscal_year) 
    This will create a new column 'Fiscal_year' in DF and calculate fiscal year for each datetime value in 'date' column 

    """
    year = date.year
    if date.month >=4:
        yr_start = year
        yr_end = str(year + 1)
    else:
        yr_start = year - 1
        yr_end = str(year)
    return f'FY{yr_start}-{yr_end[-2:]}'