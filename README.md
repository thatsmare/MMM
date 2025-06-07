# Projekt z Metod Modelowania Matematycznego 
## Zadanie 10: Implementacja symulatora układu danego za pomocą transmitancji
### Cel projektu
Implementacja symulatora układu danego za pomocą transmitancji, umożliwiającego uzyskanie odpowiedzi czasowych układu na pobudzenia sygnałami: sinusoidalnym, prostokątnym, piłokształtnym, trójkątnym, impulsem prostokątnym, impulsem jednostkowym i skokiem jednosktkowym. Parametry sygnałów oraz współczynniki licznika i mianownika transmitancji można odpowiednio ustawiać w oknie symulacji. Symulator  umożliwia określenie stabilności układu oraz wykreślanie charakterystyk częstotliwościowych Bodego - amplitudowej i fazowej.

### Zaimplementowane funkcje symulatora
1. Wybór parametrów obiektu
2. Wybór sygnału wejściowego wraz z wszystkimi jego parametrami
3. Generowanie charakterystyk Bodego
4. Implementacja różniczkowania metodą Eulera
5. Przedstawienie graficzne sygnału wejściowego i wyjściowego
6. Określenie stabilności układu z wykorzystaniem zapasu wzmocnienia i fazy

### Wykorzystane biblioteki
* PyQt5 - utworzenie interfejsu użytkownika
* matplotlib - rysowanie wykresów charakterystyk Bodego, sygnału wejściowego i wyjściowego, rozmieszczenia biegunów na płaszczyźnie zespolonej
* numpy - obliczenia, generowanie siatki czasowej
* scipy.signal - wykorzystanie TransferFunction do wyznaczania zer i biegunów transmitancji układu
