import json
import httplib2
import sqlite3
import time

dt = time.strftime("%Y%m%d")
sqlite_file = 'sqlite/sse.com.cn.db'
url = 'http://yunhq.sse.com.cn:32041/v1/sh1/snap/000001?select=open%2Chigh%2Clow%2Clast%2Cvolume%2Camount'
sql = 'INSERT INTO szzs (open, high, low, close, volume, amount) VALUES (%s)'

def insert_sqlite(entries):
    conn = sqlite3.connect(sqlite_file)
    for entry in entries:
        values = '"' + '", "'.join(entry) + '"'
        sql = sql % (values)
        conn.execute(sql)
    conn.commit()
    conn.close()

def parse_web():
    n = 0
    results = []
    print time.ctime() + ' -- ' + url
    while n < 10:
        n += 1
        try:
            http = httplib2.Http()
            response, content = http.request(url)
            c = json.loads(content)
            if dt == str(c['date']):
                results = c['snap']
            n = 10
        except:
            print n
            time.sleep(60)
   return results

def main():
    insert_sqlite(parse_web())

if __name__ == '__main__':
    main()
