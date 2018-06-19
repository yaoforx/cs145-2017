
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub
import random
# import reprlib

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        itemTable = ""
        sellerTable = ""
        priceTable = ""
        userTable = ""
        bidTable = ""
        categoryTable = ""
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            itemId = item["ItemID"]
            itemName = item["Name"] 
            itemName = "\"" + itemName.replace("\"","\"\"") + "\""
            if item["Description"] is not None :
                itemDescript = item["Description"]
                itemDescript = "\"" + itemDescript.replace( "\"", "\"\"" ) + "\""
            else:
                itemDescript = "None"


            sellUserId = item["Seller"]["UserID"]
            sellUserId = "\"" + sellUserId.replace("\"","\"\"") + "\""
            sellUserRating = item[ "Seller" ][ "Rating"]
            sellUserLocation = item["Location"]
            sellUserLocation = "\"" +  sellUserLocation.replace("\"","\"\"") + "\""
            sellUserCountry = item["Country"]
            sellUserCountry = "\"" +  sellUserCountry.replace("\"","\"\"") + "\""
             

            priceStart = transformDttm( item[ "Started" ] )
            priceStart = "\"" + priceStart.replace( "\"", "\"\"" ) + "\""
            priceEnd = transformDttm( item[ "Ends" ] )
            priceEnd = "\"" + priceEnd.replace( "\"", "\"\"" ) + "\""
            priceFirstBid = transformDollar( item[ "First_Bid" ] )
            priceCurrent = transformDollar( item[ "Currently" ] )
            priceNumberBid = item[ "Number_of_Bids"]
            
            itemTable += itemId + columnSeparator + itemName + columnSeparator + itemDescript + "\n"
            sellerTable += itemId + columnSeparator + sellUserId + "\n"
            
            if "Buy_Price" in item:
                Buy_Price = transformDollar( item[ "Buy_Price" ])
            else:
                Buy_Price = "None"

            priceTable += itemId + columnSeparator + priceStart + columnSeparator + priceEnd + columnSeparator +priceFirstBid +  \
            columnSeparator +priceCurrent + columnSeparator + priceNumberBid + columnSeparator + Buy_Price + "\n"
            userTable += sellUserId + columnSeparator + sellUserRating + columnSeparator\
                    + sellUserLocation + columnSeparator + sellUserCountry + "\n"

            for category in item["Category"]:

                categoryTable += itemId + columnSeparator + category + "\n"


            if item["Bids"] is not None:
                for bid in item["Bids"]:
                    bidUserId = bid[ "Bid" ][ "Bidder" ][ "UserID" ]
                    bidRating = bid[ "Bid" ][ "Bidder" ][ "Rating" ]
                    bidUserId = "\"" + bidUserId.replace( "\"", "\"\"" ) + "\""
                    bidTime = transformDttm( bid[ "Bid" ][ "Time" ] )
                    bidAmount = transformDollar( bid[ "Bid" ][ "Amount" ])
                    if "Location" in bid[ "Bid" ][ "Bidder" ]:
                        bidLocation = bid[ "Bid" ][ "Bidder" ][ "Location" ]
                        bidLocation = "\"" + bidLocation.replace( "\"", "\"\"" ) + "\""
                    else:
                        bidLocation = "None"

                    if "Country" in bid[ "Bid" ][ "Bidder" ]:
                        bidCountry = bid[ "Bid" ][ "Bidder" ][ "Country" ]
                        bidCountry = "\"" + bidCountry.replace( "\"", "\"\"" ) + "\""
                    else:
                        bidCountry = "None"

                    bidTable += bidUserId +  columnSeparator + itemId + columnSeparator + bidTime \
                    + columnSeparator + bidAmount +  "\n"
                    
                    userTable += bidUserId + columnSeparator + bidRating + columnSeparator\
                    + bidLocation + columnSeparator + bidCountry + "\n"


            
        file_item = open("itemTable.dat","a")
        file_item.write(itemTable + "\n")
        file_item.close()

        file_seller = open("sellerTable.dat","a")
        file_seller.write(sellerTable + "\n")
        file_seller.close()

        file_price = open("priceTable.dat","a")
        file_price.write(priceTable + "\n")
        file_price.close()

        file_user = open("userTable.dat","a")
        file_user.write(userTable + "\n")
        file_user.close()

        file_bid = open("bidTable.dat","a")
        file_bid.write(bidTable + "\n")
        file_bid.close

        file_category = open("categoryTable.dat","a")
        file_category.write(categoryTable + "\n")
        file_category.close()

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
