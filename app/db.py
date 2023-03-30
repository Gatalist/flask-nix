import psycopg2


def sql_request(sql):
    conn = psycopg2.connect(
        host = "localhost",
        database = "nix_db",
        user = 'user_db',
        password = 'xEhs5hU26nDNdeC')
    
    if conn:
        curr = conn.cursor()
        curr.execute(f'''{sql}''')
        res = curr.fetchall()
        print(res)
        conn.commit()
        conn.close()
        
    else:
        print("No conected")


# sql_request('SELECT * FROM "stars"')
# sql_request('DELETE FROM "movies" CASCADE;')
# sql_request('DELETE FROM "retings" CASCADE;')
# sql_request('DELETE FROM "stars" CASCADE;')
sql_request('DROP database "nix_db";')