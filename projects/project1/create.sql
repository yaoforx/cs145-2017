drop table if exists itemTable;
create table itemTable (
	itemId integer primary key,
	itemName text,
	itemDescript text,
	foreign key (itemId) references categoryTable(itemId),
	foreign key (itemId) references priceTable(itemId)

	foreign key (itemId) references sellerTable
);
drop table if exists priceTable;
create table priceTable (
	itemId integer primary key,
	priceStart text,
	priceEnd text,
	priceFirstBid real,
	priceCurrent real,
	priceNumberBit integer,
	Buy_Price real,
);
drop table if exists bidTable;
create table bidTable (
	bidUserId text primary key,
	bidTime text,
	bidAmount real,
	foreign key (bidUserId) references userTable(userId)
);

drop table if exists categoryTable;
create table categoryTable (
	randomId float primary key,
	itemId integer,
	category text
);

drop table if exists sellerTable;
create table sellerTable (
	itemId integer primary key,
	sellUserId text,
	foreign key (sellUserId) references userTable(userId)

);

drop table if exists userTable;
create table userTable (
	userId text primary key,
	userRating integer,
	userLocation text,
	userCountry text
	
);
