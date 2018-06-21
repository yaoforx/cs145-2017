--description: implement for constain 11 cannot bid before start or after end
PRAGMA foreign_keys = ON;
drop trigger if exists bidTimeConstrain;
create trigger bidTimeConstrain
before insert on bidTable
for each row
when exists(
	select * from
	priceTable
	where priceTable.priceStart > new.bidTime or
	priceTable.priceEnd < new.bidTime

)
begin
	select raise(rollback,'Cannot bid item due to time constrain');
end;
