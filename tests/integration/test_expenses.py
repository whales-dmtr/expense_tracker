import pytest

from tests.integration.conftest import client
from app.schemas import ExpenseDataModified, ExpenseData

url_expense = '/expense'
url_expense_with_id = '/expense/%i'
url_expenses = '/expenses'


def get_expense(id, access_token):
    url = url_expense_with_id % (id,)
    response = client.get(url, headers=access_token)
    return response


def get_expenses(access_token):
    response = client.get(url_expenses, headers=access_token)
    return response


def modify_expense(access_token, id, expense_data: ExpenseDataModified):
    url = url_expense_with_id % (id,)
    data = dict(expense_data)
    response = client.put(url, headers=access_token, json=data)
    return response


def delete_expense(access_token, id):
    url = url_expense_with_id % id
    response = client.delete(url, headers=access_token)
    return response


def test_get_expense(access_token, expense_id):
    assert get_expense(expense_id, access_token).status_code == 200


def test_get_nonexistent_expense(access_token):
    assert get_expense(0, access_token).status_code == 404


def test_get_expenses(access_token):
    assert get_expenses(access_token).status_code == 200


def test_modify_expense(access_token, expense_id):
    assert modify_expense(access_token, expense_id, 
                          ExpenseDataModified(amount=50.50))


def test_modify_nonexistent_expense(access_token):
    assert modify_expense(access_token, 0, 
                          ExpenseDataModified(amount=50.50))


def test_remove_expense(access_token, expense_id):
    assert delete_expense(access_token, expense_id)


def test_remove_nonexistent_expense(access_token, expense_id):
    assert delete_expense(access_token, 0)