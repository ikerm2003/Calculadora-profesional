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
    """Calculadora grafica basada en una ventana principal (QMainWindow)

    """

    def __init__(self):
        """Funcion de inicio
        """
        super().__init__()
        self.setWindowTitle("Calculadora")
        self.mode = "Estandar"
        self.ButtonCreator()
        self.initLateralBar()
        self.checkMode()

    def ButtonCreator(self):
        """Crea los botones de la calculadora y los conecta con su funcion correspondiente
        """
        self.LCDNumber = QLCDNumber()
        self.LCDNumber.setMinimumSize(300, 80)

        self.MCButton = QPushButton("MC")
        self.MCButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.MCButton.clicked.connect(self.MC)

        self.MRButton = QPushButton("MR")
        self.MRButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.MRButton.clicked.connect(self.MR)

        self.MPlusButton = QPushButton("M+")
        self.MPlusButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.MPlusButton.clicked.connect(self.MPlus)

        self.MMenosButton = QPushButton("M-")
        self.MMenosButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.MMenosButton.clicked.connect(self.MMenos)

        self.MSButton = QPushButton("MS")
        self.MSButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.MSButton.clicked.connect(self.MS)

        self.porcientoButton = QPushButton("%")
        self.porcientoButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.porcientoButton.clicked.connect(self.porciento)

        self.CEButton = QPushButton("CE")
        self.CEButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.CEButton.clicked.connect(self.CE)

        self.CButton = QPushButton("C")
        self.CButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.CButton.clicked.connect(self.C)

        self.deleteButton = QPushButton('\u232b')
        self.deleteButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.deleteButton.setShortcut(Qt.Key.Key_Backslash)
        self.deleteButton.clicked.connect(self.delete)

        self.fracc1overxButton = QPushButton("\u215Fx")
        self.fracc1overxButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.fracc1overxButton.clicked.connect(self.fracc1overx)

        self.cuadradoButton = QPushButton("x²")
        self.cuadradoButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.cuadradoButton.clicked.connect(self.cuadrado)

        self.sqrtButton = QPushButton("\u221Ax")
        self.sqrtButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum.Maximum))
        self.sqrtButton.clicked.connect(self.sqrt)

        self.divButton = QPushButton("\u00F7")
        self.divButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum.Maximum))
        self.divButton.clicked.connect(self.div)
        self.divButton.setShortcut(Qt.Key.Key_Bar)

        self.sevenButton = QPushButton("7")
        self.sevenButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.sevenButton.clicked.connect(lambda: self.insertNumberSTD(7))
        self.sevenButton.setShortcut(Qt.Key.Key_7)

        self.eightButton = QPushButton("8")
        self.eightButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.sevenButton.clicked.connect(lambda: self.insertNumberSTD(8))
        self.eightButton.setShortcut(Qt.Key.Key_8)

        self.nineButton = QPushButton("9")
        self.nineButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.nineButton.clicked.connect(lambda: self.insertNumberSTD(9))
        self.nineButton.setShortcut(Qt.Key.Key_9)

        self.multButton = QPushButton("x")
        self.multButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.multButton.clicked.connect(self.mult)
        self.multButton.setShortcut(Qt.Key.Key_multiply)

        self.fourButton = QPushButton("4")
        self.fourButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.fourButton.clicked.connect(lambda: self.insertNumberSTD(4))
        self.fourButton.setShortcut(Qt.Key.Key_4)

        self.fiveButton = QPushButton("5")
        self.fiveButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.fiveButton.clicked.connect(lambda: self.insertNumberSTD(5))
        self.fiveButton.setShortcut(Qt.Key.Key_5)

        self.sixButton = QPushButton("6")
        self.sixButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.sixButton.clicked.connect(lambda:self.insertNumberSTD(6))
        self.sixButton.setShortcut(Qt.Key.Key_6)

        self.minusButton = QPushButton("-")
        self.minusButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.minusButton.clicked.connect(self.minus)
        self.minusButton.setShortcut(Qt.Key.Key_Minus)

        self.oneButton = QPushButton("1")
        self.oneButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.oneButton.clicked.connect(lambda:self.insertNumberSTD(1))
        self.oneButton.setShortcut(Qt.Key.Key_1)

        self.twoButton = QPushButton("2")
        self.twoButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.twoButton.clicked.connect(lambda:self.insertNumberSTD(2))
        self.twoButton.setShortcut(Qt.Key.Key_2)

        self.threeButton = QPushButton("3")
        self.threeButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.threeButton.clicked.connect(lambda:self.insertNumberSTD(3))
        self.threeButton.setShortcut(Qt.Key.Key_3)

        self.plusButton = QPushButton("+")
        self.plusButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.plusButton.clicked.connect(self.plus)
        self.plusButton.setShortcut(Qt.Key.Key_Plus)

        self.masmenosButton = QPushButton("\u00B1")
        self.masmenosButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.masmenosButton.clicked.connect(self.plusminus)
        self.masmenosButton.setShortcut(Qt.Key.Key_plusminus)

        self.ceroButton = QPushButton("0")
        self.ceroButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.ceroButton.clicked.connect(lambda:self.insertNumberSTD(0))
        self.ceroButton.setShortcut(Qt.Key.Key_0)

        self.comaButton = QPushButton(",")
        self.comaButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.comaButton.clicked.connect(self.comma)
        self.comaButton.setShortcut(Qt.Key.Key_Period)

        self.equalButton = QPushButton("=")
        self.equalButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.equalButton.clicked.connect(self.equal)
        self.equalButton.setShortcut(Qt.Key.Key_Enter)  
        

    def MC(self):
        pass

    def MR(self):
        pass

    def MPlus(self):
        pass

    def MMenos(self):
        pass

    def porciento(self):
        pass

    def MS(self):
        pass

    def CE(self):
        pass

    def C(self):
        pass

    def delete(self):
        pass

    def fracc1overx(self):
        pass

    def cuadrado(self):
        pass

    def sqrt(self):
        pass

    def div(self):
        pass

    

    def mult(self):
        pass

    

    def minus(self):
        pass
    
    def insertNumberSTD(self, number:int):
        self.addToLCD(number)
    
    def cero(self):
        self.addToLCD(number=0)
    
    def one(self):
        self.addToLCD(number=1)

    def two(self):
        self.addToLCD(number=2)

    def three(self):
        self.addToLCD(number=3)
        
    def four(self):
        self.addToLCD(number=4)

    def five(self):
        self.addToLCD(number=5)

    def six(self):
        self.addToLCD(number=6)
        
    def seven(self):
        self.addToLCD(number=7) 
        
    def eight(self):
        self.addToLCD(number=8)

    def nine(self):
        self.addToLCD(number=9)

    def plus(self):
        pass

    def plusminus(self):
        pass


    def comma(self):
        pass

    def equal(self):
        pass
        
    def addToLCD(self, number:int):
        originalNumber = self.LCDNumber.value()
        if originalNumber == 0:
            originalNumber = int()
        finalNumber = str(int(originalNumber)) + str('{}'.format(str(number)[1:] if str(number).startswith('0') else str(number)))
        if finalNumber == int(float(finalNumber)):
            self.LCDNumber.display(str(int(finalNumber)))
        else:
            self.LCDNumber.display(str('{}'.format(finalNumber[1:] if finalNumber.startswith('0') else finalNumber)))

    def initLateralBar(self):
        pass

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
            case "ConvertirVolumen":
                self.modoConvertirVolumen()
            case "ConvertirLongitud":
                self.modoConvertirLongitud()
            case "ConvertirVolumen":
                self.modoConvertirMasa()

    def modoEstandar(self):
        centralWidget = QWidget()
        MButtonsWidget = QWidget()
        layout = QGridLayout()
        MButtonsLayout = QGridLayout()
        generalButtons = QWidget()
        generalButtonsLayout = QGridLayout()

        MButtonsLayout.addWidget(self.LCDNumber, 0, 0, 1, 5)
        MButtonsLayout.addWidget(self.MCButton, 1, 0)
        MButtonsLayout.addWidget(self.MRButton, 1, 1)
        MButtonsLayout.addWidget(self.MPlusButton, 1, 2)
        MButtonsLayout.addWidget(self.MMenosButton, 1, 3)
        MButtonsLayout.addWidget(self.MSButton, 1, 4)
        generalButtonsLayout.addWidget(self.porcientoButton, 2, 0)
        generalButtonsLayout.addWidget(self.CEButton, 2, 1)
        generalButtonsLayout.addWidget(self.CButton, 2, 2)
        generalButtonsLayout.addWidget(self.deleteButton, 2, 3)
        generalButtonsLayout.addWidget(self.fracc1overxButton, 3, 0)
        generalButtonsLayout.addWidget(self.cuadradoButton, 3, 1)
        generalButtonsLayout.addWidget(self.sqrtButton, 3, 2)
        generalButtonsLayout.addWidget(self.divButton, 3, 3)
        generalButtonsLayout.addWidget(self.sevenButton, 4, 0)
        generalButtonsLayout.addWidget(self.eightButton, 4, 1)
        generalButtonsLayout.addWidget(self.nineButton, 4, 2)
        generalButtonsLayout.addWidget(self.multButton, 4, 3)
        generalButtonsLayout.addWidget(self.fourButton, 5, 0)
        generalButtonsLayout.addWidget(self.fiveButton, 5, 1)
        generalButtonsLayout.addWidget(self.sixButton, 5, 2)
        generalButtonsLayout.addWidget(self.minusButton, 5, 3)
        generalButtonsLayout.addWidget(self.oneButton, 6, 0)
        generalButtonsLayout.addWidget(self.twoButton, 6, 1)
        generalButtonsLayout.addWidget(self.threeButton, 6, 2)
        generalButtonsLayout.addWidget(self.plusButton, 6, 3)
        generalButtonsLayout.addWidget(self.masmenosButton, 7, 0)
        generalButtonsLayout.addWidget(self.ceroButton, 7, 1)
        generalButtonsLayout.addWidget(self.comaButton, 7, 2)
        generalButtonsLayout.addWidget(self.equalButton, 7, 3)
        generalButtons.setLayout(generalButtonsLayout)
        MButtonsWidget.setLayout(MButtonsLayout)
        layout.addWidget(MButtonsWidget)
        layout.addWidget(generalButtons)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

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

    def modoConvertirVolumen(self):
        pass

    def modoConvertirLongitud(self):
        pass

    def modoConvertirMasa(self):
        pass

    def modoConvertirTemperatura(self):
        pass

    def modoConvertirEnergia(self):
        pass

    def modoConvertirArea(self):
        pass

    def modoConvertirVelocidad(self):
        pass

    def modoConvertirTiempo(self):
        pass

    def modoConvertirPotencia(self):
        pass

    def modoConvertirDatos(self):
        pass

    def modoConvertirPresion(self):
        pass

    def modoConvertirAngulo(self):
        pass

    class AcercaDe(QWindow):
        pass

    def loadHistoriy(self):
        pass

    def showHistory(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculadora()
    app.setStyleSheet(qdarktheme.load_stylesheet())
    ex.show()

    sys.exit(app.exec())
