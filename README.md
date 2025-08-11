# BackUpScript

## Описание (Description)

**BackUpScript** — простой набор скриптов для бэкапа файлов на Яндекс.Диск через WebDAV с использованием логина и пароля приложения.

BackUpScript is a simple set of scripts for backing up files to Yandex.Disk via WebDAV using login and application password.

---

## Возможности (Features)

- Загрузка файлов на Яндекс.Диск в указанную папку  
- Восстановление файлов из Яндекс.Диска  
- Удаление файлов с Яндекс.Диска  
- Создание папок на Яндекс.Диске с рекурсивной проверкой и созданием родителей  
- Работа с WebDAV по логину и паролю приложения (без OAuth)

Upload files to Yandex.Disk into a specified folder  
Restore files from Yandex.Disk  
Delete files from Yandex.Disk  
Create directories on Yandex.Disk with recursive parent folder creation  
Works with WebDAV using login and application password (no OAuth)



## Установка (Installation)

```bash
pip install git+https://github.com/ivanzuev78/BackUpScript.git
```

```python
from backup_scripts import YandexDiskBackup

backup = YandexDiskBackup("your_login", "your_app_password", backup_folder="my_backups")

# Бэкапим файл
backup.backup("local_file.txt", "2025/08")

# Восстанавливаем файл
backup.restore("my_backups/2025/08/local_file.txt", "restored")
```

## Инициализация
```
backuper = YandexDiskBackup(login, app_password, backup_folder="backup")
```
login и app_password — учетные данные для доступа к WebDAV Яндекс.Диска.

backup_folder — корневая папка на Яндекс.Диске, в которой будут храниться все бэкапы.
Если не указана, используется "backup".


## Создание бэкапа 

`backuper.backup(local_path, remote_path='')`

Описание: Загружает локальный файл на Яндекс.Диск.

Имя файла: берётся автоматически из local_path (только имя файла).

Формирование пути на Яндекс.Диске:

Итоговый путь строится как:

backup_folder / remote_path / filename
Пример:

```
backup_folder = "my_backups"
remote_path = "2025/08"
local_path = "/home/user/docs/report.pdf"
```
Тогда файл загрузится по пути:

```
my_backups/2025/08/report.pdf
```
Перед загрузкой создаётся папка my_backups/2025/08, если её ещё нет.

## Загрузка бэкапа

`backuper.restore(remote_path, local_path='.')`

Описание: Скачивает файл с Яндекс.Диска и сохраняет локально.

Имя файла: берётся из имени файла в конце remote_path.

Формирование полного пути на Яндекс.Диске:

Если в конструкторе указан backup_folder, он добавляется в начало пути:
```
backup_folder / remote_path
```
Локальный путь:

Файл сохраняется в папку local_path (по умолчанию текущая директория) с тем же именем файла.

Пример:
```
backup_folder = "my_backups"
remote_path = "2025/08/report.pdf"
local_path = "./restored_files"
```

Файл будет скачан с пути:
```
my_backups/2025/08/report.pdf
```

И сохранён локально как:
```
./restored_files/report.pdf
```
