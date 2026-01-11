from sqlalchemy import text
import pandas as pd
from sqlalchemy.orm import sessionmaker
from io import StringIO
from .database import engines
from .logger import logger

def execute_query_to_df(query, bind):
    engine = engines[bind]
    df = pd.read_sql(query, engine)
    return df

def execute_function_with_cursor_to_df(query, bind):
    engine = engines[bind]
    session_make = sessionmaker(bind=engine)
    session = session_make()
    try:
        results_cursor = session.execute(text(query)).fetchone()
        cur = session.execute(text(f'fetch all in "{results_cursor[0]}"'))
        results = cur.fetchall()
        df = pd.DataFrame(results, columns=[desc for desc in cur.keys()])
        session.commit()
        return df
    except Exception as error:
        logger.error(error)
        session.rollback()
    finally:
        session.close()

def bulk_insert_from_df_pg(df, table, bind):
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    engine = engines[bind]
    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        cursor.copy_from(buffer, table, sep=",")
        conn.commit()
        return True
    except Exception as error:
        logger.error(error)
        conn.rollback()
        return False
    finally:
        conn.close()
        cursor.close()

def bulk_insert_from_df_mssql(df, table, bind):
    engine = engines[bind]
    df.to_sql(table, engine, if_exists="append", index=False)

def execute_query_with_results(query, bind):
    engine = engines[bind]
    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()
        return results
    except Exception as error:
        logger.error(error)
        conn.rollback()
    finally:
        conn.close()
        cursor.close()

def execute_sp(bind, sp, args):
    engine = engines[bind]
    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        result = cursor.callproc(sp, args)
        conn.commit()
        return result
    except Exception as error:
        logger.error(error)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def execute_query_no_results(query, bind):
    engine = engines[bind]
    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
    except Exception as error:
        logger.error(error)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()