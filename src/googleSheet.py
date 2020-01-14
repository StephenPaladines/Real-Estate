import gspread
import json
import time
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


def writeToData(list):
    if(len(dict) > 0):
        with open('data/cacheID.json', 'w') as output:
            json.dump(list, output, indent=4)     # Convert list into JSON

# Prints a new cache file if database is not empty


def createNewCache(sheet):
    dbCache = {}
    mlsRange = sheet.col_values(1)
    priceRange = sheet.col_values(5)
    for index in range(1, len(mlsRange)):
        dbCache[mlsRange[index]] = priceRange[index]
    return dbCache


def updatePrice(sheet, house):
    cell = sheet.find(house['mlsID'])
    sheet.update_cell(cell.row, 5, house['price'])
    fmt = CellFormat(
        backgroundColor=Color(0.90, 0.00, 0.00),    # Red
        textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0))
    )
    format_cell_range(sheet, ('A' + str(cell.row) +
                              ':' + 'W' + str(cell.row)), fmt)


def addDataToGS(list):
    try:
        # GS = Google Sheet
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'creds.json', scope)
        client = gspread.authorize(credentials)
        sheet = client.open("House-Listing").sheet1
        houseID = sheet.col_values(1)  # 0(n) time complexity
        rowCount = (len(houseID))  # 0(n) time complexity
        cacheMLSID = createNewCache(sheet)
        for house in list:  # 0(m) time complexity
            if(cacheMLSID.get(house['mlsID'], -1) == -1):
                insertRow = [house['mlsID'], house['address'],
                             house['bodyDesc'], house['year'], house['price'], house['totalArea']]
                sheet.insert_row(insertRow, rowCount+1)
                orginalCell = sheet.find(house['mlsID'])
                sheet.update_cell(orginalCell.row, 10, house['price'])
                time.sleep(2)
                rowCount += 1
            else:
                orginalCell = sheet.find(house['mlsID'])
                orginalCell = sheet.acell('J' + str(orginalCell.row)).value
                if(int(orginalCell) != house['price']):
                    updatePrice(
                        sheet, {'mlsID': house['mlsID'], 'price': house['price']})

    except Exception as err:
        print(err)


# # Test Code
# addDataToGS([
#     {
#         "mlsID": 'X10196052',
#         "address": 'address',
#         "bodyDesc": 'bodyDesc',
#         "price": 123256,
#         "totalArea": 'totalArea',
#         "year": 'year'
#     }
# ])
