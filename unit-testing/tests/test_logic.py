import pytest
from app.logic import is_eligible_for_loan



def test_eligible_user():
    assert is_eligible_for_loan(60000, 30, 'employed') == True


def test_underage_user():
    assert is_eligible_for_loan(60000, 18, 'employed') == False


def test_low_income_user():
    assert is_eligible_for_loan(40000, 30, 'employed') == False


def test_unemployed_user():
    assert is_eligible_for_loan(60000, 30, 'unemployed') == False


def test_boundary_case():
    assert is_eligible_for_loan(50000 , 21 , 'employed') == True

