from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from .uilib.window import Dialog
from .uilib.util import shadowify


class CreatePlaylistDialog(Dialog):
    def __init__(self, p):
        super(CreatePlaylistDialog, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout()
        self.input_lay = QtWidgets.QVBoxLayout()
        self.cover_button_lay = QtWidgets.QVBoxLayout()

        self.addCoverButton = QtWidgets.QPushButton(self)
        self.addCoverButton.setIcon(QIcon("res/icons/create_playlist_add_cover.svg"))
        self.addCoverButton.setFixedSize(128, 128)
        self.addCoverButton.setIconSize(QSize(32, 32))
        self.addCoverButton.setObjectName("add-cover")

        self.addCoverLabel = QtWidgets.QLabel("Add a cover image\n(optional)")
        self.addCoverLabel.setAlignment(Qt.AlignCenter)

        self.playlistName = QtWidgets.QLineEdit(self)
        self.playlistName.setPlaceholderText("Give this playlist a name")
        self.playlistDesc = QtWidgets.QTextEdit(self)
        self.playlistDesc.setPlaceholderText("Give this playlist a description (optional)")
        shadowify(self.addCoverButton)
        shadowify(self.playlistName)
        shadowify(self.playlistDesc)

        self.input_lay.addWidget(self.playlistName)
        self.input_lay.addSpacing(10)
        self.input_lay.addWidget(self.playlistDesc)
        self.cover_button_lay.addWidget(self.addCoverButton, alignment=Qt.AlignHCenter)
        self.hlay.addLayout(self.cover_button_lay)
        self.hlay.addSpacing(25)
        self.hlay.addLayout(self.input_lay)
        self.mainLayout.addLayout(self.hlay)
        self.dialogButtonLayout.addWidget(self.addCoverLabel, alignment=Qt.AlignLeft)
        self.showDialogButtons()


class EqualizerDialog(Dialog):
    def __init__(self, p):
        super(EqualizerDialog, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout()

        self.pre_lay = QtWidgets.QVBoxLayout()
        self.pre_lay.setSpacing(0)
        self.eq0_lay = QtWidgets.QVBoxLayout()
        self.eq0_lay.setSpacing(0)
        self.eq1_lay = QtWidgets.QVBoxLayout()
        self.eq1_lay.setSpacing(0)
        self.eq2_lay = QtWidgets.QVBoxLayout()
        self.eq2_lay.setSpacing(0)
        self.eq3_lay = QtWidgets.QVBoxLayout()
        self.eq3_lay.setSpacing(0)
        self.eq4_lay = QtWidgets.QVBoxLayout()
        self.eq4_lay.setSpacing(0)
        self.eq5_lay = QtWidgets.QVBoxLayout()
        self.eq5_lay.setSpacing(0)
        self.eq6_lay = QtWidgets.QVBoxLayout()
        self.eq6_lay.setSpacing(0)
        self.eq7_lay = QtWidgets.QVBoxLayout()
        self.eq7_lay.setSpacing(0)
        self.eq8_lay = QtWidgets.QVBoxLayout()
        self.eq8_lay.setSpacing(0)
        self.eq9_lay = QtWidgets.QVBoxLayout()
        self.eq9_lay.setSpacing(0)

        self.pre = QtWidgets.QSlider(self)
        self.eq0 = QtWidgets.QSlider(self)
        self.eq1 = QtWidgets.QSlider(self)
        self.eq2 = QtWidgets.QSlider(self)
        self.eq3 = QtWidgets.QSlider(self)
        self.eq4 = QtWidgets.QSlider(self)
        self.eq5 = QtWidgets.QSlider(self)
        self.eq6 = QtWidgets.QSlider(self)
        self.eq7 = QtWidgets.QSlider(self)
        self.eq8 = QtWidgets.QSlider(self)
        self.eq9 = QtWidgets.QSlider(self)

        for slider in self.findChildren(QtWidgets.QSlider):
            slider.setFixedHeight(200)

        self.pre_lbl = QtWidgets.QLabel("Pre", self)
        self.eq0_lbl = QtWidgets.QLabel("31", self)
        self.eq1_lbl = QtWidgets.QLabel("62", self)
        self.eq2_lbl = QtWidgets.QLabel("125", self)
        self.eq3_lbl = QtWidgets.QLabel("250", self)
        self.eq4_lbl = QtWidgets.QLabel("500", self)
        self.eq5_lbl = QtWidgets.QLabel("1k", self)
        self.eq6_lbl = QtWidgets.QLabel("2k", self)
        self.eq7_lbl = QtWidgets.QLabel("4k", self)
        self.eq8_lbl = QtWidgets.QLabel("8k", self)
        self.eq9_lbl = QtWidgets.QLabel("16k", self)

        for label in self.findChildren(QtWidgets.QLabel):
            if label.objectName() != "window-title":
                label.setObjectName("eq-label")
                label.setFixedSize(25, 25)
                label.setAlignment(Qt.AlignCenter)

        self.pre_lay.addWidget(self.pre)
        self.pre_lay.addWidget(self.pre_lbl)

        self.eq0_lay.addWidget(self.eq0, alignment=Qt.AlignHCenter)
        self.eq0_lay.addWidget(self.eq0_lbl)
        self.eq1_lay.addWidget(self.eq1, alignment=Qt.AlignHCenter)
        self.eq1_lay.addWidget(self.eq1_lbl)
        self.eq2_lay.addWidget(self.eq2, alignment=Qt.AlignHCenter)
        self.eq2_lay.addWidget(self.eq2_lbl)
        self.eq3_lay.addWidget(self.eq3, alignment=Qt.AlignHCenter)
        self.eq3_lay.addWidget(self.eq3_lbl)
        self.eq4_lay.addWidget(self.eq4, alignment=Qt.AlignHCenter)
        self.eq4_lay.addWidget(self.eq4_lbl)
        self.eq5_lay.addWidget(self.eq5, alignment=Qt.AlignHCenter)
        self.eq5_lay.addWidget(self.eq5_lbl)
        self.eq6_lay.addWidget(self.eq6, alignment=Qt.AlignHCenter)
        self.eq6_lay.addWidget(self.eq6_lbl)
        self.eq7_lay.addWidget(self.eq7, alignment=Qt.AlignHCenter)
        self.eq7_lay.addWidget(self.eq7_lbl)
        self.eq8_lay.addWidget(self.eq8, alignment=Qt.AlignHCenter)
        self.eq8_lay.addWidget(self.eq8_lbl)
        self.eq9_lay.addWidget(self.eq9, alignment=Qt.AlignHCenter)
        self.eq9_lay.addWidget(self.eq9_lbl)

        self.hlay.addLayout(self.pre_lay)
        self.hlay.addLayout(self.eq0_lay)
        self.hlay.addLayout(self.eq1_lay)
        self.hlay.addLayout(self.eq2_lay)
        self.hlay.addLayout(self.eq3_lay)
        self.hlay.addLayout(self.eq4_lay)
        self.hlay.addLayout(self.eq5_lay)
        self.hlay.addLayout(self.eq6_lay)
        self.hlay.addLayout(self.eq7_lay)
        self.hlay.addLayout(self.eq8_lay)
        self.hlay.addLayout(self.eq9_lay)

        self.okButton.setText("Save")
        self.okButton.setObjectName("eq-save")
        shadowify(self.okButton)

        self.cancelButton.setText("Close")
        self.cancelButton.setObjectName("eq-close")
        shadowify(self.cancelButton)

        self.presetSelector = QtWidgets.QComboBox(self)
        self.presetSelector.addItems(["Flat", "Rock", "Pop", "Electronic", "Dubstep", "Bass", "Jazz", "Country",  "Classic", "In-ear", "Headphone", "TV Spk", "Laptop Spk", "Low Pass", "Mid Pass", "High Pass"])
        self.presetSelector.setIconSize(QSize(5, 5))
        self.presetSelector.setFixedWidth(114)
        shadowify(self.presetSelector)

        self.dialogButtonLayout.addWidget(self.presetSelector, alignment=Qt.AlignLeft)
        self.mainLayout.addLayout(self.hlay)
        self.showDialogButtons()
