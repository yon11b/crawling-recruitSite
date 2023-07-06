create table nation(
	nation_id integer auto_increment,
	nation_name varchar(100),

	primary key(nation_id)
);

create table tech_stack(
	tech_id integer auto_increment,
	tech_name varchar(100),

	primary key(tech_id)
);

create table recruit_post(
	recruit_id integer auto_increment,
	nation_id integer not null,
	company_name integer not null,
	company_city varchar(100),
	description_title varchar(255) not null,
	description_content varchar(255) not null,
	company_apply_link varchar(255) not null,
	posted_date datetime not null,
	is_visa_sponsored tinyint(1) default 0,
	is_remoted tinyint(1) default 0,
	remote_location varchar(100),
	company_logo mediumblob,
	salary varchar(100),
	contract_form varchar(100),
	company_page_link varchar(255),
	writer varchar(100),
	origin varchar(255) not null,
	tag varchar(255),
	location varchar(255) not null,
	is_dev tinyint(1) default 1,
	created_at datetime default now() not null,
	created_by varchar(100) not null,
	updated_at datetime on update now(),
	updated_by varchar(100),

	primary key(recruit_id),
	foreign key(nation_id) references nation(nation_id) on update cascade on delete no action
);

create table description_tech(
	tech_id integer auto_increment,
	recruit_id integer,

	primary key(tech_id,recruit_id),
	foreign key (tech_id) references tech_stack(tech_id) on update cascade on delete cascade,
	foreign key (recruit_id) references recruit_post(recruit_id) on update cascade on delete cascade
);