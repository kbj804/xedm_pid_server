-- Drop table

-- DROP TABLE public.files;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;



-- Drop table

-- DROP TABLE public.train;

CREATE TABLE public.train (
	id serial NOT NULL,
	reg_count int4 NULL DEFAULT 0,
	column1 int4 NULL DEFAULT 0,
	column2 int4 NULL DEFAULT 0,
	column3 int4 NULL DEFAULT 0,
	column4 int4 NULL DEFAULT 0,
	column5 int4 NULL DEFAULT 0,
	column6 int4 NULL DEFAULT 0,
	column7 int4 NULL DEFAULT 0,
	column8 int4 NULL DEFAULT 0,
	column9 int4 NULL DEFAULT 0,
	column10 int4 NULL DEFAULT 0,
	y int4 NULL DEFAULT 0,
	created_at timestamp NULL,
	updated_at timestamp NULL,
	page int4 NULL DEFAULT 0,
	user_id int4 NULL,
	file_id int4 NULL,
	text_data varchar NULL,
	is_train bool NULL DEFAULT false
	--CONSTRAINT train_fk FOREIGN KEY (file_id) REFERENCES files(id)
);

-- Permissions

ALTER TABLE public.train OWNER TO iztbj;
GRANT ALL ON TABLE public.train TO iztbj;



CREATE TABLE public.files (
	id serial NOT NULL,
	name varchar NULL,
	ext varchar NULL,
	created_at timestamp NULL,
	updated_at timestamp NULL,
	user_id int4 NULL,
	ip_add varchar NULL,
	file_path varchar NULL,
	is_pid bool NULL,
	doc_id varchar NULL
	--CONSTRAINT files_pk PRIMARY KEY (id)
);
COMMENT ON TABLE public.files IS '	';

-- Permissions

ALTER TABLE public.files OWNER TO iztbj;
GRANT ALL ON TABLE public.files TO iztbj;


CREATE USER airflow WITH PASSWORD '1234';
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;