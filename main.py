#####################################################
#               Calculadora en python               #
#       Podrá alternar entre el modo estándar       #
#    y modo científico, así como modo programador   #
#       y modo gráfica, de calculo de fecha y       #
#       convertidor de todo tipo, el de monedas     #
#         se actualizara con el mercado real        #
#                                                   #
#   Si, es una copia de la calculadora de windows   #
#####################################################
# *El historial se guarda en un archivo a parte (en %temp%) para poder conservarlo si cambio de modo
try:
    import sys

    import qdarktheme
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    from PyQt6.QtWidgets import *
except ImportError as err:
    raise ImportError(f"Cannot import {err.name}")


class Calculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora")
        self.mode = "Estandar"
        self.initMenu()
        self.show()
        self.checkMode()

    def initMenu(self):
        menubar = self.menuBar()
        menubar.
        
    def checkMode(self):
        match self.mode:
            case "Estandar":
                self.modoEstandar()
            case "Cientifico":
                self.modoCientifico()
            case "Grafica":
                self.modoGrafica()
            case "Programador":
                self.modoProgramador()
            case "CalcularFecha":
                self.modoCalcularFecha()
            case "ConvertirDinero":
                self.modoConvertirDinero()

    def modoEstandar(self):
        pass

    def modoCientifico(self):
        pass

    def modoGrafica(self):
        pass

    def modoProgramador(self):
        pass

    def modoCalcularFecha(self):
        pass

    def modoConvertirDinero(self):
        pass

    class ModoConvertirVolumen(QWidget):
        pass

    class ModoConvertirLongitud(QWidget):
        pass

    class ModoConvertirMasa(QWidget):
        pass

    class ModoConvertirTemperatura(QWidget):
        pass

    class ModoConvertirEnergia(QWidget):
        pass

    class ModoConvertirArea(QWidget):
        pass

    class ModoConvertirVelocidad(QWidget):
        pass

    class ModoConvertirTiempo(QWidget):
        pass

    class ModoConvertirPotencia(QWidget):
        pass

    class ModoConvertirDatos(QWidget):
        pass

    class ModoConvertirPresion(QWidget):
        pass

    class ModoConverirAngulo(QWidget):
        pass

    class AcercaDe(QWindow):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculadora()
    app.setStyleSheet(qdarktheme.load_stylesheet())
    sys.exit(app.exec())
