import httplib2
import sqlite3
import time
from bs4 import BeautifulSoup

dt = time.strftime("%Y-%m-%d")

urls = ['http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&CATALOGID=1803&TABKEY=tab1&txtQueryDate=%s' % dt,
        'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&CATALOGID=1803&TABKEY=tab2&txtQueryDate=%s' % dt,
        'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&CATALOGID=1803&TABKEY=tab3&txtQueryDate=%s' % dt,
        'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=7&CATALOGID=1803&TABKEY=tab4&txtQueryDate=%s' % dt]

sqls = ['INSERT INTO szsc (name, today, delta, percent, hvalue, hdate) VALUES (%s)',
        'INSERT INTO szzb (name, today, delta, hvalue, hdate) VALUES (%s)',
        'INSERT INTO zxb (name, today, delta, hvalue, hdate) VALUES (%s)',
        'INSERT INTO cyb (name, today, delta, hvalue, hdate) VALUES (%s)']

sqlite_file = 'sqlite/szse.cn.db'

def insert_sqlite(num, entries):
    conn = sqlite3.connect(sqlite_file)
    for entry in entries:
        values = '"' + '", "'.join(entry) + '"'
        sql = sqls[num] % values
        conn.execute(sql)
    conn.commit()
    conn.close()

def parse_web(num):
    n = 0
    results = []
    print urls[num]
    while n < 10:
        n += 1
        try:
            entries = []
            http = httplib2.Http()
            response, content = http.request(urls[num])
            if response['status'] == '200':
                soup = BeautifulSoup(content, 'lxml', from_encoding='gbk')
                for tr in soup.select('tr .cls-data-tr'):
                    entries.append(map(lambda x: x.text.strip(), tr.select('td')))
                results = entries
                n = 10
        except:
            print n
            time.sleep(600)
    return results

def main():
    for m in range(len(urls)):
        insert_sqlite(m, parse_web(m))

if __name__ == '__main__':
    main()