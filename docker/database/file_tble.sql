-- Drop table

-- DROP TABLE public.files;

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
	doc_id varchar NULL,
	CONSTRAINT files_pk PRIMARY KEY (id)
);
COMMENT ON TABLE public.files IS '	';

-- Permissions

ALTER TABLE public.files OWNER TO iztbj;
GRANT ALL ON TABLE public.files TO iztbj;
