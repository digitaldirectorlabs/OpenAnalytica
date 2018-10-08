# -*- coding: utf-8 -*-
from __future__ import division
import csv
import numpy as np
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from ggplot import *
from datetime import datetime
import pandas as pd
import itertools
import operator
import os


def schema():
    '''
    Defines data columns and types
    '''
    vf_cols = ['nationbuilder_id', 'first_name', 'middle_name', 
               'last_name', 'email1','born_at', 'sex', 'primary_country', 
                'primary_state','primary_city','primary_county','primary_zip',
                'primary_address1','primary_address2','primary_address3']

    vf_converters = {'nationbuilder_id':str,'first_name':str,'middle_name':str,
                    'last_name':str,'email1':str,'born_at':pd.to_datetime,'sex':str, 
                    'primary_country':str, 'primary_state':str,'primary_city':str,
                    'primary_county':str,'primary_zip':str,'primary_address1':str,
                    'primary_address2':str,'primary_address3':str}

    vh_converters = {'signup_id':str,'voter_guid':str,'first_name':str,
                    'last_name':str,'election_country':str,'election_state':str,
                    'election_at':pd.to_datetime,'ballot_vote_method':str,
                    'ballot_party':str,'ballot_cast_at':str}
    
    return vf_cols, vf_converters, vh_converters


def make_dataframes(vf_path, vh_path):
    '''
    Imports CSV files and creates Pandas Dataframes
    '''
    vf_cols, vf_converters, vh_converters = schema()
    voter_file = pd.read_csv(vf_path, usecols=vf_cols, converters=vf_converters)
    voter_history = pd.read_csv(vh_path, low_memory=False, converters=vh_converters)

    voter_file = voter_file.set_index('nationbuilder_id')
    voter_history = voter_history.set_index('signup_id')

    return voter_file, voter_history


def clean_dataframes(voter_file, voter_history):
    '''
    Clean data
    '''
    voter_file.replace(r'^\s*$', np.nan, regex=True, inplace = True) # Replace empty cells with NaN
    voter_history.replace(r'^\s*$', np.nan, regex=True, inplace = True) # Replace empty cells with NaN

    return voter_file, voter_history


def data_quality_check(voter_file, voter_history):
    '''
    Quick data quality check for missing data. 
    '''
    print("TOTAL REGISTERED VOTERS IN DISTRICT (Voter File):" + " " + str(len(voter_file)))
    print("TOTAL VOTES CAST OVER ALL ELECTIONS (Voter History): "
          + str(len(voter_history)))
    print("\n")

    print("VOTER FILE ROWS MISSING")
    [print(x 
           + ": " 
           + str(round(voter_file[x].isnull().sum() 
           / len(voter_file)
           * 100,1)) 
           + "%") for x in ['first_name', 'middle_name', 'last_name',
                            'email1', 'born_at', 'sex','primary_country',
                            'primary_state','primary_city','primary_county',
                            'primary_zip','primary_address1','primary_address2',
                            'primary_address3']]
    print("\n")

    print("PERCENT OF ROWS WITH UNDEFINED GENDER (i.e. not male or female): " 
          + str(round(len(voter_file[voter_file.sex == 'O']) 
          / len(voter_file) 
          * 100,1)) 
          + "%")

    print("\n")

    print("VOTER HISTORY ROWS MISSING")
    [print(x 
           + ": " 
           + str(round(voter_history[x].isnull().sum() 
           / len(voter_history) 
           * 100,1)) 
           + "%") for x in ['first_name', 'last_name','election_at', 
                            'ballot_vote_method', 'ballot_party']]


def age_distribution(voter_file):
    '''
    Plot age distribution of all registered voters.  
    '''
    age_all = 2017 - voter_file['born_at'].dt.year
    age_all.plot.hist(bins=20, alpha=0.8, label='n:'+ str(len(age_all)), 
                      facecolor='#925A92', edgecolor='black')

    ax = plt.subplot(111) 
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False) 

    plt.xlabel('Age (Years)', fontsize=12)
    plt.ylabel('Registered Voters', fontsize=12)
    legend = 'total: ' + str(len(voter_file))
    patch = mpatches.Patch(label=legend, facecolor='#925A92', edgecolor='black')
    plt.legend(handles=[patch])


def get_elections(voter_history):
    '''
    Create list of general & primary elections. 
    '''
    election_year = voter_history['election_at'].dt.year.unique()
    election_month = voter_history['election_at'].dt.month.unique()
    elections_unsorted = list(itertools.product(election_month, election_year))
    elections = [('General '
                  + str(item[0])
                  + '-'
                  + str(item[1]),item[0],item[1]) 
                 if item[0] == 11 else ('Primary '
                                        + str(item[0]) 
                                        + '-'
                                        + str(item[1]), item[0], item[1]) 
                 for item in elections_unsorted]
    elections = sorted(elections, key=operator.itemgetter(2, 1))
    return elections


def age_distribution_by_election(voter_file, voter_history, elections):
    '''
    Plot age distribution of voters who voted by election. 
    '''
    fig, axes = plt.subplots(nrows=int(len(elections)/2), ncols=2, 
                             sharex='none', sharey='all', figsize=(12,40))
    fig.subplots_adjust(hspace=0.5)
    axes_list = [item for sublist in axes for item in sublist] 

    for item in elections:

        try:
            hfont = {'fontname':'Arial'}

            ax = axes_list.pop(0)
            voters = voter_history[(voter_history['election_at'].dt.month == item[1]) 
                                   & (voter_history['election_at'].dt.year == item[2])]
            voters = voters.join(voter_file, lsuffix='_left', rsuffix='_right')
            age = item[2] - voters['born_at'].dt.year
            age.plot.hist(x='Age (Years)', y='Voter Turnout', ax=ax, legend=0, clip_on=0, 
                          facecolor='#925A92', edgecolor='black', bins=20)
            ax.set_title(item[0], fontsize=14, fontweight='bold', **hfont)
            ax.tick_params(
                which='both',
                bottom='off',
                left='off',
                right='off',
                top='off'
            )
            #ax.grid(linewidth=0.25) # Option to add gridlines
            ax.set_xlim((0, 120))
            ax.set_xlabel('Age (Years)', fontsize=12)
            ax.set_ylabel('Voter Turnout', fontsize=12)
            ax.set_xticks(range(0, 120, 20))
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            legend = 'voters: ' + str(len(age))
            blue_patch = mpatches.Patch(label=legend, facecolor='#925A92', edgecolor='black')
            ax.legend(handles=[blue_patch])

        except TypeError:
            return item[0] + ' election has no data'


def convert_party_to_int(voter_history):
    ''' 
    Convert ballot_party from string to int.
    '''
    if voter_history.ballot_party == 'republican':
        return 1
    elif voter_history.ballot_party == 'democrat':
        return -1
    else:
        return 0


def approximate_affiliation(voter_file):
    '''
    Convert the summed party int values to an approximate party affiliation. 

    This function approximates voter affiliation by taking a sum (using the grouby
    in the segments_table function) of past votes for each voter where a vote in republican 
    primary is +1 and a vote in democrat primary is -1.  So if a voter voted in the 2012 
    primary as republican, 2014 primary as democrat, and 2016 primary as republican, the sum
    total would equal 1 - 1 + 1 = 1 = weak_republican. Note: if a voter only voted in general
    elections, they will be counted as a swing voter because there is no data 
    available to determine their party affiliation.  This may be a fair assumption but requires
    deeper analysis, like comparing approximate affiliation with number of times the voter voted.
    '''
    if voter_file.ballot_party_int > 1:
        return 'strong_republican'
    elif voter_file.ballot_party_int == 1:
        return 'weak_republican'
    elif voter_file.ballot_party_int == 0:
        return 'swing'
    elif voter_file.ballot_party_int == -1:
        return 'weak_democrat'
    elif voter_file.ballot_party_int < -1:
        return 'strong_democrat'
    else:
        return 'non_voter'


def party_to_voter_file(voter_file, voter_history):
    '''
    Approximate party affiliation for each voter based on primary ballots pulled
    and merge this data into the voter_file dataframe.
    '''
    voter_history['ballot_party_int'] = voter_history.apply(convert_party_to_int, axis=1) # Convert primary ballot to integer depending on party
    voter_history_summed = voter_history.groupby(['signup_id'], 
                                                 as_index=True)['ballot_party_int'].agg('sum') # Sum the integers to approximate party affiliation
    voter_file = pd.merge(voter_file, pd.DataFrame(voter_history_summed), 
                          how = 'left',left_index=True, right_index=True) # Merge party affiliation integer into voter file
    voter_file['party_affiliation'] = voter_file.apply(approximate_affiliation, axis=1) # Convert party affiliation integer to string

    return voter_file, voter_history


def output_segment_CSVs(voter_file, voter_history, base_file_path):
    '''
    Output each voter demographic segment as a unique CSV file.
    '''
    breakpoints = [18,25,35,45,55,65,150] # Define age brackets
    file_path = base_file_path + 'Voter_Segments_' + datetime.today().strftime('%Y-%m-%d') + '/'
    directory = os.path.dirname(file_path)

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for group_name, df in voter_file[['sex','born_at','party_affiliation']].groupby(['sex',pd.cut(datetime.now().year \
                                        - voter_file.born_at.dt.year, bins=breakpoints, labels=['18 to 24','25 to 34', \
                                        '35 to 44','45 to 54','55 to 64','65+']), 'party_affiliation']):
        group_name = str(group_name) + '.csv'
        cols_to_use = df.columns.difference(voter_file.columns)
        df = pd.merge(df[cols_to_use],voter_file, how = 'left',left_index=True, right_index=True)
        df.to_csv(file_path + group_name)

    return print('Congratulations! The voter segment CSV files are saved to the base filepath you specified earlier.')


def segments_table(voter_file, voter_history, base_file_path):
    '''
    Segment voter_file into useful voter audiences and output table.
    '''
    voter_file, voter_history = party_to_voter_file(voter_file, voter_history)
    
    file_path = base_file_path
    breakpoints = [18,25,35,45,55,65,150] # Define age brackets
   
    segments_with_party = voter_file[['sex','born_at','party_affiliation']].groupby(
        ['sex',pd.cut(datetime.now().year - voter_file.born_at.dt.year, 
        bins=breakpoints, labels=['18 to 24','25 to 34', 
                                  '35 to 44','45 to 54',
                                  '55 to 64','65+']), 
        'party_affiliation']).agg('count') # Segment by age, gender, adn party affiliation
    segments_with_party.columns = ['Number of Voters']
    segments_with_party.index.names = ['Gender', 'Age Range', 'Party Affiliation'] # Groupby has 3 indeces
    segments_with_party.to_csv(file_path + 'segments_table_with_party.csv',header=True, index=True)

    output_segment_CSVs(voter_file, voter_history, base_file_path)

    return segments_with_party


