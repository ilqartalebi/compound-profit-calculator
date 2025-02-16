import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout

class PnLCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Trade PnL Calculator")
        self.setGeometry(100, 100, 400, 300)

        # Create UI elements
        self.label_margin = QLabel("Trade Margin:")
        self.entry_margin = QLineEdit()

        self.label_growth = QLabel("Expected Growth (%):")
        self.entry_growth = QLineEdit()

        self.label_trades = QLabel("Number of Trades:")
        self.entry_trades = QLineEdit()

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_pnl)

        self.results_box = QTextEdit()
        self.results_box.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_margin)
        layout.addWidget(self.entry_margin)
        layout.addWidget(self.label_growth)
        layout.addWidget(self.entry_growth)
        layout.addWidget(self.label_trades)
        layout.addWidget(self.entry_trades)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.results_box)

        self.setLayout(layout)

    def calculate_pnl(self):
        try:
            margin = int(self.entry_margin.text())
            growth = float(self.entry_growth.text()) / 100  # Convert % to decimal
            num_trades = int(self.entry_trades.text())

            total = 1
            self.results_box.clear()  # Clear previous results

            for x in range(1, num_trades + 1):
                pnl = margin * (total + growth) ** x
                self.results_box.append(f"Level {x}: {pnl:.03f} $")

        except ValueError:
            self.results_box.setText("Invalid input! Please enter valid numbers.")

# Run the app
app = QApplication(sys.argv)
window = PnLCalculator()
window.show()
sys.exit(app.exec())
