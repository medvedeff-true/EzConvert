import os
import sys

# Установить текущую рабочую директорию в папку, где находятся ресурсы
if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
