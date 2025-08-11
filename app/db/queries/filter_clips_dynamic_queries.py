import re

# Queries
def filter_all_clips_query(*, search: str = '', time_frame: str = '') -> tuple[str, list]:
    """Construct a SQL query to filter all clips based on keywords and time frame."""

    keyword_clauses, params = build_keyword_where_clause(search)
    time_condition: str = construct_time_condition_ge(time_frame)

    sql_query: str = f"""
    SELECT * FROM Clips
    WHERE {keyword_clauses} AND {time_condition}
    ORDER BY ID DESC;
    """

    return sql_query, params

def filter_n_clips_query(*, search: str = '', time_frame: str = '', n: int | None = None) -> tuple[str, list]:
    """Construct a SQL query to filter a specific number of clips based on keywords and time frame."""

    keyword_clauses, params = build_keyword_where_clause(search)
    time_condition: str = construct_time_condition_ge(time_frame)

    sql_query: str = f"""
    SELECT * FROM Clips
    WHERE {keyword_clauses} AND {time_condition}
    ORDER BY ID DESC
    LIMIT COALESCE({n}, 999999);
    """

    return sql_query, params

def filter_all_clips_after_id_query(*, search: str = '', time_frame: str = '', after_id: int) -> tuple[str, list]:
    """Construct a SQL query to filter clips based on keywords and time frame, starting after a specific ID."""

    keyword_clauses, params = build_keyword_where_clause(search)
    time_condition: str = construct_time_condition_ge(time_frame)

    sql_query: str = f"""
    SELECT * FROM Clips
    WHERE {keyword_clauses} AND {time_condition} AND ID > ?
    ORDER BY ID DESC
    """

    return sql_query, [*params, after_id]

def filter_n_clips_before_id_query(*, search: str = '', time_frame: str = '', n: int | None = None, before_id: int) -> tuple[str, list]:
    """Construct a SQL query to filter a specific number of clips based on keywords and time frame, starting before a specific ID."""

    keyword_clauses, params = build_keyword_where_clause(search)
    time_condition: str = construct_time_condition_ge(time_frame)

    sql_query: str = f"""
    SELECT * FROM Clips
    WHERE {keyword_clauses} AND {time_condition} AND ID < ?
    ORDER BY ID DESC
    LIMIT COALESCE(?, 999999);
    """

    return sql_query, [*params, before_id, n]

def get_num_filtered_clips_query(*, search: str = '', time_frame: str = '') -> tuple[str, list]:
    """Construct a SQL query to count the number of filtered clips based on keywords and time frame."""

    keyword_clauses, params = build_keyword_where_clause(search)
    time_condition: str = construct_time_condition_ge(time_frame)

    sql_query: str = f"""
    SELECT COUNT(*) FROM Clips
    WHERE {keyword_clauses} AND {time_condition}
    """

    return sql_query, params

# Query utilities
def build_keyword_where_clause(search: str) -> tuple[str, list]:
    """Build the WHERE clause for the keyword search using parameterized queries."""

    # Split the search string into individual keywords
    delimiters: list[str] = [',', ';', '|', ' ', '\n', '\t']
    regex: str = '|'.join(re.escape(d) for d in delimiters)
    split_keywords: list[str] = [kw for kw in re.split(regex, search.strip()) if kw]

    # Construct the keyword clauses and parameters
    keyword_clauses_list = []
    params = []
    for keyword in split_keywords:
        keyword_clauses_list.append("Content LIKE ?")
        params.append(f"%{keyword}%")

    if keyword_clauses_list:
        keyword_clauses = " AND ".join(keyword_clauses_list)
    else:
        keyword_clauses = "1=1"  # No search keywords, match all

    return keyword_clauses, params

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
