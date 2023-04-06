#first make sure that the file type is csv
import os
for filename in os.listdir('new_data'):
    old_path = os.path.join('new_data', filename)
    x = filename.split('_')
    os.rename(old_path,'data/'+x[2])