 drop table if exists portfolio;
    create table portfolio (
    sym text PRIMARY KEY not null,
    amount integer not null
);
