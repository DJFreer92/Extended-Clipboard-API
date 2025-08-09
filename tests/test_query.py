from app.core.db import execute_query
from app.core.db_constants import *

def run_test_query() -> None:
    execute_query(ADD_CLIP, ("abc",))
    execute_query(ADD_CLIP, ("123",))
    params: tuple[int] = (10,)
    rows: list = execute_query(GET_N_CLIPS, params)
    for row in rows:
        print(row)

if __name__ == "__main__":
    run_test_query()
