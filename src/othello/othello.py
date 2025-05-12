import numpy as np

direcciones = [(1,0), (-1,0), (0,1), (0,-1) , (1,1) , (1,-1), (-1,1) ,(-1,-1)]

def crear_tablero():
    tablero = np.zeros((8,8),dtype=int)

    tablero[3,3] = 1
    tablero[4,4] = 1
    tablero[4,3] = 2
    tablero[3,4] = 2
    return tablero

def actualizar_linea(tablero, posicion, jugador, direccion):
    seguir_buscando = True
    fila,columna = posicion
    direccion_fila, direccion_columna = direccion
    fichas_a_cambiar = []
    while(seguir_buscando):
        fila += direccion_fila
        columna += direccion_columna

        if not (0 <= fila <= 7 and 0 <= columna <= 7):
          seguir_buscando = False
          break


        if(tablero[fila,columna] == 0):
            seguir_buscando = False
        elif(tablero[fila,columna] != jugador):
            fichas_a_cambiar.append((fila, columna))
        else:
            for ficha in fichas_a_cambiar:
                f,l = ficha
                tablero[f,l]  = jugador
            seguir_buscando = False
    return tablero

def calcular_movimentos_validos(tablero, jugador):

    posiciones_validas = []

    for fila in range(8):
        for columna in range(8):
            if tablero[fila,columna] == 0:
              if(comprobar_validez_movimiento(tablero, (fila,columna), jugador)):
                  posiciones_validas.append((fila, columna))
    return posiciones_validas


def comprobar_movimiento_direccion_valido(tablero, posicion, jugador, direccion):
    seguir_buscando = True
    fila,columna = posicion
    direccion_fila, direccion_columna = direccion
    hay_ficha_en_medio = False
    while(seguir_buscando):
        fila += direccion_fila
        columna += direccion_columna


        if not (0 <= fila <= 7 and 0 <= columna <= 7):
          return False

        if(tablero[fila,columna] == 0):
            return False
        elif(tablero[fila,columna] != jugador):
            hay_ficha_en_medio = True
        else:
            return hay_ficha_en_medio
def actualizar_tablero(tablero, posicion, jugador):
      fila,columna = posicion
      tablero[fila,columna] = jugador

      for direccion in direcciones:
        tablero = actualizar_linea(tablero.copy(), posicion, jugador, direccion)


      return tablero

def comprobar_validez_movimiento(tablero, posicion, jugador):
    fila, columna = posicion
    for direccion in direcciones:
      if comprobar_movimiento_direccion_valido(tablero, (fila, columna) , jugador, direccion):
        return True
    return False

def has_finished(tablero):
   return not np.any(tablero == 0)

def get_results(tablero):
  white_points = np.count_nonzero(tablero==1)
  black_points = np.count_nonzero(tablero==2)
  return (white_points, black_points)

class Othello:

  tablero = None
  def __init__(self):
      self.tablero = crear_tablero()

  def jugar_movimiento(self, posicion,jugador):
    if not comprobar_validez_movimiento(self.tablero, posicion, jugador):
      raise ValueError("Movimiento no valido")

    self.tablero = actualizar_tablero(self.tablero, posicion, jugador)

  def get_valid_moves(self, jugador):
      return calcular_movimentos_validos(self.tablero, jugador)

  def has_finished(self):
     return has_finished(self.tablero)

  def get_results(self):
     return get_results(self.tablero)
