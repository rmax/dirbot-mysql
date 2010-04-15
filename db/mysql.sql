drop table if exists googledir;
create table sites (
    id int(11) not null auto_increment,
    name varchar(100) not null,
    url varchar(500) not null,
    description text,
    created int(11) not null comment "unix timestamp",
    primary key (id),
    key (url)
) engine=innodb default charset=utf8;
