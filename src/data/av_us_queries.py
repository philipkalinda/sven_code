
def get_min_date(table):
    """
    """
    return f"""
    select min(date) from {table}
    """


def get_max_date(table):
    """
    """
    return f"""
    select max(date) from {table}
    """


def get_all_data(table):
    """
    """
    return f"""
    select * from {table}
    """


def check_date(date, table):
    """
    """
    return f"""
    select count(1) from {table} where date={date}
    """


def insert_data(table, values):
    """
    """
    return f"""
    insert into {table} (date, open, high, low, close, volume) values {values}
    """


def create_table(table):
    """
    """
    return f"""
    CREATE TABLE if not exists {table} 
    (date text, open float, high float, low float, close float, volume float)
    """


def drop_table(table):
    """
    """
    return f"""
    delete from {table}
    """


def check_database_tables():
    """
    """
    return f"""
    select * from sqlite_master where type = 'table'
    """


def table_statistics(table):
    """
    """
    return f"""
    select 
        count(*) as n_records,
        min(date) as min_date,
        max(date) as max_date,
        min(close) as min_close,
        max(close) as max_close,
        avg(close) as avg_close
    from {table}
    """


def get_nsadaq_100_with_min_5_years():
    """
    """
    return f"""
    select 
        nas100.*,
        full_list.ipoDate as ipo_date
    from 
        nasdaq_100_list as nas100
        left join
        us_listings as full_list
        on nas100.symbol = full_list.symbol
    where 
        full_list.ipoDate <= '2015-01-01'
    """

