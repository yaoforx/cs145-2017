--description : implement for constarin 14 bid amount can only increase
PRAGMA foreign_keys = ON;
drop trigger if exists amountIncrease;
create trigger amountIncrease
before insert on bidTable
for each row
when exists(
	select *
	from priceTable
	where priceTable.priceCurrent >= new.bidAmount and
	priceTable.itemId = new.itemId
)
begin
	select raise(rollback, 'cannot bid item with bid price lower than current');
end;

