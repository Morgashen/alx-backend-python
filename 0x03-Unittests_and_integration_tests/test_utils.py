#!/usr/bin/env python3
"""Familiarize yourself with the utils.access_nested_map function and
understand its purpose. Play with it in the Python console to make
sure you understand.
In this task you will write the first unit test for utils.access_nested_map.
Create a TestAccessNestedMap class that inherits from unittest.TestCase.
Implement the TestAccessNestedMap.test_access_nested_map method to test that
the method returns what it is supposed to.
Decorate the method with @parameterized.expand to test the function for
ollowing inputs:
nested_map={"a": 1}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a", "b")
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock
def access_nested_map(nested_map, path):
"""
Accesses a nested map with a tuple of keys.
Args:
nested_map (dict): A nested map.
path (tuple): A tuple of keys to access a value in the nested map.
Returns:
The value stored in the nested map.
"""
current_map = nested_map
for key in path:
if isinstance(current_map, dict):
current_map = current_map.get(key)
else:
raise KeyError
return current_map
def get_json(url):
"""
Retrieves JSON data from a URL.
Args:
url (str): The URL to retrieve the JSON data from.
Returns:
dict: The JSON data as a dictionary.
"""
import requests
response = requests.get(url)
return response.json()
def memoize(func):
"""
A decorator that memoizes the results of a function.
Args:
func (callable): The function to be memoized.
Returns:
callable: The memoized function.
"""
cache = {}
def wrapper(*args):
if args in cache:
return cache[args]
else:
result = func(*args)
cache[args] = result
return result
return wrapper
class TestAccessNestedMap(unittest.TestCase):
"""
Test cases for the access_nested_map function.
"""
@parameterized.expand([
({"a": 1}, ("a",), 1),
({"a": {"b": 2}}, ("a",), {"b": 2}),
({"a": {"b": 2}}, ("a", "b"), 2)
])
def test_access_nested_map(self, nested_map, path, expected_output):
"""
Test the access_nested_map function.
"""
result = access_nested_map(nested_map, path)
self.assertEqual(result, expected_output)

@parameterized.expand([
    ({}, ("a",), KeyError),
    ({"a": 1}, ("a", "b"), KeyError)
])
def test_access_nested_map_exception(self, nested_map, path, expected_output):
    """
    Test that access_nested_map raises the expected exception.
    """
    with self.assertRaises(expected_output) as context:
        access_nested_map(nested_map, path)
class TestGetJson(unittest.TestCase):
"""
Test cases for the get_json function.
"""
@parameterized.expand([
('http://example.com', {'payload': True}),
('http://holberton.io', {'payload': False})
])
def test_get_json(self, url, expected_output):
"""
Test the get_json function.
"""
mock_response = Mock()
mock_response.json.return_value = expected_output
with patch('requests.get', return_value=mock_response):
response = get_json(url)
self.assertEqual(response, expected_output)
class TestMemoize(unittest.TestCase):
"""
Test cases for the memoize decorator.
"""
def test_memoize(self):
"""
Test the memoize decorator.
"""
class TestClass:
def a_method(self):
return 42

@memoize
        def a_property(self):
            return self.a_method()

    test_obj = TestClass()
    with patch.object(test_obj, 'a_method') as mock_method:
        mock_method.return_value = 42
        result1 = test_obj.a_property
        result2 = test_obj.a_property
        self.assertEqual(result1, 42)
        self.assertEqual(result2, 42)
        mock_method.assert_called_once()
