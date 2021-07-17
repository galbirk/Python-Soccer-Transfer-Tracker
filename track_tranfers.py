from operator import itemgetter
import requests
import xlsxwriter as xw
import win32api
import win32print
import argparse

data_for_excel = []
API_URL = "https://interactive.guim.co.uk/docsdata/1stnMrwQdpXwNubJelzAZDmzw9QqJhHJJ1mrjs3Bt9hQ.json"

def windows_print(filename):
    win32api.ShellExecute (
    0,
    "print",
    filename,
    #
    # If this is None, the default printer will
    # be used anyway.
    #
    '/d:"%s"' % win32print.GetDefaultPrinter (),
    ".",
    0
    )

def sort_data(data,sortBy):
    sortBy = sortBy.lower()
    return sorted(data, key=lambda k: k[sortBy]) 

# Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument('-d','--destinaton',dest='dest',help="Path to execl file to be saved.",default=r"transfer.xlsx")
parser.add_argument('-s','--sort',dest='sortBy',help="Sort the excel by: name, nation, preLeague, newLeague, preClub, newClub",default='newClub')
parser.add_argument('-p','--print',dest='toPrint',help="Add flag if you want to print the excel sheet.")
args = parser.parse_args()

# Get Data from API
res = requests.get(API_URL)
res = res.json()
transfers_list = res['sheets']['Transfers']

# Prepare Data for Excel
for transfer in transfers_list:
    data_for_excel.append({'name':transfer["Player name"],'nation':transfer["Nationality"],'pos':transfer["Primary player position"]
                            ,'preLeague':transfer["What was the previous league?"],'newLeague':transfer["What is the new league?"]
                            ,'preClub':transfer["What was the previous club?"],'newClub':transfer["What is the new club?"]})

# Sort Data
data_for_excel = sort_data(data_for_excel,args.sortBy)

# Create Excel Workbook
workbook = xw.Workbook(args.dest)

# Create Worksheet
worksheet = workbook.add_worksheet('Transfers 2021-2022')
bold = workbook.add_format({'bold': True})

worksheet.write('A1', 'Player Name',bold)
worksheet.write('B1', 'Nationality',bold)
worksheet.write('C1', 'Primary player position',bold)
worksheet.write('D1', 'Previous League',bold)
worksheet.write('E1', 'Previous Club',bold)
worksheet.write('F1', 'New League',bold)
worksheet.write('G1', 'New Club',bold)

start_row = 1
start_col = 0

# Add data to worksheet
for transfer in tuple(data_for_excel):
    col = start_col
    for attr in transfer:
        worksheet.write(start_row,col,attr)
        col += 1
    start_row += 1

workbook.close()

# Check if to print the file
if args.toPrint:
    windows_print('tranfers.xlsx')