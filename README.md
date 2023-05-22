# GPU Game Search
Find the right GPU for your video game.

### POLISH

##### Charakterystyka oprogramowania
###### Nazwa skrócona
GPU-GSearch
###### Nazwa pełna
GPU Game Search
###### Krótki opis
Narzędzie służące do rekomendowania użytkownikom układów graficznych na podstawie wybranej gry wideo. Głównym celem oprogramowania jest zapewnienie użytkownikowi najlepszego możliwego wyboru GPU.

##### Prawa autorskie
###### Autorzy
Rafał Nowak
###### Licencja
MIT License

##### Specyfikacja wymagań
| Identyfikator | Nazwa | Opis | Priorytet | Kategoria |
| --------------|-------|------|-----------|-----------|
| REQ-001 | Rekomendowanie kart graficznych | Oprogramowanie powinno być w stanie rekomendować użytkownikom odpowiednie karty graficzne dla wybranej gry komputerowej na podstawie wymagań sprzętowych gry.| Wysoki | Funkcjonalność |
| REQ-002 | Filtrowanie wyników | Oprogramowanie powinno być w stanie filtrować wyniki wyszukiwania kart graficznych w oparciu o podane przez użytkownika kryteria.| Wysoki | Funkcjonalność |
| REQ-003 | Oparcie na bazie danych | Oprogramowanie powinno być oparte na bazie danych specyfikacji gier komputerowych | Wysoki | Funkcjonalność |
| REQ-004 | Interfejs graficzny | Oprogramowanie powinno posiadać przejrzysty interfejs ułatwiający interakcje. | Średni | Użyteczność |
| REQ-005 | Optymalizacja | Oprogramowanie powinno działać szybko i sprawnie, aby użytkownicy mogli wydajnie pracować z aplikacją. | Średni | Wydajność |
| REQ-006 | Język interfejsu | Oprogramowanie powinno mieć interfejs w języku angielskim. | Niski | Interfejs użytkownika |

##### Architektura oprogramowania
###### Architektura rozwoju
Projekt GPU-GSearch jest napisany w języku Python we frameworku Flask. 

Główną funkcjonalnością projektu jest możliwość wyszukiwania oraz wybierania gier z <a name="https://www.igdb.com/api">bazy danych IGDB za pomocą publicznego API.</a>

Który jest zimplementowany przy użyciu <a href="https://github.com/twitchtv/igdb-api-python">wrappera napisanego dla języka Python</a>

GPU-GSearch zawiera dwie funkcje wysyłające zapytania do API, z których pierwsza, get_games(name), wyszukuje i wybiera grę po nazwie wprowadzonej przez użytkownika, natomiast druga, get_games_full(id) wyszukuje gre po id z dodatkowymi szczegółami.

Następnie za pomocą biblioteki mysql.connector wysyłane jest zapytanie do bazy danych w MySQL, w której zawierają się informacje na temat rekomendowanych oraz minimalnych kart graficznych dla wybranej gry.

Do zaimplementowania interfejsu wykorzystana została <a href="https://getbootstrap.com/">biblioteka Bootstrap</a>, natomist commity zostały stworzone według metody <a href="https://www.conventionalcommits.org/en/v1.0.0/">Conventional Commits</a>

###### Architektura uruchomieniowa
Aby uruchomić projekt GPU-GSearch, należy wykonać trzy główne czynności:

1. Przygotować środowisko Python Flask:
Najpierw należy utworzyć plik `.flaskenv` w katalogu projektu (na tym samym poziomie co pakiet api)
w którym zdefiniujesz 2 zmienne środowiskowe, które zostaną automatycznie ustawione
po zainstalowaniu python-dotenv.
Tak więc, plik musi zawierać następujące zmienne:
```
FLASK_ENV=development
FLASK_APP=api/__init__.py
```
Następnie należy utworzyć <a href="https://docs.python.org/3/library/venv.html">utworzyć środowisko wirtualne</a>
Po jego utworzeniu należy je aktywować. 
```
W systemie Linux polecenie to zazwyczaj `source venv/bin/activate` 
W systemie Windows jest to zazwyczaj `venv\Scripts\activate.bat`.
``` 
Jednak w szczególnych przypadkach należy ponownie zapoznać się z linkiem do tworzenia środowiska wirtualnego.

Po skonfigurowaniu virtualenv, należy ostatecznie zainstalować zależności za pomocą `pip install -r requirements.txt`.

Aby uruchomić projekt, należy użyć komendy `flask run`. 
2. Skonfigurowanie połączenia do bazy danych
Aby wyświetlać rekomendacje kart graficznych bazy danych, należy skonfigurować do niej połączenie.

W pierwszej kolejności należy stworzyć <a href="https://dev.mysql.com/doc/mysql-getting-started/en/">bazę danych w MySQL</a> oraz dodać od niej odpowiednie tabele w schemacie, który musi zawierać pola:
```
name
max_gpu_nvidia
min_gpu_nvidia
min_gpu_amd
max_gpu_amd
w tabeli 'games'
```
Zawierające odpowiednie karty graficzne dla danej gry.

Następnie należy zmodyfikować informacje dostępu do bazy danych, w szczególności hasło oraz nazwę bazy danych
```
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="database" )
```
3. Uzyskanie access tokena do API IGDB
 
 Aby uzyskać token do API IGDB należy <a href="https://api-docs.igdb.com/#getting-started">postąpić zgodnie z instrukcją na stronie API</a> a następnie zaktualizować inicjalizator wrappera
```
 wrapper = IGDBWrapper('clientName','accessToken')
```

##### Testy
###### Scenariusze testów
1. test_home_page_with_fixture: Ten test sprawdza, czy strona główna ("/") zwraca poprawną odpowiedź po żądaniu metodą GET.

2. test_about_page_with_fixture: Ten test sprawdza, czy strona informacyjna ("/about") zwraca poprawną odpowiedź po żądaniu metodą GET.

3. test_search_game_with_fixture: Ten test sprawdza, czy strona wyszukiwania ("/search") zwraca poprawny szablon listy po żądaniu metodą POST z poprawnym terminem wyszukiwania. Potwierdza również, czy odpowiedź zawiera oczekiwany termin wyszukiwania.

4. test_search_empty_with_fixture: Ten test sprawdza, czy strona wyszukiwania ("/search") zwraca wiadomość błędu po żądaniu metodą POST z niepoprawnym pustym terminem wyszukiwania. Wyodrębnia wiadomość błędu z odpowiedzi i porównuje ją z oczekiwaną wiadomością.

5. test_home_page_post_with_fixture: Ten test sprawdza, czy przesłanie żądania do strony głównej ("/") zwraca kod statusu "405" (Metoda niedozwolona), co wskazuje, że metoda POST nie jest dozwolona na tej stronie.

6. test_find_gpu_valid_id_with_fixture: Ten test sprawdza, czy strona wyszukiwania GPU ("/find_gpu") zwraca poprawną odpowiedź po żądaniu metodą POST z poprawnymi danymi. Potwierdza również, czy odpowiedź zawiera oczekiwaną grę.
###### Sprawozdanie z wykonania scenariuszy testów
Wszystkie scenariusze testowe zostały pomyślnie wykonane bez żadnych błędów. Aplikacja Flask działała zgodnie z oczekiwaniami i zwróciła poprawne odpowiedzi dla różnych ścieżek i danych wejściowych.

Podsumowanie potwierdza pomyślne wykonanie scenariuszy testowych i wskazuje, że aplikacja działa poprawnie zgodnie z obecnym zakresem testów.

### ENGLISH

##### Software Characteristics
###### Short name
GPU-GSearch
###### Full name
GPU Game Search
###### Brief Description
A tool for recommending GPUs to users based on the selected video game. The main goal of the software is to provide the user with the best possible choice of GPU.

##### Copyright
###### Authors
Rafal Nowak
###### License
MIT License

##### Requirements specification
| Identifier | Name | Description | Priority | Category |
| --------------|-------|------|-----------|-----------|
| REQ-001 | Graphics card recommendation | The software should be able to recommend users appropriate graphics cards for a selected computer game based on the game's hardware requirements.| High | Functionality |
| REQ-002 | Filtering results | The software should be able to filter the results of a graphics card search based on the criteria provided by the user.| High | Functionality | 
| REQ-003 | Database-based | The software should be based on a database of computer game specifications | High | Functionality | 
| REQ-004 | Graphical interface | The software should have a clear interface to facilitate interactions. | Medium | Usability | 
| REQ-005 | Optimization | The software should run quickly and efficiently so that users can work efficiently with the application. | Medium | Performance |
| REQ-006 | Interface Language | The software should have an interface in English. | Low | User interface | User interface | 

##### Software architecture
###### Development architecture
The GPU-GSearch project is written in Python using the Flask framework.

The main functionality of the project is the ability to search and select games from the <a href="https://www.igdb.com/api">IGDB database using a public API</a>. It is implemented using a <a href="https://github.com/twitchtv/igdb-api-python">Python wrapper</a> for the API.

GPU-GSearch includes two functions that send requests to the API. The first function, get_games(name), searches and selects a game based on the name entered by the user. The second function, get_games_full(id), searches for a game based on its ID and retrieves additional details.

The project uses the mysql.connector library to send queries to a MySQL database, which contains information about recommended and minimum graphics cards for the selected game.

The interface is implemented using the <a href="https://getbootstrap.com/">Bootstrap library</a>. Commits are structured according to the <a href="https://www.conventionalcommits.org/en/v1.0.0/">Conventional Commits</a> method.
###### Startup architecture
To run the GPU-GSearch project, you need to perform three main steps:

1. Set up the Python Flask environment:

First, create a .flaskenv file in the project directory (at the same level as the api package) to define two environment variables that will be automatically set after installing python-dotenv.

The file should contain the following variables:

```
FLASK_ENV=development
FLASK_APP=api/__init__.py
```
Next, create a virtual environment. <a href="https://docs.python.org/3/library/venv.html">You can refer to the documentation on creating a venv.</a> Once created, activate the virtual environment.
```
On Linux: source venv/bin/activate
On Windows: venv\Scripts\activate.bat
```
Note: Refer to the specific documentation for creating a virtual environment if you encounter any issues.
Once the virtual environment is set up, finally install the dependencies using pip install -r requirements.txt.

To run the project, use the command 'flask run'.

2. Configure the database connection:

To display graphics card recommendations from the database, you need to configure the connection to the database.
First, <a href="https://dev.mysql.com/doc/mysql-getting-started/en/">create a MySQL database</a> and add the necessary tables with the following fields in the 'games' table
```
name
max_gpu_nvidia
min_gpu_nvidia
min_gpu_amd
max_gpu_amd
```
Modify the database access information, especially the password and database name, in the code:
```
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="database")
```
3. Obtain an access token for the IGDB API:

To obtain a token for the IGDB API, follow the instructions <a href="https://api-docs.igdb.com/#getting-started">provided in the API documentation</a>, and update the wrapper initialization accordingly:
```
wrapper = IGDBWrapper('clientName', 'accessToken')
```
##### Tests
###### Test scenarios
1. test_home_page_with_fixture: This test ensures that the home page ("/") returns a valid response when requested with the GET method.

2. test_about_page_with_fixture: This test verifies that the about page ("/about") returns a valid response when requested with the GET method.

3. test_search_game_with_fixture: This test checks that the search page ("/search") returns the valid list template when requested with a valid search term using the POST method. It also confirms that the response contains the expected search term.

4. test_search_empty_with_fixture: This test validates that the search page ("/search") returns the error message when requested with an invalid empty search term using the POST method. It extracts the error message from the response and compares it with the expected message.

5. test_home_page_post_with_fixture: This test ensures that posting to the home page ("/") returns a "405" (Method Not Allowed) status code, indicating that the POST method is not allowed on this page.

6. test_find_gpu_valid_id_with_fixture: This test checks that the find GPU page ("/find_gpu") returns a valid response when requested with valid data using the POST method. It also confirms that the response contains the expected game.
###### Test scenarios execution report
Test Scenario Execution Report:

All test scenarios executed successfully without any failures. The Flask application performed as expected and returned valid responses for different routes and inputs.

This summary acknowledges the successful execution of the test scenarios and indicates that the application is functioning correctly based on the current test coverage.
