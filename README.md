# dziennik-ministrancki
Autorzy:
Łukasz Stanik
Mateusz Obrzut

##Use case
Ministranci w większości parafii są punktowani za wywiązywanie się z obowiązków -
w szczególności za przychodzenie lub nie na obowiązkowe msze.

## Funkcjonalność aplikacji
- definiowanie kont użytkowników (ministrantów)
- definiowanie terminów mszy (dzień tygodnia + godzina)
- przypisywanie użytkownikom obowiązkowych mszy
- rejestrowanie obecności ministrantów na mszach
- kalkulowanie punktacji i aktualizowanie bilansu punktów na kontach ministrantów

## Stos technologiczny
- MongoDB
- Python
- Flask


## Struktura bazy danych
#### uzytkownicy
Kolekcja zawierająca dane ministrantów w systemie

Dokument zawierający wymagane pola:
    
    {
        "_id" : ObjectId(...)
        "imie": string
        "nazwisko": string
    }
    
#### msze
Kolekcja zawierająca terminy mszy

Dokument zawierający wymagane pola:
    
    {
        "_id" : ObjectId(...)
        "dzien_tygodnia": string # Poniedziałek, Wtorek, Środa...
        "godzina": string # HH:MM
    }
    
#### sluzby
Kolekcja zawierająca służby (przypisania: ministrant <-> obowiązkowa msza)

Dokument zawierający wymagane pola:
    
    {
        "_id" : ObjectId(...)
        "ministrant_id": ObjectId(...) # referencja do dokumentu z kolekcji uzytkownicy
        "msza_id": ObjectId(...) # referencja do dokumentu z kolekcji msze
    }

#### obecnosci
Kolekcja zawierająca zarejestrowane obecności na mszach

Dokument zawierający wymagane pola:
    
    {
        "_id" : ObjectId(...)
        "ministrant_id": ObjectId(...) # referencja do dokumentu z kolekcji uzytkownicy
        "msza_id": ObjectId(...) # referencja do dokumentu z kolekcji msze
    }

## Opis działania
### Bilans punktów
Dla każdego ministranta obliczny jest bilans punktów na podstawie zdefiniowanych terminów obowiązkowych mszy 
oraz zarejestrowanych obecności. Bilans obliczany jest według wzoru:

    BIL = 5*OB + 2*NOB
    
gdzie

    BIL - bilans punktów
    OB - liczba obecności na mszach obowiązkowych (służbach)
    NOB - liczba obecności na mszach nieobowiązkowych
    