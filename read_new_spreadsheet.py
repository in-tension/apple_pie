
import pandas as pd
import brutils as br
import numpy as np

CELL_IDFYIER = 'Track ID'
def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', 20)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')

def read_new_spreadsheet(spreadsheet_path) :
    df = pd.read_csv(spreadsheet_path)

    cell_ids = set(df[CELL_IDFYIER])
    cell_data = {}
    for cell_id in cell_ids :
        cell_data[cell_id] = df[df[CELL_IDFYIER] == cell_id]
        print_full(cell_data[cell_id].iloc[:,[5,4,1,2,6]])
    # print(cells)
    print(df.columns)
    return df,cell_data
    # print(df)
    # cells  = {}
    # for index, row in df.iterrows():
    #     # if row
    #     if row[CELL_IDFYIER] in cells :
    #         cells[row[CELL_IDFYIER]].append(row)
    #     else :
    #         cells[row[CELL_IDFYIER]] = row
    #     #print(row['Track ID'])
    # # print(df.columns)
    # print(br.one_key(cells))

example_file = '/Volumes/baylieslab/Current Lab Members/Whitney/Rhabdo Project/Tissue Culture/Timelapse/Rhabdomyosarcoma plate movies/Post-mycoplasma data (starting 9:18:18)/RH30/18-11-07.rht/Csv/B02.csv'

cdf, cell_data = read_new_spreadsheet(example_file)

import seaborn as sns
sns.set(style="darkgrid")



c_id = 'Cell ID'
x = 'x(Pixel Position)'
y = 'y(Pixel Position)'
area = 'Area(pixels^2)'
frame = 'Time(Frame Num)'
t_id = 'Track ID'
death = 'Label'


# Load an example dataset with long-form data
fmri = sns.load_dataset("fmri")

# Plot the responses for different events and regions
sns.lineplot(x="timepoint", y="signal",
             hue="region", style="event",
             data=fmri)
# Load an example dataset with lhong-form data
# fmri = sns.load_dataset("fmri")

# Plot the responses for different events and regions
cdf['region'] ='parietal'
cdf['event'] ='stim'

distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

temp_col = [None]
# for index, row in cdf.iterrows():
row_count = cdf.shape()[0]

for r in row_count

sns.lineplot(x=frame, y='y(Pixel Position)',
             hue="region", style="event",
             data=cdf)

