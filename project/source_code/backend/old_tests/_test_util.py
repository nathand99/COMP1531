import file_path
import pytest
from util import *

def test_merge_stock():
    a = [(1,2), (3,4)]
    b = [(3,2), (4,5)]
    assert merge_stock(a,b) == [(1,2), (3,6), (4,5)]

def test_cancel_stock():
    a = [(1,2), (3,4)]
    b = [(3,2), (4,5)]
    assert cancel_stock(a,b) == [(1,2), (3,2), (4,-5)]

def test_is_contain_stock():
    a = [(1,2), (3,4)]
    b = [(3,4)]
    assert is_contain_stock(a,b)
    assert not is_contain_stock(b,a)