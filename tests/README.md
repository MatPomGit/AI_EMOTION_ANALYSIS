# Testy

Ten folder zawiera testy dla aplikacji AI_EMOTION_ANALYSIS.

## Struktura

```
tests/
├── README.md           # Ten plik
└── test_basic.py       # Podstawowe testy przykładowe
```

## Jak uruchomić testy

### Instalacja pytest

```bash
pip install pytest pytest-cov
```

### Uruchomienie testów

```bash
# Wszystkie testy
pytest tests/

# Z szczegółowym wyjściem
pytest tests/ -v

# Z pokryciem kodu
pytest tests/ --cov=emo
```

## Dodawanie nowych testów

1. Utwórz nowy plik `test_*.py` w tym folderze
2. Zaimplementuj funkcje testowe zaczynające się od `test_`
3. Użyj `assert` do weryfikacji wyników
4. Uruchom pytest

## Notatki

- To jest podstawowa struktura testów dla celów edukacyjnych
- W pełnym projekcie należałoby dodać więcej testów
- Użyj mocków dla zewnętrznych API i zależności
