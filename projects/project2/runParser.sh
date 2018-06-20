

rm ./data.db

python skeleton_parser.py ~/cs145-2017/project/ebay_data/items-*.json

sort -u bidTable.dat | sed '/^ *$/d' > bid.dat

sort -u categoryTable.dat | sed '/^ *$/d'> category.dat

sort -u itemTable.dat | sed '/^ *$/d' > item.dat

sort -u priceTable.dat | sed '/^ *$/d' > price.dat

sort -u sellerTable.dat | sed '/^ *$/d' > seller.dat

sort -u userTable.dat | sed '/^ *$/d' > user.dat



