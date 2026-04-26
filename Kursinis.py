"""Roman and Decimal Number Converter System OOP Coursework 2026"""

from abc import ABC, abstractmethod


# ABSTRACTION: Abstract base class

class BaseConverter(ABC):
    """Abstract base class defining the converter interface."""

    @abstractmethod
    def convert(self, value: str) -> str:
        """Convert the given value and return the result as a string."""

    @abstractmethod
    def validate(self, value: str) -> bool:
        """Validate whether the given value is acceptable input."""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"


# ENCAPSULATION: Data and logic hidden inside classes

class RomanToDecimalConverter(BaseConverter):
    """Converts Roman numeral strings to decimal integers."""

    # Private class-level mapping
    _roman_values: dict = {
        "I": 1, "V": 5, "X": 10, "L": 50,
        "C": 100, "D": 500, "M": 1000,
    }

    def validate(self, value: str) -> bool:
        """Return True if value is a non-empty string of valid Roman characters."""
        if not isinstance(value, str) or not value.strip():
            return False
        return all(ch in self._roman_values for ch in value.upper().strip())

    def convert(self, value: str) -> str:
        """Convert a Roman numeral string to its decimal string representation."""
        roman = value.upper().strip()
        result = 0
        prev = 0
        for ch in reversed(roman):
            curr = self._roman_values[ch]
            if curr < prev:
                result -= curr
            else:
                result += curr
            prev = curr
        return str(result)


class DecimalToRomanConverter(BaseConverter):
    """Converts decimal integers to Roman numeral strings."""

    # Private ordered list of (value, symbol) pairs
    _decimal_map: list = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"),  (90, "XC"), (50, "L"),  (40, "XL"),
        (10, "X"),   (9, "IX"),  (5, "V"),   (4, "IV"),
        (1, "I"),
    ]

    def validate(self, value: str) -> bool:
        """Return True if value is a decimal integer string in range [1, 3999]."""
        try:
            n = int(value.strip())
            return 1 <= n <= 3999
        except (ValueError, AttributeError):
            return False

    def convert(self, value: str) -> str:
        """Convert a decimal integer string to its Roman numeral representation."""
        n = int(value.strip())
        result = ""
        for decimal_val, symbol in self._decimal_map:
            while n >= decimal_val:
                result += symbol
                n -= decimal_val
        return result


# INHERITANCE: Specialised converters extend BaseConverter

class VerboseRomanToDecimalConverter(RomanToDecimalConverter):
    """
    Inherits from RomanToDecimalConverter and adds a step-by-step explanation
    of the conversion process.
    """

    def convert(self, value: str) -> str:
        """Return a verbose breakdown of the Roman-to-decimal conversion."""
        roman = value.upper().strip()
        steps = []
        result = 0
        prev = 0
        for ch in reversed(roman):
            curr = self._roman_values[ch]
            if curr < prev:
                steps.append(f"  {ch}({curr}) < previous({prev})  →  subtract {curr}")
                result -= curr
            else:
                steps.append(f"  {ch}({curr})  →  add {curr}")
                result += curr
            prev = curr
        breakdown = "\n".join(reversed(steps))
        return f"{roman} =\n{breakdown}\n  ──────\n  Total = {result}"


class VerboseDecimalToRomanConverter(DecimalToRomanConverter):
    """
    Inherits from DecimalToRomanConverter and adds a step-by-step explanation
    of the conversion process.
    """

    def convert(self, value: str) -> str:
        """Return a verbose breakdown of the decimal-to-Roman conversion."""
        n = int(value.strip())
        original = n
        steps = []
        result = ""
        for decimal_val, symbol in self._decimal_map:
            while n >= decimal_val:
                steps.append(f"  {n} >= {decimal_val}  →  append '{symbol}'  (remaining: {n - decimal_val})")
                result += symbol
                n -= decimal_val
        breakdown = "\n".join(steps)
        return f"{original} =\n{breakdown}\n  ──────\n  Result = {result}"


# DESIGN PATTERN: Factory Method

class ConverterFactory:
    """
    Factory Method pattern: creates the correct BaseConverter subclass
    based on the requested conversion mode.

    Why Factory Method?
    - The caller does not need to know which concrete class to instantiate.
    - Adding new converter types requires only a new branch here, not changes
      throughout the codebase.
    - Singleton would only help if we needed a single shared instance; here we
      may want independent converter objects per session.
    """

    @staticmethod
    def create(mode: str, verbose: bool = False) -> BaseConverter:
        """
        Return a converter instance for the given mode.

        Parameters
        ----------
        mode : str
            'rtd'  – Roman to Decimal
            'dtr'  – Decimal to Roman
        verbose : bool
            If True, return a verbose variant that shows each step.
        """
        mode = mode.lower().strip()
        if mode == "rtd":
            return VerboseRomanToDecimalConverter() if verbose else RomanToDecimalConverter()
        if mode == "dtr":
            return VerboseDecimalToRomanConverter() if verbose else DecimalToRomanConverter()
        raise ValueError(f"Unknown converter mode: '{mode}'. Use 'rtd' or 'dtr'.")



# COMPOSITION: ConversionSession owns a converter

class ConversionSession:
    """
    Manages a single user session.

    Demonstrates *composition*: a ConversionSession **has-a** BaseConverter
    and a ConversionHistory.  The session owns both objects; they do not
    exist independently.
    """

    def __init__(self, converter: BaseConverter) -> None:
        self._converter: BaseConverter = converter
        self._history: "ConversionHistory" = ConversionHistory()

    def run(self, value: str) -> str:
        """Validate, convert, record, and return the result."""
        if not self._converter.validate(value):
            raise ValueError(f"Invalid input for {self._converter}: '{value}'")
        result = self._converter.convert(value)
        self._history.add(value, result)
        return result

    def get_history(self) -> list:
        return self._history.entries

    def clear_history(self) -> None:
        self._history.clear()


# AGGREGATION: ConversionHistory can exist independently

class ConversionHistory:
    """
    Stores past conversions.

    Demonstrates *aggregation*: ConversionHistory objects can be created and
    used outside a ConversionSession (e.g. loaded from a file).
    """

    def __init__(self) -> None:
        self._entries: list[dict] = []

    @property
    def entries(self) -> list[dict]:
        return list(self._entries)

    def add(self, input_value: str, output_value: str) -> None:
        self._entries.append({"input": input_value, "output": output_value})

    def clear(self) -> None:
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)

    def __repr__(self) -> str:
        return f"ConversionHistory({len(self._entries)} entries)"


# POLYMORPHISM: Demonstrated in ConverterApp

class ConverterApp:
    """
    Top-level application class.

    Calls converter.convert() on different BaseConverter subclasses through
    a single reference – this is polymorphism in action.
    """

    def __init__(self) -> None:
        self._factory = ConverterFactory()

    # ── File I/O ──────────────────────────────
    def save_history(self, history: list[dict], filepath: str) -> None:
        """Write conversion history to a CSV file."""
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write("input,output\n")
            for entry in history:
                fh.write(f"{entry['input']},{entry['output']}\n")

    def load_history(self, filepath: str) -> list[dict]:
        """Read conversion history from a CSV file."""
        entries = []
        with open(filepath, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
        for line in lines[1:]:          # skip header
            line = line.strip()
            if "," in line:
                parts = line.split(",", 1)
                entries.append({"input": parts[0], "output": parts[1]})
        return entries

    # ── Interactive CLI ───────────────────────
    def run_interactive(self) -> None:
        """Launch the interactive command-line interface."""
        print("=" * 50)
        print("  Roman ↔ Decimal Converter")
        print("=" * 50)

        mode = ""
        while mode not in ("1", "2"):
            print("\nSelect conversion direction:")
            print("  1. Roman  →  Decimal")
            print("  2. Decimal  →  Roman")
            mode = input("Choice (1/2): ").strip()

        verbose_input = input("Show step-by-step breakdown? (y/n): ").strip().lower()
        verbose = verbose_input == "y"

        converter_key = "rtd" if mode == "1" else "dtr"
        converter = ConverterFactory.create(converter_key, verbose)
        session = ConversionSession(converter)

        print(f"\nUsing: {converter}")
        print("Type 'quit' to exit, 'history' to view past conversions,")
        print("'save' to export history, or 'load' to import history.\n")

        while True:
            raw = input("Enter value: ").strip()

            if raw.lower() == "quit":
                break

            if raw.lower() == "history":
                entries = session.get_history()
                if not entries:
                    print("  (no history yet)")
                else:
                    for i, e in enumerate(entries, 1):
                        print(f"  {i}. {e['input']}  →  {e['output']}")
                continue

            if raw.lower() == "save":
                path = input("  File path (e.g. history.csv): ").strip()
                self.save_history(session.get_history(), path)
                print(f"  Saved to {path}")
                continue

            if raw.lower() == "load":
                path = input("  File path (e.g. history.csv): ").strip()
                loaded = self.load_history(path)
                print(f"  Loaded {len(loaded)} entries:")
                for e in loaded:
                    print(f"    {e['input']}  →  {e['output']}")
                continue

            try:
                result = session.run(raw)
                print(f"  Result: {result}\n")
            except ValueError as exc:
                print(f"  Error: {exc}\n")

        # Auto-save on exit if there is history
        entries = session.get_history()
        if entries:
            self.save_history(entries, "history.csv")
            print(f"\nHistory saved to history.csv ({len(entries)} entries).")

        print("Goodbye!")


# Entry point
if __name__ == "__main__":
    app = ConverterApp()
    app.run_interactive()