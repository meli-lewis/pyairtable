import pytest
from airtable.formulas import AND, EQUAL, FIELD, STR_VALUE, field_equals_value


def test_equal():
    assert EQUAL("A", "B") == "A=B"


def test_field():
    assert FIELD("Name") == "{Name}"


# @pytest.mark.parametrize(
#     "field_name,formula_value",
#     [
#         ("First Name", "{First Name}"),
#         ("Player's Age", "{Player's Age}"),
#         ('"Session" Winners', 'Session" Winners'),
#     ],
# )
# def test_field_escape(field_name, formula_value):
#     assert FIELD("Name") == "{Name}"


def test_and():
    assert AND("A", "B", "C") == "AND(A,B,C)"


def test_string_value():
    assert STR_VALUE("A") == "'A'"


def test_combination():
    formula = AND(
        EQUAL(FIELD("First Name"), STR_VALUE("A")),
        EQUAL(FIELD("Last Name"), STR_VALUE("B")),
        EQUAL(FIELD("Age"), STR_VALUE(15)),
    )
    assert formula == ("AND({First Name}='A',{Last Name}='B',{Age}='15')")


def test_field_equals_value():
    formula = field_equals_value("First Name", "John")
    assert formula == "{First Name}='John'"