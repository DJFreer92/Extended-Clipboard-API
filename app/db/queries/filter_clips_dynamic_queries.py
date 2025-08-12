import re
from app.models.clipboard.filters import Filters

# Queries
def filter_all_clips_query(filters: Filters) -> tuple[str, list]:
    """Construct a SQL query to filter all clips based on keywords and time frame."""

    keyword_clauses, keyword_params = build_keywords_where_clause(filters.search)
    tag_clauses, tag_params = build_tags_where_clause(filters.selected_tags)
    app_clauses, app_params = build_apps_where_clause(filters.selected_apps)
    join_favorites: str = construct_favorites_join_clause(filters.favorites_only)
    time_condition: str = construct_time_condition(filters.time_frame)

    # Always LEFT JOIN FavoriteClips to compute IsFavorite; if favorites_only we already switched join_favorites to INNER JOIN
    favorites_join = join_favorites or "LEFT JOIN FavoriteClips ON Clips.ID = FavoriteClips.ClipID"
    sql_query: str = f"""
    SELECT
        Clips.ID AS ClipID,
        Clips.Content AS Content,
        Clips.FromAppName AS FromAppName,
        GROUP_CONCAT(Tags.Name, ',') AS Tags,
        Clips.Timestamp AS Timestamp,
        CASE WHEN FavoriteClips.ClipID IS NOT NULL THEN 1 ELSE 0 END AS IsFavorite
    FROM Clips
    {favorites_join}
    LEFT JOIN ClipTags ON Clips.ID = ClipTags.ClipID
    LEFT JOIN Tags ON ClipTags.TagID = Tags.ID
    WHERE ({keyword_clauses}) AND ({tag_clauses}) AND ({app_clauses}) AND ({time_condition})
    GROUP BY Clips.ID, Clips.Content, Clips.FromAppName, Clips.Timestamp
    ORDER BY Clips.ID DESC;
    """

    return sql_query, keyword_params + tag_params + app_params

def filter_n_clips_query(filters: Filters, *, n: int | None = None) -> tuple[str, list]:
    """Construct a SQL query to filter a specific number of clips based on keywords and time frame."""

    keyword_clauses, keyword_params = build_keywords_where_clause(filters.search)
    tag_clauses, tag_params = build_tags_where_clause(filters.selected_tags)
    app_clauses, app_params = build_apps_where_clause(filters.selected_apps)
    join_favorites: str = construct_favorites_join_clause(filters.favorites_only)
    time_condition: str = construct_time_condition(filters.time_frame)

    favorites_join = join_favorites or "LEFT JOIN FavoriteClips ON Clips.ID = FavoriteClips.ClipID"
    sql_query: str = f"""
    SELECT
        Clips.ID AS ClipID,
        Clips.Content AS Content,
        Clips.FromAppName AS FromAppName,
        GROUP_CONCAT(Tags.Name, ',') AS Tags,
        Clips.Timestamp AS Timestamp,
        CASE WHEN FavoriteClips.ClipID IS NOT NULL THEN 1 ELSE 0 END AS IsFavorite
    FROM Clips
    {favorites_join}
    LEFT JOIN ClipTags ON Clips.ID = ClipTags.ClipID
    LEFT JOIN Tags ON ClipTags.TagID = Tags.ID
    WHERE ({keyword_clauses}) AND ({tag_clauses}) AND ({app_clauses}) AND ({time_condition})
    GROUP BY Clips.ID, Clips.Content, Clips.FromAppName, Clips.Timestamp
    ORDER BY Clips.ID DESC
    LIMIT COALESCE({n}, 999999);
    """

    return sql_query, keyword_params + tag_params + app_params

def filter_all_clips_after_id_query(filters: Filters, *, after_id: int) -> tuple[str, list]:
    """Construct a SQL query to filter clips based on keywords and time frame, starting after a specific ID."""

    keyword_clauses, keyword_params = build_keywords_where_clause(filters.search)
    tag_clauses, tag_params = build_tags_where_clause(filters.selected_tags)
    app_clauses, app_params = build_apps_where_clause(filters.selected_apps)
    join_favorites: str = construct_favorites_join_clause(filters.favorites_only)
    time_condition: str = construct_time_condition(filters.time_frame)

    favorites_join = join_favorites or "LEFT JOIN FavoriteClips ON Clips.ID = FavoriteClips.ClipID"
    sql_query: str = f"""
    SELECT
        Clips.ID AS ClipID,
        Clips.Content AS Content,
        Clips.FromAppName AS FromAppName,
        GROUP_CONCAT(Tags.Name, ',') AS Tags,
        Clips.Timestamp AS Timestamp,
        CASE WHEN FavoriteClips.ClipID IS NOT NULL THEN 1 ELSE 0 END AS IsFavorite
    FROM Clips
    {favorites_join}
    LEFT JOIN ClipTags ON Clips.ID = ClipTags.ClipID
    LEFT JOIN Tags ON ClipTags.TagID = Tags.ID
    WHERE ({keyword_clauses}) AND ({tag_clauses}) AND ({app_clauses}) AND ({time_condition}) AND Clips.ID > ?
    GROUP BY Clips.ID, Clips.Content, Clips.FromAppName, Clips.Timestamp
    ORDER BY Clips.ID DESC;
    """

    return sql_query, [*keyword_params, *tag_params, *app_params, after_id]

def filter_n_clips_before_id_query(filters: Filters, *, n: int | None = None, before_id: int) -> tuple[str, list]:
    """Construct a SQL query to filter a specific number of clips based on keywords and time frame, starting before a specific ID."""

    keyword_clauses, keyword_params = build_keywords_where_clause(filters.search)
    tag_clauses, tag_params = build_tags_where_clause(filters.selected_tags)
    app_clauses, app_params = build_apps_where_clause(filters.selected_apps)
    join_favorites: str = construct_favorites_join_clause(filters.favorites_only)
    time_condition: str = construct_time_condition(filters.time_frame)

    favorites_join = join_favorites or "LEFT JOIN FavoriteClips ON Clips.ID = FavoriteClips.ClipID"
    sql_query: str = f"""
    SELECT
        Clips.ID AS ClipID,
        Clips.Content AS Content,
        Clips.FromAppName AS FromAppName,
        GROUP_CONCAT(Tags.Name, ',') AS Tags,
        Clips.Timestamp AS Timestamp,
        CASE WHEN FavoriteClips.ClipID IS NOT NULL THEN 1 ELSE 0 END AS IsFavorite
    FROM Clips
    {favorites_join}
    LEFT JOIN ClipTags ON Clips.ID = ClipTags.ClipID
    LEFT JOIN Tags ON ClipTags.TagID = Tags.ID
    WHERE ({keyword_clauses}) AND ({tag_clauses}) AND ({app_clauses}) AND ({time_condition}) AND Clips.ID < ?
    GROUP BY Clips.ID, Clips.Content, Clips.FromAppName, Clips.Timestamp
    ORDER BY Clips.ID DESC
    LIMIT COALESCE(?, 999999);
    """

    return sql_query, [*keyword_params, *tag_params, *app_params, before_id, n]

def get_num_filtered_clips_query(filters: Filters) -> tuple[str, list]:
    """Construct a SQL query to count the number of filtered clips based on keywords and time frame."""

    keyword_clauses, keyword_params = build_keywords_where_clause(filters.search)
    tag_clauses, tag_params = build_tags_where_clause(filters.selected_tags)
    app_clauses, app_params = build_apps_where_clause(filters.selected_apps)
    join_favorites: str = construct_favorites_join_clause(filters.favorites_only)
    time_condition: str = construct_time_condition(filters.time_frame)

    sql_query: str = f"""
    SELECT COUNT(DISTINCT Clips.ID)
    FROM Clips
    {join_favorites}
    LEFT JOIN ClipTags ON Clips.ID = ClipTags.ClipID
    LEFT JOIN Tags ON ClipTags.TagID = Tags.ID
    WHERE ({keyword_clauses}) AND ({tag_clauses}) AND ({app_clauses}) AND ({time_condition})
    """

    return sql_query, [*keyword_params, *tag_params, *app_params]

# Query utilities
def build_keywords_where_clause(search: str) -> tuple[str, list]:
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

def build_tags_where_clause(selected_tags: list[str]) -> tuple[str, list]:
    """Build the WHERE clause for the tag search using parameterized queries."""

    # Construct the keyword clauses and parameters
    tag_clauses_list = []
    params = []
    for tag in selected_tags:
        tag_clauses_list.append("Name LIKE ?")
        params.append(f"%{tag}%")

    if tag_clauses_list:
        tag_clauses = " OR ".join(tag_clauses_list)
    else:
        tag_clauses = "1=1"  # No selected tags, match all

    return tag_clauses, params


def build_apps_where_clause(selected_apps: list[str]) -> tuple[str, list]:
    """Build the WHERE clause for filtering by source application (FromAppName)."""
    if not selected_apps:
        return "1=1", []
    clauses = ["FromAppName = ?" for _ in selected_apps]
    return " OR ".join(clauses), selected_apps


def construct_favorites_join_clause(favoritesOnly: bool) -> str:
    """Construct the JOIN clause for favorite clips."""

    return "INNER JOIN FavoriteClips ON Clips.ID = FavoriteClips.ClipID" if favoritesOnly else ""

def construct_time_condition(time_frame: str) -> str:
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
