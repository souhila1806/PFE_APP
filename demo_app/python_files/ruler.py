from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QRegion, QPainterPath
from PyQt5.QtCore import Qt, QRectF



class RulerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 90)
        self.score = 0.0
        self.threshold = 0.0

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            width = self.width()
            height = self.height()

            # Add some space above the ruler
            ruler_top_padding = 30
            ruler_height = height - 40 - ruler_top_padding
            padding = 40  # Adjust the amount of padding as desired

            # Calculate the adjusted width and x positions
            adjusted_width = width - 2 * padding
            adjusted_threshold_x = int(padding + adjusted_width * (self.threshold + 1) / 2)
            adjusted_score_x = int(padding + adjusted_width * (self.score + 1) / 2)

            # Draw ruler background with transparent padding
            painter.fillRect(QRectF(padding, ruler_top_padding, adjusted_width, ruler_height), QColor(220, 220, 220,0))

            # Calculate the coordinates for rounded corners
            ruler_rect = QRectF(padding, ruler_top_padding, adjusted_threshold_x - padding, ruler_height)

            # Draw red area (left side) with rounded corners
            painter.setPen(Qt.NoPen)
            painter.setBrush(Qt.red)
            painter.drawRoundedRect(ruler_rect, 10, 10)

            # Draw green area (right side) with rounded corners
            painter.setBrush(Qt.green)
            painter.drawRoundedRect(
                QRectF(adjusted_threshold_x, ruler_top_padding, adjusted_width - (adjusted_threshold_x - padding),
                       ruler_height), 10, 10)




            # Draw threshold triangle indicator
            painter.setPen(Qt.NoPen)
            painter.setBrush(Qt.gray)
            threshold_triangle = QPainterPath()
            threshold_triangle.moveTo(adjusted_threshold_x, ruler_top_padding)
            threshold_triangle.lineTo(adjusted_threshold_x - 5, ruler_top_padding - 10)
            threshold_triangle.lineTo(adjusted_threshold_x + 5, ruler_top_padding - 10)
            threshold_triangle.lineTo(adjusted_threshold_x, ruler_top_padding)
            painter.drawPath(threshold_triangle)

            # Draw score triangle indicator
            painter.setPen(Qt.NoPen)
            painter.setBrush(Qt.gray)
            score_triangle = QPainterPath()
            score_triangle.moveTo(adjusted_score_x, ruler_top_padding + ruler_height)
            score_triangle.lineTo(adjusted_score_x - 5, ruler_top_padding + ruler_height + 10)
            score_triangle.lineTo(adjusted_score_x + 5, ruler_top_padding + ruler_height + 10)
            score_triangle.lineTo(adjusted_score_x, ruler_top_padding + ruler_height)
            painter.drawPath(score_triangle)

            painter.setPen(QPen(Qt.gray, 2))
            painter.drawLine(adjusted_threshold_x, ruler_top_padding, adjusted_threshold_x, ruler_top_padding + 10)
            painter.setPen(QPen(Qt.white, 2))
            painter.drawText(int(adjusted_threshold_x - 15), ruler_top_padding - 20, f"THR")
            #painter.drawText(int(adjusted_threshold_x - 15), ruler_top_padding - 10, f"{self.threshold:.{2}f}")

            # Draw score indicator line
            painter.setPen(QPen(Qt.gray, 2))
            painter.drawLine(adjusted_score_x, ruler_top_padding + ruler_height, adjusted_score_x,
                             ruler_top_padding + ruler_height - 10)
            if self.score > self.threshold:
                painter.setPen(QPen(Qt.green, 2))
            elif self.score < self.threshold:
                painter.setPen(QPen(Qt.red, 2))
            else:
                painter.setPen(QPen(Qt.white, 2))

            painter.drawText(int(adjusted_score_x - 15), ruler_top_padding + ruler_height + 20, f"SCR")
            #painter.drawText(int(adjusted_score_x - 15), ruler_top_padding + ruler_height + 30, f"{self.score:.{2}f}")

            painter.setPen(QPen(Qt.black, 1))
            graduation_spacing = adjusted_width / 20
            for i in range(21):
                painter.setPen(Qt.white)
                x = padding + i * graduation_spacing
                value = -1 + i * 0.1
                if value != -1 and value != 1:
                    painter.drawLine(int(x), ruler_top_padding, int(x), ruler_top_padding + 10)
                if value == 0 or value == -1 or value == 1:
                    if value==0 and self.threshold==0:
                        continue
                    painter.setPen(QPen(Qt.gray, 1))
                    painter.drawText(int(x - 10), ruler_top_padding - 20, f"{value:.{2}f}")
        except Exception as e:
            import traceback
            traceback.print_exc()



    def set_values(self, score, threshold):
        self.score = score
        self.threshold = threshold
        self.update()



if __name__ == "__main__":
    app = QApplication([])
    score = 0.73
    threshold = 0.0
    window = QWidget()
    layout=QGridLayout()
    ruler = RulerWidget()
    ruler.set_values(score,threshold)
    layout.addWidget(ruler)
    window.setLayout(layout)


    window.show()
    app.exec_()
