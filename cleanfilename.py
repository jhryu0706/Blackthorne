# #first make sure that the file type is csv
# import os

# x = input("enter file to process and file type separated by space ex)new_data xlsx")
# def set_var():
# if x == None:
#     name = 'data'
#     filetype = 'xlsx'
# else:
#     x = x.split(' ')
#     name = x[0]
#     filetype = x[1]

# def help_set_var():
#     if filetype == 'excel' or 'xlsx':
#         filetype = 1
#     elif filetype == 'csv':
#         filetype = 2
#     else:
#         print("This code only takes excel or csv filetype as input")
#         return None
# set_var()

# dict = {}
# for files in os.listdir(name):
#     #creates a dictionary with key:commodity name, value:df
#     if filetype == 1:
#         dict[files] = pd.read_excel(name+'/'+files)
#     elif filetype == 2:
#         dict[files] = pd.read_csv(name+'/'+files)

# def clean():
#     for filename in os.listdir('new_data'):
#         old_path = os.path.join('new_data', filename)
#         x = filename.split('_')
#         os.rename(old_path,'data/'+x[2])