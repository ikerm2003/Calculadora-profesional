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

from functools import partial
import os
import sys
from configparser import ConfigParser
from rembg import remove
import qdarktheme
from PyQt6.QtCore import (
    Qt,
    QSize,
    QMetaObject,
    QCoreApplication,
    QBuffer,
    QPropertyAnimation,
    QEasingCurve,
    QByteArray,
    QRect,
)
from PyQt6.QtGui import (
    QWindow,
    QAction,
    QScreen,
    QIcon,
    QPixmap,
    QFont,
    QImage,
    qRgb,
    qRgba,
    qGreen,
    qBlue,
    qRed,
    qAlpha,
    QColor,
    QMouseEvent,
)
from PyQt6.QtWidgets import (
    QMainWindow,
    QLCDNumber,
    QPushButton,
    QSizePolicy,
    QWidget,
    QGridLayout,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpacerItem,
    QLineEdit,
    QStackedWidget,
    QFrame,
    QSizeGrip,
    QRadioButton,
    QButtonGroup,
    QStackedLayout,
)
from enum import Enum
from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """Style sheet"""

    MAIN_WINDOW = "main_window"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        if theme == Theme.LIGHT:
            return qdarktheme.load_stylesheet("light")
        if theme == Theme.DARK:
            return qdarktheme.load_stylesheet("dark")


class Calculadora(QMainWindow):
    """Calculadora grafica basada en una ventana principal (QMainWindow)"""

    def __init__(self):
        """Funcion de inicio"""
        super().__init__()
        self.setWindowTitle("Calculadora")
        self.setStyleSheet(qdarktheme.load_stylesheet("dark"))
        # StyleSheet.MAIN_WINDOW.apply(self, Theme.DARK)
        self.cfg = self.config_read()
        self.themes = self.cfg.get("Theme", "posible-themes")
        self.currentTheme = self.cfg.get("Theme", "actual-theme")
        self.mode = self.cfg.get(
            "Mode", "actual-mode"
        )  # TODO: Si cambia el modo, cambia esta variable en el archivo cfg
        self.screenRect = QScreen.availableGeometry(self.screen()) # type:ignore
        self.screenWidth, self.screenHeight = (
            self.screenRect.width(),
            self.screenRect.height(),
        )
        self.screenSize = QSize(self.screenWidth, self.screenHeight)

        self.setMinimumSize(
            QSize(int(self.screenWidth / 3), int(self.screenHeight / 3))
        )

        self.actualStyleSheet = self.styleSheet() + "\n"
        self.setStyleSheet(
            self.actualStyleSheet
            + """QRadioButton::indicator{
                width: 32px; 
                height: 32px;
                }
                QRadioButton::indicator:unchecked{
                    image: url(:/Assets/icons/estandar.png);
                }
                QRadioButton::indicator:checked{
                    image: url(:/Assets/icons/estandar.png);
                } 
                QRadioButton::checked:hover{
                    background-color: #737B7A;
                }
                QRadioButton::unchecked:hover{
                    background-color: #737B7A;
                }
                QRadioButton::checked:on{
                    border-bottom: 3px solid #4AF95A;
                }
                QFrame{
                    margin: 0px;
                    spacing: 0px;
                }
                """
        )
        self.setWindowIcon(QIcon(QPixmap.fromImage(QImage(os.path.join("Assets", "icons", "calc_icon.png")))))
        # TODO: Hacer barra superior invisible y handle bottones
        self.ButtonCreator()
        self.initUI()

    def config_read(
        self, cfg_file=os.path.join("Assets", "config.cfg")
    ) -> ConfigParser:
        parser = ConfigParser(allow_no_value=True)
        parser.read(cfg_file)
        return parser

    def ButtonCreator(self):
        """Crea los botones de la calculadora y los conecta con su funcion correspondiente"""
        self.LCDNumber = QLCDNumber()
        self.LCDNumber.setMinimumSize(300, 80)
        self.LCDNumber.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.LCDNumber.setDigitCount(20)

        self.MCButton = QPushButton("MC")
        self.MCButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.MCButton.clicked.connect(self.MC)

        self.MRButton = QPushButton("MR")
        self.MRButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.MRButton.clicked.connect(self.MR)

        self.MPlusButton = QPushButton("M+")
        self.MPlusButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.MPlusButton.clicked.connect(self.MPlus)

        self.MMenosButton = QPushButton("M-")
        self.MMenosButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.MMenosButton.clicked.connect(self.MMenos)

        self.MSButton = QPushButton("MS")
        self.MSButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.MSButton.clicked.connect(self.MS)

        self.porcientoButton = QPushButton("%")
        self.porcientoButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.porcientoButton.clicked.connect(self.porciento)

        self.CEButton = QPushButton("CE")
        self.CEButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.CEButton.clicked.connect(self.CE)

        self.CButton = QPushButton("C")
        self.CButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.CButton.clicked.connect(self.C)

        self.deleteButton = QPushButton("\u232b")
        self.deleteButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.deleteButton.setShortcut(Qt.Key.Key_Backslash)
        self.deleteButton.clicked.connect(self.delete)

        self.fracc1overxButton = QPushButton("\u215Fx")
        self.fracc1overxButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.fracc1overxButton.clicked.connect(self.fracc1overx)

        self.cuadradoButton = QPushButton("x²")
        self.cuadradoButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.cuadradoButton.clicked.connect(self.cuadrado)

        self.sqrtButton = QPushButton("\u221Ax")
        self.sqrtButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.sqrtButton.clicked.connect(self.sqrt)

        self.divButton = QPushButton("\u00F7")
        self.divButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.divButton.clicked.connect(self.div)
        self.divButton.setShortcut(Qt.Key.Key_Bar)

        self.sevenButton = QPushButton("7")
        self.sevenButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.sevenButton.clicked.connect(lambda: self.addToLCD_STD(7))
        self.sevenButton.setShortcut(Qt.Key.Key_7)

        self.eightButton = QPushButton("8")
        self.eightButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.sevenButton.clicked.connect(lambda: self.addToLCD_STD(8))
        self.eightButton.setShortcut(Qt.Key.Key_8)

        self.nineButton = QPushButton("9")
        self.nineButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.nineButton.clicked.connect(lambda: self.addToLCD_STD(9))
        self.nineButton.setShortcut(Qt.Key.Key_9)

        self.multButton = QPushButton("x")
        self.multButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.multButton.clicked.connect(self.mult)
        self.multButton.setShortcut(Qt.Key.Key_multiply)

        self.fourButton = QPushButton("4")
        self.fourButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.fourButton.clicked.connect(lambda: self.addToLCD_STD(4))
        self.fourButton.setShortcut(Qt.Key.Key_4)

        self.fiveButton = QPushButton("5")
        self.fiveButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.fiveButton.clicked.connect(lambda: self.addToLCD_STD(5))
        self.fiveButton.setShortcut(Qt.Key.Key_5)

        self.sixButton = QPushButton("6")
        self.sixButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.sixButton.clicked.connect(lambda: self.addToLCD_STD(6))
        self.sixButton.setShortcut(Qt.Key.Key_6)

        self.minusButton = QPushButton("-")
        self.minusButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.minusButton.clicked.connect(self.minus)
        self.minusButton.setShortcut(Qt.Key.Key_Minus)

        self.oneButton = QPushButton("1")
        self.oneButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.oneButton.clicked.connect(lambda: self.addToLCD_STD(1))
        self.oneButton.setShortcut(Qt.Key.Key_1)

        self.twoButton = QPushButton("2")
        self.twoButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.twoButton.clicked.connect(lambda: self.addToLCD_STD(2))
        self.twoButton.setShortcut(Qt.Key.Key_2)

        self.threeButton = QPushButton("3")
        self.threeButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.threeButton.clicked.connect(lambda: self.addToLCD_STD(3))
        self.threeButton.setShortcut(Qt.Key.Key_3)

        self.plusButton = QPushButton("+")
        self.plusButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.plusButton.clicked.connect(self.plus)
        self.plusButton.setShortcut(Qt.Key.Key_Plus)

        self.masmenosButton = QPushButton("\u00B1")
        self.masmenosButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.masmenosButton.clicked.connect(self.plusminus)
        self.masmenosButton.setShortcut(Qt.Key.Key_plusminus)

        self.ceroButton = QPushButton("0")
        self.ceroButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.ceroButton.clicked.connect(lambda: self.addToLCD_STD(0))
        self.ceroButton.setShortcut(Qt.Key.Key_0)

        self.comaButton = QPushButton(",")
        self.comaButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.comaButton.clicked.connect(self.comma)
        self.comaButton.setShortcut(Qt.Key.Key_Period)

        self.equalButton = QPushButton("=")
        self.equalButton.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
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

    def plus(self):
        pass

    def plusminus(self):
        pass

    def comma(self):
        pass

    def equal(self):
        pass

    def addToLCD_STD(self, number: int):
        originalNumber = self.LCDNumber.value()
        if self.LCDNumber.checkOverflow(20):
            return None
        if originalNumber == 0:
            originalNumber = int()
        finalNumber = str(int(originalNumber)) + str(number
            # "{}".format(str(number)[1:] if str(number).startswith("0") else str(number))
        )
        if finalNumber == int(float(finalNumber)):
            self.LCDNumber.display(str(int(finalNumber)))
        else:
            self.LCDNumber.display(
                str(
                    "{}".format(
                        finalNumber[1:] if finalNumber.startswith("0") else finalNumber
                    )
                )
            )

    def constructImg(self, img_path: str, size: QSize):
        image = QImage(os.path.join("Assets", img_path))
        image = image.scaled(size, Qt.AspectRatioMode.KeepAspectRatio)
        image = image.convertToFormat(QImage.Format.Format_Mono)
        image.setColor(0, qRgba(0, 0, 0, 0))
        if self.currentTheme == "DARK":
            image.setColor(1, qRgb(255, 255, 255))
        return image

    def toggleButton(self):
        width = self.frame_lateralbar.width()
        # If minimized
        if width == 0:
            # Expand menu
            newWidth = 200
            self.openClose_sidebar_btn.setIcon(
                QIcon(os.path.join("Assets", "icons", "chevrons-left.svg"))
            )
        # If maximized
        else:
            # Restore menu
            newWidth = 0
            self.openClose_sidebar_btn.setIcon(
                QIcon(os.path.join("Assets", "icons", "align-left.svg"))
            )
        self.animation = QPropertyAnimation(
            self.frame_lateralbar, b"minimumWidth"  # type:ignore
        )  # Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)  # Start value is the current menu width
        self.animation.setEndValue(newWidth)  # end value is the new menu width
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.start()

    def initUI(self):
        self.frame_inferior = QFrame()  # frame sobre el que se coloca todo
        self.frame_inferior.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        self.frame_inferior_layout = QVBoxLayout()
        self.frame_inferior_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_inferior_layout.setSpacing(0)
        self.frame_inferior.setLayout(self.frame_inferior_layout)

        self.frame_superior = (
            QFrame()
        )  # frame para el boton de menu y botonoes superiores
        self.frame_superior.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_superior.setMaximumHeight(32)
        self.frame_superior_layout = QHBoxLayout()
        self.frame_superior_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_superior_layout.setSpacing(0)
        self.frame_superior.setLayout(self.frame_superior_layout)
        self.openClose_sidebar_btn = QPushButton("")
        self.openClose_sidebar_btn.setMaximumHeight(32)
        self.openClose_sidebar_btn.setIcon(
            QIcon(os.path.join("Assets", "icons", "chevrons-left.svg"))
        )
        self.openClose_sidebar_btn.clicked.connect(self.toggleButton)
        self.frame_superior_layout.addWidget(self.openClose_sidebar_btn)
        self.frame_superior_layout.addStretch()
        # self.frame_superior_layout.addWidget(QPushButton("Max"))
        # self.frame_superior_layout.addWidget(QPushButton("Close"))

        self.frame_contenedor = QFrame()  # frame contenedor de abajo
        self.frame_contenedor.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_contenedor_layout = QHBoxLayout()
        self.frame_contenedor.setLayout(self.frame_contenedor_layout)
        self.frame_contenedor_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_contenedor_layout.setSpacing(0)
        
        self.stackedWidget = QStackedWidget()  # lado central (donde va la calculadora)
        # self.frame_central.setFrameShape(QFrame.Shape.StyledPanel)
        self.stackedWidget.addWidget(self.modoEstandar())
        self.stackedWidget.addWidget(self.modoCientifico())
        self.stackedWidget.addWidget(self.modoGrafica())
        self.stackedWidget.addWidget(self.modoProgramador())
        self.stackedWidget.addWidget(self.modoCalcularFecha())
        self.stackedWidget.addWidget(self.modoConvertirDinero())
        self.stackedWidget.addWidget(self.modoConvertirVolumen())
        self.stackedWidget.addWidget(self.modoConvertirLongitud())
        self.stackedWidget.addWidget(self.modoConvertirMasa())
        self.stackedWidget.addWidget(self.modoConvertirTemperatura())
        self.stackedWidget.addWidget(self.modoConvertirEnergia())
        self.stackedWidget.addWidget(self.modoConvertirArea())
        self.stackedWidget.addWidget(self.modoConvertirVelocidad())
        self.stackedWidget.addWidget(self.modoConvertirTiempo())
        self.stackedWidget.addWidget(self.modoConvertirPotencia())
        self.stackedWidget.addWidget(self.modoConvertirDatos())
        self.stackedWidget.addWidget(self.modoConvertirPresion())
        self.stackedWidget.addWidget(self.modoConvertirAngulo())
        # self.frame_central.layout().setContentsMargins(0, 0, 0, 0)
        # self.frame_central.layout().setSpacing(0)
        self.stackedWidget.setCurrentIndex(0)
        self.initLateralBar()

        
        self.frame_lateralbar_layout.addWidget(self.frame_lateralbar_buttons)
        self.frame_lateralbar_layout.addWidget(self.frame_lateralbar_configButton)
        self.frame_contenedor_layout.addWidget(self.frame_lateralbar)
        self.frame_contenedor_layout.addWidget(self.stackedWidget)
        self.frame_inferior_layout.addWidget(self.frame_superior)
        self.frame_inferior_layout.addWidget(self.frame_contenedor)

        self.setCentralWidget(self.frame_inferior)
        
        self.checkMode(self.mode)

    def initLateralBar(self):
        self.frame_lateralbar_buttons = QFrame()  # Frame de los botones
        self.frame_lateralbar_buttons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_lateralbar_buttons_layout = QVBoxLayout()
        self.frame_lateralbar_buttons.setLayout(self.frame_lateralbar_buttons_layout)
        self.frame_lateralbar_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_lateralbar_buttons_layout.setSpacing(0)

        self.frame_lateralbar_configButton = QFrame()  # Frame del config button
        self.frame_lateralbar_configButton.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_lateralbar_configButton.setMaximumHeight(50)
        self.frame_lateralbar_configButton_layout = QVBoxLayout()
        self.frame_lateralbar_configButton.setLayout(
            self.frame_lateralbar_configButton_layout
        )
        self.frame_lateralbar_configButton_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_lateralbar_configButton_layout.setSpacing(0)

        self.frame_lateralbar = QFrame()  # Barra lateral
        self.frame_lateralbar.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_lateralbar.setMaximumWidth(0)
        self.frame_lateralbar.setMinimumWidth(200)
        self.frame_lateralbar_layout = QVBoxLayout()
        self.frame_lateralbar.setLayout(self.frame_lateralbar_layout)
        self.frame_lateralbar_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_lateralbar_layout.setSpacing(0)

        self.buttonGroup = QButtonGroup()

        self.calculadoraLabel = QLabel("Calculadora")  # Calculadora
        self.calculadoraLabel.setStyleSheet("font-weight: 900")
        self.calculadoraLabel.setMaximumHeight(32)
        self.standardButton = QRadioButton("Estandar")
        self.standardButton.setMaximumHeight(32)
        self.standardButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "estandar.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.standardButton.toggled.connect(partial(self.stackedWidget.setCurrentIndex, 0))
        self.buttonGroup.addButton(self.standardButton, 1)
        self.cientificaButton = QRadioButton("Cientifica")
        self.cientificaButton.setMaximumHeight(32)
        self.cientificaButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "cientifica.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.cientificaButton.toggled.connect(partial(self.stackedWidget.setCurrentIndex, 1))
        self.buttonGroup.addButton(self.cientificaButton, 1)
        self.graficaButton = QRadioButton("Grafica")
        self.graficaButton.setMaximumHeight(32)
        self.graficaButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "grafica.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.graficaButton.toggled.connect(partial(self.checkMode, "Grafica"))
        self.buttonGroup.addButton(self.graficaButton, 1)
        self.programadorButton = QRadioButton("Programador")
        self.programadorButton.setMaximumHeight(32)
        self.programadorButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "programador.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.programadorButton.toggled.connect(partial(self.stackedWidget.setCurrentIndex, 2))
        self.buttonGroup.addButton(self.programadorButton, 1)
        self.calcFechaButton = QRadioButton("Calculo de fecha")
        self.calcFechaButton.setMaximumHeight(32)
        self.calcFechaButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(os.path.join("icons", "fecha.png"), QSize(32, 32))
                )
            )
        )
        self.calcFechaButton.toggled.connect(partial(self.checkMode, "CalcularFecha"))
        self.buttonGroup.addButton(self.calcFechaButton, 1)

        self.convertidorLabel = QLabel("Convertidor")  # Convertidor
        self.convertidorLabel.setStyleSheet("font-weight: 900")
        self.convertidorLabel.setMaximumHeight(32)
        self.monedaButton = QRadioButton("Moneda")
        self.monedaButton.setMaximumHeight(32)
        self.monedaButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "moneda.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.monedaButton.toggled.connect(partial(self.checkMode, "ConvertirDinero"))
        self.buttonGroup.addButton(self.monedaButton, 1)
        self.volumenButton = QRadioButton("Volumen")
        self.volumenButton.setMaximumHeight(32)
        self.volumenButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "volumen.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.volumenButton.toggled.connect(partial(self.checkMode, "ConvertirVolumen"))
        self.buttonGroup.addButton(self.volumenButton, 1)
        self.longitudButton = QRadioButton("Longitud")
        self.longitudButton.setMaximumHeight(32)
        self.longitudButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "longitud.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.longitudButton.toggled.connect(
            partial(self.checkMode, "ConvertirLongitud")
        )
        self.buttonGroup.addButton(self.longitudButton, 1)
        self.pesoYmasaButton = QRadioButton("Peso y masa")
        self.pesoYmasaButton.setMaximumHeight(32)
        self.pesoYmasaButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(os.path.join("icons", "masa.png"), QSize(32, 32))
                )
            )
        )
        self.pesoYmasaButton.toggled.connect(partial(self.checkMode, "ConvertirMasa"))
        self.buttonGroup.addButton(self.pesoYmasaButton, 1)
        self.temperaturaButton = QRadioButton("Temperatura")
        self.temperaturaButton.setMaximumHeight(32)
        self.temperaturaButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "temperatura.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.temperaturaButton.toggled.connect(
            partial(self.checkMode, "ConvertirTemperatura")
        )
        self.buttonGroup.addButton(self.temperaturaButton, 1)
        self.energiaButton = QRadioButton("Energia")
        self.energiaButton.setMaximumHeight(32)
        self.energiaButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "energia.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.energiaButton.toggled.connect(partial(self.checkMode, "ConvertirEnergia"))
        self.buttonGroup.addButton(self.energiaButton, 1)
        self.areaButton = QRadioButton("Area")
        self.areaButton.setMaximumHeight(32)
        self.areaButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(os.path.join("icons", "area.png"), QSize(32, 32))
                )
            )
        )
        self.areaButton.toggled.connect(partial(self.checkMode, "ConvertirArea"))
        self.buttonGroup.addButton(self.areaButton, 1)
        self.velocidadButton = QRadioButton("Velocidad")
        self.velocidadButton.setMaximumHeight(32)
        self.velocidadButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(os.path.join("icons", "area.png"), QSize(32, 32))
                )
            )
        )
        self.velocidadButton.toggled.connect(
            partial(self.checkMode, "ConvertirVelocidad")
        )
        self.buttonGroup.addButton(self.velocidadButton, 1)
        self.tiempoButton = QRadioButton("Tiempo")
        self.tiempoButton.setMaximumHeight(32)
        self.tiempoButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "tiempo.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.tiempoButton.toggled.connect(partial(self.checkMode, "ConvertirTiempo"))
        self.buttonGroup.addButton(self.tiempoButton, 1)
        self.potenciaButton = QRadioButton("Potencia")
        self.potenciaButton.setMaximumHeight(32)
        self.potenciaButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "potencia.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.potenciaButton.toggled.connect(
            partial(self.checkMode, "ConvertirPotencia")
        )
        self.buttonGroup.addButton(self.potenciaButton, 1)
        self.datosButton = QRadioButton("Datos")
        self.datosButton.setMaximumHeight(32)
        self.datosButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(os.path.join("icons", "datos.png"), QSize(32, 32))
                )
            )
        )
        self.datosButton.toggled.connect(partial(self.checkMode, "ConvertirDatos"))
        self.buttonGroup.addButton(self.datosButton, 1)
        self.presionButton = QRadioButton("Presion")
        self.presionButton.setMaximumHeight(32)
        self.presionButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "presion.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.presionButton.toggled.connect(partial(self.checkMode, "ConvertirPresion"))
        self.buttonGroup.addButton(self.presionButton, 1)
        self.anguloButton = QRadioButton("Angulo")
        self.anguloButton.setMaximumHeight(32)
        self.anguloButton.setIcon(
            QIcon(
                QPixmap.fromImage(
                    self.constructImg(
                        os.path.join("icons", "angulo.png"), QSize(32, 32)
                    )
                )
            )
        )
        self.anguloButton.toggled.connect(partial(self.checkMode, "ConvertirAngulo"))
        self.buttonGroup.addButton(self.anguloButton, 1)

        self.configButton = QPushButton("Configuracion")
        self.configButton.setMaximumHeight(32)

        self.frame_lateralbar_buttons_layout.addWidget(self.calculadoraLabel)
        self.frame_lateralbar_buttons_layout.addWidget(self.standardButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.cientificaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.graficaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.programadorButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.calcFechaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.convertidorLabel)
        self.frame_lateralbar_buttons_layout.addWidget(self.monedaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.volumenButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.longitudButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.pesoYmasaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.temperaturaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.energiaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.areaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.velocidadButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.tiempoButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.potenciaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.datosButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.presionButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.anguloButton)
        self.frame_lateralbar_configButton_layout.addWidget(self.configButton)

    def writeCfg(self, section, option, value):
        self.cfg.set(section, option, value)
        with open(os.path.join("Assets", "config.cfg"), "w") as configfile:
            self.cfg.write(configfile)
    
    def checkMode(self, mode):
        match mode:
            case "Estandar":
                self.standardButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(0)
            case "Cientifico":
                self.cientificaButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(1)
            case "Grafica":
                self.graficaButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(2)
            case "Programador":
                self.programadorButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(3)
            case "CalcularFecha":
                self.calcFechaButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(4)
            case "ConvertirDinero":
                self.monedaButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(5)
            case "ConvertirVolumen":
                self.volumenButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(6)
            case "ConvertirLongitud":
                self.longitudButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(7)
            case "ConvertirMasa":
                self.pesoYmasaButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(8)
            case "ConvertirTemperatura":
                self.temperaturaButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(9)
            case "ConvertirEnergia":
                self.energiaButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(10)
            case "ConvertirArea":
                self.areaButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(11)
            case "ConvertirVelocidad":
                self.velocidadButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(12)
            case "ConvertirTiempo":
                self.tiempoButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(13)
            case "ConvertirPotencia":
                self.potenciaButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(14)
            case "ConvertirDatos":
                self.datosButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(15)
            case "ConvertirPresion":
                self.stackedWidget.setCurrentIndex(16)
            case "ConvertirAngulo":
                self.anguloButton.setChecked(True)
                self.stackedWidget.setCurrentIndex(17)

    def modoEstandar(self):
        self.writeCfg("Mode", "actual-mode", "Estandar")
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        generalFrame.setLayout(generalFrame_layout)

        lcdFrame = QFrame()
        lcdFrame.setMinimumSize(310, 90)
        lcdFrame.setFrameShape(QFrame.Shape.StyledPanel)
        lcdFrame_layout = QGridLayout()
        lcdFrame.setLayout(lcdFrame_layout)
        lcdFrame_layout.addWidget(self.LCDNumber)

        MButtonsFrame = QFrame()
        MButtonsFrame.setMinimumSize(300, 50)
        MButtonsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        MButtonsFrame_layout = QHBoxLayout()
        MButtonsFrame.setLayout(MButtonsFrame_layout)
        MButtonsFrame_layout.addWidget(self.MCButton)
        MButtonsFrame_layout.addWidget(self.MRButton)
        MButtonsFrame_layout.addWidget(self.MPlusButton)
        MButtonsFrame_layout.addWidget(self.MMenosButton)
        MButtonsFrame_layout.addWidget(self.MSButton)

        generalButtonFrame = QFrame()
        generalButtonFrame.setMinimumSize(300, 800)
        generalButtonFrame.setFrameShape(QFrame.Shape.StyledPanel)
        generalButtonFrame_layout = QGridLayout()
        generalButtonFrame.setLayout(generalButtonFrame_layout)
        generalButtonFrame_layout.addWidget(self.porcientoButton, 2, 0)
        generalButtonFrame_layout.addWidget(self.CEButton, 2, 1)
        generalButtonFrame_layout.addWidget(self.CButton, 2, 2)
        generalButtonFrame_layout.addWidget(self.deleteButton, 2, 3)
        generalButtonFrame_layout.addWidget(self.fracc1overxButton, 3, 0)
        generalButtonFrame_layout.addWidget(self.cuadradoButton, 3, 1)
        generalButtonFrame_layout.addWidget(self.sqrtButton, 3, 2)
        generalButtonFrame_layout.addWidget(self.divButton, 3, 3)
        generalButtonFrame_layout.addWidget(self.sevenButton, 4, 0)
        generalButtonFrame_layout.addWidget(self.eightButton, 4, 1)
        generalButtonFrame_layout.addWidget(self.nineButton, 4, 2)
        generalButtonFrame_layout.addWidget(self.multButton, 4, 3)
        generalButtonFrame_layout.addWidget(self.fourButton, 5, 0)
        generalButtonFrame_layout.addWidget(self.fiveButton, 5, 1)
        generalButtonFrame_layout.addWidget(self.sixButton, 5, 2)
        generalButtonFrame_layout.addWidget(self.minusButton, 5, 3)
        generalButtonFrame_layout.addWidget(self.oneButton, 6, 0)
        generalButtonFrame_layout.addWidget(self.twoButton, 6, 1)
        generalButtonFrame_layout.addWidget(self.threeButton, 6, 2)
        generalButtonFrame_layout.addWidget(self.plusButton, 6, 3)
        generalButtonFrame_layout.addWidget(self.masmenosButton, 7, 0)
        generalButtonFrame_layout.addWidget(self.ceroButton, 7, 1)
        generalButtonFrame_layout.addWidget(self.comaButton, 7, 2)
        generalButtonFrame_layout.addWidget(self.equalButton, 7, 3)

        generalFrame_layout.addWidget(lcdFrame)
        generalFrame_layout.addWidget(MButtonsFrame)
        generalFrame_layout.addWidget(generalButtonFrame)
        

        return generalFrame

    def modoCientifico(self):
        self.writeCfg("Mode", "actual-mode", "Cientifico")
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoGrafica(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoProgramador(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoCalcularFecha(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirDinero(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirVolumen(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirLongitud(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirMasa(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirTemperatura(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirEnergia(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirArea(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirVelocidad(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirTiempo(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirPotencia(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirDatos(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirPresion(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    def modoConvertirAngulo(self):
        generalFrame = QFrame()
        generalFrame_layout = QVBoxLayout()
        return generalFrame

    class AcercaDe(QWindow):
        pass

    def config(self):
        pass

    def loadHistoriy(self):
        pass

    def showHistory(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Calculadora()
    ex.show()

    sys.exit(app.exec())
