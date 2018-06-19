--description : implement for constrain 9 cannot bid item oneself is selling
PRAGMA forein_keys = ON;
drop trigger if exists preventBidSelf;
create trigger preventBidSelf
after insert on bidTable
for each row
when exists (
	select * from
	sellerTable
	where sellUserId = new.bidUserId
	and itemId = new.itemId
)
begin
	select raise(rollback,'Cannot bid item that selling by self');
end;

