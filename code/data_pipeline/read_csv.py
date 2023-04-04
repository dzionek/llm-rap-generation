import pandas as pd
import numpy as np
from lyrics_cleaner import LyricsCleaner
import re


class CsvToDataFrame:
    def __init__(self, file_path):
        self.file_path = file_path

    def remove_empty_strings(self, lst):
        return [x for x in lst if x != '']

    def clean_string(self, input_string):
        # Make string lowercase
        input_string = input_string.lower()

        #remove anything in brackets
        input_string = re.sub(r'\([^()]*\)', '', input_string)

        # Remove non-alphanumeric characters
        cleaned_string = re.sub(r'[^\w\s]', '', input_string)

        

        return cleaned_string
        
    def add_next_lyric_column(self, df):
        df['next lyric'] = df.groupby(['artist', 'song'])['lyric'].shift(-1)
    
        return df
    
    def create_cleaned_df(self):
        df = pd.read_csv(self.file_path, error_bad_lines=False)
        for k in range(len(df.index)):
            LC = LyricsCleaner(str(df['lyrics'].iloc[k]))
            df['lyrics'].iloc[k] = self.remove_empty_strings(self.clean_string(LC.clean()).split('\n'))
            
        df = df.explode('lyrics')
        df = df.rename(columns = {'lyrics': 'lyric'})
        
        df = self.add_next_lyric_column(df)
        df = df.dropna(subset=['next lyric'])
        
        
        return df
            
   
CSV = CsvToDataFrame('data.csv')
df = CSV.create_cleaned_df()
df.to_csv('updated_rappers.csv')

