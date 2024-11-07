# MKVRebuilder: rebuilder docs 
 Тут описываются переменные содержащиеся в классе "ребилдера"(почему бы и нет?)
 
# Переменные из MainWindow
```bash 
    main_window: экземпляр класса главного окна,
    source_path: путь к исходному файлу,
    output_file: путь к файлу сохранения,
    track_data: словарь с метаданными звуковой дорожки,
    subtitle_data: словарь с метаданными дорожки субтитров,
    temp_path: путь к папке временных файлов,
    restricted_codec: кодеки запрещенные для конвертации,
    bitrate: битрейт
```

# Переменные методанных дорожек
```bash 
    track_id: id звуковой дорожки,
    track_name: название звуковой дорожки,
    track_lang: язык звуковой дорожки,
    track_data: словарь с метаданными звуковой дорожки,
    subtitle_id: id дорожки субтитров,
    subtitle_name: название дорожки субтитров,
    subtitle_lang: язык дорожки субтитров
```

# Переменные временной папки
```bash 
    temp_dir: словарь с путями для сохранения звуковых дорожек и субтитров,
    subtitle_temp_path_id: файл для сохранения дорожки субтитров с id, пример: 11:F:/test/temp/46002242/11.srt,
    sound_temp_path_id: : файл для сохранения звуковой дорожки с id, пример: 1:F:/test/temp/46002242/1.dts,
    extract_eac3_track_path: файл для сохранения звуковой дорожки eac3, пример: F:/test/temp/46002242/1.eac3,
    extract_ac3_track_path: файл для сохранения звуковой дорожки ac3, пример: F:/test/temp/46002242/1.ac3,
    extract_eac3_track_path: файл для сохранения звуковой дорожки dts, пример: F:/test/temp/46002242/1.dts,
    extract_srt_path: файл для сохранения дорожки субтитров, пример: F:/test/temp/46002242/1.srt,
    sound_temp_dir: не полный путь до папки сохранения звуковой дорожки, пример: F:/test/temp/46002242/,
    subtitle_temp_dir: не полный путь до папки сохранения дорожки субтитров, пример: F:/test/temp/46002242/,
    dts_path: полный путь к dts, пример: F:\test\temp\46002242\1.dts,
    ac3_path: полный путь к ac3, пример: F:\test\temp\46002242\1.ac3,
    eac3_path: полный путь к eac3, пример: F:\test\temp\46002242\1.eac3,
    subtitle_path: полный путь к srt, пример: F:\test\temp\46002242\1.srt
```

# Переменные для сторонних приложений
```bash 
    mkv_merge_path: путь до папки с mkvmerge,
    mkv_extract_path: путь до папки с mkvextract,
    ac3_converter: путь до папки с eac3to
```
