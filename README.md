# MKVRebuilder
 Приложение предназначено для конвертации звуковых дорожек в формате DTS в формат AC3.
 
 # Для чего и главное зачем
 1. Для экономии места за счет вырезания всех звуковых дорожек и субтитров кроме нужных.
 2. Для конвертации DTS дорожек в AC3.

# Функции

1. Сохранение нужной звуковой дорожки и конвертация ее в AC3 с последующей записью в новый mkv файл.
2. Сохранение нужной звуковой дорожки и субтитров и конвертация ее в AC3 с последующей записью в новый mkv файл.
3. Сохранение нужной звуковой дорожки и субтитров без конвертации(если дорожка уже AC3) с последующей записью в новый mkv файл. 


# Этапы запуска

1. Выбор исходного файла(Файл из которого будут вырезаться дорожки и субтитры).
2. Выбор директории куда будет сохраняться новый mkv файл(Название автоматически формируется из исходного файла).
3. Выбор директории для сохранение временных файлов(Можно выбрать всего 1 раз, изменить директорию можно через приложение или конфиг).
4. Выбрать из списка звуковых дорожек нужную.
5. Нажать на кнопку "Обновить субтитры" если нужно сохранить дорожку субтитров(Без нее вырезаются все субтитры).
6. Нажать на "Настройки ac3".
7. Если формат звуковой дорожки AC3 то нажать на кнопку в появившимся окне.
8. Если формат звуковой дорожки не AC3 то выбрать битрейт для конвертации и нажать на кнопку.
9. Дождаться конвертации.

# Установка приложения(Для разработчиков)

1. Установим менеджер пакетов Poetry.
```bash 
pip install poetry
```
2. Установим необходимые библиотеки.
```bash 
poetry install
```
3. Запуск приложения.
```bash 
python main.py
```

# Принцип работы(Для разработчиков)
Общие принципы работы приложения(не код)

1. Информация о звуковых дорожках и субтитров формируются из json с помощью mkvmerge(ниже расположение mkvmerge).
```bash 
path: static/mkv_tools/mkvmerge.exe
```
2. На основе json формируется список звуковых дорожек и выводится пользователю(ниже пример словаря информации о звуковой дорожке).
```bash 
dict example: {"id": 2, "codec": "AC-3", "name": "Dub, Blu-Ray", "lang": "rus"}
```
3. Если пользователь нажимает на "обновить субтитры" то формируется список субтитров и выводится пользователю(ниже пример словаря информации о дорожке субтитров).
```bash 
dict example: {"id": 15, "name": "Forced", "lang": "rus"}
```
4. После выбора дорожки(и субтитров если выбраны), происходит проверка кодека, и если дорожка не формата AC3, пользователь может выбрать битрейт для конвертации(ниже варианты значений битрейта).
```bash 
bitrate variables: 192, 256, 384, 448, 640
```
4.1. Если дорожка имеет формат AC3 то выбор битрейта блокируется и пользователь может нажать только на кнопку сборки.
```bash 
bitrate variables: 192, 256, 384, 448, 640
```
5. После нажатия на кнопку сборки создается временная папка и в отдельном потоке запускается mkvextract(Ниже расположение mkvextract).
```bash 
path: static/mkv_tools/mkvextract.exe
```
6. После завершения извлечения звуковой дорожки в отдельном потоке извлекается дорожка субтитров(если была выбрана).

7. После извлечения звуковой дорожки отдельном потоке запускается ее конвертация в AC3 с помощью eac3to(Ниже расположение eac3to).
```bash 
path: static/eac3/eac3to.exe
```
7.1 Если кодек файла AC3 то конвертация пропускается.

8. После конвертации или извлечения дорожки(зависит от изначального кодека) в отдельном потоке запускается сборка нового mkv файла с нужной дорожкой и субтитрами(все другие дорожки и субтитры вырезаются). 

# Планируемые изменения


1. Добавление возможности выбора сразу нескольких звуковых дорожек и субтитров.
2. Изменение окна настройки ac3.


# Известные проблемы


1. Не корректно работает выделение выбраной звуковой дорожки.

2. Нельзя закрыть обычным способом окно с этапами сборки.

3. Не собирается информация о файлах с пробелами в названиях

