\c mensaku

CREATE TABLE IF NOT EXISTS public.shops
(
    id integer NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT shops_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.information
(
    id integer NOT NULL,
    shop_id integer NOT NULL,
    score real,
    address character varying COLLATE pg_catalog."default",
    latitude real,
    longitude real,
    operating_hours character varying COLLATE pg_catalog."default",
    shop_holidays character varying COLLATE pg_catalog."default",
    sns character varying COLLATE pg_catalog."default",
    CONSTRAINT information_pkey PRIMARY KEY (id),
    CONSTRAINT shop_id FOREIGN KEY (shop_id)
        REFERENCES public.shops (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS public.reviews
(
    id integer NOT NULL,
    shop_id integer NOT NULL,
    review character varying COLLATE pg_catalog."default",
    CONSTRAINT reviews_pkey PRIMARY KEY (id, shop_id),
    CONSTRAINT shop_id FOREIGN KEY (shop_id)
        REFERENCES public.shops (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS public.menus
(
    id integer NOT NULL,
    shop_id integer NOT NULL,
    menu character varying COLLATE pg_catalog."default",
    price character varying COLLATE pg_catalog."default",
    CONSTRAINT menus_pkey PRIMARY KEY (id),
    CONSTRAINT shop_id FOREIGN KEY (shop_id)
        REFERENCES public.shops (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS public.images
(
    id integer NOT NULL,
    shop_id integer NOT NULL,
    image_url character varying COLLATE pg_catalog."default",
    context character varying COLLATE pg_catalog."default",
    CONSTRAINT images_pkey PRIMARY KEY (id),
    CONSTRAINT shop_id FOREIGN KEY (shop_id)
        REFERENCES public.shops (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);