import pytest

from tests.integration.conftest import client, create_expense
from app.schemas import ExpenseData


def search(access_token, query):
    data = {"query": query}
    response = client.get('/expenses/search', headers=access_token, params=data)
    return response


def regex_search(access_token, pattern, flags=None):
    data = {"pattern": pattern}
    if flags:
        data["flags"] = flags
    response = client.get('/expenses/search/regex', headers=access_token, 
                          params=data)
    return response


def test_search(access_token):
    assert len(search(access_token, 'lime').json()) == 3


def test_regex_search(access_token):
    assert regex_search(access_token, '(lime)+').json()[0]["description"] == \
    "lime lime lime"


def test_regex_search_with_flags(access_token):
    assert regex_search(access_token, '(lime)+', 'gi').json()[0]["description"] == \
    "lime lime lime"


def test_regex_search_invalid_pattern(access_token):
    assert regex_search(access_token, '+').status_code == 400


def test_regex_search_invalid_flags(access_token):
    assert regex_search(access_token, '.*', 'flag').status_code == 400


def test_regex_search_no_global_flag(access_token):
    assert regex_search(access_token, '.*', 'i').status_code == 200