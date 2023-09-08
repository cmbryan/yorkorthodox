#!/usr/bin/python3
# York Orthodox Calendar Project v2
# Fr Deacon David Hoskin   2018

# --------------------------------------------------------------------------------
# Dependencies: python3, sqlite3, apsw python sqlite wrapper, the datetime module.
# --------------------------------------------------------------------------------

# This script populates the Year tables with the events of fixed date.
# For the most part this is straightforward copying exercice from the Menaion table
# of the major, Class 5 and British Isles and Ireland commemorations.
#
# Whether the Apostle reading, or both the Apostle and Gospel for a major commemoration
# (Class 4 and above) are preferred over the daily readings at the Liturgy will depend
# on whether or not they fall on a Sunday. The appropriate column (is_comm_apos, is_comm_gosp)
# is set only after checking whether or not it is a Sunday, the data being drawn from the
# is_sun_apos, is_sun_gosp, is_wkdy_apos and is_wkdy_gosp columns of the Menaion table.
#
# Certain of the 'fixed' commemorations are, on occasion, transferred. These are
# considered separately.
#
# The Forefeasts, Afterfeasts and Leavetakings of such major feasts that have them are
# recorded in the fore_after column.
#
# The Year Table columns major_commem, fore_after, class_5, british are populated.
#
# The fixed table 'Menaion' must already exist and be populated.
# The scripts 3_insert_ID_date and 4_paschalion_cycle must have been run and the relevant
# Year table columns populated.

# =======================================================================================

# Import the SQLite wrapper for Python:

import apsw

# Import the date handling modules:

import datetime
from datetime import date
from datetime import timedelta
import calendar

# Open the database as 'cal' and set the cursor to 'cur':

cal = apsw.Connection('YOCal.db')
cur = cal.cursor()

# Begin:

cur.execute('BEGIN TRANSACTION')

# Get the first and last years to have a table in the database.
# Set initial values and scan for the actual values.

yr = 1999         # We scan upwards from here
yr_final = 2100   # We scan downwards from here

name = ''
while name == '' and yr < 2100:
   yr += 1
   cur.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name= ?''', ('Year_'+str(yr),))
   name = cur.fetchone()
   if not name: name = ''

name = ''
while name == '' and yr_final > 1999:
   yr_final -= 1
   cur.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name= ?''', ('Year_'+str(yr_final),))
   name = cur.fetchone()
   if not name: name = ''

print('Tables for the years '+str(yr)+'-'+str(yr_final)+' will be populated')

# Cycle through the range of years:

while yr <= yr_final:

    # Set table name to that of the current year:

    tn = 'Year_' + str(yr)

    # Get the Year table id of Pascha using the Gospel Code already set:

    cur.execute('''SELECT id FROM %s WHERE g_code = "J1Sun"''' % tn)
    pascha_id = cur.fetchone()[0]

    # Set reference date for calculations which use the table ids.
    # The last day of the previous year is treated as id = 0:

    base_date = date(yr-1,12,31)

    # Get the end of year id on the current Year table. It may be 365 or 366:

    end_yr_id = (date(yr,12,31) - base_date).days

    # Copy the Global (Class 5), British commemorations, Forefeasts, Afterfeasts
    # and Leavetakings to the Year table. This is done by matching the date_key
    # on the Menaion table to that on the Year table.

    row =1

    while row <= end_yr_id:

        # Get and date_key and day_name for the row ID

        cur.execute('''SELECT date_key, day_name FROM %s WHERE id = ?''' % tn, (row,))
        result = cur.fetchone()
        d_key = result[0]
        d_name = result[1]

        # Set the is_apos and is_gosp variables according to whether or not it is a Sunday:

        if d_name == "Sunday":
            is_apos = "is_sun_apos"
            is_gosp = "is_sun_gosp"
        else:
            is_apos = "is_wkdy_apos"
            is_gosp = "is_wkdy_gosp"
        cur.execute('''UPDATE %s SET
            class_5 = (SELECT class_5 FROM Menaion WHERE date_key = ?),
            british = (SELECT british FROM Menaion WHERE date_key = ?),
            fore_after = (SELECT fore_after FROM Menaion WHERE date_key = ?),
            is_comm_apos = (SELECT %s FROM Menaion WHERE date_key = ?),
            is_comm_gosp = (SELECT %s FROM Menaion WHERE date_key = ?)
            WHERE date_key = ?
            ''' % (tn, is_apos, is_gosp), (d_key, d_key, d_key, d_key, d_key, d_key))

        # If the Eve of the Nativity or Theophany falls on Saturday or Sunday
        # ignore the major data and continue to next row because
        # this date is celebrated as the Saturday or Sunday before the feast.

        if (d_key == '12-24' or d_key == '01-05') and (d_name == 'Saturday' or d_name == 'Sunday'):
           row += 1
           continue

        # Copy the major commemorations and associated data to the Year table.
        # For the exceptions see below.

        if d_key not in ("02-10","02-24","04-23","04-25","04-30"):
            cur.execute('''SELECT major FROM Menaion WHERE date_key = ?''', (d_key,))
            major = cur.fetchone()[0]
            if major != "":
               cur.execute('''UPDATE %s SET
                major_commem = ?,
                apos_comm = (SELECT apostle FROM Menaion WHERE date_key = ?),
                gosp_comm = (SELECT gospel FROM Menaion WHERE date_key = ?),
                is_comm_apos = (SELECT %s FROM Menaion WHERE date_key = ?),
                is_comm_gosp = (SELECT %s FROM Menaion WHERE date_key = ?),
                c_code = ?
                WHERE date_key = ?
                ''' % (tn, is_apos, is_gosp), (major, d_key, d_key, d_key, d_key, d_key, d_key))
        row += 1

    # Five major feasts may be transferred. They are:
    #    02-10    Haralampos moves to 02-09 if the 10th is the Saturday of All Souls.
    #    02-24    The Forerunner (1st & 2nd findings of the head)
    #                    moves to 02-23 if the 24th is the Saturday of All Souls.
    #    04-23    George moves to Bright Monday if it falls ealier.
    #    04-25    Mark moves to Bright Tuesday if it falls ealier.
    #    04-30    James of Zebedee moves to Bright Wednesday if it falls ealier.

    # Set the ids for these five to their normal dates:

    hara_id = (date(yr,2,10) - base_date).days
    john_id = (date(yr,2,24) - base_date).days
    george_id = (date(yr,4,23) - base_date).days
    mark_id = (date(yr,4,25) - base_date).days
    james_id = (date(yr,4,30) - base_date).days

    # Soul Sabbath falls 57 days before Pascha. Its Year table id is therefore:

    soul_sab_id = pascha_id - 57

    # If Haralampos or John coincide, move their id back one day and set the 'Transferred' text:

    if hara_id == soul_sab_id:
        hara_id -= 1
        hara_txt = " (Transferred from February 10th)"
    else: hara_txt = ""

    if john_id == soul_sab_id:
        john_id -= 1
        john_txt = " (Transferred from February 24th)"
    else: john_txt = ""

    # Similarly reset the other three if needed:

    if george_id < pascha_id +1:
        george_id = pascha_id +1
        george_txt = " (Transferred from April 23rd)"
    else: george_txt = ""

    if mark_id < pascha_id +2:
        mark_id = pascha_id +2
        mark_txt = " (Transferred from April 25th)"
    else: mark_txt = ""

    if james_id < pascha_id +3:
        james_id = pascha_id +3
        james_txt = " (Transferred from April 30th)"
    else: james_txt = ""

    # Assemble the data.

    data = [("02-10",hara_id,hara_txt),("02-24",john_id,john_txt),("04-23",george_id,george_txt),("04-25",mark_id,mark_txt),("04-30",james_id,james_txt)]

    # Cycle through, collecting the data for the feast from its original date_key position in
    # the Menaion table and placing it in its actual location for this year in the Year table.

    for d_key, yr_tbl_id, txt in data:

        # Get the Day Name for the Table ID

        cur.execute('''SELECT day_name FROM %s WHERE date_key = ?''' % tn, (d_key,))
        d_name = cur.fetchone()[0]

        # Set the is_apos and is_gosp variables according to whether or not it is a Sunday:

        if d_name == "Sunday":
            is_apos = "is_sun_apos"
            is_gosp = "is_sun_gosp"
        else:
            is_apos = "is_wkdy_apos"
            is_gosp = "is_wkdy_gosp"

       # if is_apos != 1: is_apos = 0
       # if is_gosp != 1: is_apos = 0

        # Get and set the major_commem column adding the 'transferred' text if it exists

        cur.execute('''SELECT major FROM Menaion WHERE date_key = ?''', (d_key,))
        major = cur.fetchone()[0]
        major = major + txt

        cur.execute('''UPDATE %s SET major_commem = ?, c_code = ? WHERE id = ?''' % tn, (major, d_key, yr_tbl_id))

        # Get and set the rest of the data

        cur.execute('''UPDATE %s SET
                apos_comm = (SELECT apostle FROM Menaion WHERE date_key = ?),
                gosp_comm = (SELECT gospel FROM Menaion WHERE date_key = ?),
                is_comm_apos = (SELECT %s FROM Menaion WHERE date_key = ?),
                is_comm_gosp = (SELECT %s FROM Menaion WHERE date_key = ?)
                WHERE id = ?
                ''' % (tn, is_apos, is_gosp), (d_key, d_key, d_key, d_key, yr_tbl_id))

    # If the Presentation falls on a Sunday before the triodion the Gospel for the feast is used
    pres_id = (date(yr,2,2) - base_date).days
    if pres_id < pascha_id - 70:
        cur.execute('''UPDATE %s SET is_comm_gosp = 1
                WHERE id = %s''' % (tn, pres_id))

    # If the Feast of St Athanasius falls on Pascha or Thomas Sunday his Apostle reading is suppressed
    athan_id = (date(yr,5,2) - base_date).days
    if athan_id == pascha_id or athan_id == pascha_id + 7:
        cur.execute('''UPDATE %s SET is_comm_apos = 0
                WHERE id = %s''' % (tn, athan_id))

     # If a feast falls on the Ascension both Apostle and Gospel readings are suppressed
    cur.execute('''UPDATE %s SET is_comm_apos = 0, is_comm_gosp = 0
                WHERE id = %s''' % (tn, pascha_id+39))
  
 # If a feast - e.g. Metrophanes - falls on Pentecost the festal Apostle reading is supressed
    cur.execute('''UPDATE %s SET is_comm_apos = 0
                WHERE id = %s''' % (tn, pascha_id+49))

    # Check that the Afterfeast and Leavetaking of the Meeting in the Temple (nominally Feb 9th) does not overrun the Sunday of the Prodigal Son which is 63 days before Pascha.

    prodigal_id = pascha_id - 63
    meeting_id = (date(yr,2,2) - base_date).days

    if prodigal_id < meeting_id + 8:

        # Set new_leave to the day before the Sun of the Prodigal:

        new_leave_id = prodigal_id - 1

        # Update the table with the new leavetaking provided there is at least one day between
        # the Meeting and the Sunday of the Prodigal.

        if new_leave_id > meeting_id:
            cur.execute('''UPDATE %s SET fore_after = "Leavetaking of the Meeting of the Lord in the Temple"
                    WHERE id = ?''' % tn, (new_leave_id,))

        # Delete any references to Afterfeast or Leaving which were initially placed
        # on or after the Sunday of the Prodigal

            x_id = prodigal_id
            while x_id < meeting_id + 8:
                cur.execute('''UPDATE %s SET fore_after = "" WHERE id = ?''' % tn, (x_id,))
                x_id += 1

    # We will also set the Afterfeasts and Leavetakings from the Pentecostarion.
    # They run from the eve of the Ascension (pascha + 38) to the eve of All Saints Sunday (pascha + 55)

    cur.execute('''UPDATE %s SET fore_after = "Leavetaking of Pascha" WHERE id = ?''' % tn, (pascha_id+38,))
    cur.execute('''UPDATE %s SET fore_after = "Afterfeast of the Ascension" WHERE id BETWEEN ? AND ?''' % tn, (pascha_id+40, pascha_id+46))
    cur.execute('''UPDATE %s SET fore_after = "Leavetaking of the Ascension" WHERE id = ?''' % tn, (pascha_id+47,))
    cur.execute('''UPDATE %s SET fore_after = "Afterfeast of Pentecost" WHERE id BETWEEN ? AND ?''' % tn, (pascha_id+50, pascha_id+54))
    cur.execute('''UPDATE %s SET fore_after = "Leavetaking of Pentecost" WHERE id = ?''' % tn, (pascha_id+55,))

    # In non Leap Years the commemorations for Feb 29th need to be appended to Feb 28th:

    if not calendar.isleap(yr):
          cur.execute('''UPDATE %s SET
            class_5 = (class_5 || " John Cassian the Roman, confessor (435) (t/f from Feb 29th).")
            WHERE date_key = "02-28" ''' % tn)
          cur.execute('''UPDATE %s SET
            british = (british || " Oswald of Worcester and York (t/f from Feb 29th).")
            WHERE date_key = "02-28" ''' % tn)

# If the feast of St George has been transferred to Bright Monday, add a note on April 23rd to thay effect

    if george_txt:
       cur.execute('''UPDATE %s SET
            class_5 = ("[The Great Martyr George – the feast is transferred to Bright Monday this year] " || class_5)
            WHERE date_key = "04-23"''' % tn)


    # St. Raphael (Hawaweeny) is commemorated on the first Saturday of November.
    # We need to add his name to the class_5 list for the appropriate day.

    # What is the date key of the first Saturday of November?

    cur.execute('''SELECT date_key FROM %s
            WHERE month = "November" AND day_num < 8 AND Day_name = "Saturday"''' % tn)
    d_key = cur.fetchone()[0]

    # Add Hawaweeny and update the table

    cur.execute('''UPDATE %s SET
            class_5 = (class_5 || " Raphael (Hawaweeny) Bishop of Brooklyn (1915).")
            WHERE date_key = ?''' % tn, (d_key,))


    # St. Joseph the Betrothed, St. David the Psalmist & St. James the brother of the Lord are added to the class_5 list on the last Sunday of December, but if that is the 25th, the Nativity, they are added to Dec 26th.

    # What is the date key of the last Sunday of December?
    cur.execute('''SELECT date_key FROM %s
            WHERE month = "December" AND day_num > 24 AND Day_name = "Sunday"''' % tn)
    d_key = cur.fetchone()[0]

    # If the date key is for the Nativity, update it to the 26th.    
    if d_key == '12-25': d_key = '12-26'

    # Add the extra commemorations to beginning of the class_5 list for that day and update the table.
    cur.execute('''UPDATE %s SET
            class_5 = ("St. Joseph the Betrothed. St. David the Psalmist. St. James the brother of the Lord. " || class_5)
            WHERE date_key = ?''' % tn, (d_key,))


    # Stephen (12-27) does not have a Gospel if it falls on a Saturday

    cur.execute('''UPDATE %s SET
            is_comm_gosp = 0
            WHERE date_key = "12-27" AND day_name = "Saturday"''' % tn)

    # Move on to the next year:

    yr += 1

# Write the data to the table

cur.execute('COMMIT')

cal.close()
