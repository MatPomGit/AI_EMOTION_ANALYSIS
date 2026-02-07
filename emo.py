# ==================================================================================
# ANALIZATOR EMOCJI I ZACHOWANIA - Główny plik aplikacji
# ==================================================================================
# Ten program analizuje emocje i zachowania człowieka na podstawie wideo używając
# zaawansowanych bibliotek sztucznej inteligencji.
#
# Autor: MatPomGit
# Przeznaczenie: Projekt edukacyjny dla studentów uczących się AI i Python
# ==================================================================================

# SEKCJA 1: IMPORTOWANIE BIBLIOTEK
# ==================================================================================
# W tej sekcji importujemy wszystkie potrzebne biblioteki (moduły) do działania programu.
# Każda biblioteka dostarcza konkretne funkcjonalności.

import cv2  # OpenCV - biblioteka do przetwarzania obrazów i wideo
            # cv2 pozwala na: odczyt wideo, manipulację obrazami, rysowanie na obrazach

import numpy as np  # NumPy - biblioteka do operacji na tablicach numerycznych
                    # np używamy do obliczeń matematycznych na dużych zbiorach danych

import streamlit as st  # Streamlit - framework do tworzenia aplikacji webowych
                        # st pozwala na szybkie stworzenie interfejsu użytkownika

from deepface import DeepFace  # DeepFace - biblioteka do rozpoznawania emocji na twarzy
                                # DeepFace wykorzystuje głębokie sieci neuronowe

import mediapipe as mp  # MediaPipe - biblioteka Google do analizy multimedialnej
                        # mp dostarcza gotowe rozwiązania do wykrywania twarzy i dłoni

import datetime  # datetime - wbudowana biblioteka do pracy z datą i czasem
                # Używamy jej do oznaczania czasu w raportach

import json  # json - wbudowana biblioteka do pracy z formatem JSON
            # JSON to format przechowywania danych, używamy go do komunikacji z API

import tempfile  # tempfile - wbudowana biblioteka do tworzenia plików tymczasowych
                # Używamy jej do zapisywania przesłanych plików wideo

import os  # os - wbudowana biblioteka do operacji systemowych
          # Używamy jej do pracy ze ścieżkami plików i usuwania plików

from google import genai  # Google Generative AI - API do generowania analiz przez AI
                          # genai pozwala nam używać modeli AI Google (np. Gemini)

# SEKCJA 2: INICJALIZACJA NARZĘDZI MEDIAPIPE
# ==================================================================================
# MediaPipe oferuje gotowe rozwiązania (solutions) do różnych zadań.
# Musimy je zainicjalizować przed użyciem.

mp_hands = mp.solutions.hands  # Rozwiązanie do wykrywania dłoni
                               # Wykrywa 21 punktów charakterystycznych na dłoni

mp_face_mesh = mp.solutions.face_mesh  # Rozwiązanie do wykrywania siatki twarzy
                                       # Wykrywa 468 punktów charakterystycznych na twarzy

mp_drawing = mp.solutions.drawing_utils  # Narzędzia do rysowania punktów na obrazie
                                         # Używamy tego do wizualizacji wykrytych punktów

# SEKCJA 3: ZMIENNE GLOBALNE - PRZECHOWYWANIE DANYCH ANALIZY
# ==================================================================================
# Streamlit używa "session_state" do przechowywania danych między kolejnymi
# odświeżeniami strony. To jak "pamięć" aplikacji.
# Wszystkie dane zbierane podczas analizy są tutaj zapisywane.

# Raport z analizy behawioralnej - lista wszystkich zdarzeń podczas analizy
if "behavior_report" not in st.session_state:
    st.session_state.behavior_report = []  # Pusta lista na rozpoczęcie

# Sumy procentowe wszystkich emocji wykrytych w każdej klatce
# Kluczami są nazwy emocji, wartościami - suma procentów ze wszystkich klatek
if "emotion_totals" not in st.session_state:
    st.session_state.emotion_totals = {
        "happy": 0,      # Radość
        "sad": 0,        # Smutek
        "angry": 0,      # Złość
        "surprise": 0,   # Zaskoczenie
        "fear": 0,       # Strach
        "disgust": 0,    # Wstręt
        "neutral": 0     # Neutralność
    }

# Licznik przeanalizowanych klatek wideo
# Potrzebny do obliczenia średniej wartości emocji
if "frame_count" not in st.session_state:
    st.session_state.frame_count = 0

# Liczniki gestów dłoni wykrytych podczas analizy
if "hand_gesture_count" not in st.session_state:
    st.session_state.hand_gesture_count = {
        "tense": 0,      # Napięte gesty (palce zaciśnięte)
        "relaxed": 0     # Rozluźnione gesty (palce rozluźnione)
    }

# Liczniki kierunku spojrzenia wykrytego podczas analizy
if "eye_direction_count" not in st.session_state:
    st.session_state.eye_direction_count = {
        "left": 0,       # Spojrzenie w lewo
        "right": 0,      # Spojrzenie w prawo
        "center": 0      # Spojrzenie prosto
    }

# Liczniki ruchów głowy wykrytych podczas analizy
if "head_movement_count" not in st.session_state:
    st.session_state.head_movement_count = {
        "up": 0,         # Głowa w górę
        "down": 0,       # Głowa w dół
        "still": 0       # Głowa nieruchomo
    }

# Flaga kontrolująca czy kamera/analiza jest aktywna
# True = analiza trwa, False = analiza zatrzymana
if "camera_running" not in st.session_state:
    st.session_state.camera_running = False


# SEKCJA 4: FUNKCJE POMOCNICZE
# ==================================================================================
# W tej sekcji definiujemy funkcje, które wykonują konkretne zadania.
# Podział na funkcje sprawia, że kod jest bardziej czytelny i łatwiejszy w utrzymaniu.

# FUNKCJA 1: Logowanie danych do raportu
# ==================================================================================
def log_to_report(mode, analysis):
    """
    Zapisuje dane do raportu behawioralnego z aktualnym znacznikiem czasu.
    
    Parametry:
    ----------
    mode : str
        Tryb analizy (np. "Detective", "Student Behavior", "Interview")
    analysis : str
        Tekst z wynikiem analizy do zapisania w raporcie
        
    Działanie:
    ----------
    1. Pobiera aktualny czas
    2. Formatuje go do czytelnej postaci (RRRR-MM-DD GG:MM:SS)
    3. Dodaje wpis do listy raportów w pamięci aplikacji
    
    Przykład użycia:
    ----------------
    log_to_report("Detective", "Wykryto emocję: radość (85%)")
    """
    # Pobierz aktualną datę i czas
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Dodaj sformatowany wpis do listy raportów
    # Format: "2024-01-15 14:30:45 - Detective: Wykryto emocję: radość (85%)"
    st.session_state.behavior_report.append(f"{timestamp} - {mode}: {analysis}")


# FUNKCJA 2: Analiza emocji za pomocą DeepFace
# ==================================================================================
def analyze_emotion(frame):
    """
    Analizuje emocje widoczne na twarzy w pojedynczej klatce wideo.
    
    Parametry:
    ----------
    frame : numpy.ndarray
        Pojedyncza klatka wideo (obraz) w formacie OpenCV (BGR)
        
    Zwraca:
    -------
    dict
        Słownik z wynikami analizy, gdzie:
        - klucze to nazwy emocji (np. "happy", "sad")
        - wartości to procentowe prawdopodobieństwo dla każdej emocji (0-100)
        
    Działanie:
    ----------
    1. DeepFace.analyze() przetwarza obraz
    2. Wykrywa twarz na obrazie (jeśli jest)
    3. Analizuje cechy twarzy (kształt ust, oczu, brwi)
    4. Porównuje z wytrenowanym modelem sieci neuronowej
    5. Zwraca prawdopodobieństwa dla każdej z 7 emocji
    
    Uwaga:
    ------
    enforce_detection=False sprawia, że funkcja nie zgłasza błędu,
    jeśli nie wykryje twarzy - zamiast tego zwraca neutralne wyniki
    """
    try:
        # Wywołaj analizę DeepFace na bieżącej klatce
        # actions=['emotion'] - analizujemy tylko emocje (nie wiek, płeć, rasę)
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        # Sprawdź czy wynik jest prawidłowy i niepusty
        if result and len(result) > 0 and 'emotion' in result[0]:
            # Wyciągnij słownik z wynikami emocji z wyniku analizy
            # result[0] bo DeepFace może zwracać listę wyników (dla wielu twarzy)
            emotion_scores = result[0]['emotion']
            return emotion_scores
        else:
            # Jeśli wynik jest pusty, zwróć neutralne wartości
            return {
                "happy": 0.0,
                "sad": 0.0,
                "angry": 0.0,
                "surprise": 0.0,
                "fear": 0.0,
                "disgust": 0.0,
                "neutral": 100.0
            }
    except Exception as e:
        # W przypadku błędu (np. problem z modelem, uszkodzony obraz)
        # Zwróć neutralne wartości i zaloguj ostrzeżenie
        print(f"Ostrzeżenie: Błąd analizy emocji: {e}")
        return {
            "happy": 0.0,
            "sad": 0.0,
            "angry": 0.0,
            "surprise": 0.0,
            "fear": 0.0,
            "disgust": 0.0,
            "neutral": 100.0
        }


# FUNKCJA 3: Analiza gestów dłoni za pomocą MediaPipe
# ==================================================================================
def analyze_hands(frame, hands):
    """
    Analizuje gesty dłoni widoczne w klatce wideo.
    
    Parametry:
    ----------
    frame : numpy.ndarray
        Pojedyncza klatka wideo (obraz) w formacie OpenCV (BGR)
    hands : mediapipe.solutions.hands.Hands
        Zainicjalizowany obiekt MediaPipe Hands do wykrywania dłoni
        
    Działanie:
    ----------
    1. Konwertuje obraz z BGR (OpenCV) do RGB (MediaPipe)
    2. Wykrywa dłonie i ich punkty charakterystyczne (21 punktów na dłoń)
    3. Dla każdej wykrytej dłoni:
       - Mierzy odległość między kciukiem a palcem wskazującym
       - Jeśli odległość < 0.1: gest napięty (palce zaciśnięte)
       - Jeśli odległość >= 0.1: gest rozluźniony (palce rozluźnione)
    4. Rysuje punkty i połączenia na obrazie (wizualizacja)
    5. Aktualizuje liczniki gestów w pamięci aplikacji
    
    Uwaga:
    ------
    MediaPipe wymaga obrazu w formacie RGB, a OpenCV używa BGR,
    dlatego konwertujemy kolory przed przetwarzaniem
    """
    # Konwersja z BGR (format OpenCV) na RGB (format MediaPipe)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Przetwórz klatkę przez MediaPipe Hands
    results = hands.process(frame_rgb)

    # Sprawdź czy wykryto jakiekolwiek dłonie
    if results.multi_hand_landmarks:
        # Iteruj przez wszystkie wykryte dłonie
        for hand_landmarks in results.multi_hand_landmarks:
            # Pobierz współrzędne kciuka (punkt 4 z 21 punktów dłoni)
            # HandLandmark.THUMB_TIP to stała określająca czubek kciuka
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            
            # Pobierz współrzędne czubka palca wskazującego (punkt 8)
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            # Oblicz odległość między kciukiem a palcem wskazującym
            # Używamy zarówno odległości w poziomie (x) jak i pionie (y)
            distance = abs(thumb_tip.x - index_tip.x) + abs(thumb_tip.y - index_tip.y)

            # Klasyfikacja gestu na podstawie odległości
            if distance < 0.1:
                # Mała odległość = palce blisko siebie = gest napięty
                st.session_state.hand_gesture_count["tense"] += 1
            else:
                # Duża odległość = palce daleko od siebie = gest rozluźniony
                st.session_state.hand_gesture_count["relaxed"] += 1

            # Narysuj punkty charakterystyczne dłoni i połączenia między nimi
            # HAND_CONNECTIONS to predefiniowana lista połączeń między punktami
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


# FUNKCJA 4: Analiza kierunku spojrzenia i ruchów głowy
# ==================================================================================
def analyze_face(frame, face_mesh):
    """
    Analizuje kierunek spojrzenia oczu i ruchy głowy w klatce wideo.
    
    Parametry:
    ----------
    frame : numpy.ndarray
        Pojedyncza klatka wideo (obraz) w formacie OpenCV (BGR)
    face_mesh : mediapipe.solutions.face_mesh.FaceMesh
        Zainicjalizowany obiekt MediaPipe Face Mesh do wykrywania twarzy
        
    Działanie:
    ----------
    1. Konwertuje obraz z BGR na RGB
    2. Wykrywa twarz i jej punkty charakterystyczne (468 punktów)
    3. Analizuje kierunek oczu:
       - Punkt 33: lewe oko
       - Punkt 263: prawe oko
       - Na podstawie pozycji x określa kierunek spojrzenia
    4. Analizuje pozycję głowy:
       - Punkt 4: czubek nosa
       - Na podstawie pozycji y określa ruch głowy (góra/dół/nieruchomo)
    5. Rysuje siatkę twarzy na obrazie (wizualizacja)
    6. Aktualizuje liczniki w pamięci aplikacji
    
    Uwaga:
    ------
    Współrzędne są znormalizowane (0.0 - 1.0):
    - x=0.0 to lewa krawędź obrazu, x=1.0 to prawa krawędź
    - y=0.0 to górna krawędź obrazu, y=1.0 to dolna krawędź
    """
    # Konwersja z BGR (format OpenCV) na RGB (format MediaPipe)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Przetwórz klatkę przez MediaPipe Face Mesh
    results = face_mesh.process(frame_rgb)

    # Sprawdź czy wykryto jakąkolwiek twarz
    if results.multi_face_landmarks:
        # Iteruj przez wszystkie wykryte twarze (zazwyczaj jedna)
        for face_landmarks in results.multi_face_landmarks:
            # ANALIZA KIERUNKU SPOJRZENIA
            # ----------------------------
            # Pobierz współrzędne lewego oka (punkt 33 z 468 punktów siatki)
            left_eye = face_landmarks.landmark[33]
            
            # Pobierz współrzędne prawego oka (punkt 263)
            right_eye = face_landmarks.landmark[263]

            # Określ kierunek spojrzenia na podstawie pozycji oczu
            if left_eye.x < 0.4:
                # Lewe oko jest bardzo na lewo -> osoba patrzy w lewo
                st.session_state.eye_direction_count["left"] += 1
            elif right_eye.x > 0.6:
                # Prawe oko jest bardzo na prawo -> osoba patrzy w prawo
                st.session_state.eye_direction_count["right"] += 1
            else:
                # Oczy są mniej więcej centralnie -> osoba patrzy prosto
                st.session_state.eye_direction_count["center"] += 1

            # ANALIZA RUCHÓW GŁOWY
            # ---------------------
            # Pobierz współrzędne czubka nosa (punkt 4) - środkowy punkt twarzy
            nose_tip = face_landmarks.landmark[4]
            
            # Określ pozycję głowy na podstawie współrzędnej y nosa
            if nose_tip.y < 0.4:
                # Nos jest wysoko -> głowa podniesiona w górę
                st.session_state.head_movement_count["up"] += 1
            elif nose_tip.y > 0.6:
                # Nos jest nisko -> głowa opuszczona w dół
                st.session_state.head_movement_count["down"] += 1
            else:
                # Nos jest mniej więcej centralnie -> głowa w pozycji neutralnej
                st.session_state.head_movement_count["still"] += 1

            # Narysuj siatkę twarzy na obrazie
            # FACEMESH_CONTOURS to zestaw linii tworzących kontur twarzy
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)


# FUNKCJA 5: Rozpoczęcie analizy wideo (główna pętla programu)
# ==================================================================================
def start_analysis(mode, input_source):
    """
    Uruchamia główną pętlę analizy wideo z kamery lub pliku.
    
    Parametry:
    ----------
    mode : str
        Tryb analizy: "Detective", "Student Behavior" lub "Interview"
    input_source : str
        Źródło wideo: "camera" (kamera) lub "video" (plik)
        
    Działanie:
    ----------
    1. Otwiera źródło wideo (kamera lub plik)
    2. Inicjalizuje narzędzia MediaPipe do analizy dłoni i twarzy
    3. Wchodzi w pętlę przetwarzania klatek:
       - Odczytuje kolejną klatkę
       - Analizuje emocje (DeepFace)
       - Analizuje gesty dłoni (MediaPipe)
       - Analizuje kierunek oczu i ruchy głowy (MediaPipe)
       - Wyświetla wyniki na obrazie
       - Loguje dane do raportu
    4. Po zakończeniu generuje raport
    
    Uwaga:
    ------
    Pętla działa dopóki st.session_state.camera_running == True
    Użytkownik zatrzymuje analizę przyciskiem "Stop Analysis"
    """
    # KROK 1: Otwórz źródło wideo
    # ----------------------------
    temp_file_path = None  # Zmienna do przechowania ścieżki tymczasowego pliku
    
    if input_source == "camera":
        # Otwórz domyślną kamerę (0 = pierwsza kamera w systemie)
        cap = cv2.VideoCapture(0)
        
        # Sprawdź czy kamera została poprawnie otwarta
        if not cap.isOpened():
            st.error("❌ Nie można otworzyć kamery. Sprawdź czy:")
            st.info("• Kamera jest podłączona\n• Żadna inna aplikacja nie używa kamery\n• Masz uprawnienia do dostępu do kamery")
            return
    else:
        # Pozwól użytkownikowi przesłać plik wideo
        file_path = st.file_uploader("Prześlij plik wideo", type=["mp4", "avi", "mov"])
        
        # Sprawdź czy plik został przesłany
        if file_path is None:
            st.warning("Proszę przesłać plik wideo.")
            return
        
        # Walidacja rozmiaru pliku (max 200 MB)
        max_size_mb = 200
        file_size_mb = file_path.size / (1024 * 1024)  # Konwersja na MB
        
        if file_size_mb > max_size_mb:
            st.error(f"❌ Plik jest za duży ({file_size_mb:.1f} MB). Maksymalny rozmiar: {max_size_mb} MB.")
            st.info("💡 Tip: Skompresuj wideo lub użyj krótszego fragmentu.")
            return
        
        # Wyświetl informację o rozmiarze pliku
        st.info(f"📁 Przetwarzanie pliku: {file_path.name} ({file_size_mb:.1f} MB)")
        
        # POPRAWKA: Zapisz przesłany plik tymczasowo
        # Streamlit file_uploader zwraca obiekt UploadedFile, nie ścieżkę
        # Musimy zapisać plik tymczasowo, aby OpenCV mógł go odczytać
        
        try:
            # Utwórz tymczasowy plik z odpowiednim rozszerzeniem
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_path.name)[1])
            tfile.write(file_path.read())
            tfile.close()
            temp_file_path = tfile.name  # Zapisz ścieżkę do późniejszego usunięcia
            
            # Otwórz tymczasowy plik
            cap = cv2.VideoCapture(temp_file_path)
            
            # Sprawdź czy plik został poprawnie otwarty
            if not cap.isOpened():
                st.error("❌ Nie można otworzyć pliku wideo. Sprawdź czy plik jest prawidłowy.")
                if temp_file_path and os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                return
        except Exception as e:
            st.error(f"❌ Błąd podczas przetwarzania pliku: {e}")
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            return

    # Utwórz pusty kontener Streamlit do wyświetlania wideo
    stframe = st.empty()

    # KROK 2: Zainicjalizuj narzędzia MediaPipe
    # ------------------------------------------
    # Używamy kontekstu "with" aby automatycznie zwolnić zasoby po zakończeniu
    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands, \
            mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7) as face_mesh:
        
        # min_detection_confidence=0.7 oznacza, że wykrywanie musi mieć
        # pewność co najmniej 70%, aby uznać coś za dłoń/twarz
        
        # min_tracking_confidence=0.7 oznacza, że śledzenie musi mieć
        # pewność co najmniej 70%, aby kontynuować śledzenie tego samego obiektu

        # KROK 3: Główna pętla przetwarzania klatek
        # ------------------------------------------
        while st.session_state.camera_running and cap.isOpened():
            # Odczytaj kolejną klatkę z wideo
            # ret = True jeśli klatka została odczytana poprawnie
            # frame = tablica NumPy zawierająca obraz (klatkę)
            ret, frame = cap.read()
            
            # Jeśli nie udało się odczytać klatki (koniec wideo), przerwij pętlę
            if not ret:
                break

            # ANALIZA EMOCJI
            # --------------
            # Analizuj emocje widoczne na twarzy w bieżącej klatce
            emotion_scores = analyze_emotion(frame)

            # Dodaj wyniki emocji do sum całkowitych (do obliczenia średniej później)
            for emotion, score in emotion_scores.items():
                st.session_state.emotion_totals[emotion] += score
            
            # Zwiększ licznik przeanalizowanych klatek
            st.session_state.frame_count += 1

            # ANALIZA GESTÓW DŁONI
            # ---------------------
            analyze_hands(frame, hands)

            # ANALIZA TWARZY (oczy i głowa)
            # ------------------------------
            analyze_face(frame, face_mesh)

            # OKREŚLENIE DOMINUJĄCEJ EMOCJI
            # ------------------------------
            # Znajdź emocję z najwyższym wynikiem w bieżącej klatce
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            dominant_emotion_score = emotion_scores[dominant_emotion]

            # WIZUALIZACJA WYNIKÓW NA OBRAZIE
            # --------------------------------
            # Wyświetl dominującą emocję na górze obrazu
            emotion_text = f"{dominant_emotion}: {dominant_emotion_score:.2f}%"
            frame = cv2.putText(frame, emotion_text, (50, 50), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # cv2.putText() parametry:
            # - frame: obraz na którym rysujemy
            # - emotion_text: tekst do wyświetlenia
            # - (50, 50): pozycja x, y tekstu
            # - cv2.FONT_HERSHEY_SIMPLEX: typ czcionki
            # - 1: rozmiar czcionki
            # - (0, 255, 0): kolor BGR (zielony)
            # - 2: grubość linii

            # Wyświetl wszystkie emocje z ich procentami
            y_offset = 100  # Początkowa pozycja y dla pierwszej emocji
            for emotion, score in emotion_scores.items():
                frame = cv2.putText(frame, f"{emotion}: {score:.2f}%", 
                                  (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 
                                  0.7, (0, 255, 0), 2)
                y_offset += 30  # Przesuń pozycję y o 30 pikseli dla kolejnej emocji

            # LOGOWANIE DO RAPORTU
            # --------------------
            # Zapisz wynik analizy do raportu (w zależności od trybu)
            if mode == "Detective":
                log_to_report(mode, f"Wykrywanie: {dominant_emotion} ({dominant_emotion_score:.2f}%)")
            elif mode == "Student Behavior":
                log_to_report(mode, f"Śledzenie: {dominant_emotion} ({dominant_emotion_score:.2f}%)")
            elif mode == "Interview":
                log_to_report(mode, f"Analiza: {dominant_emotion} ({dominant_emotion_score:.2f}%)")

            # WYŚWIETLENIE KLATKI W APLIKACJI STREAMLIT
            # ------------------------------------------
            # Wyświetl przetworzoną klatkę z nałożonymi adnotacjami
            stframe.image(frame, channels="BGR", use_container_width=True)
            
            # channels="BGR" - OpenCV używa BGR zamiast RGB
            # use_container_width=True - dostosuj szerokość do kontenera

            # Sprawdź czy naciśnięto klawisz 'q' (opcjonalne zatrzymanie)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # KROK 4: Zwolnij zasoby
    # -----------------------
    cap.release()  # Zamknij strumień wideo
    cv2.destroyAllWindows()  # Zamknij wszystkie okna OpenCV
    
    # Usuń tymczasowy plik wideo jeśli został utworzony
    if temp_file_path is not None:
        try:
            os.remove(temp_file_path)  # Usuń plik tymczasowy z dysku
        except Exception as e:
            # Jeśli nie udało się usunąć pliku, wyświetl ostrzeżenie
            st.warning(f"Nie można usunąć pliku tymczasowego: {e}")

    # KROK 5: Wygeneruj raport końcowy
    # ---------------------------------
    generate_report(mode)


# FUNKCJA 6: Generowanie i wyświetlanie raportu końcowego
# ==================================================================================
def generate_report(mode):
    """
    Generuje szczegółowy raport z analizy emocji i zachowania.
    
    Parametry:
    ----------
    mode : str
        Tryb analizy, który został użyty
        
    Działanie:
    ----------
    1. Oblicza średnie wartości emocji ze wszystkich klatek
    2. Wyświetla statystyki emocji
    3. Wyświetla statystyki gestów, kierunku oczu i ruchów głowy
    4. Wysyła dane do Google Gemini AI w celu uzyskania analizy behawioralnej
    5. Wyświetla sugestie AI dotyczące zachowania
    
    Uwaga:
    ------
    Ta funkcja używa API Google Gemini, które wymaga klucza API.
    Klucz jest zakodowany na stałe w kodzie (nie zalecane w produkcji!)
    """
    # KROK 1: Zabezpieczenie przed dzieleniem przez zero
    # ---------------------------------------------------
    if st.session_state.frame_count == 0:
        st.session_state.frame_count = 1

    # KROK 2: Oblicz średnie wartości emocji
    # ---------------------------------------
    # Dla każdej emocji, podziel sumę przez liczbę klatek
    # Otrzymujemy średnią wartość procentową dla każdej emocji w całym wideo
    average_emotion_scores = {
        emotion: score / st.session_state.frame_count 
        for emotion, score in st.session_state.emotion_totals.items()
    }

    # KROK 3: Wyświetl nagłówek raportu
    # ----------------------------------
    st.subheader("Raport Analizy Emocji i Zachowania")
    st.write("=" * 40)

    # KROK 4: Wyświetl wyniki analizy emocji
    # ---------------------------------------
    st.write(f"Tryb analizy: {mode}\n")
    st.write("ŚREDNIE WARTOŚCI EMOCJI:")
    for emotion, score in average_emotion_scores.items():
        # Wyświetl nazwę emocji z wielkiej litery i jej średni procent
        st.write(f"{emotion.capitalize()}: {score:.2f}%")

    # KROK 5: Wyświetl analizę mowy ciała
    # ------------------------------------
    st.write("\nAnaliza Mowy Ciała:")
    st.write(f"Napięte Gesty Dłoni: {st.session_state.hand_gesture_count['tense']}")
    st.write(f"Rozluźnione Gesty Dłoni: {st.session_state.hand_gesture_count['relaxed']}")
    st.write(f"Kierunek Oczu (Lewo): {st.session_state.eye_direction_count['left']}")
    st.write(f"Kierunek Oczu (Prawo): {st.session_state.eye_direction_count['right']}")
    st.write(f"Kierunek Oczu (Centrum): {st.session_state.eye_direction_count['center']}")
    st.write(f"Ruchy Głowy (Góra): {st.session_state.head_movement_count['up']}")
    st.write(f"Ruchy Głowy (Dół): {st.session_state.head_movement_count['down']}")
    st.write(f"Ruchy Głowy (Nieruchomo): {st.session_state.head_movement_count['still']}")

    # KROK 6: Przygotuj dane do analizy AI
    # -------------------------------------
    # Utwórz tekstowy opis wszystkich zebranych danych
    analysis = ""
    for emotion, score in average_emotion_scores.items():
        analysis += f"{emotion.capitalize()}: {score:.2f}%\n"

    analysis += f"Napięte Gesty Dłoni: {st.session_state.hand_gesture_count['tense']}\n"
    analysis += f"Rozluźnione Gesty Dłoni: {st.session_state.hand_gesture_count['relaxed']}\n"
    analysis += f"Kierunek Oczu (Lewo): {st.session_state.eye_direction_count['left']}\n"
    analysis += f"Kierunek Oczu (Prawo): {st.session_state.eye_direction_count['right']}\n"
    analysis += f"Kierunek Oczu (Centrum): {st.session_state.eye_direction_count['center']}\n"
    analysis += f"Ruchy Głowy (Góra): {st.session_state.head_movement_count['up']}\n"
    analysis += f"Ruchy Głowy (Dół): {st.session_state.head_movement_count['down']}\n"
    analysis += f"Ruchy Głowy (Nieruchomo): {st.session_state.head_movement_count['still']}\n"

    # KROK 7: Wywołaj Google Gemini AI do analizy
    # --------------------------------------------
    # ✅ BEZPIECZNE ROZWIĄZANIE - Użycie zmiennych środowiskowych lub Streamlit secrets
    # Próbuje załadować klucz API w kolejności:
    # 1. Ze zmiennych środowiskowych (GEMINI_API_KEY)
    # 2. Z Streamlit secrets (dla aplikacji wdrożonych na Streamlit Cloud)
    # 3. W przypadku braku klucza - wyświetla ostrzeżenie
    
    api_key = None
    
    # Próba 1: Zmienne środowiskowe
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Próba 2: Streamlit secrets (jeśli aplikacja jest wdrożona)
    if not api_key:
        try:
            api_key = st.secrets.get("gemini_api_key")
        except:
            pass
    
    # Sprawdź czy klucz API został znaleziony
    if not api_key:
        st.error("❌ Brak klucza API Google Gemini! Ustaw zmienną środowiskową GEMINI_API_KEY lub dodaj klucz do Streamlit secrets.")
        st.info("ℹ️ Jak uzyskać klucz API: https://makersuite.google.com/app/apikey")
        return "Brak konfiguracji API - nie można wygenerować analizy AI."
    
    # Inicjalizuj klienta z bezpiecznie pobranym kluczem
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Błąd inicjalizacji klienta Google Gemini: {e}")
        return "Błąd konfiguracji API - nie można wygenerować analizy AI."
    
    # Wyślij prompt do modelu Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # Model AI do użycia
        contents=f"""Na podstawie tej Analizy Emocji i Zachowania dla trybu {mode}: {analysis}, 
    użyj formatu JSON do ustrukturyzowania odpowiedzi:

    {{
        "behavior": "opisz ogólne zachowanie na podstawie analizy",
        "action": "zasugeruj odpowiednie działanie"
    }}
    """
    )

    # KROK 8: Przetwórz odpowiedź AI
    # -------------------------------
    # Odpowiedź AI jest w formacie JSON, ale często opakowana w znaczniki markdown
    # Bezpiecznie wyodrębnij JSON z odpowiedzi
    ans = response.text
    
    # Usuń znaczniki markdown jeśli są obecne (np. ```json ... ```)
    # Sprawdź czy odpowiedź zawiera znaczniki kodu
    if "```" in ans:
        # Znajdź początek JSON (pierwszy nawias klamrowy)
        start = ans.find("{")
        # Znajdź koniec JSON (ostatni nawias klamrowy)
        end = ans.rfind("}") + 1
        
        # Sprawdź czy znaleziono prawidłowe granice JSON
        if start != -1 and end > start:
            ans = ans[start:end]
        else:
            # Jeśli nie znaleziono prawidłowych granic, spróbuj usunąć tylko znaczniki ```
            ans = ans.replace("```json", "").replace("```", "").strip()
    
    # Spróbuj sparsować JSON
    try:
        ans = json.loads(ans)  # Parsuj JSON na słownik Python
    except json.JSONDecodeError as e:
        # Jeśli parsowanie nie powiedzie się, wyświetl błąd i użyj domyślnych wartości
        st.error(f"Nie udało się sparsować odpowiedzi AI: {e}")
        st.info(f"Otrzymana odpowiedź: {response.text[:200]}...")  # Pokaż fragment odpowiedzi
        ans = {
            "behavior": "Nie można było przeanalizować zachowania z powodu błędu parsowania JSON",
            "action": "Spróbuj ponownie przeprowadzić analizę"
        }
    
    # KROK 9: Wyświetl analizę behawioralną AI
    # -----------------------------------------
    st.write("\nAnaliza Behawioralna (wygenerowana przez AI):")
    st.write(f"Zachowanie: {ans['behavior']}")
    st.write(f"Sugerowane działanie: {ans['action']}")

    st.write("\nAnaliza Zakończona.")
    st.write("=" * 40)


# ==================================================================================
# SEKCJA 5: INTERFEJS UŻYTKOWNIKA STREAMLIT
# ==================================================================================
# Poniższy kod tworzy interfejs webowy aplikacji przy użyciu Streamlit.
# Streamlit automatycznie generuje elementy UI na podstawie poniższych komend.

# NAGŁÓWEK GŁÓWNY APLIKACJI
# --------------------------
st.title("Analizator Emocji i Zachowania")
# Wyświetla duży, wyróżniony tytuł na górze strony

# PANEL BOCZNY (SIDEBAR) - USTAWIENIA
# ------------------------------------
st.sidebar.header("Ustawienia")
# Tworzy nagłówek w panelu bocznym po lewej stronie

# Element 1: Wybór trybu analizy
# -------------------------------
mode = st.sidebar.selectbox(
    "Wybierz Tryb Analizy", 
    ["Detective", "Student Behavior", "Interview"]
)
# selectbox tworzy listę rozwijaną (dropdown) z opcjami do wyboru
# Wartość wybranej opcji jest zapisywana w zmiennej "mode"
# 
# Wyjaśnienie trybów:
# - Detective: Tryb ogólny do wykrywania emocji
# - Student Behavior: Tryb do monitorowania uwagi studenta
# - Interview: Tryb do analizy podczas rozmowy kwalifikacyjnej

# Element 2: Wybór źródła wideo
# ------------------------------
input_source = st.sidebar.radio(
    "Wybierz Źródło Wideo", 
    ["camera", "video"]
)
# radio tworzy przyciski opcji (radio buttons)
# Użytkownik może wybrać tylko jedną opcję
# 
# Opcje:
# - camera: Użyj kamery internetowej w czasie rzeczywistym
# - video: Prześlij plik wideo z dysku

# Element 3: Przycisk rozpoczęcia analizy
# ----------------------------------------
if st.sidebar.button("Rozpocznij Analizę"):
    # button tworzy przycisk klikalny
    # Kod wewnątrz if wykona się tylko gdy użytkownik kliknie przycisk
    
    # Ustaw flagę na True - rozpocznij analizę
    st.session_state.camera_running = True
    
    # Wywołaj funkcję główną rozpoczynającą przetwarzanie wideo
    start_analysis(mode, input_source)

# Element 4: Przycisk zatrzymania analizy
# ----------------------------------------
if st.sidebar.button("Zatrzymaj Analizę"):
    # Ten przycisk zatrzymuje przetwarzanie wideo
    
    # Ustaw flagę na False - zatrzymaj analizę
    st.session_state.camera_running = False
    
    # Wyświetl komunikat sukcesu dla użytkownika
    st.success("Analiza zatrzymana. Generowanie raportu...")
    
    # Wygeneruj i wyświetl raport końcowy
    generate_report(mode)

# ==================================================================================
# KONIEC PROGRAMU
# ==================================================================================
# 
# JAK DZIAŁA STREAMLIT?
# ----------------------
# 1. Streamlit wykonuje cały skrypt od góry do dołu
# 2. Gdy użytkownik kliknie przycisk/zmieni wartość, Streamlit wykonuje skrypt ponownie
# 3. session_state zachowuje dane między wykonaniami (nie tracisz zebranych danych)
# 4. Każde polecenie st.* dodaje element do interfejsu w kolejności wykonania
#
# PRZEPŁYW DZIAŁANIA APLIKACJI:
# ------------------------------
# 1. Użytkownik uruchamia: streamlit run emo.py
# 2. Streamlit otwiera aplikację w przeglądarce
# 3. Użytkownik wybiera tryb i źródło wideo
# 4. Użytkownik klika "Rozpocznij Analizę"
# 5. Funkcja start_analysis() rozpoczyna przetwarzanie wideo:
#    - Otwiera kamerę/plik
#    - W pętli przetwarza kolejne klatki
#    - Analizuje emocje i gesty
#    - Wyświetla wyniki na żywo
# 6. Użytkownik klika "Zatrzymaj Analizę"
# 7. Funkcja generate_report() tworzy raport:
#    - Oblicza średnie wartości
#    - Wysyła dane do AI
#    - Wyświetla wyniki i sugestie
#
# WSKAZÓWKI DLA STUDENTÓW:
# -------------------------
# - Spróbuj zmienić progi w funkcjach analyze_hands() i analyze_face()
# - Dodaj własne emocje lub gesty do wykrywania
# - Zmień kolory tekstu na obrazie (wartości BGR)
# - Dodaj nowe tryby analizy
# - Zapisz raport do pliku zamiast tylko wyświetlać
# - Dodaj wykresy do wizualizacji wyników (użyj matplotlib)
#
# ==================================================================================
