from abc import ABC, abstractmethod


class BaseConverter(ABC):

    @abstractmethod
    def convert(self, value: str) -> str:
        pass

    @abstractmethod
    def validate(self, value: str) -> bool:
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"


class RomanToDecimalConverter(BaseConverter):

    _roman_values: dict = {
        "I": 1, "V": 5, "X": 10, "L": 50,
        "C": 100, "D": 500, "M": 1000,
    }

    def validate(self, value: str) -> bool:
        if not isinstance(value, str) or not value.strip():
            return False
        return all(ch in self._roman_values for ch in value.upper().strip())

    def convert(self, value: str) -> str:
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

    _decimal_map: list = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"),
        (1, "I"),
    ]

    def validate(self, value: str) -> bool:
        try:
            n = int(value.strip())
            return 1 <= n <= 3999
        except (ValueError, AttributeError):
            return False

    def convert(self, value: str) -> str:
        n = int(value.strip())
        result = ""
        for decimal_val, symbol in self._decimal_map:
            while n >= decimal_val:
                result += symbol
                n -= decimal_val
        return result


class VerboseRomanToDecimalConverter(RomanToDecimalConverter):

    def convert(self, value: str) -> str:
        roman = value.upper().strip()
        steps = []
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


class VerboseDecimalToRomanConverter(DecimalToRomanConverter):

    def convert(self, value: str) -> str:
        n = int(value.strip())
        result = ""
        for decimal_val, symbol in self._decimal_map:
            while n >= decimal_val:
                result += symbol
                n -= decimal_val
        return result


class ConverterFactory:

    @staticmethod
    def create(mode: str, verbose: bool = False) -> BaseConverter:
        mode = mode.lower().strip()
        if mode == "rtd":
            return VerboseRomanToDecimalConverter() if verbose else RomanToDecimalConverter()
        if mode == "dtr":
            return VerboseDecimalToRomanConverter() if verbose else DecimalToRomanConverter()
        raise ValueError(f"Unknown converter mode: '{mode}'")


class ConversionSession:

    def __init__(self, converter: BaseConverter) -> None:
        self._converter = converter
        self._history = ConversionHistory()

    def run(self, value: str) -> str:
        if not self._converter.validate(value):
            raise ValueError(f"Invalid input for {self._converter}: '{value}'")
        result = self._converter.convert(value)
        self._history.add(value, result)
        return result

    def get_history(self) -> list:
        return self._history.entries

    def clear_history(self) -> None:
        self._history.clear()


class ConversionHistory:

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


class ConverterApp:

    def __init__(self) -> None:
        self._factory = ConverterFactory()

    def save_history(self, history: list[dict], filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write("input,output\n")
            for entry in history:
                fh.write(f"{entry['input']},{entry['output']}\n")

    def load_history(self, filepath: str) -> list[dict]:
        entries = []
        with open(filepath, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
        for line in lines[1:]:
            line = line.strip()
            if "," in line:
                parts = line.split(",", 1)
                entries.append({"input": parts[0], "output": parts[1]})
        return entries

    def run_interactive(self) -> None:
        print("=" * 50)
        print("  Roman ↔ Decimal Converter")
        print("=" * 50)

        mode = ""
        while mode not in ("1", "2"):
            mode = input("Choice (1/2): ").strip()

        verbose = input("Verbose? (y/n): ").strip().lower() == "y"

        converter_key = "rtd" if mode == "1" else "dtr"
        converter = ConverterFactory.create(converter_key, verbose)
        session = ConversionSession(converter)

        while True:
            raw = input("Enter value: ").strip()

            if raw.lower() == "quit":
                break

            if raw.lower() == "history":
                entries = session.get_history()
                for i, e in enumerate(entries, 1):
                    print(f"{i}. {e['input']} → {e['output']}")
                continue

            if raw.lower() == "save":
                path = input("File: ").strip()
                self.save_history(session.get_history(), path)
                continue

            if raw.lower() == "load":
                path = input("File: ").strip()
                loaded = self.load_history(path)
                for e in loaded:
                    print(f"{e['input']} → {e['output']}")
                continue

            try:
                print(session.run(raw))
            except ValueError as exc:
                print(exc)

        print("Goodbye!")


if __name__ == "__main__":
    ConverterApp().run_interactive()
