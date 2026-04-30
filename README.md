# Romėniškų ↔ Dešimtainių skaičių konvertavimo sistema

## 1. Įvadas

### Kas yra ši programa?

Ši programa yra Python pagrindu sukurta sistema, skirta skaičių konvertavimui tarp **romėniškų skaitmenų** ir **dešimtainės (sveikųjų skaičių) sistemos**. Ji palaiko abipusį konvertavimą ir gali pateikti žingsnis po žingsnio paaiškinimus, kaip atliekamas skaičiavimas.

---

### Kaip paleisti programą

1. Įsitikinkite, kad įdiegtas Python 3.
2. Atidarykite terminalą projekto aplanke.
3. Paleiskite komandą:

```bash
python app/main.py
```

---

### Kaip naudotis programa

* Pasirinkite konvertavimo tipą:

  * `1` → Romėniški → Dešimtainiai
  * `2` → Dešimtainiai → Romėniški
* Pasirinkite, ar rodyti žingsnius (verbose režimas).
* Įveskite norimą skaičių.
* Galimos komandos:

  * `history` → peržiūrėti istoriją
  * `save` → išsaugoti istoriją
  * `load` → įkelti istoriją
  * `quit` → išeiti iš programos

---

## 2. Analizė

### Funkciniai reikalavimai

Sistema įgyvendina šias funkcijas:

* Romėniškų skaičių konvertavimas į dešimtainius
* Dešimtainių skaičių konvertavimas į romėniškus
* Įvesties validacija
* Konvertavimo istorijos saugojimas
* Duomenų įrašymas ir nuskaitymas iš CSV failų
* Komandinės eilutės sąsaja (CLI)

---

### Objektinio programavimo principai

#### 1. Abstrakcija

Abstrakcija realizuota naudojant `BaseConverter` abstrakčią klasę, kuri apibrėžia bendrą sąsają:

* `convert()`
* `validate()`

---

#### 2. Inkapsuliacija

Duomenys slepiami klasėse:

* `_roman_values` – romėniškų reikšmių žodynas
* `_decimal_map` – konvertavimo lentelė
* `_entries` – istorijos įrašai

---

#### 3. Paveldėjimas

Paveldėjimas naudojamas funkcionalumui plėsti:

* `VerboseRomanToDecimalConverter` paveldi `RomanToDecimalConverter`
* `VerboseDecimalToRomanConverter` paveldi `DecimalToRomanConverter`

---

#### 4. Polimorfizmas

Polimorfizmas leidžia naudoti bendrą sąsają:

```python
converter.convert(value)
```

Nepriklausomai nuo konkrečios klasės.

---

### Dizaino šablonas: Factory Method

Naudojamas `ConverterFactory`.

Privalumai:

* Slėpia objektų kūrimo logiką
* Palengvina sistemos plėtimą
* Pagerina kodo lankstumą

---

### Kompozicija ir agregacija

**Kompozicija:**

* `ConversionSession` valdo konverterį ir istoriją

**Agregacija:**

* `ConversionHistory` gali egzistuoti atskirai

---

### Failų valdymas

* Istorija išsaugoma CSV formatu
* Istorija įkeliama iš CSV failo

---

### Testavimas

Naudojamas `unittest`:

* Konversijų tikrinimas
* Validacija
* Factory testavimas
* Sesijos logikos testai

---

## 3. Rezultatai

* Sistema sėkmingai konvertuoja skaičius abiem kryptimis
* Įvesties validacija apsaugo nuo klaidų
* Verbose režimas pagerina supratimą
* Didžiausias iššūkis – romėniškų skaičių atimties taisyklės

---

## 4. Išvados

Projektas demonstruoja objektinio programavimo principų taikymą Python kalboje.

### Pasiekimai

* Įgyvendinti visi OOP principai
* Pritaikytas Factory Method šablonas
* Sukurta CLI programa
* Realizuotas failų saugojimas ir testavimas

### Ateities tobulinimai

* Grafinė sąsaja (GUI)
* Platesnis skaičių intervalas
* Patobulinta validacija
* JSON eksportas

---

## 5. Literatūra

* [https://docs.python.org/3/](https://docs.python.org/3/)
* [https://realpython.com/python3-object-oriented-programming/](https://realpython.com/python3-object-oriented-programming/)
* [https://refactoring.guru/design-patterns](https://refactoring.guru/design-patterns)

---

# 6. Kodo fragmentas (OOP įgyvendinimas)

Žemiau pateikiu svarbiausias sistemos kodo fragmentus, demonstruojančius **abstrakciją, paveldėjimą ir inkapsuliaciją**:

```python
from abc import ABC, abstractmethod

# ABSTRAKCIJA
class BaseConverter(ABC):

    @abstractmethod
    def convert(self, value: str) -> str:
        pass

    @abstractmethod
    def validate(self, value: str) -> bool:
        pass


# INKAPSULIACIJA + KONKRETUS REALIZAVIMAS
class RomanToDecimalConverter(BaseConverter):

    _roman_values = {
        "I": 1, "V": 5, "X": 10,
        "L": 50, "C": 100, "D": 500, "M": 1000
    }

    def validate(self, value: str) -> bool:
        return all(ch in self._roman_values for ch in value.upper())

    def convert(self, value: str) -> str:
        roman = value.upper()
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


