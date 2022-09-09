drop table if exists ttwlrefs;
drop table if exists ttwlobject;

create table ttwlobject
(
    id int not null auto_increment,
    name varchar(512) character set latin1 not null,
    primary key (id),
    unique index idx_name (name)
) engine=innodb;

create table ttwlrefs
(
    from_obj int not null,
    to_obj int not null,
    unique index idx_from (from_obj, to_obj),
    index idx_to (to_obj, from_obj)
) engine=innodb;

