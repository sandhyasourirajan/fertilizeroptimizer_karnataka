drop table if exists micronutrient_ref_tbl;

create table micronutrient_ref_tbl(
		ref_id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_name varchar(30),
        irrigation_type_code varchar(10),
        N_per_hectare int,
        P_per_hectare int,
        K_per_hectare int,
        S_per_hectare int
);

select sqlite_version();

create unique index micronutrient_idx on micronutrient_ref_tbl(crop_name,irrigation_type_code);

insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Paddy','Irrigated',100,75,75);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Paddy','Rainfed',100,75,75);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('DSR Paddy','Rainfed',100,50,50);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Sorghum','Irrigated',100,75,40);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Sorghum','Rainfed',50,25,0);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Maize','Irrigated',150,75,38);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Green gram','Irrigated',25,50,0);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Green gram','Rainfed',25,50,0);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Chilli','Irrigated',150,75,75);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Chilli','Rainfed',100,50,50);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Cotton','Irrigated',80,40,40);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Cotton','Rainfed',30,15,15);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Redgram','Irrigated',25,50,0);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Redgram','Rainfed',25,50,0);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Bengalgram','Irrigated',25,50,0);
insert into micronutrient_ref_tbl (crop_name, irrigation_type_code, N_per_hectare, P_per_hectare, K_per_hectare) values ('Bengalgram','Rainfed',25,50,0);

select * from micronutrient_ref_tbl;