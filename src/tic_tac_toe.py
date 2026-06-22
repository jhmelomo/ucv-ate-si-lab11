"""
Tres en raya (Tic-Tac-Toe) con agente inteligente basado en Minimax.
"""

from typing import Optional, Tuple, List


class Tablero:
    """Representa el tablero de 3x3 y sus operaciones."""

    def __init__(self):
        self.celdas = [None] * 9

    def imprimir(self) -> None:
        """Muestra el tablero en consola."""
        for i in range(0, 9, 3):
            fila = [self.celdas[i+j] if self.celdas[i+j] is not None else ' ' for j in range(3)]
            print('|'.join(fila))
            if i < 6:
                print('-' * 5)

    def movimientos_disponibles(self) -> List[int]:
        """Devuelve índices de casillas vacías."""
        return [i for i, v in enumerate(self.celdas) if v is None]

    def hay_ganador(self, jugador: str) -> bool:
        """Verifica si el 'jugador' ('X' o 'O') ha ganado."""
        combinaciones = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]         
        ]
        for combo in combinaciones:
            if all(self.celdas[i] == jugador for i in combo):
                return True
        return False

    def tablero_lleno(self) -> bool:
        """Devuelve True si no quedan movimientos."""
        return None not in self.celdas

    def estado_final(self) -> Optional[str]:
        """
        Retorna:
          - 'X' si gana X
          - 'O' si gana O
          - 'empate' si empate
          - None si el juego continúa
        """
        if self.hay_ganador('X'):
            return 'X'
        if self.hay_ganador('O'):
            return 'O'
        if self.tablero_lleno():
            return 'empate'
        return None

    def hacer_movimiento(self, indice: int, jugador: str) -> bool:
        """Coloca la ficha en la casilla si está vacía. Retorna True si éxito."""
        if self.celdas[indice] is None:
            self.celdas[indice] = jugador
            return True
        return False

    def deshacer_movimiento(self, indice: int) -> None:
        """Deshace un movimiento (para la búsqueda)."""
        self.celdas[indice] = None

    def copiar(self) -> 'Tablero':
        """Crea una copia superficial (para la búsqueda recursiva)."""
        nuevo = Tablero()
        nuevo.celdas = self.celdas[:]
        return nuevo


class Agente:
    """Agente que elige el mejor movimiento usando Minimax."""

    def __init__(self, jugador: str, oponente: str):
        self.jugador = jugador
        self.oponente = oponente

    def mejor_movimiento(self, tablero: Tablero) -> Optional[int]:
        """
        Retorna el índice del mejor movimiento para el jugador actual,
        o None si no hay movimientos.
        """
        disponibles = tablero.movimientos_disponibles()
        if not disponibles:
            return None

        mejor_valor = float('-inf')
        mejor_idx = disponibles[0]

        for idx in disponibles:
            tablero.hacer_movimiento(idx, self.jugador)
            valor = self._minimax(tablero, 0, False)
            tablero.deshacer_movimiento(idx)

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_idx = idx

        return mejor_idx

    def _minimax(self, tablero: Tablero, profundidad: int, es_max: bool) -> int:
        """
        Algoritmo Minimax recursivo.
        Retorna el valor del tablero desde la perspectiva del jugador actual.
        """
        estado = tablero.estado_final()

        # Casos base
        if estado == self.jugador:
            return 10 - profundidad 
        if estado == self.oponente:
            return profundidad - 10
        if estado == 'empate':
            return 0

        if es_max:
            mejor = float('-inf')
            for idx in tablero.movimientos_disponibles():
                tablero.hacer_movimiento(idx, self.jugador)
                valor = self._minimax(tablero, profundidad + 1, False)
                tablero.deshacer_movimiento(idx)
                mejor = max(mejor, valor)
            return mejor
        else:
            peor = float('inf')
            for idx in tablero.movimientos_disponibles():
                tablero.hacer_movimiento(idx, self.oponente)
                valor = self._minimax(tablero, profundidad + 1, True)
                tablero.deshacer_movimiento(idx)
                peor = min(peor, valor)
            return peor


class Juego:
    """Controla la partida entre un humano y el agente."""

    def __init__(self):
        self.tablero = Tablero()
        self.humano = 'X'
        self.agente = Agente(jugador='O', oponente='X')

    def jugar(self) -> None:
        """Bucle principal del juego."""
        turno = 'X'

        while True:
            self.tablero.imprimir()
            estado = self.tablero.estado_final()
            if estado:
                self._mostrar_resultado(estado)
                break

            if turno == self.humano:
                print("Tu turno (X). Elige una casilla (0-8):")
                try:
                    idx = int(input())
                    if idx not in self.tablero.movimientos_disponibles():
                        print("Casilla ocupada o inválida. Intenta de nuevo.")
                        continue
                    self.tablero.hacer_movimiento(idx, self.humano)
                    turno = self.agente.jugador
                except ValueError:
                    print("Ingresa un número válido.")
            else:
                print("Turno del agente (O)...")
                idx = self.agente.mejor_movimiento(self.tablero)
                if idx is not None:
                    self.tablero.hacer_movimiento(idx, self.agente.jugador)
                    turno = self.humano
                else:
                    break

    def _mostrar_resultado(self, estado: str) -> None:
        self.tablero.imprimir()
        if estado == self.humano:
            print("¡Felicidades! Has ganado.")
        elif estado == self.agente.jugador:
            print("El agente ha ganado. ¡Mejor suerte la próxima!")
        else:
            print("Empate.")

if __name__ == "__main__":
    juego = Juego()
    juego.jugar()