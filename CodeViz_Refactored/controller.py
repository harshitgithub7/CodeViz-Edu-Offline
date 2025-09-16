import time

class AppController:
    """
    Central controller to manage shared app state.
    """
    def __init__(self):
        self.current_screen = "Home"
        self.last_viewed = "Home"
        self.db_path = "db/content.db"
        self.examples_path = "db/examples.json"  # You can change it later if moved
        self.study_minutes = 0  # Can be used later
        self.theme = "Dark"

    def set_screen(self, name: str):
        self.last_viewed = self.current_screen
        self.current_screen = name

    def toggle_theme(self):
        self.theme = "Light" if self.theme == "Dark" else "Dark"

class AppController:
    def __init__(self):
        self.session_start = time.time()
        self.last_tab = "Home"

    def get_session_duration_minutes(self):
        return int((time.time() - self.session_start) / 60)

    def save_session_data(self, tab_name):
        self.last_tab = tab_name

