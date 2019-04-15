
import pandas as pd
import brutils as br

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
    cells = {}
    for cell_id in cell_ids :
        cells[cell_id] = df[df[CELL_IDFYIER] == cell_id]
        print_full(cells[cell_id].iloc[:,[5,4,1,2,6]])
    # print(cells)
    print(df.columns)
    return cells
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

cells = read_new_spreadsheet(example_file)

