--description : implement for constrain 13 to match number of bids
PRAGMA foreign_keys = ON;
drop trigger if exists incrementBids;
create trigger incrementBids
after insert on bidTable
for each row
when exists (
	select * from
	priceTable
	where priceTable.itemId = new.itemId
)
begin
	update priceTable set priceNumberBid = priceNumberBid + 1
	where priceTable.itemId = new.itemId;
end;
