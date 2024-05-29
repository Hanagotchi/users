from fastapi import Query
from typing import Optional


def get_query_params(query_params_dic: dict):
    filters = {}
    for filterName, value in query_params_dic.items():
        if value is not None:
            filters[filterName] = value.lower() if value is str else value
    return filters


class GetUsersQueryParams:
    def __init__(
        self,
        offset: Optional[int] = Query(0, ge=0),
        limit: Optional[int] = Query(200, le=200),
        ids: Optional[str] = Query(None),
        nickname: Optional[str] = Query(None),
    ):
        self.query_params = {
            'offset': offset,
            'limit': limit,
            'ids': ids,
            'nickname': nickname
        }

    def get_query_params(self):
        return get_query_params(self.query_params)
