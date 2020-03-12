from PyQt5.QtWidgets import *

app = QApplication([])
layout = QVBoxLayout()
label = QLabel('Hello World!')
button = QPushButton('this')


def generator(layouter):  # type: (QVBoxLayout) -> function
    def on_button_clicked():
        newLabel = QLabel('hi world')
        # layouter.replaceWidget()
        widget_to_replace = layouter.itemAt(0).widget()
        print(widget_to_replace)
        widget_to_replace.close()
        layouter.replaceWidget(widget_to_replace, newLabel)


    return on_button_clicked


button.clicked.connect(generator(layout))
layout.addWidget(label)
layout.addWidget(button)
# print(layout.widget())
window = QWidget()
window.setLayout(layout)
window.show()
app.exec()
