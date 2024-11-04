#!/usr/bin/env python3
"""Module for testing utility functions."""

import unittest
from typing import Dict, Tuple, Union
from unittest.mock import patch, Mock
from parameterized import parameterized

from utils import (
    access_nested_map,
    get_json,
    memoize,
)


class AccessNestedMapTests(unittest.TestCase):
    """Unit tests for the `access_nested_map` function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_map_success(
            self,
            data: Dict,
            keys: Tuple[str],
            expected_value: Union[Dict, int],
            ) -> None:
        """Tests if `access_nested_map` returns the correct value."""
        self.assertEqual(access_nested_map(data, keys), expected_value)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_map_exception(
            self,
            data: Dict,
            keys: Tuple[str],
            expected_exception: Exception,
            ) -> None:
        """Tests if `access_nested_map` raises the correct exception."""
        with self.assertRaises(expected_exception):
            access_nested_map(data, keys)


class GetJsonTests(unittest.TestCase):
    """Unit tests for the `get_json` function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json_response(
            self,
            url: str,
            response_data: Dict,
            ) -> None:
        """Tests if `get_json` returns the expected JSON response."""
        mock_response = {'json.return_value': response_data}
        with patch("requests.get", return_value=Mock(**mock_response)) as mock_get:
            self.assertEqual(get_json(url), response_data)
            mock_get.assert_called_once_with(url)


class MemoizeTests(unittest.TestCase):
    """Unit tests for the `memoize` function."""

    def test_memoize_cache(self) -> None:
        """Tests if `memoize` caches the result of a method call."""

        class SampleClass:
            def compute_value(self):
                return 42

            @memoize
            def cached_property(self):
                return self.compute_value()

        with patch.object(
                SampleClass,
                "compute_value",
                return_value=lambda: 42,
                ) as mock_method:
            instance = SampleClass()
            self.assertEqual(instance.cached_property(), 42)
            self.assertEqual(instance.cached_property(), 42)
            mock_method.assert_called_once()
