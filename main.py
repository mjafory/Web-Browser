from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create a QWebEngineView widget to display web content
        self.browser = QWebEngineView()

        # Set the initial URL to Google
        self.browser.setUrl(QUrl("http://google.com"))

        # Connect signals for URL and title updates
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

        # Set the browser widget as the central widget of the main window
        self.setCentralWidget(self.browser)

        # Create a status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Create a navigation toolbar and add it to the main window
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        # Create Home button with an action to navigate to the home page (Google)
        home_btn = QAction("⌂", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # Create Back button with an action to go back in the web history
        back_btn = QAction("◄", self)
        back_btn.setStatusTip("Back to the previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # Create Forward button with an action to go forward in the web history
        next_btn = QAction("►", self)
        next_btn.setStatusTip("Forward to the next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # Add a separator in the toolbar
        navtb.addSeparator()

        # Create a QHBoxLayout to arrange the URL input and search bars horizontally
        url_search_layout = QHBoxLayout()

        # Create a QLineEdit for entering URLs and connect it to a function
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # Set the size policy to make it medium-sized
        self.urlbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create a QLineEdit for Google searches
        self.searchbar = QLineEdit()
        self.searchbar.returnPressed.connect(self.search_google)

        # Set the size policy to make it medium-sized
        self.searchbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add both input bars to the layout
        url_search_layout.addWidget(self.urlbar)
        url_search_layout.addWidget(self.searchbar)

        # Create Refresh button with an action to refresh the current page
        self.refresh_btn = QAction("⟳", self)
        self.refresh_btn.setStatusTip("Refresh page")
        self.refresh_btn.triggered.connect(self.browser.reload)
        navtb.addAction(self.refresh_btn)

        # Create Stop button with an action to stop loading the current page
        self.stop_btn = QAction("X", self)
        self.stop_btn.setStatusTip("Stop loading the current page")
        self.stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(self.stop_btn)
        self.stop_btn.setVisible(False)  # Initially hidden

        # Connect signals for page load started and finished events
        self.browser.loadStarted.connect(self.page_load_started)
        self.browser.loadFinished.connect(self.page_load_finished)

        # Create an action for performing Google searches
        search_action = QAction("🔍", self)
        search_action.setStatusTip("Search Google")
        search_action.triggered.connect(self.search_google)
        navtb.addAction(search_action)

        # Add the layout containing the URL input and search bars to a QWidget
        url_search_widget = QWidget()
        url_search_widget.setLayout(url_search_layout)

        # Add the combined widget to the toolbar
        navtb.addWidget(url_search_widget)

        # Show the main window
        self.show()

    # Update the window title with the current page title
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - My Browser" % title)

    # Navigate to the home page (Google)
    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    # Navigate to the URL entered in the QLineEdit
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    # Update the URL bar with the current page's URL
    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # Handle the page load started event (hide refresh, show stop button)
    def page_load_started(self):
        self.refresh_btn.setVisible(False)
        self.stop_btn.setVisible(True)

    # Handle the page load finished event (show refresh, hide stop button)
    def page_load_finished(self):
        self.refresh_btn.setVisible(True)
        self.stop_btn.setVisible(False)

    # Implement the Google search functionality
    def search_google(self):
        query = self.searchbar.text()
        google_url = "https://www.google.com/search?q={}".format(query)
        self.browser.setUrl(QUrl(google_url))

# Create a QApplication
app = QApplication([])

# Set the application name
app.setApplicationName("My Browser")

# Create an instance of the MainWindow class
window = MainWindow()

# Start the application event loop
app.exec_()
