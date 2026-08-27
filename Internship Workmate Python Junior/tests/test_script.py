import pytest 
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from script import parse_filter_condition, parse_aggregate_condition, filter_records

# pytest tests/test_script.py -v

def test_parse_filter_condition_eq():
    column, operation, value = parse_filter_condition("price=999")
    assert column == "price"
    assert operation == "eq"
    assert value == "999"

def test_parse_filter_condition_gt():
    column, operation, value = parse_filter_condition("price>500")
    assert column == "price"
    assert operation == "gt"
    assert value == "500"

def test_parse_filter_condition_lt():
    column, operation, value = parse_filter_condition("price<880")
    assert column == "price"
    assert operation == "lt"
    assert value == "880"

def test_parse_aggregate_condition():
    column, operation = parse_aggregate_condition("price=min")
    assert column == "price"
    assert operation == "min"

def test_filter_records_eq_numeric():
    data = [
        {"name": "iPhone", "price": "999"},
        {"name": "Galaxy", "price": "1199"},
        {"name": "Redmi", "price": "199"},
    ]

    result = filter_records(data, "price", "eq", "999")

    assert len(result) == 1
    assert result[0]["name"] == "iPhone"


def test_filter_records_gt_numeric():
    data = [
        {"name": "iPhone", "price": "999"},
        {"name": "Galaxy", "price": "1199"},
        {"name": "Redmi", "price": "199"},
    ]

    result = filter_records(data, "price", "gt", "500")

    assert len(result) == 2
    assert result[0]["name"] == "iPhone"
    assert result[1]["name"] == "Galaxy"

def test_filter_records_lt_numeric():
    data = [
        {"name": "iPhone", "price": "999"},
        {"name": "Galaxy", "price": "1199"},
        {"name": "Redmi", "price": "199"},
    ]

    result = filter_records(data, "price", "lt", "500")

    assert len(result) == 1
    assert result[0]["name"] == "Redmi"


def test_filter_records_eq_string(): 
    data = [
        {"name": "iPhone", "price": "999"},
        {"name": "Galaxy", "price": "1199"},
        {"name": "Redmi", "price": "199"},
    ]

    result = filter_records(data, "name", "eq", "iPhone")

    assert len(result) == 1
    assert result[0]["price"] == "999"