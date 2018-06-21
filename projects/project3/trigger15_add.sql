--description : implement for constrain 15 bid time matches AuctionBase system
PRAGMA foreign_keys = ON;
drop trigger if exists timeMatch;
create trigger timeMatch
before insert on bidTable
for each row
when exists (
	select *
	from CurrentTime
	where CurrentTime.currentTime <> new.bidTime
	
)
begin 
	select raise(rollback,'Newly created bid does not match system time');
end;

