https://docs.google.com/document/d/1FTu9GTPfYdB4rMh78692R0HTbTtnsxleJcHWmBXNjB4/edit

my_model_2.keras - wytrenowany testowo na dwóch gestach (cześć i dzień dobry)

my_model_3_1.keras - wytrenowany na 3 pierwszych lekcjach, dla każdej +- 30 nagrań/gest

my_model_4_3.keras - najnowszy model, wytrenowany na trzech pierwszych lekcjach, dla każdej na 60 nagraniach/gest

## Nagrywanie danych
* data_collection.py
* w 60 linijce trzeba wybrać, dla której lekcji chce się nagrywać (listy wyrażeń są w expressions.py - 1 lekcje przydałoby się uzupełnić z YT, bo z jakiegoś powodu kiedyś z niej prawie wszystko usunęłam xd)
* po uruchomieniu kodu, jak się wszystko załaduje, powinno się wyświetlić okienko z podglądem z kamery, w którym będzie też widać pozaznaczane landmarki na dłoniach
* w terminalu powinno się na bieżąco wyświetlać co się dzieje, ale ogólnie:
    * spacja - zaczyna się nagrywanie sekwencji (teraz jest ustawione 30 klatek i jak sprawdzałam to można w tym czasie całkiem sensownie i dokładnie te gesty wykonać)
    * strzałka w prawo - zmiana gestu na kolejny z listy
    * ESC - koniec nagrywania
* z istotnych rzeczy, kolejne gesty powinny się po nagraniu dodawać do odpowiedniego katalogu - numerują się automatycznie po kolei, więc przed nagrywaniem musimy się pilnować, żeby sobie wszystko z gita wcześniej ściągnąć i potem scommitować, tak żeby sie numerki zgadzały

## Trening modelu
Do treningu modelu można użyć skryptu model.py, ale chyba wygodniej to zrobić wykrozystując notebook training.ipynb (z potencjalnie głupich ale istotnych błędów - trzeba pamiętać o zmianie nazwy modelu, który zapisujemy).

## Uruchomienie aplikacji
Główna aplikacja znajduje się w skrypcie main.py. Po uruchomieniu (trzeba pamiętać o odpowiedniej nazwie modelu + klasy, które chcemy przewidywać, muszą się zgadzać z tymi, które aktualnie są w folderze data - przydałoby się to w przyszłości jakoś ogarnąć lepiej) powinno się otworzyć takie samo okienko jak przy nagrywaniu danych. po wciśnięciu spacji zaczyna się zbieranie 30 klatek do predykcji (póki co przed każdym gestem trzeba tą spację wciskać, potencjalnie do ogarnięcia w przyszłości, żeby tłumaczyło się "symultanicznie")
