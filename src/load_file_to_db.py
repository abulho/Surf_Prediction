import io

import pandas as pd
from sqlalchemy import create_engine

def write_to_table(df, db_engine, table_name, if_exists='fail'):
    string_data_io = io.StringIO()
    df.to_csv(string_data_io, sep='|', index=False)
    pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine)
    table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df,
                               index=False, if_exists=if_exists)
    table.create()
    string_data_io.seek(0)
    string_data_io.readline()  # remove header
    with db_engine.connect() as connection:
        with connection.connection.cursor() as cursor:
            copy_cmd = "COPY %s FROM STDIN HEADER DELIMITER '|' CSV" % table_name
            cursor.copy_expert(copy_cmd, string_data_io)
        connection.connection.commit()

if __name__ == '__main__':
    import getpass
    password = getpass.getpass("Enter your password: ")
    address = 'postgresql://abdulla05:{}@abdulladatabase.cfrfukypowpw.us-west-2.rds.amazonaws.com:5432/wavedata'.format(password)

    engine = create_engine(address)
    df = pd.read_csv('data_46002.csv', parse_dates=['Date'])

    table_name = 'data_46002'
    print('Writing table {} to database'.format(table_name))
    write_to_table(df, engine, table_name, 'replace' )
