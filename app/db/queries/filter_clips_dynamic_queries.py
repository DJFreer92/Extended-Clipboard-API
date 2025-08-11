import re

# Queries
def filter_all_clips_query(*, search: str = '', time_frame: str = '') -> str:
    """Construct a SQL query to filter all clips based on keywords and time frame."""

    keyword_clauses: str = build_keyword_where_clause(search)
    time_condition: str = construct_time_condition_ge(time_frame)

    sql_query: str = f"""
    SELECT * FROM Clips
    WHERE {keyword_clauses} AND {time_condition}
    ORDER BY ID DESC;
    """

    return sql_query

def filter_n_clips_query(*, search: str = '', time_frame: str = '', n: int | None = None) -> str:
    """Construct a SQL query to filter a specific number of clips based on keywords and time frame."""

    keyword_clauses: str = build_keyword_where_clause(search)
    time_condition: str = construct_time_condition_ge(time_frame)

    sql_query: str = f"""
    SELECT * FROM Clips
    WHERE {keyword_clauses} AND {time_condition}
    ORDER BY ID DESC
    LIMIT COALESCE({n}, 999999);
    """

    return sql_query

def filter_all_clips_after_id_query(*, search: str = '', time_frame: str = '', after_id: int) -> str:
    """Construct a SQL query to filter clips based on keywords and time frame, starting after a specific ID."""

    keyword_clauses: str = build_keyword_where_clause(search)
    time_condition: str = construct_time_condition_ge(time_frame)

    sql_query: str = f"""
    SELECT * FROM Clips
    WHERE {keyword_clauses} AND {time_condition} AND ID > {after_id}
    ORDER BY ID DESC
    """

    return sql_query

def filter_n_clips_before_id_query(*, search: str = '', time_frame: str = '', n: int | None = None, before_id: int) -> str:
    """Construct a SQL query to filter a specific number of clips based on keywords and time frame, starting before a specific ID."""

    keyword_clauses: str = build_keyword_where_clause(search)
    time_condition: str = construct_time_condition_ge(time_frame)

    sql_query: str = f"""
    SELECT * FROM Clips
    WHERE {keyword_clauses} AND {time_condition} AND ID < {before_id}
    ORDER BY ID DESC
    LIMIT COALESCE({n}, 999999);
    """

    return sql_query

def get_num_filtered_clips_query(*, search: str = '', time_frame: str = '') -> str:
    """Construct a SQL query to count the number of filtered clips based on keywords and time frame."""

    keyword_clauses: str = build_keyword_where_clause(search)
    time_condition: str = construct_time_condition_ge(time_frame)

    sql_query: str = f"""
    SELECT COUNT(*) FROM Clips
    WHERE {keyword_clauses} AND {time_condition}
    """

    return sql_query

# Query utilities
def build_keyword_where_clause(search: str) -> str:
    """Build the WHERE clause for the keyword search."""

    # Split the search string into individual keywords
    delimiters: list[str] = [',', ';', '|', ' ', '\n', '\t']
    regex: str = '|'.join(re.escape(d) for d in delimiters)
    split_keywords: list[str] = re.split(regex, search.strip())

    # Construct the keyword clauses
    keyword_clauses: str = ''
    for keyword in split_keywords:
        keyword_clauses += f"Content LIKE '%{keyword}%' OR "

    # Remove the trailing ' OR ' from the WHERE clause
    return keyword_clauses[:-4]

def construct_time_condition_ge(time_frame: str) -> str:
    """Construct the time condition based on the selected time frame."""

    match time_frame:
        case 'past_24_hours':
            return "Timestamp >= datetime('now', '-1 day')"
        case 'past_week':
            return "Timestamp >= datetime('now', '-7 days')"
        case 'past_month':
            return "Timestamp >= datetime('now', '-1 month')"
        case 'past_3_months':
            return "Timestamp >= datetime('now', '-3 months')"
        case 'past_year':
            return "Timestamp >= datetime('now', '-1 year')"
        case _:
            return "Timestamp >= '1970-01-01 00:00:00'"
