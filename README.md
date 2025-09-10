## [Русский](#русский) | [English](#english)

## Русский
# EzConvert
Если вам тоже надоело постоянно заходить на онлайн конвертеры, когда вам необходимо, например, перевести фото heic с айфона в жизнеспособный png, то EzConvert специально для вас!

***EzConvert*** - это программа, основанная на библиотеке Pillow, позволяющая конвертировать картинки между форматами: JPEG, PNG, BMP, TIFF, WEBP, ICO, GIF, TGA, HEIC

## 🎯 Основные возможности
**1.** Почти моментальная конвертация между указанными форматами. (`Скорость больших объёмов фотографий зависит от системы`).<br>
**2.** Реализован "Drag and Drop" - просто перетащи нужные фотографии на окно приложения и они откроются. (Либо выбери их через кнопку).<br>
**3.** Предпросмотр картинок - наведи мышку на любую картинку в списке выбранных тобой фотографий и увидишь её миниатюру.<br>

<img width="795" height="626" alt="image" src="https://github.com/user-attachments/assets/1528d7d6-9148-440e-afd5-08747264a328" />
<br>
<br>

**4.** Мультиязычность - при запуске программы вам будет дан выбор языка, на котором будет выполнен весь интерфейс программы.<br>

<img width="501" height="169" alt="image" src="https://github.com/user-attachments/assets/190ccd3e-1c14-4aac-b274-45dfe2b9243c" />


## 🛠️ Требования к системе
+ Windows 10/11 , Linux <br>
+ ~100 мб свободного места<br>

## 🚀 Установка
- Для Windows <br>
**1.** Скачайте приложение `EzConvert.exe` по ссылке из релиза [Скачать](https://github.com/medvedeff-true/EzConvert/releases/tag/v1.0-stable)<br>
**2.** Запустите программу.<br>

- Для Linux <br>
**1.** Скачайте исходный код `EzConvert` из репозитория [Скачать](https://github.com/medvedeff-true/EzConvert/archive/refs/heads/main.zip) <br> 
**2.** Распакуйте в удобную для вас папку все файлы из архива.<br>
**3.** Установите PyQt6 и Pillow: `pip install PyQt6` и `pip install pillow-heif`.<br>
**4.** **Если не качаются пакеты**, создайте виртуальное окружение в скачанной папке с проектом: `python3 -m venv venv` и `source venv/bin/activate`.<br>
**5.** Запустите приложение командой `python3 EzConvert.py`.


## 🤔 Сборка билда на Windows (Реализована на случай каких-либо проблем с .exe файлом)
**1.** Скачайте файлы проекта и откройте в удобном для Вас редакторе.<br>
**2.** Скомпилируйте и запустите `build.py` и дождитесь завершения процесса сборки.<br>
#### У вас должен быть установлен PyInstaller, если его нет, сначала установите его командой `pip install pyinstaller`
**3.** В папке с проектом появится папка `dist`, в которой будет EzConvert.exe<br>
**4.** Запустите программу.<br>

<br>
<br>
<br>
<br>

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<br>
<br>
<br>
<br>

## English
# EzConvert
If you are tired of constantly visiting online converters when you need to convert, for example, a HEIC photo from your iPhone to a viable PNG, then EzConvert is for you!

***EzConvert*** is a program based on the Pillow library that allows you to convert images between formats: JPEG, PNG, BMP, TIFF, WEBP, ICO, GIF, TGA, HEIC

## 🎯 Key features
**1.** Almost instant conversion between the specified formats. (`The speed for large volumes of photos depends on the system`).<br>
**2.** Drag and drop functionality - simply drag the desired photos to the application window and they will open. (Or select them using the button).<br>
**3.** Image preview - hover your mouse over any image in the list of photos you have selected to see a thumbnail. <br>

<img width="802" height="639" alt="image" src="https://github.com/user-attachments/assets/b2109e6b-7b55-4ec7-a780-228afc2f64a0" />
<br>
<br>

**4.** Multi language - when you start the program, you will be given a choice of languages for the entire program interface.<br>

<img width="498" height="176" alt="image" src="https://github.com/user-attachments/assets/f0fbb087-9d47-4976-9843-e68a2b588a53" />


## 🛠️ System requirements
+ Windows 10/11, Linux
+ ~100 MB of free space

## 🚀 Installation
- For Windows <br>
**1.** Download the `EzConvert.exe` application from the release link [Download](https://github.com/medvedeff-true/EzConvert/releases/tag/v1.0-stable)<br>
**2.** Run the program.<br>

- For Linux <br>
**1.** Download the `EzConvert` source code from the repository [Download](https://github.com/medvedeff-true/EzConvert/archive/refs/heads/main.zip)<br>
**2.** Extract all files from the archive to a convenient folder.
**3.** Install PyQt6 and Pillow: `pip install PyQt6` and `pip install pillow-heif`.
**4.** **If the packages are not downloaded**, create a virtual environment in the downloaded folder with the project: `python3 -m venv venv` and `source venv/bin/activate`.<br>
**5.** Run the application with the command `python3 EzConvert.py`.


## 🤔 Building on Windows (Implemented in case of any problems with the .exe file)
**1.** Download the project files and open them in your preferred editor.<br>
**2.** Compile and run `build.py` and wait for the build process to complete.<br>
#### You must have PyInstaller installed. If you don't have it, install it first with the command `pip install pyinstaller`
**3.** A `dist` folder will appear in the project folder, containing EzConvert.exe<br>
**4.** Run the program.<br>
