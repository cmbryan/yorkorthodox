#!/usr/bin/env sh

rm -rf ./YOCal.db ./YOCal_Master.db

./1_fixed_tables_create_populate.py
./2_year_tables_create.py 2023 2099
./3_insert_ID_date.py
./4_paschalion_cycle.py
./5_menaion_cycle.py
./6_fast_codes.py
./7_tone_eoth.py
./8_master_main_create.py
./9_master_lection_create.py
./10_master_main_tbl_pop.py 2023 2099
./11_master_lection_pop.py
./12_master_lection_correct.py
./13_master_lection_create_mods_file.py
# ./21_mysql_lections_file_create.py
# ./22_mysql_main_file_create.py

mkdir -p ../app/db
mv ./YOCal_Master.db ../app/db
