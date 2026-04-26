# Roman ↔ Decimal Converter System

## 1. Introduction

### What is this application?

This application is a Python-based system designed to convert numbers between **Roman numerals** and **decimal (integer) format**. It supports both conversion directions and provides optional step-by-step explanations of how the conversion is performed.

### How to run the program

1. Make sure Python 3 is installed.
2. Open a terminal in the project directory.
3. Run the following command:

```bash
python app/main.py
```

### How to use the program

* Choose conversion type:

  * `1` → Roman to Decimal
  * `2` → Decimal to Roman
* Choose whether to enable verbose mode (step-by-step explanation).
* Enter values to convert.
* Available commands:

  * `history` → view previous conversions
  * `save` → save history to file
  * `load` → load history from file
  * `quit` → exit program

---

## 2. Body / Analysis

### Functional Requirements Implementation

The system fulfills the required functionality by:

* Converting Roman numerals to decimal numbers
* Converting decimal numbers to Roman numerals
* Validating user input before conversion
* Storing conversion history
* Saving and loading data from CSV files
* Providing an interactive command-line interface

---

### Object-Oriented Programming Principles

#### 1. Abstraction

Abstraction is implemented using the `BaseConverter` abstract class.
It defines the interface for all converters:

* `convert()`
* `validate()`

This ensures all converter classes follow a consistent structure.

---

#### 2. Encapsulation

Encapsulation is used by hiding internal data inside classes:

* `_roman_values` dictionary
* `_decimal_map` list
* `_entries` in history

These are accessed only through class methods, protecting internal logic.

---

#### 3. Inheritance

Inheritance is used to extend functionality:

* `VerboseRomanToDecimalConverter` inherits from `RomanToDecimalConverter`
* `VerboseDecimalToRomanConverter` inherits from `DecimalToRomanConverter`

This allows reuse of logic while adding new behavior (step-by-step explanation).

---

#### 4. Polymorphism

Polymorphism is demonstrated when different converter objects are used through a single interface:

```python
converter.convert(value)
```

The program does not need to know which specific converter class is used.

---

### Design Pattern: Factory Method

The system uses the **Factory Method pattern** via `ConverterFactory`.

#### Why Factory Method?

* It hides object creation logic from the user
* Makes the system more flexible
* Allows easy addition of new converter types

Example:

```python
converter = ConverterFactory.create("rtd", verbose=True)
```

---

### Composition and Aggregation

#### Composition

* `ConversionSession` contains a converter and history
* These objects exist only within the session

#### Aggregation

* `ConversionHistory` can exist independently
* It can be reused or loaded from external sources

---

### File Handling

The program supports:

* Saving history to a CSV file
* Loading history from a CSV file

This is implemented using standard file operations in Python.

---

### Testing

Core functionality is tested using the `unittest` framework:

* Conversion correctness
* Input validation
* Factory behavior
* Session and history logic

Tests can be run using:

```bash
python -m unittest
```

---

## 3. Results

* The system successfully converts values between Roman and decimal formats.
* Input validation prevents incorrect or invalid data.
* The verbose mode improves understanding of conversion logic.
* One challenge was handling Roman numeral subtraction rules correctly.
* The modular design made the code easier to extend and maintain.

---

## 4. Conclusions

This project demonstrates the practical use of object-oriented programming principles in Python.
The system is flexible, maintainable, and easy to extend.

### Achievements

* Implemented all OOP principles
* Applied a design pattern (Factory Method)
* Built a working CLI application
* Added file persistence and testing

### Future Improvements

* Add a graphical user interface (GUI)
* Support larger number ranges
* Improve Roman numeral validation rules
* Add more export formats (e.g., JSON)

---

## 5. References

* Python documentation: https://docs.python.org/3/
* OOP concepts: https://realpython.com/python3-object-oriented-programming/
* Design patterns: https://refactoring.guru/design-patterns
