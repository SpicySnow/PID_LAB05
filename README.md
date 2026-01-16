# Zadanie grupowe PID LAB05


## Opis zadania

Zadanie to jest zadaniem grupowym. Grupa realizująca zadanie powinna liczyć od 5 do 10 osób, przy czym preferowana wielkość grupy to 7 osób.

Celem jest wykorzystanie wiedzy uzyskanej w trakcie realizacji poprzednich zadań laboratoryjnych do wspólnego wytworzenia małego systemu przetwarzania danych. Do dyspozycji grupy są wszystkie skrypty i pliki z poprzednich zajęć, oraz dodatkowo pliki do pobrania z cofta.eu/pid5.zip.

System realizuje zbieranie i przetwarzanie danych. W systemie istnieje szereg generatorów danych, regularnie wysyłających do brokera informacje o napięciu (V1) i częstotliwości (F), wraz ze znacznikiem czasu. Liczba tych generatorów nie jest z góry znana, i może ulec zmianie w czasie pracy systemu. Dane z tych generatorów powinny być buforowane w brokerze i zapamiętywane w bazie danych.

Jakkolwiek nie są znane wszystkie metody poboru danych z systemu, wiadomo, iż użytkownik potrzebuje:
1. ostatnie wartości V1 i F dla wszystkich generatorów, przy czym przez ‘ostatnie’ rozumiane są wartości z najwyższym znacznikiem czasu.

2. liczba odebranych próbek dla każdego generatora, liczona dla każdej minuty, z możliwością łatwego odczytywana dla każdej godziny (np. zapytanie dla generatora ‘ONE’, godzina 12:00, w dniu dzisiejszym produkuje do 60 rekordów)

Funkcja (1) powinna być zrealizowana w postaci tablicy z której można pobrać dane dla danego generatora. Funkcja (2) powinna być zrealizowana w postaci tablicy z której można pobrać dane dla wybranej godziny i dnia.

System powinien być całkowicie uruchamiany przy pomocy skryptu, który kasowałby poprzednie działające instancje systemu. Konieczne jest uruchomienie go jako zestawu kontenerów. Powinien on zawierać, jako minimum, minimalny  serwer Kafka i minimalny serwer Cassandra, oraz inne potrzebne komponenty.

Istnieje szereg rozwiązań tego problemu, różniących się między sobą przydatnością do pracy środowisku bardzo równoległym. Celem jest opracowanie takiego rozwiązania, które byłoby:
- skalowalne (w sensie bazy danych, brokera, liczby generatorów)
- odporne na typowe problemy środowiska współbieżnego (deadlock, race condition)
- pozwalające na zrównoleglenie opracowanych aplikacji

Ponieważ jest to zadanie grupowe, realizacja zadania powinna być grupowa. Powinna nastąpić np. dekompozycja zadania na elementy które mogłyby być realizowane równolegle, czy też grupowe uzgadnianie decyzji dotyczących systemu. Role członków grupy są pozostawione do decyzji grupy, ale wszyscy członkowie grupy muszą być zaangażowani w realizację.

## PODZIAŁ ZADAŃ

### JULIUSZ SULECKI – Docker & start systemu
Pliki:
- docker-compose.yml
- start.sh

Zakres:
- Kafka (minimalna konfiguracja)
- Cassandra (1 node)
- Sieć dockerowa
- Wolumeny

start.sh:

docker compose down -v

docker compose up --build


--------------------------------------------------

### JAN DRZAŻDŻYŃSKI – Generator danych (Kafka Producer)
Plik:
- generator.py

Zakres:
- Wysyła dane co X sekund do Kafki
- Topic: measurements
- ID generatora z ENV (GEN_ID)

Format danych:
`{
  "generator": "ONE",
  "ts": 1710000000,
  "V1": 230.5,
  "F": 50.02
}`

--------------------------------------------------

### KUBA WITENBERG – Kafka Consumer
Plik:
- consumer.py

Zakres:
- Czyta z topicu measurements
- Parsuje JSON
- Przekazuje dane do logiki zapisu do bazy

--------------------------------------------------

### ADRIANNA WIERZBIŃSKA – Zapis surowych danych
Pliki:
- schema_raw.cql
- db_raw.py

Tabela:
`raw_measurements(generator, day, ts, V1, F)`

Funkcja:
`save_raw(generator, ts, V1, F)`

--------------------------------------------------

### WIKTORIA CENDROWSKA-KOCIUGA – Ostatnie wartości
Pliki:
- schema_latest.cql
- db_latest.py

Tabela:
`latest(generator PRIMARY KEY, ts, V1, F)`

Funkcje:
- `update_latest(generator, ts, V1, F)`

- `get_latest(generator)`

--------------------------------------------------

### PAWEŁ CIEPŁUCH – Liczniki próbek
Pliki:
- schema_counts.cql
- db_counts.py

Tabela:
`counts(generator, day, hour, minute, count)`

Funkcje:
- `increment_count(generator, ts)`
- `get_counts(generator, day, hour)`

--------------------------------------------------

### OSOBA 7 – Integracja konsumenta
Plik:
- main_consumer.py

Kolejność wywołań:
1. save_raw(...)
2. update_latest(...)
3. increment_count(...)

Dodatkowo:
- Parsowanie danych
- Obsługa błędów
- Logowanie
- Brak testów i zapytań

--------------------------------------------------

### OSOBA 8 – Testy i zapytania
Plik:
- test_queries.py

Zakres:
- Tylko odczyt z Cassandry
- Brak Kafki
- Brak zapisu danych

Zapytania:
- Ostatnie wartości V1 i F
- Liczba próbek dla minuty i godziny

Weryfikacja:
- print lub assert
- Przykładowy output w komentarzu lub screenshot
