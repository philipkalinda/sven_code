
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

