'''
DB Fields: Name=0, CR=1, XP=2, Size=4, Type=5
Init=7, Senses=8, AC=10, HP=12, Speed=26, Melee=28
Reach=31, Environment=47, Description_Visual=50
Description=53
'''

import sqlite3 as sql
import os


def monsters_by_name(name_str):
    db_name = 'bestiary.db'
    mon_schema = 'SELECT * FROM Bestiary WHERE Name LIKE \'' + name_str + '\''
    print(mon_schema)
    #db_exists = os.path.exists(db_name)
    #print(str(db_exists))

    conn = sql.connect(db_name)
    c = conn.cursor()
    c.execute(mon_schema)
    #print(c.fetchone())
    results = c.fetchall()
    print(results)
    print(type(results))
    print("----------------------------------------------")
    conn.close()
    return results


def monsters_like(field, term):
    db_name = 'bestiary.db'
    mon_schema = 'SELECT DISTINCT * FROM Bestiary WHERE ' + field + ' LIKE \'%' + term +'%\''

    conn = sql.connect(db_name)
    c = conn.cursor()
    c.execute(mon_schema)
    #print(c.fetchone())
    results = c.fetchall()
    conn.close()
    return results

def monsters_all_terms(name, cr, cr_crit, env, desc):
    db_name = 'bestiary.db'
    #mon_schema = 'SELECT DISTINCT * FROM Bestiary WHERE Name LIKE \'%' + name + '%\' AND CR LIKE \'%' + cr + '%\' AND Environment LIKE \'%' + env + '%\' AND Description LIKE \'%' + desc + '%\''
    mon_schema = 'SELECT DISTINCT * FROM Bestiary WHERE Name LIKE \'%' + name + '%\' AND CR ' + cr_crit + cr + ' AND Environment LIKE \'%' + env + '%\' AND Description LIKE \'%' + desc + '%\' ORDER BY 2, 1'
    print(mon_schema)
    conn = sql.connect(db_name)
    c = conn.cursor()
    c.execute(mon_schema)
    #print(c.fetchone())
    results = c.fetchall()
    conn.close()
    return results