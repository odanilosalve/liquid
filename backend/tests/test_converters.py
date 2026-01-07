import pytest
from converters import calculate_conversion


class TestCalculateConversion:
    def test_simple_conversion(self):
        result = calculate_conversion(100, 5.2)
        assert result == 520.0

    def test_conversion_with_decimals(self):
        result = calculate_conversion(100.5, 5.2)
        assert result == 522.6

    def test_rounding_two_decimals(self):
        result = calculate_conversion(100, 5.234567)
        assert result == 523.46

    def test_zero_amount(self):
        result = calculate_conversion(0, 5.2)
        assert result == 0.0

    def test_zero_rate(self):
        result = calculate_conversion(100, 0)
        assert result == 0.0

    def test_negative_amount(self):
        result = calculate_conversion(-100, 5.2)
        assert result == -520.0

    def test_negative_rate(self):
        result = calculate_conversion(100, -5.2)
        assert result == -520.0

    def test_small_amount(self):
        result = calculate_conversion(0.01, 5.2)
        assert result == 0.05

    def test_large_amount(self):
        result = calculate_conversion(1000000, 5.2)
        assert result == 5200000.0

    def test_precise_rounding(self):
        result = calculate_conversion(1.11, 2.22)
        assert result == 2.46

