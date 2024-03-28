my_model_2.keras - wyrenowany testowo na dwóch gestach (cześć i dzień dobry)

## Nagrywanie danych
* data_collection.py
* w 60 linijce trzeba wybrać, dla której lekcji chce się nagrywać (listy wyrażeń są w expressions.py - 1 lekcje przydałoby się uzupełnić z YT, bo z jakiegoś powodu kiedyś z niej prawie wszystko usunęłam xd)
* po uruchomieniu kodu, jak się wszystko załaduje, powinno się wyświetlić okienko z podglądem z kamery, w którym będzie też widać pozaznaczane landmarki na dłoniach
* w terminalu powinno się na bieżąco wyświetlać co się dzieje, ale ogólnie:
    * spacja - zaczyna się nagrywanie sekwencji (teraz jest ustawione 30 klatek i jak sprawdzałam to można w tym czasie całkiem sensownie i dokładnie te gesty wykonać)
    * strzałka w prawo - zmiana gestu na kolejny z listy
    * ESC - koniec nagrywania
* z istotnych rzeczy, kolejne gesty powinny się po nagraniu dodawać do odpowiedniego katalogu - numerują się automatycznie po kolei, więc przed nagrywaniem musimy się pilnować, żeby sobie wszystko z gita wcześniej ściągnąć i potem scommitować, tak żeby sie numerki zgadzały