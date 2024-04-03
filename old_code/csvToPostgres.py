import psycopg2, os, sys
import pandas as pd


def read_arg():
    if len(sys.argv) != 2:
        print('only two argumens required')
        exit()
    if not os.path.exists(sys.argv[1]):
        print('file not present')
        exit()

    return {
        'file_path':sys.argv[1]
    }

def csv_to_postgres(file):
    df = pd.read_csv(file)
    replacements = {
        'object':'varchar',
        'float64':'float',
        'int64':'int',
        'datetime64':'timestamp',
        'timedelta64[ns]':'varchar'
    }
    col_string = ','.join(f'{x} {y}' for (x, y) in zip(df.columns, df.dtypes.replace(replacements)))
    conn = psycopg2.connect(dbname='postgres',user='postgres',password='******',host='127.0.0.1',port='5432')
    with conn:
        with conn.cursor() as cur:
            cur.execute('drop table if exists newContract;')
            cur.execute('create table newContract(%s)' % col_string)
            csv_file = open(file)
            SQL = """
            COPY newContract FROM STDIN WITH
                CSV
                HEADER
                DELIMITER AS ','
            """
            cur.copy_expert(sql=SQL, file=csv_file)
    conn.close()



def main():
    arg = read_arg()
    result = csv_to_postgres(arg['file_path'])
    print(result)

if __name__ == '__main__':
    main()


