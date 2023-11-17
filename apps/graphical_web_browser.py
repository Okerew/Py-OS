import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo
from PyQt6.QtWebEngineCore import QWebEnginePage

class AdBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self, ad_domains):
        super().__init__()
        self.ad_domains = ad_domains

    def interceptRequest(self, info: QWebEngineUrlRequestInfo):
        url = info.requestUrl().toString()
        for ad_domain in self.ad_domains:
            if ad_domain in url:
                info.block(True)
                return

class Widgets(QMainWindow):
    def __init__(self):
        super().__init__()
        ad_domains = self.import_domains("ad_domains.txt")
        self.page = QWebEnginePage()
        self.page.setUrlRequestInterceptor(AdBlocker(ad_domains))
        # Set the page for the webview
        self.webview = QWebEngineView()
        self.webview.setPage(self.page)
        # Load default URL
        self.webview.load(QUrl("https://sipeq--okerew.repl.co/"))
        layout = QVBoxLayout()
        self.toplayout = QHBoxLayout()
        self.back_button = QPushButton("<")
        self.forward_button = QPushButton(">")
        self.refresh_button = QPushButton("Refresh")
        self.url_text = QLineEdit()
        self.go_button = QPushButton("Go")
        self.home_button = QPushButton("Home")
        self.back_button.clicked.connect(self.webview.back)
        self.forward_button.clicked.connect(self.webview.forward)
        self.refresh_button.clicked.connect(self.webview.reload)
        self.go_button.clicked.connect(self.url_set)
        self.home_button.clicked.connect(self.go_home)
        self.toplayout.addWidget(self.back_button)
        self.toplayout.addWidget(self.forward_button)
        self.toplayout.addWidget(self.refresh_button)
        self.toplayout.addWidget(self.url_text)
        self.toplayout.addWidget(self.go_button)
        self.toplayout.addWidget(self.home_button)
        layout.addLayout(self.toplayout)
        layout.addWidget(self.webview)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def import_domains(self, file_path):
        """Import domains from a file"""
        try:
            with open(file_path, "r") as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            QMessageBox.warning(self, "File Not Found", "Ad domains file not found. Using an empty list for ad domains.")
            return []

    def url_set(self):
        """Load the new URL"""
        self.webview.setUrl(QUrl(self.url_text.text()))

    def go_home(self):
        """Load the default home page"""
        default_homepage = "https://sipeq--okerew.repl.co/"  # Change this to your desired home page
        self.webview.load(QUrl(default_homepage))
        self.url_text.setText(default_homepage)

def main():
    app = QApplication(sys.argv)
    window = Widgets()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
