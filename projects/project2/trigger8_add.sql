--description : implement for constraints 8 current price match amount
PRAGMA foreign_keys = ON;
drop trigger if exists matchAmount;
create trigger matchAmount
after insert on bidTable
for each row
when exists (
	select * from
	priceTable
	where priceTable.itemId = new.itemId
	and priceTable.priceCurrent <> new.Amount

)
begin
	update priceTable set priceCurrent = new.Amount
	where priceTable.itemId = new.itemId;
end;
	 
