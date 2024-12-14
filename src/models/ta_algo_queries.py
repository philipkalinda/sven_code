def get_all_data(table):
    """
    """
    return f"""
    select * from {table}
    """


def check_database_tables():
    """
    """
    return f"""
    select * from sqlite_master where type = 'table'
    """

