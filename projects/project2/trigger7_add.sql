--descripition : implement for constrain 7 end_time before start_time

PRAGMA foreign_keys = ON;
drop trigger if exists endBeforeStart;
create trigger endBeforeStart
after insert ON priceTable
for each row
when exists (
	select * from
	priceTable
	where priceTable.itemId  = new.itemId and priceStart >= priceEnd
)
begin
	select raise(rollback, 'Auction StartTime Can not after EndTime');
end;
