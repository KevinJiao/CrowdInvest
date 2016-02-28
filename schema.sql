 drop table if exists portfolio;
    create table portfolio (
    sym text PRIMARY KEY not null,
    amount integer not null
);
drop table if exists orders;
create table orders (
        ID INTEGER PRIMARY KEY,
        trade TEXT not null
);
INSERT into portfolio VALUES('funds', 1000000);
