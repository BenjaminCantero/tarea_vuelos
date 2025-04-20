class Nodo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.anterior = None
        self.siguiente = None

class ListaDoble:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def insertar_al_frente(self, vuelo):
        nuevo = Nodo(vuelo)
        if not self.primero:
            self.primero = self.ultimo = nuevo
        else:
            nuevo.siguiente = self.primero
            self.primero.anterior = nuevo
            self.primero = nuevo

    def insertar_al_final(self, vuelo):
        nuevo = Nodo(vuelo)
        if not self.ultimo:
            self.primero = self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo

    def obtener_primero(self):
        return self.primero.vuelo if self.primero else None

    def obtener_ultimo(self):
        return self.ultimo.vuelo if self.ultimo else None

    def longitud(self):
        actual = self.primero
        contador = 0
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion <= 0 or not self.primero:
            self.insertar_al_frente(vuelo)
            return
        if posicion >= self.longitud():
            self.insertar_al_final(vuelo)
            return

        nuevo = Nodo(vuelo)
        actual = self.primero
        for _ in range(posicion - 1):
            actual = actual.siguiente

        siguiente = actual.siguiente
        nuevo.siguiente = siguiente
        nuevo.anterior = actual
        actual.siguiente = nuevo
        if siguiente:
            siguiente.anterior = nuevo

    def extraer_de_posicion(self, posicion):
        if not self.primero:
            return None

        actual = self.primero
        if posicion == 0:
            vuelo = self.primero.vuelo
            self.primero = self.primero.siguiente
            if self.primero:
                self.primero.anterior = None
            else:
                self.ultimo = None
            return vuelo

        for _ in range(posicion):
            if not actual.siguiente:
                return None
            actual = actual.siguiente

        vuelo = actual.vuelo
        if actual.anterior:
            actual.anterior.siguiente = actual.siguiente
        if actual.siguiente:
            actual.siguiente.anterior = actual.anterior
        if actual == self.ultimo:
            self.ultimo = actual.anterior
        return vuelo
