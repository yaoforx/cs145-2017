--description : implement for constrain 16 time only increase
PRAGMA foreign_keys = ON;
drop trigger if exists timeForward;
create trigger timeForward
before update on CurrentTime
for each row
when exists (
	select * from 
	CurrentTime
	where currentTime >=new.currentTime
	
)
begin
	select raise(rollback,'Time can only increase');
end;
