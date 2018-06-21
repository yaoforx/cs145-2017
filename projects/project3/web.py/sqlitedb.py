import web

db = web.database(dbn='sqlite',
        db='data.db' #TODO: add your SQLite database filename
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    query_string = 'select * from CurrentTime'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    return results[0]['currentTime'] # TODO: update this as well to match the
                                  # column name

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from itemTable where itemId = $itemID'
    result = query(query_string, {'itemID': item_id})
    if len(result) > 0:
        return result[0]
    else:
        return None

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time

#Method: UPDATE current Time
def updateTime(time):

    query_string = 'UPDATE CurrentTime SET currentTime = $time'
    t = transaction()
    try:
        sqlitedb.query(query_string,{'time':time})
    except Exception as e:
        t.rollback()
        return (False,str(e))
    else: 
        t.commit()
        return (True,"Time changed successfully.")
def bidItem(itemID,userID,price):

    bidTime = getTime()
    query_string = 'INSERT INTO bidTable VALUES($userID,$itemID,$bidTime,$price)'
    t = transaction() 
    try:
        result = query(query_string,{'userID':userID,'itemID':itemID,'bidTime':time,'price':price})
    except Exception as e:
        t.rollback()
        return (False,str(e))
    else:
        t.commit()
    return result

def getAuction(itemID,userID,category,description,minPrice,maxPrice,status):

    query_string = "SELECT * from itemTable as i, priceTable as p, categoryTable as c,sellerTable as s WHERE i.itemId = p.itemId AND i.itemId = c.itemId AND i.itemId = s.itemId"
    
    def getStatus(status):
        time = getTime()
        if status == "open":
            return " AND priceStart <= '%s' AND priceEnd >= '%s'" % (time,time)
        elif status == "closed":
            return " AND priceEnd <= '%s'" % (time)
        elif status =="notStarted":
            return " AND priceStart >= '%s'" % (time)
        else:
            pass

    if itemID:
        query_string += " AND i.itemId = $itemID"
    if userID:
        query_string += " AND sellUserId = $userID"
    if category: 
        query_string += " AND category = $category"
    if description:
        query_string += " AND itemDescript LIKE $description"
    if minPrice:
        query_string += " AND priceCurrent >= $minPrice"
    if maxPrice:
        query_string += " AND priceCurrent <= $maxPrice"
    if status:
        query_string += getStatus(status)

    t = transaction() 
    try:
        result = query(query_string,{'itemID': itemID, 'userID': userID, 'minPrice': minPrice, 'maxPrice': maxPrice, 'category': category, 'description': "%" + description + "%"})

    except Exception as e:
        t.rollback()
        return (False,str(e))
    else:
        t.commit()
        return (True,result)

def getCategory(itemID):

    query_string = "SELECT category from categoryTable WHERE itemId = $itemID"
    t = transaction()
    try:
        result = query(query_string,{'itemID': itemID})
    except Exception as e:
        t.rollback()
        return (False,str(e))
    else:
        t.commit()
        return (True,result)

def getPriceById(itemID):

    query_string = "SELECT * from priceTable WHERE itemId = $itemID"
    return query(query_string,{'itemID': itemID})

def getStatus(itemID):

    current = getTime()
    status = "open"
    s = getPriceById(itemID)


    if s[0]['priceStart'] > current:
        status = "notStarted"
    if s[0]['priceStart'] <  current:
        status =  "closed"
        if getBidder(itemID) != "No bids":
            status += " Winning Bid : %s" % (getBidder(itemID)[0].bidUserId)
   
    return status

def getBidder(itemID):

    query_string = "SELECT * from bidTable WHERE itemId = $itemID"
    result = query(query_string,{'itemID': itemID})
    if len(result) > 0:
        return result
    else:
        result = "No bids"
    return result
def getSeller(itemID):

    query_string = "SELECT u.userId, u.userRating,u.userLocation,u.userCountry from sellerTable s,userTable u WHERE s.sellUserId = u.userId AND s.itemId = $itemID"
    return query(query_string,{'itemID': itemID})

def getInfo(itemID):
    
    item_info = getItemById(itemID)
    bidder = getBidder(itemID)
    status = getStatus(itemID)
    category = getCategory(itemID)

   

    return (item_info,bidder,status,category) 












