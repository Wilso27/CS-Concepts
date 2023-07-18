# test_specs.py


import specs
import pytest


def test_add():
    assert specs.add(1, 3) == 4, "failed on positive integers"
    assert specs.add(-5, -7) == -12, "failed on negative integers"
    assert specs.add(-6, 14) == 8


def test_divide():
    assert specs.divide(4,2) == 2, "integer division"
    assert specs.divide(5,4) == 1.25, "float division"
    with pytest.raises(ZeroDivisionError) as excinfo:
        specs.divide(4, 0)
    assert excinfo.value.args[0] == "second input cannot be zero"


def test_smallest_factor():
    #try the 1 case, prime case, smallest prime case, odd square case
    assert specs.smallest_factor(7) == 7, "1 is not prime"
    assert specs.smallest_factor(1) == 1, '1 returns 1'
    assert specs.smallest_factor(2) == 2, '2 is the smallest'
    assert specs.smallest_factor(9) == 3, '3 is the smallest'


def test_month_length():
    assert specs.month_length('September') == 30, '30 days'
    assert specs.month_length('January') == 31, '31 days'
    assert specs.month_length('February') == 28, 'not leap year'
    assert specs.month_length('February',True) == 29, 'leap year'
    assert specs.month_length('lol') is None, 'invalid input'


def test_operate():
    pytest.raises(TypeError, specs.operate,a=4,b=3,oper=5)
    assert specs.operate(5,4,'+') == 9, 'Addition ++'
    assert specs.operate(-5,-4,'+') == -9, 'Addition --'
    assert specs.operate(-5,4,'+') == -1, 'Addition -+'
    assert specs.operate(5,4,'-') == 1, 'Subtraction ++'
    assert specs.operate(-5,-4,'-') == -1, 'Subtraction --'
    assert specs.operate(-5,4,'-') == -9, 'Subtraction -+'
    assert specs.operate(5,4,'*') == 20, 'Mult ++'
    assert specs.operate(-5,-4,'*') == 20, 'Mult --'
    assert specs.operate(-5,4,'*') == -20, 'Mult -+'
    assert specs.operate(5,2,'/') == 2.5, 'division ++'
    assert specs.operate(-5,-2,'/') == 2.5, 'division --'
    assert specs.operate(-5,2,'/') == -2.5, 'division -+'
    pytest.raises(ZeroDivisionError,specs.operate,a=4,b=0,oper='/')
    pytest.raises(ValueError,specs.operate,a=4,b=3,oper='p')


@pytest.fixture
def set_up_fractions():
    frac_1_3 = specs.Fraction(1, 3)
    frac_1_2 = specs.Fraction(1, 2)
    frac_n2_3 = specs.Fraction(-2, 3)
    return frac_1_3, frac_1_2, frac_n2_3


def test_fraction_init(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_3.numer == 1
    assert frac_1_2.denom == 2
    assert frac_n2_3.numer == -2
    frac = specs.Fraction(30, 42)
    assert frac.numer == 5
    assert frac.denom == 7
    pytest.raises(ZeroDivisionError,specs.Fraction,numerator=3,denominator=0)
    pytest.raises(TypeError,specs.Fraction,numerator='5',denominator=5)
    pytest.raises(TypeError,specs.Fraction,numerator='5',denominator='5')
    pytest.raises(TypeError,specs.Fraction,numerator=5,denominator='5')


def test_fraction_str(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    frac_4_1 = specs.Fraction(4,1)
    assert str(frac_1_3) == "1/3"
    assert str(frac_1_2) == "1/2"
    assert str(frac_n2_3) == "-2/3"
    assert str(frac_4_1) == "4"


def test_fraction_float(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert float(frac_1_3) == 1 / 3.
    assert float(frac_1_2) == .5
    assert float(frac_n2_3) == -2 / 3.


def test_fraction_eq(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2 == specs.Fraction(1, 2)
    assert frac_1_3 == specs.Fraction(2, 6)
    assert frac_n2_3 == specs.Fraction(8, -12)
    assert frac_1_2 == .5, 'float input'


def test_fraction_add(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2+frac_1_3 == specs.Fraction(5,6), 'addition'


def test_fraction_sub(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2-frac_1_3 == specs.Fraction(1,6), 'subtraction'


def test_fraction_mul(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2*frac_1_3 == specs.Fraction(1,6), 'multiplication'


def test_fraction_truediv(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2/frac_1_3 == specs.Fraction(3,2), 'division'
    with pytest.raises(ZeroDivisionError) as excinfo:
        specs.Fraction(1,4)/specs.Fraction(0,5)


def test_count_sets():
    #checks if there are 12
    with pytest.raises(ValueError) as excinfo:
        specs.count_sets( ["1022", "1122"])
    #checks uniqueness
    with pytest.raises(ValueError) as excinfo:
        specs.count_sets(["1122", "1122", "0100", "2021","0010", "2201", "2111", "0020","1102", "0210", "2110", "1020"])
    #checks number of digits in each set
    with pytest.raises(ValueError) as excinfo:
        specs.count_sets(["1022", "1122", "010", "2021","0010", "2201", "2111", "0020","1102", "0210", "2110", "1020"])
    #checks if base 3
    with pytest.raises(ValueError) as excinfo:
        specs.count_sets(["1022", "1122", "0100", "2021","0010", "2201", "2111", "0023","1102", "0210", "2110", "1020"])


def test_is_set():
    #checks if it isn't a set
    assert specs.is_set("1022", "1122", "0100") is False, 'Not set is wrong'
    assert specs.is_set("1022", "1122", "1222") is True, 'Is set is wrong'
