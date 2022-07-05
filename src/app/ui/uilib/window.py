from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5 import QtWidgets
from PyQt5.QtCore import (
    Qt,
    QPropertyAnimation,
    QPoint,
    QEasingCurve,
    pyqtSignal,
    QVariantAnimation,
    QObject
)
from PyQt5.QtGui import QColor
from .util import get_screen_size


class WindowTitleNotch(QtWidgets.QFrame):
    def __init__(self, p, title):
        super(WindowTitleNotch, self).__init__(p)
        self.setObjectName("window-title-notch")
        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.title = QtWidgets.QLabel(title, self)
        self.title.setObjectName("window-title")
        self.title.adjustSize()
        self.setFixedSize(self.title.width() + 25, 20)
        self.hbox.addWidget(self.title, alignment=Qt.AlignCenter)

    def setTitle(self, title):
        self.title.setText(title)
        self.title.adjustSize()
        self.setFixedSize(self.title.width()+35, 20)
        self.parent().centerTitleNotch()


class TitleBar(QtWidgets.QFrame):
    def __init__(self, p=None):
        super(TitleBar, self).__init__(p)
        self.setObjectName("titlebar")
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(0, 0, 9, 0)
        self.hlay.setSpacing(11)
        self.hlay.setAlignment(Qt.AlignRight)

        self.windowNotch = WindowTitleNotch(self, "Window")

        self.closeButton = QtWidgets.QPushButton(self)
        self.sizeButton = QtWidgets.QPushButton(self)
        self.minimizeButton = QtWidgets.QPushButton(self)

        self.closeButton.setToolTip("Close")
        self.sizeButton.setToolTip("Maximize/Restore")
        self.minimizeButton.setToolTip("Minimize")

        self.closeButton.clicked.connect(self.parent().parent().windowCloseEvent)
        self.sizeButton.clicked.connect(self.parent().parent().sizeEvent)
        self.minimizeButton.clicked.connect(self.parent().parent().minimizeEvent)

        self.closeButton.setObjectName("control-close")
        self.sizeButton.setObjectName("control-size")
        self.minimizeButton.setObjectName("control-minimize")

        for button in self.findChildren(QtWidgets.QPushButton):
            button.setFixedSize(12, 12)

        self.hlay.addWidget(self.minimizeButton)
        self.hlay.addWidget(self.sizeButton)
        self.hlay.addWidget(self.closeButton)

    def mouseDoubleClickEvent(self, a0) -> None:
        self.sizeButton.click()

    def centerTitleNotch(self):
        self.windowNotch.move((self.width() // 2) - self.windowNotch.width() // 2, 0)

    def resizeEvent(self, a0) -> None:
        self.centerTitleNotch()

    def mousePressEvent(self, event) -> None:
        self.window().windowHandle().startSystemMove()
        self.parent().setUpdateState(True)
        QtWidgets.QFrame.mousePressEvent(self, event)

    def mouseReleaseEvent(self, a0) -> None:
        self.parent().setUpdateState(False)
        QtWidgets.QFrame.mouseReleaseEvent(self, a0)


class Window(QtWidgets.QFrame):
    onMove = pyqtSignal(QPoint)

    def __init__(self, p, width: int = 640, height: int = 480):
        super(Window, self).__init__(p)
        self.setWindowTitle("Window")
        self.setObjectName("main-window")
        self.resize(width, height)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.titlebar = TitleBar(self)
        self.opacity = 255
        self.isUpdating = False
        self.closingQueue = []

    def raiseBaseWidget(self):
        self.titlebar.raise_()

    def moveEvent(self, a0) -> None:
        self.onMove.emit(self.pos())
        QWidget.moveEvent(self, a0)

    def resizeEvent(self, event) -> None:
        self.titlebar.resize(self.width(), 30)
        QWidget.resizeEvent(self, event)

    def setOpacity(self, opacity: int):
        self.opacity = opacity

    def setUpdateState(self, isUpdating):
        self.isUpdating = isUpdating

    # def paintEvent(self, event) -> None:
    #     window_border_radius = 16
    #     s = self.size()
    #     qp = QPainter(self)
    #     qp.setBrush(QColor(249, 249, 249, self.opacity))
    #     qp.setPen(QColor("transparent"))
    #     qp.setRenderHint(QPainter.Antialiasing)
    #     qp.setRenderHint(QPainter.HighQualityAntialiasing)
    #     qp.drawRoundedRect(0, 0, s.width(), s.height(),
    #                        window_border_radius, window_border_radius)
    #     qp.end()
    #     QWidget.paintEvent(self, event)


class CornerGrip(QtWidgets.QSizeGrip):
    isResizing = pyqtSignal(bool)

    def __init__(self, p):
        super(CornerGrip, self).__init__(p)
        self.setFixedSize(20, 20)

    def mousePressEvent(self, a0) -> None:
        self.isResizing.emit(True)
        QtWidgets.QSizeGrip.mousePressEvent(self, a0)

    def mouseReleaseEvent(self, mouseEvent) -> None:
        self.isResizing.emit(False)
        QtWidgets.QSizeGrip.mouseReleaseEvent(self, mouseEvent)


class SideGrip(QtWidgets.QFrame):
    isResizing = pyqtSignal(bool)

    def __init__(self, p, edge, cursor):
        super(SideGrip, self).__init__(p)
        self.edge = edge
        self.setObjectName("side-grip")
        self.setCursor(cursor)

    def mousePressEvent(self, a0) -> None:
        self.window().windowHandle().startSystemResize(self.edge)
        self.isResizing.emit(True)
        QtWidgets.QFrame.mousePressEvent(self, a0)

    def mouseReleaseEvent(self, mouseEvent) -> None:
        self.isResizing.emit(False)
        QtWidgets.QFrame.mouseReleaseEvent(self, mouseEvent)


class WindowContainer(QWidget):
    def __init__(self, window, p=None, width=854, height=480):
        super(WindowContainer, self).__init__(p)
        self.setSize(width, height)
        self.setMinimumSize(300, 100)
        self.windowObject = window(self)
        self.windowObject.move(20, 20)
        self.dropShadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.dropShadow.setBlurRadius(32)
        self.dropShadow.setColor(QColor(0, 0, 0, 135))
        self.dropShadow.setOffset(0, 0)
        self.windowObject.setGraphicsEffect(self.dropShadow)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        with open("res/style.qss") as style:
            self.setStyleSheet(style.read())

        self.rightSizeGrip = SideGrip(self, Qt.RightEdge, Qt.SizeHorCursor)
        self.leftSizeGrip = SideGrip(self, Qt.LeftEdge, Qt.SizeHorCursor)
        self.topSizeGrip = SideGrip(self, Qt.TopEdge, Qt.SizeVerCursor)
        self.bottomSizeGrip = SideGrip(self, Qt.BottomEdge, Qt.SizeVerCursor)

        self.bottomRightGrip = CornerGrip(self)
        self.topRightGrip = CornerGrip(self)
        self.bottomLeftGrip = CornerGrip(self)
        self.topLeftGrip = CornerGrip(self)

        for sideGrip in self.findChildren(SideGrip):
            sideGrip.isResizing.connect(lambda resizing: self.windowObject.setUpdateState(resizing))

        for cornerGrip in self.findChildren(CornerGrip):
            cornerGrip.isResizing.connect(lambda resizing: self.windowObject.setUpdateState(resizing))

        self.showAnimation = QPropertyAnimation(self, b"pos")
        self.showAnimation.setDuration(500)
        self.hideAnimation = QPropertyAnimation(self, b"pos")
        self.hideAnimation.setDuration(500)
        self.opacityAnimation = QVariantAnimation(self)
        self.opacityAnimation.setDuration(500)
        self.opacityAnimation.valueChanged.connect(self.setWindowOpacity)

        self.oldPos = self.get_center()

    def setSize(self, width, height):
        self.resize(width + 40, height + 40)

    def get_center(self):
        geometry = self.frameGeometry()
        geometry.moveCenter(get_screen_size().center())
        return geometry.topLeft()

    def sizeEvent(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def windowCloseEvent(self) -> None:
        self.oldPos = self.pos()
        self.hideAnimation.setStartValue(self.oldPos)
        self.hideAnimation.setEndValue(QPoint(self.x(), get_screen_size().height()))
        self.hideAnimation.setEasingCurve(QEasingCurve.InCubic)
        self.hideAnimation.start()
        self.hideAnimation.finished.connect(self.close)

        self.opacityAnimation.setStartValue(1.0)
        self.opacityAnimation.setEndValue(0.0)
        self.opacityAnimation.setEasingCurve(QEasingCurve.InCubic)
        self.opacityAnimation.finished.connect(self.cleanup)
        self.opacityAnimation.start()

    def cleanup(self):
        for item in self.windowObject.closingQueue:
            if isinstance(item, QObject):
                item.close()
            else:
                if callable(item):
                    item()
                else:
                    raise Exception(f"Item '{item}' in closing queue is not an instance of QObject, "
                                    f"nor is it a callable.")

    def showEvent(self, event) -> None:
        self.showAnimation.setStartValue(QPoint(self.x(), get_screen_size().height()))
        self.showAnimation.setEndValue(self.oldPos)
        self.showAnimation.setEasingCurve(QEasingCurve.OutCubic)
        self.showAnimation.start()

        self.opacityAnimation.setStartValue(0.0)
        self.opacityAnimation.setEndValue(1.0)
        self.opacityAnimation.setEasingCurve(QEasingCurve.OutCubic)
        self.opacityAnimation.start()
        QWidget.showEvent(self, event)

    def minimizeEvent(self):
        self.oldPos = self.pos()
        self.hideAnimation.setStartValue(self.oldPos)
        self.hideAnimation.setEndValue(QPoint(self.x(), get_screen_size().height()))
        self.hideAnimation.setEasingCurve(QEasingCurve.InCubic)
        self.hideAnimation.start()
        self.hideAnimation.finished.connect(self.showMinimized)

        self.opacityAnimation.setStartValue(1.0)
        self.opacityAnimation.setEndValue(0.0)
        self.opacityAnimation.setEasingCurve(QEasingCurve.InCubic)
        self.opacityAnimation.start()

    def resizeEvent(self, a0) -> None:
        self.windowObject.resize(self.width() - 40, self.height() - 40)
        self.bottomRightGrip.move(self.windowObject.width() + 10, self.windowObject.height() + 10)
        self.topRightGrip.move(self.windowObject.width() + 15, 15)
        self.bottomLeftGrip.move(15, self.windowObject.height() + 10)
        self.topLeftGrip.move(10, 10)

        self.leftSizeGrip.move(0, 20)
        self.leftSizeGrip.resize(20, self.windowObject.height())
        self.topSizeGrip.move(20, 0)
        self.topSizeGrip.resize(self.windowObject.width(), 20)
        self.rightSizeGrip.move(self.width() - 20, 20)
        self.rightSizeGrip.resize(20, self.windowObject.height())
        self.bottomSizeGrip.move(20, self.height() - 20)
        self.bottomSizeGrip.resize(self.windowObject.width(), 20)
        QWidget.resizeEvent(self, a0)


class Dialog(Window):
    def __init__(self, p):
        super(Dialog, self).__init__(p)
        self.titlebar.windowNotch.setTitle("Dialog")
        self.titlebar.hlay.removeWidget(self.titlebar.minimizeButton)
        del self.titlebar.minimizeButton
        self.titlebar.hlay.removeWidget(self.titlebar.sizeButton)
        del self.titlebar.sizeButton

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(32, 35, 32, 8)
        self.dialogButtonLayout = QtWidgets.QHBoxLayout(self)

        self.okButton = QtWidgets.QPushButton("Ok", self)
        self.okButton.setObjectName("ok-button")
        self.okButton.setFixedSize(100, 25)
        self.okButton.hide()
        self.okButton.clicked.connect(self.onOk)

        self.cancelButton = QtWidgets.QPushButton("Cancel", self)
        self.cancelButton.setObjectName("cancel-button")
        self.cancelButton.setFixedSize(100, 25)
        self.cancelButton.hide()
        self.cancelButton.clicked.connect(self.onCancel)

    def onOk(self):
        pass

    def onCancel(self):
        self.titlebar.closeButton.click()

    def showDialogButtons(self):
        self.okButton.show()
        self.cancelButton.show()
        self.dialogButtonLayout.addWidget(self.cancelButton, alignment=Qt.AlignRight)
        self.dialogButtonLayout.addWidget(self.okButton)
        self.mainLayout.addLayout(self.dialogButtonLayout)


class DialogContainer(WindowContainer):
    def __init__(self, dialog, title, parent, width=500, height=300):
        super(DialogContainer, self).__init__(dialog, parent, width, height)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.windowObject.titlebar.windowNotch.setTitle(title)

    def setResizable(self, resizable):
        if resizable:
            for sideGrip in self.findChildren(SideGrip):
                sideGrip.show()
            for conerGrip in self.findChildren(CornerGrip):
                conerGrip.show()
        else:
            for sideGrip in self.findChildren(SideGrip):
                sideGrip.hide()
            for conerGrip in self.findChildren(CornerGrip):
                conerGrip.hide()

    def show(self) -> None:
        # move the dialog to the center of the parent window
        self.oldPos.setX(self.parent().parent().pos().x() + (self.parent().width() // 2) - (self.width() // 2) + 22)
        self.oldPos.setY(self.parent().parent().pos().y() + (self.parent().height() // 2) - (self.height() // 2) + 22)
        WindowContainer.show(self)
