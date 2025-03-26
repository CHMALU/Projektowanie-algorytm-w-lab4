import networkx as nx
import matplotlib.pyplot as plt
import time

class TuringMachine:
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

    def przetworz_wejscie(self, slowo):
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

# Zadanie 1
stn_p = 'q0'
stn_ak = 'qa'
stn_od = 'qr'
alfbt_wej = {"a", "o", "_"}
alfbt_tsm = {"a", "o", "å", "_"}

w1 = "aaa_"
print(f"\nZadanie 1 dla słowa: {w1}")

fun_prz = {
    "q0": {"a": ["q1", "å", "R"], "_": ["qr", "a", "L"]},
    "q1": {"a": ["q2", "a", "L"], "o": ["q1", "o", "R"], "_": ["qa", "_", "L"]},
    "q2": {"o": ["q2", "o", "L"], "å": ["q3", "å", "L"]},
    "q3": {"a": ["q4", "a", "R"], "o": ["q3", "o", "R"], "å": ["q4", "å", "R"], "_": ["q6", "_", "L"]},
    "q4": {"a": ["q5", "o", "R"], "o": ["q4", "o", "R"], "_": ["qr", "_", "L"]},
    "q5": {"a": ["q3", "o", "R"], "o": ["q5", "o", "R"], "_": ["qr", "_", "L"]},
    "q6": {"a": ["q6", "a", "L"], "o": ["q6", "o", "L"], "å": ["q1", "å", "R"]},
}

machine_1 = TuringMachine(set(fun_prz.keys()), alfbt_wej, alfbt_tsm, fun_prz, stn_p, stn_ak, stn_od)
steps = machine_1.przetworz_wejscie(w1)

# Definicja maszyny Turinga dla Zadania 2
states = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "qa", "qr"}
input_alphabet = {"0", "1", "b", "_"}
tape_alphabet = {"0", "1", "b", "ϕ", "†", "_"}
start_state = "q0"
accept_state = "qa"
reject_state = "qr"

transitions = {
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

# Uruchomienie symulacji i wizualizacji
machine = TuringMachine(states, input_alphabet, tape_alphabet, transitions, start_state, accept_state, reject_state)

w1 = "1b1b0_"
print(f"\nZadanie 2 dla słowa: {w1}")
steps = machine.przetworz_wejscie(w1)
wizualizuj_maszyne(machine, steps)