from collections import deque

# ── Colori ANSI ───────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GRIGIO = "\033[90m"   # non ancora scoperto
BLU    = "\033[94m"   # nodo estratto / in elaborazione
VERDE  = "\033[92m"   # già visitato
ARANCIO= "\033[93m"   # scoperto, in attesa in coda/pila

def col(colore, testo):
    return f"{colore}{testo}{RESET}"

def pausa():
    input(col(DIM, "\n  [Invio per continuare...]"))

def intestazione(titolo):
    linea = "═" * 54
    print(f"\n{col(BOLD+BLU, linea)}")
    print(col(BOLD+BLU, f"  {titolo}"))
    print(col(BOLD+BLU, linea))

def passo(n):
    print(f"\n{col(BOLD, f'── Passo {n} ')}{'─'*40}")


# ── Classe Graph────────────────────────────────────────
class Graph:
    def __init__(self):
        self._adj = {}

    def addEdge(self, a, b):
        if a not in self._adj: self._adj[a] = []
        if b not in self._adj: self._adj[b] = []
        if b not in self._adj[a]: self._adj[a].append(b)
        if a not in self._adj[b]: self._adj[b].append(a)

    def getNeighbors(self, node):
        return sorted(self._adj.get(node, []))

    def nodes(self):
        return sorted(self._adj.keys())


# ── Grafo ───────────────────────────────────────────────────────
def costruisci_grafo():
    g = Graph()
    g.addEdge("A", "B")
    g.addEdge("A", "C")
    g.addEdge("B", "D")
    g.addEdge("B", "E")
    g.addEdge("C", "E")
    g.addEdge("C", "F")
    g.addEdge("D", "E")
    return g


# ── Grafo ASCII colorato ──────────────────────────────────────────────────────
def stampa_grafo(visitati=None, corrente=None, in_attesa=None):
    visitati  = visitati  or set()
    in_attesa = in_attesa or set()

    def stile(n):
        if n == corrente:       return col(BOLD+BLU,    f"[{n}]")
        elif n in visitati:     return col(BOLD+VERDE,  f"[{n}]")
        elif n in in_attesa:    return col(BOLD+ARANCIO,f"[{n}]")
        else:                   return col(GRIGIO,      f" {n} ")

    A=stile("A"); B=stile("B"); C=stile("C")
    D=stile("D"); E=stile("E"); F=stile("F")

    print(f"""
        {A}
       /   \\
      {B}   {C}
     / \\ / \\
    {D}  {E}  {F}
     \\ /
    (D─E)
""")

def stampa_legenda():
    print(col(BLU,    "  [X] = estratto / in elaborazione"))
    print(col(ARANCIO,"  [X] = scoperto, in attesa in coda/pila"))
    print(col(VERDE,  "  [X] = già visitato"))
    print(col(GRIGIO, "   X  = non ancora scoperto"))

def stampa_stato(struttura, nome_struttura, visitati, result, messaggio):
    items = ", ".join(struttura) if struttura else "vuota"
    vis   = "{ " + ", ".join(sorted(visitati)) + " }" if visitati else "{ }"
    res   = "[ " + ", ".join(result) + " ]"          if result    else "[ ]"
    print(f"  {col(BOLD, nome_struttura+':')}  {col(ARANCIO, f'[ {items} ]')}")
    print(f"  {col(BOLD, 'visited:     ')}  {col(VERDE,   vis)}")
    print(f"  {col(BOLD, 'result:      ')}  {col(BLU,     res)}")
    print(f"\n  → {messaggio}")


# ── BFS ──────────────────────────────
def bfs(graph, start):
    intestazione("BFS — Breadth First Search  (Queue / FIFO)")
    print(f"""
  Visita prima tutti i vicini diretti, poi i vicini dei vicini.
  Si espande {col(BOLD,"a livelli")}, come un'onda.
  Struttura: {col(BOLD+ARANCIO,"Queue (FIFO)")} — il primo entrato è il primo uscito.
  Serve anche {col(BOLD+VERDE,"visited")} (set) per non girare in ciclo.
""")
    stampa_legenda()
    pausa()

    visited = set()
    queue   = deque()

    visited.add(start)
    queue.append(start)

    result = []

    n = 0

    def mostra(msg, corrente=None):
        nonlocal n
        n += 1
        passo(n)
        stampa_grafo(visited, corrente, set(queue))
        stampa_stato(list(queue), "queue", visited, result, msg)
        pausa()

    mostra(
        f"Aggiungo {col(BOLD,start)} alla coda e lo segno in visited.",
        corrente=start
    )

    while queue:
        node = queue.popleft()        # prendo il primo della coda
        result.append(node)

        mostra(
            f"Estraggo {col(BOLD+BLU, node)} dalla testa della coda (popleft). "
            f"Lo aggiungo a result.",
            corrente=node
        )

        for neighbor in graph.getNeighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                mostra(
                    f"Vicino {col(BOLD+ARANCIO, neighbor)} di {col(BOLD,node)}: "
                    f"non in visited → lo aggiungo in {col(BOLD,'fondo')} alla coda e in visited.",
                    corrente=node
                )
            else:
                mostra(
                    f"Vicino {col(BOLD+VERDE, neighbor)} di {col(BOLD,node)}: "
                    f"già in visited → {col(DIM,'ignorato')}.",
                    corrente=node
                )

    print(f"\n{col(BOLD+VERDE,'  ✓ BFS completato!')}")
    stampa_grafo(visited)
    print(f"  Ordine di visita: {col(BOLD+BLU, ' → '.join(result))}")
    print(col(DIM,"  (L'ordine riflette la distanza dal nodo di partenza.)"))
    return result


# ── DFS ──────────────────────────────
def dfs(graph, start):
    intestazione("DFS — Depth First Search  (Stack / LIFO)")
    print(f"""
  Segue un percorso fino in fondo, poi torna indietro.
  Non si espande a livelli: sceglie una direzione e la segue.
  Struttura: {col(BOLD+ARANCIO,"Stack (LIFO)")} — l'ultimo entrato è il primo uscito.
  Serve anche {col(BOLD+VERDE,"visited")} (set) per non girare in ciclo.
""")
    stampa_legenda()
    pausa()

    visited = set()
    stack   = []

    stack.append(start)

    result = []

    n = 0

    def mostra(msg, corrente=None):
        nonlocal n
        n += 1
        passo(n)
        stampa_grafo(visited, corrente, set(stack))
        stampa_stato(list(reversed(stack)), "stack (top→)", visited, result, msg)
        pausa()

    mostra(
        f"Inserisco {col(BOLD,start)} in cima alla pila.",
    )

    while stack:
        node = stack.pop()            # prendo l'ultimo della pila

        if node not in visited:
            visited.add(node)
            result.append(node)

            mostra(
                f"Estraggo {col(BOLD+BLU, node)} dalla cima (pop). "
                f"Non era in visited → lo segno e lo aggiungo a result.",
                corrente=node
            )

            for neighbor in graph.getNeighbors(node):
                if neighbor not in visited:
                    stack.append(neighbor)
                    mostra(
                        f"Vicino {col(BOLD+ARANCIO, neighbor)} di {col(BOLD,node)}: "
                        f"non in visited → lo metto in {col(BOLD,'cima')} alla pila.",
                        corrente=node
                    )
        else:
            mostra(
                f"Estraggo {col(BOLD+VERDE, node)} dalla cima: "
                f"già in visited → {col(DIM,'ignorato')}.",
                corrente=node
            )

    print(f"\n{col(BOLD+VERDE,'  ✓ DFS completato!')}")
    stampa_grafo(visited)
    print(f"  Ordine di visita: {col(BOLD+BLU, ' → '.join(result))}")
    print(col(DIM,"  (DFS segue un percorso alla volta, non per livelli.)"))
    return result


# ── Benchmark velocità ────────────────────────────────────────────────────────
import time
import random

def _bfs_puro(graph, start):
    visited = set()
    queue   = deque()
    visited.add(start)
    queue.append(start)
    result  = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for nb in graph.getNeighbors(node):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return result

def _dfs_puro(graph, start):
    visited = set()
    stack   = []
    stack.append(start)
    result  = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)
            for nb in graph.getNeighbors(node):
                if nb not in visited:
                    stack.append(nb)
    return result

def _grafo_casuale(n_nodi, n_archi):
    """Crea un grafo connesso con n_nodi nodi e n_archi archi aggiuntivi."""
    g = Graph()
    nodi = [str(i) for i in range(n_nodi)]
    # prima un percorso per garantire connessione
    for i in range(n_nodi - 1):
        g.addEdge(nodi[i], nodi[i+1])
    # poi archi casuali extra
    for _ in range(n_archi):
        a, b = random.sample(nodi, 2)
        g.addEdge(a, b)
    return g, nodi[0]

def _misura(fn, graph, start, ripetizioni=500):
    t0 = time.perf_counter()
    for _ in range(ripetizioni):
        fn(graph, start)
    return (time.perf_counter() - t0) / ripetizioni * 1_000_000  # µs

def benchmark():
    intestazione("Benchmark velocità — BFS vs DFS")
    print(f"""
  Vengono creati grafi casuali di dimensione crescente.
  Ogni algoritmo viene eseguito {col(BOLD,"500 volte")} per grafo
  e si calcola il tempo medio in microsecondi (µs).

  {col(ARANCIO,"Nota:")} entrambi hanno complessità {col(BOLD,"O(V + E)")} — la
  differenza dipende solo dalle costanti interne (deque vs list).
""")
    taglie = [
        (10,   15),
        (100,  200),
        (500,  1000),
        (2000, 5000),
        (5000, 12000),
    ]
    W = 10  # larghezza colonne
    sep = "─" * (W*4 + 7)
    print(col(DIM, "  " + sep))
    print(f"  {col(BOLD,'Nodi'):<{W+9}} {col(BOLD,'Archi'):<{W+9}} "
          f"{col(BOLD+BLU,'BFS (µs)'):<{W+9}} {col(BOLD+VERDE,'DFS (µs)'):<{W+9}} "
          f"{col(BOLD,'Più veloce')}")
    print(col(DIM, "  " + sep))

    random.seed(42)
    for n_nodi, n_archi in taglie:
        g, start = _grafo_casuale(n_nodi, n_archi)
        t_bfs = _misura(_bfs_puro, g, start)
        t_dfs = _misura(_dfs_puro, g, start)
        if t_bfs < t_dfs:
            vincitore = col(BLU,   f"BFS  ({t_dfs/t_bfs:.1f}x)")
        elif t_dfs < t_bfs:
            vincitore = col(VERDE, f"DFS  ({t_bfs/t_dfs:.1f}x)")
        else:
            vincitore = col(DIM, "pari")
        print(f"  {str(n_nodi):<{W+9}} {str(n_archi):<{W+9}} "
              f"{col(BLU, f'{t_bfs:>6.1f}'):<{W+9}} "
              f"{col(VERDE, f'{t_dfs:>6.1f}'):<{W+9}} "
              f"{vincitore}")

    print(col(DIM, "  " + sep))
    print(f"""
  {col(DIM,"Perché visited è un set e non controlliamo result?")}
  {col(DIM,"  set → O(1)  |  lista → O(n): su grafi grandi la differenza è enorme.")}
  {col(DIM,"BFS usa deque.popleft() O(1); DFS usa list.pop() O(1) — entrambi efficienti.")}
""")


def main():
    g = costruisci_grafo()

    print(col(BOLD+BLU, "\n  ╔══════════════════════════════════════╗"))
    print(col(BOLD+BLU,   "  ║   BFS & DFS — Visualizzatore Python  ║"))
    print(col(BOLD+BLU,   "  ╚══════════════════════════════════════╝"))
    print(f"""
  Grafo usato:

        {col(GRIGIO,' A ')}
       /   \\
      {col(GRIGIO,' B ')}   {col(GRIGIO,' C ')}
     / \\ / \\
    {col(GRIGIO,' D ')}  {col(GRIGIO,' E ')}  {col(GRIGIO,' F ')}
     \\ /
    (D─E)

  Archi: A-B, A-C, B-D, B-E, C-E, C-F, D-E
  Nodo di partenza: {col(BOLD,'A')}
""")

    while True:
        print(col(BOLD, "  Cosa vuoi fare?"))
        print("   1)  BFS  passo-passo")
        print("   2)  DFS  passo-passo")
        print("   3)  Benchmark velocità BFS vs DFS")
        print("   0)  Esci")
        scelta = input(col(BLU, "\n  Scelta: ")).strip()

        if   scelta == "1": bfs(g, "A")
        elif scelta == "2": dfs(g, "A")
        elif scelta == "3": benchmark()
        elif scelta == "0":
            print(col(DIM, "\n  Arrivederci!\n")); break
        else:
            print(col(BLU, "  Scelta non valida."))

if __name__ == "__main__":
    main()