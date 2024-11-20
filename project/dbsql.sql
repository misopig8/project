--테이블을 생ㅇ성하기 위한 SQL
-- create table user(
--     userid integer primary key autoincrement, 
--     username text not null, 
--     password text not null,
--     station_number text not null,
--     create_at timestamp default create_timestamp
-- );

drop table user 
create table user(
    userid integer primary key autoincrement, 
    username text not null, 
    password text not null,
    station_number text not null,
    create_at timestamp default CURRENT_TIMESTAMP
);
