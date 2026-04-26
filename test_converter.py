import unittest

from Kursinis import (
    RomanToDecimalConverter,
    DecimalToRomanConverter,
    ConversionSession,
    ConverterFactory
)


class TestRomanToDecimalConverter(unittest.TestCase):

    def setUp(self):
        self.converter = RomanToDecimalConverter()

    def test_valid_conversion(self):
        self.assertEqual(self.converter.convert("X"), "10")
        self.assertEqual(self.converter.convert("IV"), "4")
        self.assertEqual(self.converter.convert("MCMXC"), "1990")

    def test_lowercase_input(self):
        self.assertEqual(self.converter.convert("x"), "10")

    def test_invalid_input(self):
        self.assertFalse(self.converter.validate("ABC"))
        self.assertFalse(self.converter.validate(""))

    def test_validation_success(self):
        self.assertTrue(self.converter.validate("XVI"))


class TestDecimalToRomanConverter(unittest.TestCase):

    def setUp(self):
        self.converter = DecimalToRomanConverter()

    def test_valid_conversion(self):
        self.assertEqual(self.converter.convert("10"), "X")
        self.assertEqual(self.converter.convert("4"), "IV")
        self.assertEqual(self.converter.convert("1990"), "MCMXC")

    def test_invalid_input(self):
        self.assertFalse(self.converter.validate("0"))      # out of range
        self.assertFalse(self.converter.validate("4000"))   # out of range
        self.assertFalse(self.converter.validate("abc"))    # not a number

    def test_validation_success(self):
        self.assertTrue(self.converter.validate("3999"))


class TestConversionSession(unittest.TestCase):

    def test_session_history(self):
        converter = RomanToDecimalConverter()
        session = ConversionSession(converter)

        session.run("X")
        session.run("V")

        history = session.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["output"], "10")

    def test_invalid_input_raises(self):
        converter = RomanToDecimalConverter()
        session = ConversionSession(converter)

        with self.assertRaises(ValueError):
            session.run("INVALID")


class TestFactory(unittest.TestCase):

    def test_factory_rtd(self):
        converter = ConverterFactory.create("rtd")
        self.assertIsInstance(converter, RomanToDecimalConverter)

    def test_factory_dtr(self):
        converter = ConverterFactory.create("dtr")
        self.assertIsInstance(converter, DecimalToRomanConverter)

    def test_factory_invalid(self):
        with self.assertRaises(ValueError):
            ConverterFactory.create("unknown")


if __name__ == "__main__":
    unittest.main()