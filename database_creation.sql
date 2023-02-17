drop database if exists mybasket;
create database MyBasket;
use MyBasket;
-- drop table if exists customer;
-- drop table if exists retailer;
-- drop table if exists address;
-- drop table if exists product;
-- drop table if exists category;
-- drop table if exists cart;
-- drop table if exists customer;
-- drop table if exists payment;
-- drop table if exists order;
-- drop table if exists deliveryboy;

create table customer(
	cid INT NOT NULL AUTO_INCREMENT unique,
	fname varchar(255) NOT NULL,
	mname varchar(255),
	lname varchar(255),
	email varchar(255) NOT NULL unique,
	password varchar(255) NOT NULL,
	number varchar(20) NOT NULL unique,
	PRIMARY KEY (cid)
);
-- SET SQL_SAFE_UPDATES=0;
-- delete from customer;
-- SET SQL_SAFE_UPDATES=1;

create table Retailer(
	rid INT NOT NULL AUTO_INCREMENT unique,
	fname varchar(255) NOT NULL,
	mname varchar(255),
	lname varchar(255),
	email varchar(255) NOT NULL unique,
	password varchar(255) NOT NULL,
	number varchar(20) NOT NULL unique,
	PRIMARY KEY (rid)
);
create table Address(
	aid INT NOT NULL AUTO_INCREMENT unique,
    cid INT NOT NULL,
	locality varchar(255) NOT NULL,
    pincode varchar(255) NOT NULL,
    state varchar(255) NOT NULL,
    city varchar(255) NOT NULL,
    PRIMARY KEY (aid),
    FOREIGN KEY (cid) REFERENCES customer(cid) ON UPDATE CASCADE ON DELETE CASCADE
);
create table category(
	catid int NOT NULL AUTO_INCREMENT unique,
    name VARCHAR(255) NOT NULL,
    primary key (catid)
);
create table Product(
	name varchar(255) NOT NULL,
	pid INT NOT NULL AUTO_INCREMENT unique,
    catid INT NOT NULL,
    rid INT NOT NULL,
    manufacturingDate varchar(255) NOT NULL,
    rating smallint NOT NULL default 0, 
    quantity int NOT NULL ,
    price int NOT NULL,
    PRIMARY KEY (pid),
    FOREIGN KEY (rid) REFERENCES Retailer(rid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (catid) REFERENCES category(catid) ON UPDATE CASCADE ON DELETE CASCADE,
	check (rating<=5),
    check(rating>=0),
    check (price>=0),
    check(quantity>=0)
);
create table Admin(
	fname varchar(255) NOT NULL,
	mname varchar(255),
	lname varchar(255),
	email varchar(255) NOT NULL unique,
	password varchar(255) NOT NULL,
    PRIMARY KEY(email,password)
);
create table payment(
	modeofpayment varchar (255) NOT NULL,
    aid int NOT NULL,
    payid int NOT NULL AUTO_INCREMENT unique,
    PRIMARY KEY (payid),
    FOREIGN KEY (aid) REFERENCES address(aid) ON UPDATE CASCADE ON DELETE CASCADE
);
create table cart(
	quantity int NOT NULL,
    price int NOT NULL,
    pid int NOT NULL,
    cid int NOT NULL,
    status varchar(255) default 'not delivered',
    FOREIGN KEY (pid) REFERENCES product(pid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (cid) REFERENCES customer(cid) ON UPDATE CASCADE ON DELETE CASCADE
);
create table orderdetails(
    orderdate date NOT NULL,
    payid int not null,
    FOREIGN KEY (payid) REFERENCES payment(payid) ON UPDATE CASCADE ON DELETE CASCADE
);
create table  deliveryboy(
	name varchar (255) NOT NULL,
    age int NOT NULL,
    rating smallint NOT NULL default 0,
    did int NOT NULL AUTO_INCREMENT unique,
    PRIMARY KEY (did),
    check(age>=18),
    check (rating<=5),
    check(rating>=0)
    
);
create table makepayment(
	payid int not null,
	cid int not null,
    pid int not null,
    FOREIGN KEY (pid) REFERENCES product(pid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (cid) REFERENCES customer(cid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (payid) REFERENCES payment(payid) ON UPDATE CASCADE ON DELETE CASCADE
);
create table delivery(
	payid int not null,
	did int not null,
    FOREIGN KEY (did) REFERENCES deliveryboy(did) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (payid) REFERENCES payment(payid) ON UPDATE CASCADE ON DELETE CASCADE
);
create table department(
    depid int not null unique, 
    name varchar(255) not null,
    dephead varchar(255) not null,
    primary key (depid)
);
