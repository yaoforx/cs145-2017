# CS 145 Project Part 3
# Hao Wu, Stephanie Tang

###Notice that we purposefully hide what we check###
###The script just contains all the queries we will call to your server###


# Some people didn't create a web.py folder - attempt to do this for them
#if [ ! -d "web.py" ]; then
#   echo "=== Creating web.py directory, as they were missing it ==="
#   mkdir web.py
#   cp -r $(ls | grep -Ev 'web.py|GRADING|.sql|.sh') web.py/
#fi

#echo "===================== Running Parser ====================="
#chmod +x runParser.sh
#./runParser.sh > /dev/null

#echo "=================== Creating Database ===================="
#chmod +x createDatabase.sh
#./createDatabase.sh

# Move database into web.py
#mv *.db web.py/

# Make auctionbase.py executable
#chmod +x web.py/auctionbase.py

# Turn on debug mode
#touch web.py/.suexecd

# Cleanup
#rm -f *.dat

#echo "http://web.stanford.edu/~$USER/cgi-bin/Part3/${PWD##*/}/web.py/auctionbase.py/selecttime"

# Run the server
python auctionbase.py 14500 &
sleep 2s


# function to check list of results, resArray is the result of the students
# our_res is the correct result
checkListOfResults(){
    # check if found same number of items

    ###Notice that we purposefully hide what we check###
    resArray=(`echo "$resArray"`)
    #echo "${#resArray[@]}"

    each_is_correct=true
    #check if each item is right
    for ((i = 0; i < ${#resArray[@]}; ++i)); do
        # bash arrays are 0-indexed, use nop to hide our checks
        :
    done
}


# Test view time
html=$(curl -s localhost:14500/currtime)
expected="2001-12-20 00:00:01"
#echo "$html"

# Test set time
# Move time forward
html=$(curl -s localhost:14500/selecttime?MM=12&dd=20&yyyy=2001&HH=00&mm=00&ss=02)
# Make sure no error message

# Then check the currtime again
html=$(curl -s localhost:14500/currtime)
expected="2001-12-20 00:00:02"
#echo "$html"

# Move time backward
# Check for error message (if not present, dock x points)
html=$(curl -s -d "MM=12&dd=20&yyyy=2001&HH=00&mm=00&ss=02&entername=bob" -X POST localhost:14500/selecttime)
# check error message
# Then check the currtime again to make sure it didn't go through
html=$(curl -s localhost:14500/currtime)
#echo "$html"


# Hao Wu, Nov 9, 2017

# Test search

html=$(curl -s -d "itemID=1043374545&category=&maxPrice=&minPrice=&status=&description=&userID=" -X POST localhost:14500/search)


html=$(curl -s -d "category=Collectibles&itemID=&maxPrice=&minPrice=&status=&description=&userID=" -X POST localhost:14500/search)
resArray=`echo "$html" | grep -Eo "view\?itemID=[0-9]+" | sed 's/view?itemID=//g' | sort | uniq`


html=$(curl -s -d "itemID=1043397459&userID=dollface94&category=&maxPrice=&minPrice=&status=&description=" -X POST localhost:14500/search)
resArray=`echo "$html" | grep -Eo "view\?itemID=[0-9]+" | sed 's/view?itemID=//g' | sort | uniq`


html=$(curl -s -d "maxPrice=99.99&category=&itemID=&minPrice=&status=&description=&userID=" -X POST localhost:14500/search)
resArray=`echo "$html" | grep -Eo "view\?itemID=[0-9]+" | sed 's/view?itemID=//g' | sort | uniq`


html=$(curl -s -d "minPrice=9.99&category=&itemID=&maxPrice=&status=&description=&userID=" -X POST localhost:14500/search)
resArray=`echo "$html" | grep -Eo "view\?itemID=[0-9]+" | sed 's/view?itemID=//g' | sort | uniq`

html=$(curl -s -d "status=open&category=&itemID=&maxPrice=&minPrice=&description=&userID=" -X POST localhost:14500/search)
resArray=`echo "$html" | grep -Eo "view\?itemID=[0-9]+" | sed 's/view?itemID=//g' | sort | uniq`
# only Items with ID 1048723305 and 1048723313 and 1044517180 should be returned

html=$(curl -s -d "description=Free%20Honesty%20Counters&&category=&itemID=&maxPrice=&minPrice=&status=&userID=" -X POST localhost:14500/search)
# %20 is the escape sequence for space, this should return item 1043562035
resArray=`echo "$html" | grep -Eo "view\?itemID=[0-9]+" | sed 's/view?itemID=//g' | sort | uniq`


# Test view
# view item 1044104207, check each attribute is correct
html=$(curl -s localhost:14500/view?itemID=1044104207)

# view item 1043402767, and the winning bid is made by: goldcoastvideo
html=$(curl -s localhost:14500/view?itemID=1043402767)

# Test automatic closing of auction by moving time
curl -s -d "MM=12&dd=21&yyyy=2001&HH=17&mm=59&ss=05&entername=bob" -X POST localhost:14500/selecttime > /dev/null
html=$(curl -s localhost:14500/view?itemID=1048723305)
# Make sure no error message

html=$(curl -s localhost:14500/view?itemID=1048723313)
# Make sure no error message

# close an auction by reaching Buy_price
html=$(curl -s localhost:14500/view?itemID=1044517180)
# Make sure no error message

# Test add bid
html=$(curl -s -d "itemID=1044517180&userID=Antonios&price=21.0" -X POST http://localhost:14500/add_bid)
# Make sure no error message

# Kill server
#kill $!

echo "Point total: $points"
