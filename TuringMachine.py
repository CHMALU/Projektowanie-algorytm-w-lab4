import networkx as nx
import matplotlib.pyplot as plt
import time

class MT:
    def __init__(self, zb_stnw, alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od):
        self.zb_stnw = zb_stnw
        self.alfbt_wej = alfbt_wej
        self.alfbt_tsm = alfbt_tsm
        self.fun_prz = fun_prz
        self.stn_p = stn_p
        self.stn_ak = stn_ak
        self.stn_od = stn_od
        self.akt_stan = stn_p
        self.tasma = []
        self.glowa = 0

    def start(self, slowo):
        self.tasma = list(slowo) + ['_']
        self.glowa = 0
        kroki = []

        while True:
            akt_symbol = self.tasma[self.glowa]
            kroki.append((self.akt_stan, self.glowa, list(self.tasma)))

            if self.akt_stan == self.stn_ak:
                print("Akceptacja")
                break
            if self.akt_stan == self.stn_od or akt_symbol not in self.fun_prz.get(self.akt_stan, {}):
                print("Odrzucenie")
                break

            nowy_stan, nowy_symbol, ruch = self.fun_prz[self.akt_stan][akt_symbol]

            print(f"Przejście: z (Stan: {self.akt_stan}, Symbol: {akt_symbol}) -> (Stan: {nowy_stan}, Nowy symbol: {nowy_symbol}, Ruch: {ruch})")


            self.tasma[self.glowa] = nowy_symbol
            self.akt_stan = nowy_stan

            if ruch == "R":
                self.glowa += 1
                if self.glowa >= len(self.tasma):
                    self.tasma.append('_')
            elif ruch == "L":
                self.glowa = max(0, self.glowa - 1)

        return kroki

def wizualizuj_maszyne(mt, kroki):
    G = nx.DiGraph()
    for stan, przejscia in mt.fun_prz.items():
        for symbol, (nast_stan, _, _) in przejscia.items():
            G.add_edge(stan, nast_stan, label=symbol)

    pos = nx.spring_layout(G)
    etykiety = {krawedz: G.edges[krawedz]['label'] for krawedz in G.edges}

    def rysuj_graf(akt_stan, tasma, glowa):
        plt.clf()
        nx.draw(G, pos, with_labels=True,
                node_color=['lightgreen' if stan == mt.stn_ak else 'lightblue' for stan in G.nodes],
                edge_color='gray', node_size=2000, font_size=12)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=etykiety)
        nx.draw_networkx_nodes(G, pos, nodelist=[akt_stan], node_color='red', node_size=2000)
        plt.title(f"Stan: {akt_stan}\nTaśma: {''.join(tasma)}\n{' ' * glowa + '^'}")
        plt.pause(1)

    plt.figure(figsize=(8, 6))
    for stan, glowa, tasma in kroki:
        rysuj_graf(stan, tasma, glowa)
    plt.show()

#!Zadanie 1
#przepisuje dane z obrazka
zb_stnw = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "qa", "qr"}
stn_p = 'q0'
stn_ak = 'qa'
stn_od = 'qr'
alfbt_wej = {"a", "o", "_"}
alfbt_tsm = {"a", "o", "å", "_"}

#zadanie przykładowe od Pana, lecz można zmienić na dowolny inny który obejmuje słownik
w1 = "aaa_"
print(f"\nZadanie 1 dla słowa: {w1}")

#przepisuje przejścia na grafie z obrazka
fun_prz = {
    "q0": {"a": ["q1", "å", "R"], "_": ["qr", "a", "L"]},
    "q1": {"a": ["q2", "a", "L"], "o": ["q1", "o", "R"], "_": ["qa", "_", "L"]},
    "q2": {"o": ["q2", "o", "L"], "å": ["q3", "å", "L"]},
    "q3": {"a": ["q4", "a", "R"], "o": ["q3", "o", "R"], "å": ["q4", "å", "R"], "_": ["q6", "_", "L"]},
    "q4": {"a": ["q5", "o", "R"], "o": ["q4", "o", "R"], "_": ["qr", "_", "L"]},
    "q5": {"a": ["q3", "o", "R"], "o": ["q5", "o", "R"], "_": ["qr", "_", "L"]},
    "q6": {"a": ["q6", "a", "L"], "o": ["q6", "o", "L"], "å": ["q1", "å", "R"]},
}

#wrzucamy parametry do defa maszyny turinga
mt = MT(zb_stnw, alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od)
#odpalam 'maszyne' i tworzę zmienną kroki, która może przydać się do przyszłej wizualizacji
steps = mt.start(w1)


#!Zadania 2
#przepisuje dane z obrazka
zb_stnw = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "qa", "qr"}
alfbt_wej = {"0", "1", "b", "_"}
alfbt_tsm = {"0", "1", "b", "ϕ", "†", "_"}
stn_p = "q0"
stn_ak = "qa"
stn_od = "qr"

#przepisuje przejścia na grafie z obrazka
fun_prz = {
    "q0": {"b": ["q1", "b", "R"], "0": ["q2", "ϕ", "R"], "1": ["q3", "†", "R"], "ϕ": ["q7", "ϕ", "R"],
           "†": ["q7", "†", "R"]},
    "q1": {"ϕ": ["q1", "ϕ", "R"], "†": ["q1", "†", "R"], "0": ["qr", "0", "L"], "1": ["qr", "1", "L"],
           "_": ["qa", "_", "L"]},
    "q2": {"0": ["q2", "0", "R"], "1": ["q2", "1", "R"], "b": ["q4", "b", "R"], "_": ["qr", "_", "R"]},
    "q3": {"0": ["q3", "0", "R"], "1": ["q3", "1", "R"], "b": ["q5", "b", "R"], "_": ["qr", "_", "R"]},
    "q4": {"ϕ": ["q4", "ϕ", "R"], "_": ["qr", "_", "R"], "1": ["qr", "1", "R"]},
    "q5": {"ϕ": ["q5", "ϕ", "R"], "†": ["q5", "†", "R"], "_": ["qr", "_", "R"], "0": ["qr", "0", "R"]},
    "q6": {"ϕ": ["q6", "ϕ", "L"], "†": ["q6", "†", "L"], "b": ["q7", "b", "L"], "0": ["q7", "ϕ", "L"]},
    "q7": {"0": ["q0", "0", "L"], "1": ["q0", "1", "L"], "ϕ": ["q7", "ϕ", "R"], "†": ["q7", "†", "R"]}
}

#wrzucamy parametry do defa maszyny turinga
mt = MT(zb_stnw, alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od)

#zadanie przykładowe od Pana, lecz można zmienić na dowolny inny który obejmuje słownik
w1 = "1b1b0_"
print(f"\nZadanie 2 dla słowa: {w1}")
#odpalam 'maszyne' i tworzę zmienną kroki, która może przydać się do przyszłej wizualizacji
steps = mt.start(w1)
#wizualizacja
wizualizuj_maszyne(mt, steps)

#! Zadanie 3
def decyduj_jezyk(alphabet, word):
    if word.count('x') != 1:
        return f"{word}\n Język nierozstrzygnięty: nie ma x"

    # Podziel słowo na a, b możemy tak zrobić bo wiemy ze w a i b nie ma 'x'
    a, b = word.split('x')

    # Sprawdź, czy a i b zawierają tylko symbole z (alphabet - {'x'})
    allowed = alphabet - {'x'}
    if not all(ch in allowed for ch in a + b):
        return f"{word}\n Język nierozstrzygnięty nie ma znaku z alfabetu"

    # Sprawdź, czy długości a i b są równe
    if len(a) == len(b):
        return f"{word}\n Język rozstrzygnięty"
    else:
        return f"{word}\n Język nierozstrzygnięty różne długości a i b"


alphabet = set("ehf_") # dodatkowo dodałem _ bo nie ma go w przykładzie a jest blank

w1 = "x_"
print(decyduj_jezyk(alphabet, w1))
w2 = "hexhf_"
print(decyduj_jezyk(alphabet, w2))
w3 = "hexhff_"
print(decyduj_jezyk(alphabet, w3))

#! Zadanie 4
'''
Maszyna Turinga: Weryfikacja poprawności zapisu listy wierzchołków

Stan q0 (start):
    - Jeśli aktualny symbol == '[', przejdź do stanu q1; w przeciwnym razie -> Odrzuć (qr).

Stan q1:
    - Jeśli aktualny symbol == ']' (pusta lista), przejdź do stanu akceptacji (qa).
    - Jeśli aktualny symbol jest cyfrą (0-9), przejdź do stanu q2.
    - W przeciwnym razie -> Odrzuć.

Stan q2 (odczyt wierzchołka):
    - Dopóki aktualny symbol jest cyfrą, przesuwaj głowicę w prawo.
    - Gdy napotkasz symbol niebędący cyfrą:
        - Jeśli symbol to ',' – przejdź do stanu q1 (oczekiwanie kolejnego wierzchołka).
        - Jeśli symbol to ']' – przejdź do stanu akceptacji (qa).
        - W przeciwnym razie -> Odrzuć.

Stan qa:
    - Akceptuj zapis.

Stan qr:
    - Odrzuć zapis.

Komentarz dotyczący złożoności:
Maszyna wykonuje jeden przebieg taśmą – każdy symbol jest sprawdzany co najwyżej raz, zatem złożoność czasowa wynosi O(n), gdzie n to długość słowa.
'''

#! Zadanie 5
zb_stnw = {"q0", "q1", "q2", "q3", "qa", "qr"}

# Alfabet wejściowy
alfbt_wej = set("[],0123456789 ")
alfbt_tsm = set("[],0123456789 _")  # dodajemy '_' jako symbol pusty

stn_p = "q0"
stn_ak = "qa"
stn_od = "qr"

fun_prz = {
    # q0: Na początku ignorujemy spacje, oczekujemy znaku '['
    "q0": {
        " ": ["q0", " ", "R"],
        "[": ["q1", "[", "R"]
    },
    # q1: Oczekiwanie na pierwszy wierzchołek lub koniec listy
    "q1": {
        " ": ["q1", " ", "R"],
        "]": ["qa", "]", "R"],
        ",": ["qr", ",", "R"]  # przecinek na początku jest niedozwolony
    },
    # q2: Czytanie wierzchołka – ciąg cyfr
    "q2": {
        # Dla każdej cyfry pozostajemy w q2
        "0": ["q2", "0", "R"],
        "1": ["q2", "1", "R"],
        "2": ["q2", "2", "R"],
        "3": ["q2", "3", "R"],
        "4": ["q2", "4", "R"],
        "5": ["q2", "5", "R"],
        "6": ["q2", "6", "R"],
        "7": ["q2", "7", "R"],
        "8": ["q2", "8", "R"],
        "9": ["q2", "9", "R"],
        # Po cyfrze można mieć spację lub od razu przecinek albo ']'
        " ": ["q3", " ", "R"],
        ",": ["q1", ",", "R"],
        "]": ["qa", "]", "R"]
    },
    # q3: Pomijanie spacji po wierzchołku
    "q3": {
        " ": ["q3", " ", "R"],
        ",": ["q1", ",", "R"],
        "]": ["qa", "]", "R"],
        # Jeżeli trafimy na cyfrę w stanie q3, to oznacza, że wierzchołek został źle zapisany (cyfry nie mogą wystąpić po spacji)
        "0": ["qr", "0", "R"],
        "1": ["qr", "1", "R"],
        "2": ["qr", "2", "R"],
        "3": ["qr", "3", "R"],
        "4": ["qr", "4", "R"],
        "5": ["qr", "5", "R"],
        "6": ["qr", "6", "R"],
        "7": ["qr", "7", "R"],
        "8": ["qr", "8", "R"],
        "9": ["qr", "9", "R"]
    }
}

# W stanie q1, gdy trafimy na cyfrę, przechodzimy do q2
for d in "0123456789":
    fun_prz["q1"][d] = ["q2", d, "R"]

cyfry_maszyna = MT(zb_stnw, alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od)

# Funkcja pomocnicza do symulacji i wizualizacji
def symuluj(tape_input):
    print(f"\nSymulacja dla wejścia: {tape_input}")
    steps = cyfry_maszyna.start(tape_input)
    # wizualizuj_maszyne(cyfry_maszyna, steps)

w1 = "[0107, 999422, 3]"
w2 = "[0107 999422, 3]"
w3 = "[0107, 999a22, 3]"

# Symulacje
symuluj(w1)
time.sleep(2)
cyfry_maszyna = MT(zb_stnw, alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od)
symuluj(w2)
time.sleep(2)
cyfry_maszyna = MT(zb_stnw, alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od)
symuluj(w3)