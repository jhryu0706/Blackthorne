#first make sure that the file type is csv
#make sure to delete and recreate file name 'data' before using functions
import os
import pandas as pd



def clean(file):
        """
        input (string): dataset that you want to clean and use for analysis
        output (None)
        """
        x = os.listdir(file)[0]
        type = 'csv'
        for filename in os.listdir(file):
            if filename == '.DS_Store':
                     os.rmdir(file+"/"+filename)
            old_path = os.path.join(file, filename)
            x = filename.split('_')
            os.rename(old_path,'data/'+x[2])
        return type
    