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
        self.screenRect = QScreen.availableGeometry(self.screen())
        self.screenWidth, self.screenHeight = (
            self.screenRect.width(),
            self.screenRect.height(),
        )
        self.screenSize = QSize(self.screenWidth, self.screenHeight)
        # TODO: Añadir icono
        # TODO: Hacer barra superior invisible y handle bottones
        self.ButtonCreator()
        self.initLateralBar()
        self.checkMode()

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
        if originalNumber == 0:
            originalNumber = int()
        finalNumber = str(int(originalNumber)) + str(
            "{}".format(str(number)[1:] if str(number).startswith("0") else str(number))
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
        image = image.convertToFormat(QImage.Format.Format_MonoLSB)
        image.setColor(0, qRgba(0, 0, 0, 0))
        if self.currentTheme == "dark":
            image.setColor(1, qRgb(255, 255, 255))
        else:
            pass
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

    def initLateralBar(self):
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

        self.calculadoraLabel = QLabel("Calculadora")  # Calculadora
        self.calculadoraLabel.setStyleSheet("font-weight: 900")
        self.standardButton = QPushButton()
        self.cienficaButton = QPushButton()
        self.graficaButton = QPushButton()
        self.progrmadorButton = QPushButton()
        self.calcFechaButton = QPushButton()

        self.convertidorLabel = QLabel("Convertidor")  # Convertidor
        self.convertidorLabel.setStyleSheet("font-weight: 900")
        self.monedaButton = QPushButton()
        self.volumenButton = QPushButton()
        self.longitudButton = QPushButton()
        self.pesoYmasaButton = QPushButton()
        self.temperaturaButton = QPushButton()
        self.energiaButton = QPushButton()
        self.areaButton = QPushButton()
        self.velocidadButton = QPushButton()
        self.tiempoButton = QPushButton()
        self.potenciaButton = QPushButton()
        self.datosButton = QPushButton()
        self.presionButton = QPushButton()
        self.anguloButton = QPushButton()

        self.configButton = QPushButton()

        self.frame_lateralbar_buttons_layout.addWidget(self.calculadoraLabel)
        self.frame_lateralbar_buttons_layout.addWidget(self.standardButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.cienficaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.graficaButton)
        self.frame_lateralbar_buttons_layout.addWidget(self.progrmadorButton)
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

        self.frame_central = QFrame()  # lado central (donde va la calculadora)
        self.frame_central.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_central_layout = QVBoxLayout()
        self.frame_central.setLayout(self.frame_central_layout)
        self.frame_central_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_central_layout.setSpacing(0)

        self.frame_lateralbar_layout.addWidget(self.frame_lateralbar_buttons)
        self.frame_lateralbar_layout.addWidget(self.frame_lateralbar_configButton)
        self.frame_contenedor_layout.addWidget(self.frame_lateralbar)
        self.frame_contenedor_layout.addWidget(self.frame_central)
        self.frame_inferior_layout.addWidget(self.frame_superior)
        self.frame_inferior_layout.addWidget(self.frame_contenedor)

        self.setCentralWidget(self.frame_inferior)

        """
        self.logo_label_standard = QLabel("")
        self.logo_label_standard.setMinimumSize(QSize(50, 50))
        self.logo_label_standard.setMaximumSize(QSize(50, 50))
        self.logo_label_standard.setPixmap(
            QPixmap.fromImage(
                self.constructImg("estandar.png", self.logo_label_standard.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_standard)

        self.logo_label_cientifico = QLabel("")
        self.logo_label_cientifico.setMinimumSize(QSize(50, 50))
        self.logo_label_cientifico.setMaximumSize(QSize(50, 50))
        self.logo_label_cientifico.setPixmap(
            QPixmap.fromImage(
                self.constructImg("cientifica.png", self.logo_label_cientifico.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_cientifico)

        self.logo_label_grafica = QLabel("")
        self.logo_label_grafica.setMinimumSize(QSize(50, 50))
        self.logo_label_grafica.setMaximumSize(QSize(50, 50))
        self.logo_label_grafica.setPixmap(
            QPixmap.fromImage(
                self.constructImg("grafica.png", self.logo_label_grafica.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_grafica)

        self.logo_label_programador = QLabel("")
        self.logo_label_programador.setMinimumSize(QSize(50, 50))
        self.logo_label_programador.setMaximumSize(QSize(50, 50))
        self.logo_label_programador.setPixmap(
            QPixmap.fromImage(
                self.constructImg("programador.png", self.logo_label_programador.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_programador)

        self.separator = QLabel("-")
        self.separator.setMinimumSize(QSize(50, 50))
        self.separator.setMaximumSize(QSize(50, 50))
        self.separator.setScaledContents(True)
        self.icon_only_widget_layout.addWidget(self.separator)

        self.logo_label_calcularFecha = QLabel("")
        self.logo_label_calcularFecha.setMinimumSize(QSize(50, 50))
        self.logo_label_calcularFecha.setMaximumSize(QSize(50, 50))
        self.logo_label_calcularFecha.setPixmap(
            QPixmap.fromImage(
                self.constructImg("Fecha.png", self.logo_label_calcularFecha.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_calcularFecha)

        self.logo_label_convertirDinero = QLabel("")
        self.logo_label_convertirDinero.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirDinero.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirDinero.setPixmap(
            QPixmap.fromImage(
                self.constructImg("moneda.png", self.logo_label_convertirDinero.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirDinero)

        self.logo_label_convertirVolumen = QLabel("")
        self.logo_label_convertirVolumen.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirVolumen.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirVolumen.setPixmap(
            QPixmap.fromImage(
                self.constructImg(
                    "volumen.png", self.logo_label_convertirVolumen.size()
                )
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirVolumen)

        self.logo_label_convertirLongitud = QLabel("")
        self.logo_label_convertirLongitud.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirLongitud.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirLongitud.setPixmap(
            QPixmap.fromImage(
                self.constructImg(
                    "longitud.png", self.logo_label_convertirLongitud.size()
                )
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirLongitud)

        self.logo_label_convertirMasa = QLabel("")
        self.logo_label_convertirMasa.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirMasa.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirMasa.setPixmap(
            QPixmap.fromImage(
                self.constructImg("masa.png", self.logo_label_convertirMasa.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirMasa)

        self.logo_label_convertirTemperatura = QLabel("")
        self.logo_label_convertirTemperatura.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirTemperatura.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirTemperatura.setPixmap(
            QPixmap.fromImage(
                self.constructImg(
                    "temperatura.png", self.logo_label_convertirTemperatura.size()
                )
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirTemperatura)

        self.logo_label_convertirEnergia = QLabel("")
        self.logo_label_convertirEnergia.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirEnergia.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirEnergia.setPixmap(
            QPixmap.fromImage(
                self.constructImg(
                    "energia.png", self.logo_label_convertirEnergia.size()
                )
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirEnergia)

        self.logo_label_convertirArea = QLabel("")
        self.logo_label_convertirArea.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirArea.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirArea.setPixmap(
            QPixmap.fromImage(
                self.constructImg("area.png", self.logo_label_convertirArea.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirArea)

        self.logo_label_convertirVelocidad = QLabel("")
        self.logo_label_convertirVelocidad.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirVelocidad.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirVelocidad.setPixmap(
            QPixmap.fromImage(
                self.constructImg(
                    "velocidad.png", self.logo_label_convertirVelocidad.size()
                )
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirVelocidad)

        self.logo_label_convertirTiempo = QLabel("")
        self.logo_label_convertirTiempo.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirTiempo.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirTiempo.setPixmap(
            QPixmap.fromImage(
                self.constructImg("tiempo.png", self.logo_label_convertirTiempo.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirTiempo)

        self.logo_label_convertirPotencia = QLabel("")
        self.logo_label_convertirPotencia.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirPotencia.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirPotencia.setPixmap(
            QPixmap.fromImage(
                self.constructImg(
                    "potencia.png", self.logo_label_convertirPotencia.size()
                )
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirPotencia)

        self.logo_label_convertirDatos = QLabel("")
        self.logo_label_convertirDatos.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirDatos.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirDatos.setPixmap(
            QPixmap.fromImage(
                self.constructImg("datos.png", self.logo_label_convertirDatos.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirDatos)

        self.logo_label_convertirPresion = QLabel("")
        self.logo_label_convertirPresion.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirPresion.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirPresion.setPixmap(
            QPixmap.fromImage(
                self.constructImg(
                    "presion.png", self.logo_label_convertirPresion.size()
                )
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirPresion)

        self.logo_label_convertirAngulo = QLabel("")
        self.logo_label_convertirAngulo.setMinimumSize(QSize(50, 50))
        self.logo_label_convertirAngulo.setMaximumSize(QSize(50, 50))
        self.logo_label_convertirAngulo.setPixmap(
            QPixmap.fromImage(
                self.constructImg("angulo.png", self.logo_label_convertirAngulo.size())
            )
        )
        self.icon_only_widget_layout.addWidget(self.logo_label_convertirAngulo)
        self.setCentralWidget(self.icon_only_widget)
        """

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
            case "ConvertirMasa":
                self.modoConvertirMasa
            case "ConvertirTemperatura":
                self.modoConvertirTemperatura()
            case "ConvertirEnergia":
                self.modoConvertirEnergia()
            case "ConvertirArea":
                self.modoConvertirArea()
            case "ConvertirVelocidad":
                self.modoConvertirVelocidad()
            case "ConvertirTiempo":
                self.modoConvertirTiempo()
            case "ConvertirPotencia":
                self.modoConvertirPotencia()
            case "ConvertirDatos":
                self.modoConvertirDatos()
            case "ConvertirPresion":
                self.modoConvertirPresion()
            case "ConvertirAngulo":
                self.modoConvertirAngulo()

    def modoEstandar(self):
        """
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
        return centralWidget
        """

    def modoCientifico(self):
        centralWidget = QWidget()
        return centralWidget

    def modoGrafica(self):
        centralWidget = QWidget()
        return centralWidget

    def modoProgramador(self):
        centralWidget = QWidget()
        return centralWidget

    def modoCalcularFecha(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirDinero(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirVolumen(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirLongitud(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirMasa(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirTemperatura(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirEnergia(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirArea(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirVelocidad(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirTiempo(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirPotencia(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirDatos(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirPresion(self):
        centralWidget = QWidget()
        return centralWidget

    def modoConvertirAngulo(self):
        centralWidget = QWidget()
        return centralWidget

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
