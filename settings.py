import configparser
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets


# Settings class
# Used to hold settings and execute read/write operations on the configuration file.
class Settings:
    # Init
    # Args : None
    def __init__(self):
        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        elif __file__:
            self.application_path = os.path.dirname(__file__)

        self.file = os.path.join(self.application_path, 'config.ini')

        self.fp = open(self.file)
        self.cfg = configparser.ConfigParser()
        self.cfg.read_file(self.fp)

    # Get
    # Read configuration file at section k, line v
    # Args : k=section, v=line
    def get(self, k, v):
        return self.cfg.get(k, v)

    # Write
    # Re-write configuration file.
    # Args : threads, timeout, behavior, browser, ftp, media
    def write(self, threads, timeout, behavior):
        self.fp.close()
        config = configparser.ConfigParser()
        config.add_section("Core")
        config.set("Core", "threads", str(threads))
        config.set("Core", "timeout", str(timeout))
        config.set("Core", "behavior", str(behavior))

        with open(self.file, "w") as config_file:
            config.write(config_file)

        self.fp = open(self.file, "r")
        self.cfg = configparser.ConfigParser()
        self.cfg.readfp(self.fp)

# Settings Window UI class
# QT class of the settings window
class Ui_Settings(QtWidgets.QMainWindow):
    # Init
    # Args : settings=settings object, parent=main window
    def __init__(self, settings, parent=None):
        super(Ui_Settings, self).__init__(parent.mw)
        self.par = parent
        self.s = settings
        self.behaviors = \
            {0: "For <b>one</b> address generated, <b>one</b> scanner is randomly picked.",
             1: "A <b>succeeded</b> scan will trigger every other active scanners on the <b>same</b> address.",
             2: "For <b>every</b> generated address, <b>all</b> active scanners are used."}
        self.setupUi(self)

    # Setup UI
    # UI creation
    # Args : Settings=window
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.setMinimumSize(400, 400)

        self.centralWidget = QtWidgets.QWidget(Settings)
        self.centralWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        #OK, Cancel
        self.Button_OK = QtWidgets.QPushButton(self.centralWidget)
        self.Button_OK.setObjectName("Button_OK")
        self.Button_Cancel = QtWidgets.QPushButton(self.centralWidget)
        self.Button_Cancel.setObjectName("Button_Cancel")

        # Groupbox 1
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")

        # Max threads
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.Spinbox_Threads = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.Spinbox_Threads.setMaximum(99999)
        self.Spinbox_Threads.setObjectName("Spinbox_Threads")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Spinbox_Threads)

        # Timeout
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.Spinbox_Timeout = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.Spinbox_Timeout.setDecimals(1)
        self.Spinbox_Timeout.setMaximum(999999.0)
        self.Spinbox_Timeout.setObjectName("Spinbox_Timeout")

        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Spinbox_Timeout)
        self.groupBox.setLayout(self.formLayout)


        # Groupbox 2
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_4.setObjectName("label_4")

        self.ComboBox_Scanmode = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.ComboBox_Scanmode.setObjectName("ComboBox_Scanmode")
        self.ComboBox_Scanmode.addItem("")
        self.ComboBox_Scanmode.addItem("")
        self.ComboBox_Scanmode.addItem("")

        self.Label_Scanmode = QtWidgets.QLabel(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.Label_Scanmode.setFont(font)
        self.Label_Scanmode.setObjectName("Label_Scanmode")
        self.Label_Scanmode.setWordWrap(True)

        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ComboBox_Scanmode)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Label_Scanmode)
        self.groupBox_2.setLayout(self.formLayout_2)

        # Central layout
        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.addWidget(self.groupBox)
        self.centralLayout.addWidget(self.groupBox_2)
        self.centralLayout.addWidget(self.Button_OK)
        self.centralLayout.addWidget(self.Button_Cancel)
        self.centralWidget.setLayout(self.centralLayout)
        Settings.setCentralWidget(self.centralWidget)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

        self.handleEvents()
        self.loadContent()

        qtRectangle = Settings.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        Settings.move(qtRectangle.topLeft())

    # Retranslate UI
    # Apply language on UI
    # Args : Settings=QT window
    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Settings"))
        self.Button_OK.setText(_translate("Settings", "Save"))
        self.Button_Cancel.setText(_translate("Settings", "Cancel"))
        self.groupBox.setTitle(_translate("Settings", "Core"))
        self.label.setText(_translate("Settings", "Threads:"))
        self.label_6.setText(_translate("Settings", "Timeout: "))
        self.groupBox_2.setTitle(_translate("Settings", "Behaviors"))
        self.label_4.setText(_translate("Settings", "Scan mode : "))
        self.ComboBox_Scanmode.setItemText(0, _translate("Settings", "Random"))
        self.ComboBox_Scanmode.setItemText(1, _translate("Settings", "Intelligent"))
        self.ComboBox_Scanmode.setItemText(2, _translate("Settings", "Everything"))
        self.Label_Scanmode.setText(_translate("Settings", "TextLabel"))

    # Handle events
    # Link UI events to functions.
    # Args : None
    def handleEvents(self):
        self.Button_Cancel.clicked.connect(self.onButtonCancel)
        self.Button_OK.clicked.connect(self.onButtonOK)
        self.ComboBox_Scanmode.currentIndexChanged.connect(self.onScanmode)

    # Load content
    # Fill UI with values from the core.
    # Args : None
    def loadContent(self):
        self.Spinbox_Threads.setValue(int(self.s.get('Core', 'threads')))
        self.Spinbox_Timeout.setValue(int(self.s.get('Core', 'timeout')))
        self.ComboBox_Scanmode.setCurrentIndex(int(self.s.get('Core', 'behavior')))
        self.Label_Scanmode.setText(self.behaviors[self.ComboBox_Scanmode.currentIndex()])

    # Save content
    # Write a new configuration file based on this window's values.
    # Args : None
    def saveContent(self):
        self.s.write(int(self.Spinbox_Threads.value()), int(self.Spinbox_Timeout.value()),
                     int(self.ComboBox_Scanmode.currentIndex()))

    # On button OK
    # Called when the "OK" button is pressed.
    # Args : None
    def onButtonOK(self):
        self.saveContent()
        if self.par.ol.core.running:
            self.par.actionStartStop()
        self.par.ol.core.reboot()
        self.par.loadContent()
        self.close()

    # On button Cancel
    # Called when the "Cancel" button is pressed.
    # Args : None
    def onButtonCancel(self):
        self.close()

    # On scan mode
    # Called when the scan mode combobox selection changed.
    # Args : None
    def onScanmode(self):
        self.Label_Scanmode.setText(self.behaviors[self.ComboBox_Scanmode.currentIndex()])