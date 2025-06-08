from PyQt6.QtWidgets import (
    QApplication ,QWidget,QLineEdit,QLabel,QPushButton,QVBoxLayout,QTextEdit
)
from PyQt6.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanves
from matplotlib.figure import Figure
import sys
import random
import matplotlib.pyplot as plt 

class cmp_prf_suf_chart(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COMPOUND PROFIT CALCULATOR WITH CHART")

        #input && labels

        self.label_start = QLabel("Starting Money:")
        self.input_start = QLineEdit()

        self.lable_profit = QLabel("Profit Rate (%):")
        self.input_profit = QLineEdit()

        self.lable_loss = QLabel("Loss Rate (%):")
        self.input_loss = QLineEdit()

        self.lable_accuracy = QLabel("Accuracy Rate (%):")
        self.input_accuracy = QLineEdit()

        self.lable_period = QLabel("How Many Trades :")
        self.input_period = QLineEdit()

        #calc button 

        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate_result)

        #result
        self.result_lable = QLabel("Final Amount:")
        self.trade_log = QTextEdit()
        self.trade_log.setReadOnly(True)

        #chart stuff  MATPLOTLIB

        self.figure = Figure(figsize=(5,3))
        self.canvas = FigureCanves(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        
        #layout setup
        layout = QVBoxLayout()

        layout.addWidget(self.label_start)
        layout.addWidget(self.input_start)
        
        layout.addWidget(self.lable_profit)
        layout.addWidget(self.input_profit)

        layout.addWidget(self.lable_loss)
        layout.addWidget(self.input_loss)

        layout.addWidget(self.lable_accuracy)
        layout.addWidget(self.input_accuracy)

        layout.addWidget(self.lable_period)
        layout.addWidget(self.input_period)

        layout.addWidget(self.calc_button)
        layout.addWidget(self.result_lable)
        layout.addWidget(QLabel("Trade History:"))
        layout.addWidget(self.trade_log)
        layout.addWidget(QLabel("Capital Growth Chart:"))
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def calculate_result(self):
        try:
            #conert inputs
            start = float(self.input_start.text())
            profit_rate = float(self.input_profit.text()) / 100
            loss_rate = float(self.input_loss.text()) / 100
            accuracy = float(self.input_accuracy.text()) / 100
            total_trades = int(self.input_period.text())

            # outcome list 
            win_count = int(accuracy * total_trades)
            loss_count = total_trades - win_count
            outcomes = [1 + profit_rate] * win_count + [1 - loss_rate] * loss_count
            random.shuffle(outcomes)

            #calculating 

            capital = start
            capital_history = [capital]
            log = ""

            for i , factor in enumerate(outcomes,1):
                capital *=factor
                capital_history.append(capital)
                log += f"Trade {i}:{'WIN' if factor > 1 else 'LOSS'} => \t {capital:.2f}\n"

            self.result_lable.setText(f"Final Amount: {capital:.2f}")
            self.trade_log.setText(log)

            #plot capital curve
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(capital_history, color = 'blue', marker = 'o')
            ax.set_title("Capital Growth Over Trades")
            ax.set_xlabel("Trade Number")
            ax.set_ylabel("Capital")
            ax.grid(True)
            self.canvas.draw()

        except ValueError:
            self.result_lable.setText("Please enter valid numbers")
            self.trade_log.clear()
            self.figure.clear()
            self.canvas.draw()

#gui exe
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = cmp_prf_suf_chart()
    window.show()
    sys.exit(app.exec())