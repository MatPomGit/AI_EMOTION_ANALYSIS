# Analizator Emocji i Zachowania

## Wprowadzenie

**Analizator Emocji i Zachowania** to aplikacja stworzona w języku Python, która wykorzystuje zaawansowane biblioteki sztucznej inteligencji (DeepFace, MediaPipe) oraz framework do tworzenia aplikacji webowych (Streamlit) do analizy ludzkich emocji i zachowań na podstawie materiału wideo. Program może pracować zarówno z kamerą internetową w czasie rzeczywistym, jak i z przesłanymi plikami wideo.

### Czym jest ten projekt?

Ten projekt jest doskonałym przykładem zastosowania sztucznej inteligencji do analizy zachowań człowieka. Aplikacja potrafi:
- **Rozpoznawać emocje** na twarzy (radość, smutek, złość, zaskoczenie, strach, wstręt, neutralność)
- **Analizować gesty dłoni** (napięte vs. rozluźnione)
- **Śledzić kierunek spojrzenia** (lewo, prawo, centrum)
- **Wykrywać ruchy głowy** (góra, dół, nieruchomo)
- **Generować szczegółowe raporty** z analizy behawioralnej

### Dla kogo jest ten projekt?

Ten projekt jest przeznaczony dla **początkujących programistów i studentów**, którzy:
- Uczą się programowania w Pythonie
- Chcą poznać zastosowania sztucznej inteligencji
- Interesują się analizą obrazu i wideo
- Pragną stworzyć swoją pierwszą aplikację AI

## Funkcjonalności

### 1. Wykrywanie Emocji w Czasie Rzeczywistym
Wykorzystując bibliotekę **DeepFace**, aplikacja analizuje twarz osoby i rozpoznaje 7 różnych emocji:
- Szczęście (happy)
- Smutek (sad)
- Złość (angry)
- Zaskoczenie (surprise)
- Strach (fear)
- Wstręt (disgust)
- Neutralność (neutral)

### 2. Analiza Gestów Dłoni
Za pomocą **MediaPipe Hands** program wykrywa:
- **Napięte gesty** - gdy palce są zaciśnięte, co może wskazywać na stres
- **Rozluźnione gesty** - gdy palce są rozluźnione, co sugeruje spokój

### 3. Śledzenie Ruchu Oczu
Biblioteka **MediaPipe Face Mesh** pozwala na wykrywanie kierunku spojrzenia:
- **Lewo** - osoba patrzy w lewą stronę
- **Prawo** - osoba patrzy w prawą stronę
- **Centrum** - osoba patrzy prosto w kamerę

### 4. Wykrywanie Ruchów Głowy
Program analizuje pozycję głowy:
- **Góra** - głowa podniesiona
- **Dół** - głowa opuszczona
- **Nieruchomo** - głowa w pozycji neutralnej

### 5. Tryby Analizy
Aplikacja oferuje trzy różne tryby dostosowane do konkretnych zastosowań:

#### Tryb Detektywistyczny (Detective Mode)
- Ogólna analiza emocji i zachowania
- Przydatny do badania ogólnych reakcji emocjonalnych

#### Tryb Zachowania Studenta (Student Behavior Mode)
- Skupia się na śledzeniu uwagi i zaangażowania
- Idealny do monitorowania skupienia podczas nauki

#### Tryb Rozmowy Kwalifikacyjnej (Interview Mode)
- Analizuje emocje i mowę ciała podczas wywiadów
- Pomocny w ocenie reakcji w sytuacjach stresowych

### 6. Raport Analizy Behawioralnej
Po zakończeniu analizy, aplikacja generuje szczegółowy raport zawierający:
- Procentowy rozkład wszystkich wykrytych emocji
- Statystyki gestów dłoni
- Dane o kierunku spojrzenia
- Informacje o ruchach głowy
- **Analizę AI** wygenerowaną przez Google Gemini API z sugestiami działań

## Instalacja

### Krok 1: Sprawdź wymagania wstępne

Przed rozpoczęciem upewnij się, że masz zainstalowane:

1. **Python 3.8 lub nowszy**
   - Sprawdź wersję: `python --version` lub `python3 --version`
   - Na wielu systemach (Linux/macOS) może być wymagane użycie `python3` zamiast `python`
   - Jeśli nie masz Pythona, pobierz go ze strony: https://www.python.org/downloads/

2. **Menedżer pakietów pip**
   - Zazwyczaj instalowany razem z Pythonem
   - Sprawdź: `pip --version` lub `pip3 --version`

3. **Git** (opcjonalnie, do pobrania repozytorium)
   - Pobierz ze strony: https://git-scm.com/

### Krok 2: Pobierz projekt

Możesz pobrać projekt na dwa sposoby:

**Opcja A: Użyj Git** (zalecane)
```bash
git clone https://github.com/MatPomGit/AI_EMOTION_ANALYSIS.git
cd AI_EMOTION_ANALYSIS
```

**Opcja B: Pobierz ZIP**
- Wejdź na stronę projektu GitHub
- Kliknij zielony przycisk "Code"
- Wybierz "Download ZIP"
- Rozpakuj archiwum i wejdź do folderu

### Krok 3: Zainstaluj wymagane biblioteki

Biblioteki wymienione w pliku `requirement.txt` to:
- **streamlit** - framework do tworzenia aplikacji webowych
- **opencv-python-headless** - biblioteka do przetwarzania obrazów i wideo
- **numpy** - biblioteka do obliczeń numerycznych
- **deepface** - biblioteka do rozpoznawania emocji
- **mediapipe** - biblioteka Google do analizy twarzy i dłoni
- **google-generativeai** - API do generowania analiz AI

Zainstaluj wszystkie biblioteki jedną komendą:
```bash
pip install -r requirement.txt
```

Lub zainstaluj je pojedynczo:
```bash
pip install opencv-python-headless numpy streamlit deepface mediapipe google-generativeai
```

**Wyjaśnienie różnicy między opencv-python a opencv-python-headless:**
- `opencv-python` - pełna wersja z obsługą GUI (okna wyświetlania obrazów)
- `opencv-python-headless` - wersja bez GUI, lżejsza, lepsza do aplikacji webowych jak Streamlit

W tym projekcie używamy wersji headless, ponieważ Streamlit wyświetla obrazy w przeglądarce.

### Krok 4: Konfiguracja klucza API Google Gemini

⚠️ **WAŻNE - Bezpieczeństwo!** ⚠️

Aplikacja wykorzystuje Google Gemini API do generowania analiz behawioralnych. **Aplikacja została zaktualizowana i teraz używa bezpiecznych metod przechowywania klucza API.**

**✅ Bezpieczne rozwiązania zaimplementowane w aplikacji:**

1. **Użyj zmiennych środowiskowych** (najlepsze dla produkcji):
   ```bash
   # Linux/macOS
   export GEMINI_API_KEY="twój_klucz_api"
   
   # Windows (PowerShell)
   $env:GEMINI_API_KEY="twój_klucz_api"
   
   # Windows (CMD)
   set GEMINI_API_KEY=twój_klucz_api
   ```
   
   Możesz też użyć pliku `.env` (wzór w `.env.example`):
   ```bash
   # Skopiuj przykładowy plik
   cp .env.example .env
   
   # Edytuj plik .env i dodaj swój klucz
   GEMINI_API_KEY=twój_klucz_api
   ```

2. **Użyj Streamlit Secrets** (zalecane dla aplikacji Streamlit):
   ```bash
   # Skopiuj przykładowy plik
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   
   # Edytuj plik i dodaj swój klucz
   # gemini_api_key = "twój_klucz_api"
   ```

**Aby uzyskać własny klucz API:**
1. Odwiedź: https://makersuite.google.com/app/apikey
2. Zaloguj się kontem Google
3. Utwórz nowy klucz API
4. Skonfiguruj go jedną z powyższych metod

**📌 Uwaga:** Jeśli nie skonfigurujesz klucza API, aplikacja będzie działać, ale nie wygeneruje analizy AI w raporcie końcowym.

### Krok 5: Zainstaluj pakiety systemowe (Linux)

Jeśli używasz systemu Linux, zainstaluj dodatkowo wymagane pakiety systemowe:
```bash
# Na Ubuntu/Debian:
sudo apt-get install libgl1 libsm6 libxext6 libxrender-dev

# Na innych dystrybucjach użyj odpowiedniego menedżera pakietów
```

## Użytkowanie

### Uruchomienie Aplikacji

#### Krok 1: Otwórz terminal/wiersz polecenia
- **Windows**: Wyszukaj "cmd" lub "PowerShell"
- **Mac/Linux**: Otwórz aplikację "Terminal"

#### Krok 2: Przejdź do folderu projektu
```bash
cd ścieżka/do/AI_EMOTION_ANALYSIS
```

#### Krok 3: Uruchom aplikację
```bash
streamlit run emo.py
```

Po uruchomieniu, aplikacja automatycznie otworzy się w przeglądarce internetowej (zazwyczaj pod adresem: `http://localhost:8501`)

### Korzystanie z Aplikacji

#### Krok 1: Wybierz Tryb Analizy
W panelu bocznym (sidebar) wybierz jeden z trzech trybów:
- **Detective** - do ogólnej analizy emocji
- **Student Behavior** - do monitorowania uwagi studenta
- **Interview** - do analizy podczas rozmowy kwalifikacyjnej

#### Krok 2: Wybierz Źródło Wideo
Możesz wybrać:
- **camera** - użycie kamery internetowej w czasie rzeczywistym
- **video** - przesłanie pliku wideo (formaty: mp4, avi, mov)

#### Krok 3: Rozpocznij Analizę
Kliknij przycisk **"Start Analysis"**:
- Jeśli wybrałeś kamerę, natychmiast rozpocznie się analiza
- Jeśli wybrałeś wideo, pojawi się opcja przesłania pliku

#### Krok 4: Zatrzymaj i Wygeneruj Raport
Kliknij przycisk **"Stop Analysis"**, aby:
- Zatrzymać analizę
- Wygenerować szczegółowy raport
- Otrzymać sugestie od AI (Google Gemini)

### Czego Się Spodziewać?

Podczas analizy zobaczysz:
1. **Podgląd wideo** z nałożonymi oznaczeniami:
   - Dominującą emocję z procentem pewności
   - Wszystkie wykryte emocje z ich wartościami
   - Punkty charakterystyczne twarzy i dłoni

2. **Raport końcowy** zawierający:
   - Średnie wartości procentowe dla wszystkich emocji
   - Liczby wykrytych gestów (napięte/rozluźnione)
   - Statystyki kierunku spojrzenia
   - Statystyki ruchów głowy
   - **Analizę behawioralną AI** z sugestiami działań

## Użyte Technologie

Ten projekt wykorzystuje następujące narzędzia i biblioteki:

### 1. Python
**Język programowania** używany w całym projekcie. Python jest popularny w dziedzinie AI i data science ze względu na prostą składnię i bogaty ekosystem bibliotek.

### 2. OpenCV (Open Source Computer Vision Library)
**Biblioteka do przetwarzania obrazów i wideo**. OpenCV pozwala na:
- Przechwytywanie klatek wideo z kamery
- Manipulację obrazami (zmiana kolorów, rozmiaru)
- Rysowanie na obrazach (tekst, kształty)

### 3. DeepFace
**Biblioteka do rozpoznawania twarzy i emocji**. Wykorzystuje głębokie sieci neuronowe do:
- Wykrywania twarzy na obrazie
- Analizy emocji widocznych na twarzy
- Zwracania wyników w postaci procentowej dla każdej emocji

### 4. MediaPipe
**Framework Google do analizy multimedialnej**. Oferuje gotowe rozwiązania do:
- Wykrywania punktów charakterystycznych dłoni (21 punktów)
- Wykrywania siatki twarzy (468 punktów)
- Śledzenia ruchów w czasie rzeczywistym

### 5. Streamlit
**Framework do tworzenia aplikacji webowych**. Pozwala na szybkie stworzenie interfejsu użytkownika bez znajomości HTML/CSS/JavaScript.

### 6. Google Gemini API
**API sztucznej inteligencji Google**. Wykorzystywane do generowania inteligentnych analiz i sugestii na podstawie zebranych danych.

### 7. NumPy
**Biblioteka do obliczeń numerycznych**. Używana do pracy z tablicami danych i operacji matematycznych.

## Struktura Projektu

```
📂 AI_EMOTION_ANALYSIS/
│
│── emo.py                 # Główny plik aplikacji Streamlit
│                            Zawiera całą logikę programu:
│                            - Inicjalizację bibliotek
│                            - Funkcje analizy emocji
│                            - Funkcje analizy gestów i ruchów
│                            - Interfejs użytkownika
│
│── requirement.txt        # Lista wymaganych bibliotek Python
│                            (używana przez: pip install -r requirement.txt)
│
│── package.txt            # Pakiety systemowe dla Linux
│
│── running.txt            # Informacja o wymaganej wersji Pythona
│
│── README.md              # Dokumentacja projektu (ten plik)
│                            Zawiera instrukcje i opis projektu
```

## Wskazówki dla Początkujących

### Jak Działa Analiza Emocji?

1. **Przechwytywanie klatki**: Kamera lub wideo dostarcza pojedyncze klatki (obrazy)
2. **Wykrywanie twarzy**: Algorytm znajduje twarz na obrazie
3. **Ekstrakcja cech**: Z twarzy wyodrębniane są charakterystyczne cechy (kształt ust, oczu, brwi)
4. **Klasyfikacja**: Sieć neuronowa porównuje cechy z nauczonym modelem i przypisuje emocję
5. **Wynik**: Otrzymujemy prawdopodobieństwo dla każdej z 7 emocji

### Jak Działa Wykrywanie Gestów?

1. **Lokalizacja dłoni**: MediaPipe znajduje dłoń na obrazie
2. **Punkty charakterystyczne**: Wyznacza 21 punktów na dłoni (palce, stawy, nadgarstek)
3. **Obliczenie odległości**: Program mierzy odległość między punktami (np. kciuk-palec wskazujący)
4. **Klasyfikacja gestu**: Na podstawie odległości określa, czy gest jest napięty czy rozluźniony

### Typowe Problemy i Rozwiązania

#### Problem: "Nie można znaleźć polecenia streamlit"
**Rozwiązanie**: Upewnij się, że Streamlit jest zainstalowany: `pip install streamlit`

#### Problem: "Kamera nie działa"
**Rozwiązanie**: 
- Sprawdź, czy kamera nie jest używana przez inną aplikację
- Sprawdź uprawnienia do kamery w ustawieniach systemu
- Spróbuj zamknąć i ponownie uruchomić aplikację

#### Problem: "Błędy podczas instalacji bibliotek"
**Rozwiązanie**:
- Zaktualizuj pip: `pip install --upgrade pip`
- Instaluj biblioteki pojedynczo, aby zidentyfikować problematyczną
- Sprawdź wersję Pythona (wymagana 3.8+)

#### Problem: "Aplikacja działa wolno"
**Rozwiązanie**:
- Analiza AI jest zasobożerna - to normalne
- Możesz zmniejszyć rozdzielczość wideo
- Zamknij inne aplikacje zużywające zasoby komputera

#### Problem: "Błąd: Brak klucza API Google Gemini"
**Rozwiązanie**:
- Uzyskaj klucz API: https://makersuite.google.com/app/apikey
- Ustaw zmienną środowiskową: `export GEMINI_API_KEY="twój_klucz"`
- Lub utwórz plik `.streamlit/secrets.toml` i dodaj: `gemini_api_key = "twój_klucz"`

#### Problem: "ImportError: No module named 'deepface'"
**Rozwiązanie**:
- Zainstaluj wszystkie zależności: `pip install -r requirement.txt`
- Sprawdź czy używasz właściwego środowiska Python

#### Problem: "Plik wideo nie może być przetworzony"
**Rozwiązanie**:
- Sprawdź format pliku (obsługiwane: mp4, avi, mov)
- Sprawdź rozmiar pliku (max 200 MB)
- Upewnij się, że plik nie jest uszkodzony

#### Problem: "ValueError podczas analizy emocji"
**Rozwiązanie**:
- Upewnij się, że twarz jest dobrze oświetlona
- Sprawdź czy twarz jest widoczna w kadrze
- Aplikacja automatycznie obsługuje brak twarzy

## Wymagania Sprzętowe

### Minimalne Wymagania
- **Procesor**: Intel Core i3 lub równoważny
- **RAM**: 4 GB
- **Kamera**: Dowolna kamera USB lub wbudowana (dla trybu kamery)
- **Miejsce na dysku**: 2 GB (dla bibliotek i modeli AI)
- **System operacyjny**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)

### Zalecane Wymagania
- **Procesor**: Intel Core i5/i7 lub równoważny
- **RAM**: 8 GB lub więcej
- **Kamera**: HD (720p) lub lepsza
- **Miejsce na dysku**: 5 GB
- **GPU**: Opcjonalnie dla szybszego przetwarzania (CUDA compatible)

### Uwagi o Wydajności
- Aplikacja wykorzystuje modele głębokiego uczenia, które są zasobożerne
- Pierwszy uruchomienie może potrwać dłużej (pobieranie modeli)
- Analiza wideo w czasie rzeczywistym wymaga lepszego sprzętu
- Na słabszych komputerach zalecamy analizę krótszych filmów

## Dalsze Kroki i Rozszerzenia

### Pomysły na Modyfikacje dla Studentów:

1. **Dodaj nowe emocje**: Rozszerz listę wykrywanych emocji
2. **Zapisz wyniki do pliku**: Dodaj funkcję zapisywania raportu do PDF lub CSV
3. **Statystyki graficzne**: Użyj biblioteki matplotlib do tworzenia wykresów
4. **Powiadomienia**: Dodaj alerty, gdy wykryta zostanie konkretna emocja
5. **Tryb grupowy**: Rozszerz aplikację do analizy wielu osób jednocześnie
6. **Historia analiz**: Zapisuj poprzednie analizy i porównuj wyniki
7. **Dostosuj UI**: Zmień wygląd aplikacji (kolory, czcionki, layout)

### Materiały do Nauki:

- **Python**: https://www.python.org/about/gettingstarted/
- **Streamlit**: https://docs.streamlit.io/
- **OpenCV**: https://docs.opencv.org/
- **DeepFace**: https://github.com/serengil/deepface
- **MediaPipe**: https://google.github.io/mediapipe/

## Wkład w Projekt

Zachęcamy do współtworzenia projektu! Możesz:
- Zgłaszać błędy (issues) na GitHubie
- Proponować nowe funkcje
- Przesyłać poprawki kodu (pull requests)
- Dzielić się swoimi modyfikacjami

## Licencja

Ten projekt jest udostępniony na licencji MIT. Zobacz plik [LICENSE](LICENSE) dla szczegółów.

Możesz swobodnie:
- Używać projektu w celach edukacyjnych i komercyjnych
- Modyfikować kod
- Dystrybuować kopie
- Używać w swoich projektach

Pod warunkiem zachowania informacji o prawach autorskich i licencji.

---

**Powodzenia w nauce programowania i pracy ze sztuczną inteligencją! 🚀**

*Jeśli masz pytania lub napotkasz problemy, nie wahaj się otworzyć issue na GitHubie lub skontaktować z autorem projektu.*
