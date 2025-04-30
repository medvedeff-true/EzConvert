import os
from functools import partial
from PIL import Image
import pillow_heif
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QComboBox, QSlider, QCheckBox, QFileDialog,
    QProgressBar, QGridLayout, QHBoxLayout, QVBoxLayout,
    QSizePolicy, QStyle
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import (
    Qt, QEvent, QPoint, QSize, QTimer
)

# Enable HEIF/HEIC support (decoder + encoder)
pillow_heif.register_heif_opener()

# Supported output formats including HEIC
SUPPORTED_FORMATS = {
    "JPEG": "jpg", "PNG": "png", "BMP": "bmp", "TIFF": "tiff",
    "WEBP": "webp", "ICO": "ico", "GIF": "gif", "TGA": "tga",
    # Для HEIC будет использоваться формат Pillow "HEIF" при сохранении
    "HEIC": "heic"
}

# Formats that support lossless compression
LOSSLESS_SUPPORTED = {"PNG", "TIFF", "WEBP"}

# UI translations
translations = {
    'en': {
        'app_title': "EzConvert — Image Converter",
        'settings_title': "Settings",
        'clear': "🗑 Clear",
        'select_images': "📁 Select Images",
        'select_folder': "📂 Output Folder",
        'format': "Format:",
        'quality': "Quality:",
        'lossless': "Lossless Compression",
        'settings': "🌐 Choose Language",
        'convert': "💾 Convert",
        'choose_language': "Choose language:"
    },
    'ru': {
        'app_title': "EzConvert — Конвертер изображений",
        'settings_title': "Настройки",
        'clear': "🗑 Очистить",
        'select_images': "📁 Выбрать изображения",
        'select_folder': "📂 Папка для сохранения",
        'format': "Формат:",
        'quality': "Качество:",
        'lossless': "Сжатие без потерь",
        'settings': "🌐 Выбрать язык",
        'convert': "💾 Конвертировать",
        'choose_language': "Выберите язык:"
    },
    'de': {
        'app_title': "EzConvert — Bildkonverter",
        'settings_title': "Einstellungen",
        'clear': "🗑 Löschen",
        'select_images': "📁 Bilder auswählen",
        'select_folder': "📂 Ausgabeordner",
        'format': "Format:",
        'quality': "Qualität:",
        'lossless': "Verlustfreie Kompression",
        'settings': "🌐 Sprache wählen",
        'convert': "💾 Konvertieren",
        'choose_language': "Sprache auswählen:"
    },
    'zh': {
        'app_title': "EzConvert — 图像转换器",
        'settings_title': "设置",
        'clear': "🗑 清除",
        'select_images': "📁 选择图像",
        'select_folder': "📂 输出文件夹",
        'format': "格式：",
        'quality': "质量：",
        'lossless': "无损压缩",
        'settings': "🌐 选择语言",
        'convert': "💾 转换",
        'choose_language': "选择语言："
    },
    'ja': {
        'app_title': "EzConvert — 画像コンバーター",
        'settings_title': "設定",
        'clear': "🗑 クリア",
        'select_images': "📁 画像を選択",
        'select_folder': "📂 出力フォルダ",
        'format': "フォーマット：",
        'quality': "品質：",
        'lossless': "ロスレス圧縮",
        'settings': "🌐 言語を選択",
        'convert': "💾 変換",
        'choose_language': "言語を選択："
    },
    'ko': {
        'app_title': "EzConvert — 이미지 변환기",
        'settings_title': "설정",
        'clear': "🗑 지우기",
        'select_images': "📁 이미지 선택",
        'select_folder': "📂 출력 폴더",
        'format': "형식:",
        'quality': "품질:",
        'lossless': "무손실 압축",
        'settings': "🌐 언어 선택",
        'convert': "💾 변환",
        'choose_language': "언어 선택:"
    },
    'ar': {
        'app_title': "EzConvert — محول الصور",
        'settings_title': "الإعدادات",
        'clear': "🗑 مسح",
        'select_images': "📁 اختيار الصور",
        'select_folder': "📂 مجلد الإخراج",
        'format': "الصيغة:",
        'quality': "الجودة:",
        'lossless': "ضغط بدون فقد",
        'settings': "🌐 اختر اللغة",
        'convert': "💾 تحويل",
        'choose_language': "اختر اللغة:"
    },
    'fr': {
        'app_title': "EzConvert — Convertisseur d'images",
        'settings_title': "Paramètres",
        'clear': "🗑 Effacer",
        'select_images': "📁 Sélectionner des images",
        'select_folder': "📂 Dossier de sortie",
        'format': "Format :",
        'quality': "Qualité :",
        'lossless': "Compression sans perte",
        'settings': "🌐 Choisir la langue",
        'convert': "💾 Convertir",
        'choose_language': "Choisissez la langue :"
    },
    'pt': {
        'app_title': "EzConvert — Conversor de Imagens",
        'settings_title': "Configurações",
        'clear': "🗑 Limpar",
        'select_images': "📁 Selecionar Imagens",
        'select_folder': "📂 Pasta de Saída",
        'format': "Formato:",
        'quality': "Qualidade:",
        'lossless': "Compressão sem Perda",
        'settings': "🌐 Escolher idioma",
        'convert': "💾 Converter",
        'choose_language': "Escolha o idioma:"
    },
    'kk': {
        'app_title': "EzConvert — Сурет түрлендіргіш",
        'settings_title': "Баптаулар",
        'clear': "🗑 Тазалау",
        'select_images': "📁 Суреттерді таңдау",
        'select_folder': "📂 Шығыс қалтасы",
        'format': "Формат:",
        'quality': "Сапа:",
        'lossless': "Сапасыз сығымдау",
        'settings': "🌐 Тілді таңдау",
        'convert': "💾 Түрлендіру",
        'choose_language': "Тілді таңдаңыз:"
    },
    'be': {
        'app_title': "EzConvert — Канвертар выяв",
        'settings_title': "Налады",
        'clear': "🗑 Ачысціць",
        'select_images': "📁 Выбраць выявы",
        'select_folder': "📂 Папка вываду",
        'format': "Фармат:",
        'quality': "Якасць:",
        'lossless': "Без страт",
        'settings': "🌐 Выбраць мову",
        'convert': "💾 Канвертаваць",
        'choose_language': "Выберыце мову:"
    }
}

def format_bytes(size):
    for unit in ['B','KB','MB','GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

class SettingsWindow(QWidget):
    def __init__(self, main_window, initial=False):
        super().__init__()
        self.main_window = main_window
        self.initial = initial
        lang = main_window.current_language

        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowSystemMenuHint |
            Qt.WindowType.WindowCloseButtonHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        title = "EzConvert" if self.initial else translations[lang]['settings_title']
        self.setWindowTitle(title)
        self.setFixedSize(500, 140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10,10,10,10)
        layout.setSpacing(8)

        self.lbl_choose = QLabel(translations[lang]['choose_language'], self)
        self.lbl_choose.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_choose.setStyleSheet("font-weight:bold; font-size:14px;")
        layout.addWidget(self.lbl_choose)

        flags_row = QHBoxLayout()
        flags_row.setSpacing(8)
        flags_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        langs = {
            'en':'English','ru':'Русский','de':'Deutsch',
            'zh':'中文','ja':'日本語','ko':'한국어',
            'ar':'العربية','fr':'Français','pt':'Português (Brasil)',
            'kk':'Қазақша','be':'Беларуская'
        }
        for code, name in langs.items():
            btn = QPushButton()
            btn.setIcon(QIcon(f"flags/{code}.png"))
            btn.setIconSize(QSize(32,32))
            btn.setFixedSize(40,40)
            btn.setToolTip(name)
            btn.clicked.connect(lambda _, c=code: self._on_lang(c))
            flags_row.addWidget(btn)
        layout.addLayout(flags_row)

        powered = QLabel("Powered by Medvedeff", self)
        powered.setAlignment(Qt.AlignmentFlag.AlignCenter)
        powered.setStyleSheet("color:#4CAF50; font-size:11px;")
        layout.addSpacing(5)
        layout.addWidget(powered)

    def _on_lang(self, code):
        self.main_window.set_language(code)
        if self.initial:
            self.close()
        self.main_window.set_language(code)
        if self.initial:
            self.close()
            return

        self.setWindowTitle(translations[code]['settings_title'])
        self.lbl_choose.setText(translations[code]['choose_language'])

class FileListContainer(QWidget):
    """Контейнер для списка файлов + кнопка очистить + DnD-оверлей."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # сам QListWidget
        self.file_list = QListWidget(self)
        self.file_list.viewport().setMouseTracking(True)

        # кнопка «Очистить»
        self.clear_btn = QPushButton(translations[parent.current_language]['clear'], self)
        self.clear_btn.setStyleSheet("""
            background-color:e09299;
            border:1px solid #ccc;
            border-radius:6px;
            padding:4px;
        """)
        self.clear_btn.setFixedSize(100,28)

        # оверлей для DnD.png
        self.overlay = QLabel(self)
        pix = QPixmap("DnD.png")
        self.overlay.setPixmap(pix)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.overlay.hide()

    def resizeEvent(self, e):
        # список
        self.file_list.setGeometry(0, 0, self.width(), self.height())
        # кнопка внизу
        y = self.height() - self.clear_btn.height() - 10
        self.clear_btn.move(10, y)
        # центрируем оверлей
        if self.overlay.pixmap():
            ow, oh = self.overlay.pixmap().width(), self.overlay.pixmap().height()
            x = (self.width() - ow) // 2
            y2 = (self.height() - oh) // 2
            self.overlay.move(x, y2)
        super().resizeEvent(e)

    def update_overlay(self):
        # показывать, когда пусто
        if self.file_list.count() == 0:
            self.overlay.show()
        else:
            self.overlay.hide()

class EzConvert(QWidget):
    def __init__(self):
        super().__init__()

        # иконка приложения
        app_icon = QIcon("icon.ico")
        self.setWindowIcon(app_icon)

        # папка с настройками
        self.settings_dir  = os.path.join(os.path.expanduser("~"), "Documents", "EzConvert")
        self.settings_file = os.path.join(self.settings_dir, "settings.txt")
        os.makedirs(self.settings_dir, exist_ok=True)

        # язык
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    lg = f.read().strip()
                self.current_language = lg if lg in translations else 'ru'
            except:
                self.current_language = 'ru'
        else:
            self.current_language = 'en'

        # список картинок
        self.images = []
        self.output_folder = ""

        # превью всплывающее
        self.preview_label = QLabel(self)
        self.preview_label.setStyleSheet("background:white; border:1px solid gray;")
        self.preview_label.hide()

        # билдим UI
        self.setup_ui()
        self.file_container.update_overlay()
        self.set_language(self.current_language, save=False)

        # при первом запуске
        if not os.path.exists(self.settings_file):
            QTimer.singleShot(0, self._show_initial_settings)

    def _show_initial_settings(self):
        w = SettingsWindow(self, initial=True)
        w.show()
        w.raise_()
        w.activateWindow()

    def setup_ui(self):
        t = translations[self.current_language]
        self.setWindowTitle(t['app_title'])
        self.setFixedSize(800,600)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QWidget { background:#333; font:13px Segoe UI; color:white; }
            QPushButton { background:#333; padding:6px 12px; border:2px solid #ccc; border-radius:8px; }
            QPushButton:hover { background:#878787; }
            QComboBox,QSlider,QListWidget { background:#333; border:2px solid #ccc; padding:4px; border-radius:6px; }
            QSlider::groove:horizontal { border:1px solid #999; height:6px; background:#ccc; border-radius:3px; }
            QSlider::handle:horizontal { background:#4CAF50; border:1px solid #5c5c5c; width:12px; margin:-4px 0; border-radius:6px; }
            QCheckBox { background:#333; border-radius:6px; padding:4px; }
            QProgressBar { border:1px solid #bbb; border-radius:8px; text-align:center; height:20px; }
            QProgressBar::chunk { background-color:#4CAF50; border-radius:8px; }
            QListWidget::item { text-align:center; }
        """)

        layout = QVBoxLayout(self)

        # контейнер списка
        self.file_container = FileListContainer(self)
        self.file_list = self.file_container.file_list
        self.file_container.clear_btn.clicked.connect(self.clear_file_list)
        layout.addWidget(self.file_container)

        # настройки конвертации
        grid = QGridLayout()
        self.select_btn = QPushButton(t['select_images']);    self.select_btn.clicked.connect(self.load_images)
        self.folder_btn = QPushButton(t['select_folder']);    self.folder_btn.clicked.connect(self.select_output_folder)
        grid.addWidget(self.select_btn, 0, 0)
        grid.addWidget(self.folder_btn, 0, 1)

        # формат
        fmt_box = QVBoxLayout()
        self.lbl_fmt = QLabel(t['format'], alignment=Qt.AlignmentFlag.AlignCenter)
        self.format_box = QComboBox(); self.format_box.addItems(SUPPORTED_FORMATS.keys())
        self.format_box.currentTextChanged.connect(self.check_lossless_support)
        fmt_box.addWidget(self.lbl_fmt); fmt_box.addWidget(self.format_box)
        grid.addLayout(fmt_box, 1, 0)

        # качество
        q_box = QVBoxLayout()
        row = QHBoxLayout()
        self.lbl_q = QLabel(t['quality'], alignment=Qt.AlignmentFlag.AlignRight)
        self.lbl_q_val = QLabel("100", alignment=Qt.AlignmentFlag.AlignLeft)
        row.addWidget(self.lbl_q); row.addWidget(self.lbl_q_val); row.addStretch()
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(1,100); self.quality_slider.setValue(100)
        self.quality_slider.valueChanged.connect(lambda v: self.lbl_q_val.setText(str(v)))
        q_box.addLayout(row); q_box.addWidget(self.quality_slider)
        grid.addLayout(q_box, 1, 1)

        # нижняя строка
        lower = QHBoxLayout()
        self.settings_btn = QPushButton(t['settings']);    self.settings_btn.clicked.connect(self.open_settings)
        self.lossless_cb  = QCheckBox(t['lossless'])
        lower.addWidget(self.settings_btn); lower.addWidget(self.lossless_cb)
        grid.addLayout(lower, 2, 0)

        self.convert_btn = QPushButton(t['convert'])
        self.convert_btn.setStyleSheet("border:2px solid #4CAF50; border-radius:8px;")
        self.convert_btn.clicked.connect(self.convert_images)
        grid.addWidget(self.convert_btn, 2, 1)

        grid.setColumnStretch(0,1); grid.setColumnStretch(1,1)
        layout.addLayout(grid)

        # прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

    def set_language(self, lang, save=True):
        self.current_language = lang
        t = translations[lang]
        self.setWindowTitle(t['app_title'])
        self.file_container.clear_btn.setText(t['clear'])
        self.select_btn.setText(t['select_images'])
        self.folder_btn.setText(t['select_folder'])
        self.lbl_fmt.setText(t['format'])
        self.lbl_q.setText(t['quality'])
        self.lossless_cb.setText(t['lossless'])
        self.settings_btn.setText(t['settings'])
        self.convert_btn.setText(t['convert'])
        # обновим окно настроек, если открыто
        if save:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                f.write(lang)

    def open_settings(self):
        w = SettingsWindow(self, initial=False)
        w.show()
        w.raise_()
        w.activateWindow()

    def check_lossless_support(self, fmt):
        self.lossless_cb.setEnabled(fmt in LOSSLESS_SUPPORTED)

    def load_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, translations[self.current_language]['select_images'], "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp *.gif *.tiff *.ico *.tga *.heic)"
        )
        if files:
            self.images.extend(files)
            self.update_file_list()

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, translations[self.current_language]['select_folder']
        )
        if folder:
            self.output_folder = folder

    def clear_file_list(self):
        self.images.clear()
        self.update_file_list()

    def remove_item(self, path):
        if path in self.images:
            self.images.remove(path)
        self.update_file_list()

    def update_file_list(self):
        self.file_list.clear()
        for p in self.images:
            size = format_bytes(os.path.getsize(p))
            name = os.path.basename(p)
            short = name if len(name) <= 30 else name[:30] + "…"
            ext = os.path.splitext(name)[1][1:].upper()

            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, p)
            w = QWidget(); w.setMouseTracking(True)
            hl = QHBoxLayout(w); hl.setContentsMargins(4,2,4,2)
            lbl = QLabel(f"{short} | {ext} | {size}", alignment=Qt.AlignmentFlag.AlignCenter)
            btn = QPushButton(); btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton))
            btn.setFixedSize(24,24); btn.setStyleSheet("border:none;")
            btn.clicked.connect(partial(self.remove_item, p))
            hl.addWidget(lbl,1); hl.addWidget(btn)
            item.setSizeHint(w.sizeHint()); self.file_list.addItem(item)
            self.file_list.setItemWidget(item, w)
            w.installEventFilter(self); lbl.installEventFilter(self); btn.installEventFilter(self)

        # обновляем DnD-оверлей
        self.file_container.update_overlay()

    def convert_images(self):
        if not self.images or not self.output_folder:
            self.select_output_folder()
            if not self.output_folder:
                return

        fmt = self.format_box.currentText()
        ext = SUPPORTED_FORMATS[fmt]
        qual = self.quality_slider.value()
        loss = self.lossless_cb.isChecked()

        self.progress_bar.setMaximum(len(self.images))
        self.progress_bar.setValue(0)

        for i, p in enumerate(self.images):
            try:
                img = Image.open(p)

                # Для JPEG/WEBP/HEIC преобразуем в RGB, если это не RGB
                if fmt in ("JPEG", "WEBP", "HEIC") and img.mode not in ("RGB",):
                    img = img.convert("RGB")
                base = os.path.splitext(os.path.basename(p))[0]
                out = os.path.join(self.output_folder, f"{base}_converted.{ext}")
                params = {}
                save_fmt = "HEIF" if fmt == "HEIC" else fmt
                if fmt in ("JPEG", "WEBP", "HEIC"):
                    if loss and fmt == "WEBP":
                        params["lossless"] = True
                    else:
                        params["quality"] = qual
                img.save(out, format=save_fmt, **params)
            except Exception as e:
                print(f"Error converting {p}: {e}")
            self.progress_bar.setValue(i+1)

        # когда закончили — показать галочку 8 секунд, потом сбросить
        self.progress_bar.setFormat("✔")
        QTimer.singleShot(8000, self.reset_progress)

    def reset_progress(self):
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setValue(0)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.MouseMove:
            # логика превью при ховере
            if source == self.file_list.viewport():
                pos = event.pos()
            else:
                gp  = source.mapToGlobal(event.pos())
                pos = self.file_list.viewport().mapFromGlobal(gp)
            item = self.file_list.itemAt(pos)
            if item:
                path = item.data(Qt.ItemDataRole.UserRole)
                if os.path.exists(path):
                    pix = QPixmap(path).scaled(200,200,Qt.AspectRatioMode.KeepAspectRatio)
                    self.preview_label.setPixmap(pix)
                    self.preview_label.adjustSize()
                    gp = self.file_list.viewport().mapToGlobal(pos)
                    lp = self.mapFromGlobal(gp)
                    self.preview_label.move(lp + QPoint(30,30))
                    self.preview_label.raise_()
                    self.preview_label.show()
                else:
                    self.preview_label.hide()
            else:
                self.preview_label.hide()
            return True

        elif event.type() == QEvent.Type.Leave:
            self.preview_label.hide()
            return True

        return super().eventFilter(source, event)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        paths = [u.toLocalFile() for u in e.mimeData().urls()]
        imgs  = [p for p in paths if os.path.isfile(p) and p.lower().endswith(
            ('.png','.jpg','.jpeg','.bmp','.webp','.gif','.tiff','.ico','.tga','.heic')
        )]
        self.images.extend(imgs)
        self.update_file_list()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # глобальная иконка
    app.setWindowIcon(QIcon("icon.ico"))
    w = EzConvert()
    w.show()
    sys.exit(app.exec())