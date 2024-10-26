--테이블을 생ㅇ성하기 위한 SQL
-- create table user(
--     userid integer primary key autoincrement, 
--     username text not null, 
--     password text not null,
--     email text not null,
--     gender text check(gender in ('male', 'female')),
--     create_at timestamp default create_timestamp
-- );
--데이터 삽입하기 위한 SQL
--INSERT into user(username,password,email,gender)
--VALUES('test','123','tese@gmail.com'


create table user(
    userid integer primary key autoincrement, 
    username text not null, 
    password text not null,
    email text not null,
    gender text check(gender in ('male', 'female')),
    create_at timestamp default CURRENT_TIMESTAMP
);
