\COPY public.shops FROM '/docker-entrypoint-initdb.d/shops.csv' WITH CSV HEADER DELIMITER ',';

\COPY public.reviews FROM '/docker-entrypoint-initdb.d/reviews.csv' WITH CSV HEADER DELIMITER ',';

\COPY public.information FROM '/docker-entrypoint-initdb.d/information.csv' WITH CSV HEADER DELIMITER ',';

\COPY public.images FROM '/docker-entrypoint-initdb.d/images.csv' WITH CSV HEADER DELIMITER ',';