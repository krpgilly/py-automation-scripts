# TODO: write tests for normalize_price() function
# TODO: test rounding, missing data, weird formats

from normalize import normalize_price

def test_basic():
    assert normalize_price("£1.00", "100g") == 1.0

def test_double_weight():
    assert normalize_price("£2.00", "200g") == 1.0

def test_weird_spacing():
    assert normalize_price(" £1.50 ", " 150g ") == 1.0

def test_rounding():
    assert normalize_price("£1.49", "200g") == 0.745