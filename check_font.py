from PySide6.QtGui import QFontDatabase, QGuiApplication
import sys
import os

app = QGuiApplication(sys.argv)
db = QFontDatabase()
font_path = os.path.join(os.getcwd(), "fonts/Tangerine-Regular.ttf")
id = db.addApplicationFont(font_path)
if id != -1:
    families = db.applicationFontFamilies(id)
    print(f"Loaded families: {families}")
else:
    print("Failed to load font")
