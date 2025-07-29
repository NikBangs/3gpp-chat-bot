# src/ui/run_graph_gui.py

import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox, QStyleFactory
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon


class GraphWindow(QMainWindow):
    def __init__(self, html_path):
        super().__init__()

        self.setWindowTitle("📊 3GPP Chat Bot - Semantic Graph Viewer")
        self.setGeometry(100, 100, 1280, 860)
        self.setStyle(QStyleFactory.create("Fusion"))  # Apply dark fusion style

        # Optional: set app icon
        icon_path = Path(__file__).parent / "icon.png"  # Add your custom icon here
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Create WebView and load HTML
        self.web_view = QWebEngineView()
        abs_path = Path(html_path).resolve()

        if not abs_path.exists():
            QMessageBox.critical(self, "File Not Found", f"graph.html was not found at:\n{abs_path}")
            sys.exit(1)

        self.web_view.load(QUrl.fromLocalFile(str(abs_path)))

        # Layout setup
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.web_view)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Look for graph.html in project root
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    html_file = project_root / "data" / "graph.html"

    if not html_file.exists():
        QMessageBox.critical(None, "graph.html Missing", f"File not found at:\n{html_file}")
        sys.exit(1)

    print(f"✅ Found graph.html at: {html_file}")

    window = GraphWindow(html_file)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
