#!/usr/bin/python3
# York Orthodox Calendar Project v2
# Fr Deacon David Hoskin   2018

# Dependencies: python3, sqlite3, apsw python sqlite wrapper.

# Creates Static Tables and populates them from the data in csv files
# NB The files pascha.csv, menaion.csv, apostle.csv, gospel.csv must be available.
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# First import the SQLite wrapper for Python:
import apsw

# Open the database as 'cal' and set the cursor to 'cur':
cal = apsw.Connection('YOCal.db')
cur = cal.cursor()

# Begin:
cur.execute('BEGIN TRANSACTION')

# Create the tables:

# Table "Pascha" - Dates of Pascha
# ================================
cur.execute("""CREATE TABLE Pascha (
    year INTEGER,
    pascha_date DATE
)""")

f = open('pascha.csv','r')

for row in f:
   items = row.split('\t')
   cur.execute('''INSERT INTO Pascha (year, pascha_date) VALUES (?,?)
               ''', (items[0], items[1].rstrip()))

f.close()

# Table "Menaion" - Fixed Commemorations
# ======================================
cur.execute("""CREATE TABLE Menaion (
    date_key TEXT,
    major TEXT,
    class TEXT,
    apostle TEXT,
    gospel TEXT,
    is_sun_apos INTEGER,
    is_sun_gosp INTEGER,
    is_wkdy_apos INTEGER,
    is_wkdy_gosp INTEGER,
    fore_after TEXT,
    class_5 TEXT,
    british TEXT
)""")

f = open('menaion.csv','r')
for row in f:
   items = row.split('|')
   if len(items[11]) < 5: items[11] =''
   for x in (5,6,7,8):
      if len(items[x]) <1:
         items[x] = 0
      
   cur.execute('''INSERT INTO Menaion (
               date_key, major, class, apostle, gospel,
               is_sun_apos, is_sun_gosp, is_wkdy_apos, is_wkdy_gosp,
               fore_after, class_5, british) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
               ''', (items[0], items[1], items[2], items[3], items[4],
               items[5], items[6], items[7], items[8], items[9],
               items[10], items[11]))
f.close()


# Table "A_Lections" - Apostle and Old Testament Readings
# ====================================================
cur.execute("""CREATE TABLE A_Lections (
    code TEXT,
    designation TEXT,
    lection TEXT,
    a_id INTEGER
)""")

f = open('apostle.csv','r')

for row in f:
   items = row.split('\t')
   cur.execute('''INSERT INTO A_Lections (code, designation, lection, a_id) VALUES (?,?,?,?)
               ''', (items[0], items[1], items[2], items[3]))

f.close()


# Table "G_Lections" - Gospel and any additional Readings
# =======================================================
cur.execute("""CREATE TABLE G_Lections (
    code TEXT,
    designation TEXT,
    lection TEXT,
    extra TEXT,
    g_id INTEGER
)""")

f = open('gospel.csv','r')
for row in f:
   items = row.split('\t')
   cur.execute('''INSERT INTO G_Lections (code, designation, lection, extra, g_id) VALUES (?,?,?,?,?)
               ''', (items[0], items[1], items[2], items[3], items[4]))
f.close()


# Table "X_Lections" - Readings for Matins, hours, etc
# ====================================================
# The codes comprise the day code - e.g. J1Sun, 1224 (24th Dec), preceded by:
# m = matins
# v = vespers
# f,t,s,n = first, third, sixth, ninth hours
# u = service of holy unction
# w = foot-washing
# b = lessing of the waters

cur.execute("""CREATE TABLE X_Lections (
    code TEXT,
    apostle TEXT,
    gospel TEXT
)""")

f = open('lects_extra.csv','r')
for row in f:
   items = row.split('\t')
   cur.execute('''INSERT INTO X_Lections (code, apostle, gospel) VALUES (?,?,?)
               ''', (items[0], items[1], items[2]))
f.close()

# Write the data to the database:
cur.execute('COMMIT')

# Close the database and report back
cal.close()
