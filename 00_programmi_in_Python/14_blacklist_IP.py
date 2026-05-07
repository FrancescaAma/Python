import ipaddress
import random
import time
from collections import deque


# QUEUE

class Queue:
    def __init__(self):
        self.__data = deque()

    def enqueue(self, item):
        self.__data.append(item)         

    def dequeue(self):
        if self.isEmpty():
            raise IndexError("dequeue from empty queue")
        return self.__data.popleft()      

    def peek(self):
        if self.isEmpty():
            raise IndexError("empty queue")
        return self.__data[0]

    def isEmpty(self):
        return len(self.__data) == 0

    def size(self):
        return len(self.__data)

    def __repr__(self):
        return f"Queue({list(self.__data)})"

# BST

class NodoBST:
    def __init__(self, valore):
        self.valore = valore
        self.left   = None
        self.right  = None


class BST:
    def __init__(self):
        self.__radice = None

    def insert(self, valore):
        if self.__radice is None:
            self.__radice = NodoBST(valore)
        else:
            self.__insertRicorsivo(self.__radice, valore)

    def __insertRicorsivo(self, nodo, valore):
        if valore < nodo.valore:
            if nodo.left is None:
                nodo.left = NodoBST(valore)
            else:
                self.__insertRicorsivo(nodo.left, valore)
        else:
            if nodo.right is None:
                nodo.right = NodoBST(valore)
            else:
                self.__insertRicorsivo(nodo.right, valore)

    def search(self, valore):
        return self.__searchRicorsivo(self.__radice, valore)

    def __searchRicorsivo(self, nodo, valore):
        if nodo is None:
            return False
        if nodo.valore == valore:
            return True
        if valore < nodo.valore:
            return self.__searchRicorsivo(nodo.left, valore)
        else:
            return self.__searchRicorsivo(nodo.right, valore)

    def isEmpty(self):
        return self.__radice is None


#  1. Scrivi due funzioni di conversione - ipToInt(ip) e intToIp(n) - usando ipaddress.ip_address()

def ipToInt(ip: str) -> int:
    return int(ipaddress.ip_address(ip))

def intToIp(n: int) -> str:
    return str(ipaddress.ip_address(n))



#  2. Genera 1000 IP casuali per la blacklist usando una list comprehension, convertili in interi e inseriscili nel BST

IP_MIN = int(ipaddress.ip_address("10.0.0.0"))
IP_MAX = int(ipaddress.ip_address("10.255.255.255"))

blacklist_int = list({random.randint(IP_MIN, IP_MAX) for _ in range(1200)})[:1000]

bst_blacklist = BST()
for ip_int in blacklist_int:
    bst_blacklist.insert(ip_int)

print(f"Blacklist caricata: {len(blacklist_int)} IP nel BST")
print(f"IP: {intToIp(blacklist_int[0])} ---> intero: {blacklist_int[0]}")


#  3. Genera 20 pacchetti in arrivo - 10 IP presi dalla blacklist e 10 IP nuovi mai visti - mescolali casualmente e inseriscili nella Queue

ip_bloccati  = random.sample(blacklist_int, 10)

IP_MIN_N = int(ipaddress.ip_address("172.16.0.0"))
IP_MAX_N = int(ipaddress.ip_address("172.31.255.255"))
ip_permessi = list({random.randint(IP_MIN_N, IP_MAX_N) for _ in range(20)})[:10]

def crea_pacchetto(ip_src_int: int) -> dict:
    return {
        "ip_sorgente":          intToIp(ip_src_int),
        "ip_destinazione":      "192.168.100.1",
        "porta_sorgente":       random.randint(1024, 65535),
        "porta_destinazione":   random.choice([80, 443, 22, 53]),
        "protocollo":           random.choice(["TCP", "UDP"]),
        "dimensione":           random.randint(64, 1500)
    }

pacchetti = [crea_pacchetto(ip) for ip in ip_bloccati + ip_permessi]
random.shuffle(pacchetti)

coda_router = Queue()
for p in pacchetti:
    coda_router.enqueue(p)

print(f"\nPacchetti in attesa: {coda_router.size()}\n")


#  4. Processa i pacchetti dalla Queue uno per uno - per ognuno cerca l'IP nel BST e stampa BLOCCATO o PERMESSO
print(f"IP BLOCCATI O PERMESSI")
print(f"{'-'*65}")

bloccati = 0
permessi = 0
i = 1

while not coda_router.isEmpty():
    pkt    = coda_router.dequeue()
    ip_int = ipToInt(pkt["ip_sorgente"])

    if bst_blacklist.search(ip_int):
        esito     = "🔴 BLOCCATO"
        bloccati += 1
    else:
        esito    = "🟢 PERMESSO"
        permessi += 1

    print(f"  {i:<4} {pkt['ip_sorgente']:<18} {pkt['protocollo']:<6} 5{pkt['porta_destinazione']:<8} {pkt['dimensione']:<10} {esito}")
    i += 1

print(f"{'-'*65}")


#  5. Stampa il riepilogo finale - quanti pacchetti bloccati e quanti permessi

totale = bloccati + permessi
print(f"\nRIEPILOGO FINALE")
print(f"{'-'*65}")
print(f"   Pacchetti totali  : {totale}")
print(f"   🔴 Bloccati        : {bloccati}")
print(f"   🟢 Permessi        : {permessi}")
print(f"{'-'*65}")


#  6. Misura e confronta il tempo di ricerca nel BST e in una lista Python con gli stessi 1000 IP - stampa quante volte una struttura è più veloce dell'altra.

target_int   = blacklist_int[499]
lista_python = blacklist_int[:]
RIPETIZIONI  = 10_000

inizio = time.perf_counter()
for _ in range(RIPETIZIONI):
    bst_blacklist.search(target_int)
tempo_bst = (time.perf_counter() - inizio) / RIPETIZIONI

inizio = time.perf_counter()
for _ in range(RIPETIZIONI):
    target_int in lista_python
tempo_lista = (time.perf_counter() - inizio) / RIPETIZIONI

print(f"\nTEMPO DI RICERCA")
print(f"{'-'*48}")
print(f"   BST: {tempo_bst:.10f} s")
print(f"   Lista Python: {tempo_lista:.10f} s")

if tempo_bst < tempo_lista:
    print(f"   Il BST è {tempo_lista/tempo_bst:.1f}x più veloce della lista Python")
else:
    print(f"   La lista Python è {tempo_bst/tempo_lista:.1f}x più veloce del BST")

print(f"{'-'*48}")