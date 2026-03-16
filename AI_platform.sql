-- one time usage only --
create database ai_platform_db;
-- USERS TABLE --------------------------------
use ai_platform_db;
create table users (
id int auto_increment primary key,
username varchar(50) unique not null,
email varchar(255) unique not null,
password_hash text not null,
is_active boolean default true,
created_at timestamp default current_timestamp,
UserInputID varchar(10) unique not  null,
UserOutputID varchar(10) unique not null
);
-- ----------------------------------------------

-- API KEYS TABLE -------------------------------
create table api_keys (
id int auto_increment primary key,
user_id int not null,
key_prefix varchar(10) not null,
key_hash text not null,
name varchar(50) ,
revoked boolean default false,
is_active boolean default true,
created_at timestamp default current_timestamp,
last_used timestamp,

constraint fk_api_keys_user
foreign key (user_id)
references users(id)
on delete cascade);
-- --------------------------------------------


-- RATE LIMITS TABLE --------------------------
create table rate_limits(
id int auto_increment primary key,
api_key_id int not null,
requests_per_minute int default 20,
requests_per_day int default 500,

constraint fk_rate_limit_key
foreign key (api_key_id)
references api_keys(id)
on delete cascade) ;
-- ---------------------------------------------

-- MODELS TABLE --------------------------------
create table models (
id int auto_increment primary key,
name varchar(50) unique not null,
provider varchar(50) not null,
version_model varchar(50),
max_tokens int,
created_at timestamp default current_timestamp);
-- ---------------------------------------------
-- REQUESTS TABLE --------------------------------
create table requests (
id int auto_increment primary key,
user_id int not null,
api_key_id int not null,
model_id int not null,
prompt text not null,
response text,
tokens_used int default 0,
status varchar(20),
created_at timestamp default current_timestamp,

constraint fk_requests_user
foreign key (user_id)
references users(id)
on delete cascade,

constraint fk_requests_key
foreign key (api_key_id)
references api_keys(id)
on delete cascade,

constraint fk_requests_model
foreign key (model_id)
references models(id));
-- ------------------------------------------

-- USAGE TABLE -----------------------------
create table usage_stats (
id int auto_increment primary key,
user_id int not null,
date date not null,
requests_count int default 0,
tokens_used int default 0,

constraint fk_usage_user
foreign key (user_id)
references users(id)
on delete cascade);
-- -----------------------------------------

-- INDEXES ---------------------------------
create index idx_api_keys_user on api_keys(user_id);
create index idx_requests_user on requests(user_id);
create index idx_requests_model on requests(model_id);
create index idx_usage_user on usage_stats(user_id);

-- -----------------------------------------