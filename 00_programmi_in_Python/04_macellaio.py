from collections import deque


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


fila = Queue()


for cliente in ["Mario", "Giulia", "Tonino", "Rosa"]:
    fila.enqueue(cliente)
    print(f"{cliente} si mette in fila")
print()

primo = fila.dequeue()
print(f"Servizio: {primo}")
print()

fila.enqueue("Enzo")
print("Enzo si mette in fila")
print()

print(f"Persone ancora in fila: {fila.size()}")
print(f"Fila attuale: {fila}")
print()

while not fila.isEmpty():
    print(f"Servo: {fila.dequeue()}")

print("\nIl macellaio ha chiuso.")