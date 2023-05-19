import os
import numpy as np
from PySide6.QtWidgets import QPushButton, QLabel, QGraphicsDropShadowEffect, QLineEdit, QApplication, QWidget
from PySide6.QtGui import Qt, QPainter, QBrush, QColor, QPixmap,QImage, QPen, QTransform
from PySide6.QtCore import QRect, QEvent, QPoint




def set_svg_icon(icon_name):
    app_path = os.path.abspath(os.getcwd())
    folder = "./gui/images/svg_icons/"
    path = os.path.join(app_path, folder)
    icon = os.path.normpath(os.path.join(path, icon_name))
    return icon
style = '''
QLineEdit {{
	background-color: {_bg_color}; 
	border-radius: {_radius}px;
	border: {_border_size}px solid transparent;
	padding-left: 10px;
    padding-right: 10px;
	selection-color: {_selection_color};
	selection-background-color: {_context_color};
    color: {_color};
}}
QLineEdit:focus {{
	border: {_border_size}px solid {_context_color};
    background-color: {_bg_color_active};
}}
'''
class PyLineEdit(QLineEdit):
    def __init__(
        self, 
        text = "",
        place_holder_text = "",
        radius = 8,
        border_size = 2,
        color = "#FFF",
        selection_color = "#FFF",
        bg_color = "#333",
        bg_color_active = "#222",
        context_color = "#00ABE8"
    ):
        super().__init__()
        if text:
            self.setText(text)
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)
        self.set_stylesheet(
            radius,
            border_size,
            color,
            selection_color,
            bg_color,
            bg_color_active,
            context_color
        )
    def set_stylesheet(
        self,
        radius,
        border_size,
        color,
        selection_color,
        bg_color,
        bg_color_active,
        context_color
    ):
        style_format = style.format(
            _radius = radius,
            _border_size = border_size,           
            _color = color,
            _selection_color = selection_color,
            _bg_color = bg_color,
            _bg_color_active = bg_color_active,
            _context_color = context_color
        )
        self.setStyleSheet(style_format)

class PyIconButton(QPushButton):
    def __init__(
        self,
        icon_path = None,
        parent = None,
        app_parent = None,
        tooltip_text = "",
        btn_id = None,
        width = 30,
        height = 30,
        radius = 8,
        bg_color = "#343b48",
        bg_color_hover = "#3c4454",
        bg_color_pressed = "#2c313c",
        icon_color = "#c3ccdf",
        icon_color_hover = "#dce1ec",
        icon_color_pressed = "#edf0f5",
        icon_color_active = "#f5f6f9",
        dark_one = "#1b1e23",
        text_foreground = "#8a95aa",
        context_color = "#568af2",
        top_margin = 40,
        is_active = False
    ):
        super().__init__()
        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName(btn_id)
        self._bg_color = bg_color
        self._bg_color_hover = bg_color_hover
        self._bg_color_pressed = bg_color_pressed        
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._context_color = context_color
        self._top_margin = top_margin
        self._is_active = is_active
        self._set_bg_color = bg_color
        self._set_icon_path = icon_path
        self._set_icon_color = icon_color
        self._set_border_radius = radius
        self._parent = parent
        self._app_parent = app_parent
        self._tooltip_text = tooltip_text
        self._tooltip = _ToolTip(
            app_parent,
            tooltip_text,
            dark_one,
            text_foreground
        )
        self._tooltip.hide()
    def clicked(self):
        self.clicked.emit()
    def set_active(self, is_active):
        self._is_active = is_active
        self.repaint()
    def is_active(self):
        return self._is_active
    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self._is_active:
            brush = QBrush(QColor(self._context_color))
        else:
            brush = QBrush(QColor(self._set_bg_color))
        rect = QRect(0, 0, self.width(), self.height())
        paint.setPen(Qt.NoPen)
        paint.setBrush(brush)
        paint.drawRoundedRect(
            rect, 
            self._set_border_radius, 
            self._set_border_radius
        )
        self.icon_paint(paint, self._set_icon_path, rect)
        paint.end()
    def change_style(self, event):
        if event == QEvent.Enter:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.repaint()         
        elif event == QEvent.Leave:
            self._set_bg_color = self._bg_color
            self._set_icon_color = self._icon_color
            self.repaint()
        elif event == QEvent.MouseButtonPress:            
            self._set_bg_color = self._bg_color_pressed
            self._set_icon_color = self._icon_color_pressed
            self.repaint()
        elif event == QEvent.MouseButtonRelease:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.repaint()
    def enterEvent(self, event):
        self.change_style(QEvent.Enter)
        self.move_tooltip()
        self._tooltip.show()
    def leaveEvent(self, event):
        self.change_style(QEvent.Leave)
        self.move_tooltip()
        self._tooltip.hide()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonPress)
            self.setFocus()
            return self.clicked.emit()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            
            self.change_style(QEvent.MouseButtonRelease)
            return self.released.emit()
    def icon_paint(self, qp, image, rect):
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        if self._is_active:
            painter.fillRect(icon.rect(), self._icon_color_active)
        else:
            painter.fillRect(icon.rect(), self._set_icon_color)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2, 
            (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()
    def set_icon(self, icon_path):
        self._set_icon_path = icon_path
        self.repaint()
    def move_tooltip(self):
        gp = self.mapToGlobal(QPoint(0, 0))
        pos = self._parent.mapFromGlobal(gp)
        pos_x = (pos.x() - (self._tooltip.width() // 2)) + (self.width() // 2)
        pos_y = pos.y() - self._top_margin
        self._tooltip.move(pos_x, pos_y)
        
class _ToolTip(QLabel):
    style_tooltip = """ 
    QLabel {{		
        background-color: {_dark_one};	
        color: {_text_foreground};
        padding-left: 5px;
        padding-right: 5px;
        border-radius: 10px;
        border: 0px solid transparent;
        font: 800 9pt "Segoe UI";
    }}
    """
    def __init__(
        self,
        parent, 
        tooltip,
        dark_one,
        text_foreground
    ):
        QLabel.__init__(self)
        style = self.style_tooltip.format(
            _dark_one = dark_one,
            _text_foreground = text_foreground
        )
        self.setObjectName(u"label_tooltip")
        self.setStyleSheet(style)
        self.setMinimumHeight(20)
        self.setParent(parent)
        self.setText(tooltip)
        self.adjustSize()
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)

class Rectangle:
    def __init__(self):
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.mid = None

    def update_coordinates(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.mid = [(self.p1.x() + self.p3.x()) / 2, (self.p1.y() + self.p3.y()) / 2]

class DrawingWidget(QWidget):
    def __init__(self, background=None):
        super().__init__()
        self.dragging = False
        self.background = background
        self.rectangle = Rectangle()
        self.drawing = False
        self.rectangle = Rectangle()
        
        self.x_input = PyLineEdit(
            text = "",
            place_holder_text = "Place holder text",
            radius = 8,
            border_size = 2,
            color = '#8a95aa',
            selection_color = '#f5f6f9',
            bg_color = '#1b1e23',
            bg_color_active = '#21252d',
            context_color = '#568af2'
        )
        self.x_input.setMinimumHeight(30)
        
        self.y_input = PyLineEdit(
            place_holder_text = "Place holder text",
            radius = 8,
            border_size = 2,
            color = '#8a95aa',
            selection_color = '#f5f6f9',
            bg_color = '#1b1e23',
            bg_color_active = '#21252d',
            context_color = '#568af2'
        )
        self.y_input.setMinimumHeight(30)
        
        self.a_input = PyLineEdit(
            place_holder_text = "Place holder text",
            radius = 8,
            border_size = 2,
            color = '#8a95aa',
            selection_color = '#f5f6f9',
            bg_color = '#1b1e23',
            bg_color_active = '#21252d',
            context_color = '#568af2'
        )
        self.a_input.setMinimumHeight(30)
        
        self.scale_input_x = PyLineEdit(
            place_holder_text = "Place holder text",
            radius = 8,
            border_size = 2,
            color = '#8a95aa',
            selection_color = '#f5f6f9',
            bg_color = '#1b1e23',
            bg_color_active = '#21252d',
            context_color = '#568af2'
        )
        self.scale_input_x.setMinimumHeight(30)
        
        self.scale_input_y = PyLineEdit(
            place_holder_text = "Place holder text",
            radius = 8,
            border_size = 2,
            color = '#8a95aa',
            selection_color = '#f5f6f9',
            bg_color = '#1b1e23',
            bg_color_active = '#21252d',
            context_color = '#568af2'
        )
        self.scale_input_y.setMinimumHeight(30)
        
        self.start_button_translation = PyIconButton(
            icon_path = set_svg_icon("icon_heart.svg"),
            parent = self,
            app_parent = self,
            tooltip_text = "Start",
            width = 40,
            height = 40,
            radius = 20,
            dark_one = '#1b1e23',
            icon_color = '#c3ccdf',
            icon_color_hover = '#dce1ec',
            icon_color_pressed = '#f5f6f9',
            icon_color_active = '#f5f6f9',
            bg_color = '#1b1e23',
            bg_color_hover = '#21252d',
            bg_color_pressed = '#ff007f'
        )
        
        self.start_button_rotation = PyIconButton(
            icon_path = set_svg_icon("icon_heart.svg"),
            parent = self,
            app_parent = self,
            tooltip_text = "Start",
            width = 40,
            height = 40,
            radius = 20,
            dark_one = '#1b1e23',
            icon_color = '#c3ccdf',
            icon_color_hover = '#dce1ec',
            icon_color_pressed = '#f5f6f9',
            icon_color_active = '#f5f6f9',
            bg_color = '#1b1e23',
            bg_color_hover = '#21252d',
            bg_color_pressed = '#ff007f'
        )
        self.start_button_scaling = PyIconButton(
            icon_path = set_svg_icon("icon_heart.svg"),
            parent = self,
            app_parent = self,
            tooltip_text = "Start",
            width = 40,
            height = 40,
            radius = 20,
            dark_one = '#1b1e23',
            icon_color = '#c3ccdf',
            icon_color_hover = '#dce1ec',
            icon_color_pressed = '#f5f6f9',
            icon_color_active = '#f5f6f9',
            bg_color = '#1b1e23',
            bg_color_hover = '#21252d',
            bg_color_pressed = '#ff007f'
        )
        
        self.start_button_translation.clicked.connect(self.start_translation)
        self.start_button_rotation.clicked.connect(self.start_rotation)
        self.start_button_scaling.clicked.connect(self.scale)

    def set_input_fields(self, x_input, y_input, a_input, scale_input_x, scale_input_y):
        self.x_input = x_input
        self.y_input = y_input
        self.a_input = a_input
        self.scale_input_x = scale_input_x
        self.scale_input_y = scale_input_y

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.rectangle.update_coordinates(event.position(), event.position(), event.position(), event.position())

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.rectangle.update_coordinates(
                self.rectangle.p1,
                QPoint(self.rectangle.p2.x(), event.position().y()),
                event.pos(),
                QPoint(event.position().x(), self.rectangle.p4.y())
            )
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.rectangle.update_coordinates(
                self.rectangle.p1,
                QPoint(self.rectangle.p2.x(), event.position().y()),
                event.pos(),
                QPoint(event.position().x(), self.rectangle.p4.y())
            )
            self.drawing = False
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.background is not None:
            qimage = QImage(self.background.data, self.background.shape[1], self.background.shape[0], QImage.Format_RGB888)
            painter.drawImage(0, 0, qimage)
        painter.setRenderHint(QPainter.Antialiasing)
        bg_color = Qt.blue
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(Qt.blue, 2))
        if self.rectangle.p1 and self.rectangle.p2 and self.rectangle.p3 and self.rectangle.p4:
            points = [self.rectangle.p1, self.rectangle.p2, self.rectangle.p3, self.rectangle.p4]
            painter.drawPolygon(points)
        painter.end()
    
    def create_white_bg(self):
        blank = np.ones((750, 750, 3), dtype="uint8") * 255
        return blank

    def start_translation(self):
        if self.x_input is not None and self.y_input is not None:
            x = int(self.x_input.text())
            y = int(self.y_input.text())
            self.translate(x, y)
            self.update()

    def translate(self, x, y):
        if self.rectangle.p1 and self.rectangle.p3:
            new_p1 = QPoint(self.rectangle.p1.x() + x, self.rectangle.p1.y() + y)
            new_p2 = QPoint(self.rectangle.p2.x() + x, self.rectangle.p2.y() + y)
            new_p3 = QPoint(self.rectangle.p3.x() + x, self.rectangle.p3.y() + y)
            new_p4 = QPoint(self.rectangle.p4.x() + x, self.rectangle.p4.y() + y)
            self.rectangle.update_coordinates(new_p1, new_p2, new_p3, new_p4)
    
    def start_rotation(self):
        if self.a_input is not None:
            angle = int(self.a_input.text())
            self.rotate(angle)
            self.update()
            
    def rotate(self, angle):
        if self.rectangle.mid:
            center = self.rectangle.mid
            rotation = QTransform().translate(center[0], center[1]).rotate(angle).translate(-center[0], -center[1])
            new_p1 = rotation.map(self.rectangle.p1)
            new_p2 = rotation.map(self.rectangle.p2)
            new_p3 = rotation.map(self.rectangle.p3)
            new_p4 = rotation.map(self.rectangle.p4)
            self.rectangle.update_coordinates(new_p1, new_p2, new_p3, new_p4)
            self.update()
    
    def scale(self):
        sx = float(self.scale_input_x.text())
        sy = float(self.scale_input_y.text())
        if sx!=0 and sy != 0 and self.rectangle.p1 and self.rectangle.p3:
            center = self.rectangle.mid
            scaling = QTransform().translate(center[0], center[1]).scale(sx, sy).translate(-center[0], -center[1])
            new_p1 = scaling.map(self.rectangle.p1)
            new_p2 = scaling.map(self.rectangle.p2)
            new_p3 = scaling.map(self.rectangle.p3)
            new_p4 = scaling.map(self.rectangle.p4)
            self.rectangle.update_coordinates(new_p1, new_p2, new_p3, new_p4)
            self.update()
