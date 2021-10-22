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
	is_train bool NULL DEFAULT false,
	CONSTRAINT train_fk FOREIGN KEY (file_id) REFERENCES files(id)
);

-- Permissions

ALTER TABLE public.train OWNER TO iztbj;
GRANT ALL ON TABLE public.train TO iztbj;
