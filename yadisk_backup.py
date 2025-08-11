import requests
import os


class YandexDiskBackup:
    def __init__(self, login: str, app_password: str, backup_folder: str = "backup",
                 base_url: str = "https://webdav.yandex.ru"):
        self.login = login
        self.password = app_password
        self.base_url = base_url
        self.backup_folder = backup_folder

    def backup(self, local_path: str, remote_path: str = ''):
        if not os.path.isfile(local_path):
            raise FileNotFoundError(local_path)

        filename = os.path.basename(local_path)

        parts = []
        if self.backup_folder:
            parts.append(self.backup_folder)
        if remote_path:
            parts.append(remote_path.strip("/"))
        remote_dir = "/".join(parts)

        if remote_dir:
            self.ensure_dir(remote_dir)

        remote_file_path = f"{remote_dir}/{filename}" if remote_dir else filename

        with open(local_path, "rb") as f:
            r = requests.put(
                f"{self.base_url}/{remote_file_path}",
                data=f,
                auth=(self.login, self.password)
            )

        if r.status_code not in (200, 201, 204):
            raise Exception(f"Ошибка загрузки: {r.status_code} {r.text}")

        print(f"[+] Файл {local_path} загружен в {remote_file_path}")

    def restore(self, remote_path: str, local_path: str = '.'):
        """
        Скачивает файл с Яндекс.Диска по полному пути remote_path (относительному к backup_folder),
        сохраняет в папку local_path с тем же именем.
        """
        parts = []
        if self.backup_folder:
            parts.append(self.backup_folder)
        if remote_path:
            parts.append(remote_path.strip("/"))
        full_remote_path = "/".join(parts)

        filename = os.path.basename(full_remote_path)
        local_folder = local_path or "."
        local_folder = os.path.abspath(local_folder)
        os.makedirs(local_folder, exist_ok=True)

        r = requests.get(
            f"{self.base_url}/{full_remote_path}",
            auth=(self.login, self.password)
        )

        if r.status_code != 200:
            raise FileNotFoundError(f"Файл {full_remote_path} не найден на Яндекс.Диске ({r.status_code})")

        local_file = os.path.join(local_folder, filename)
        with open(local_file, "wb") as f:
            f.write(r.content)

        print(f"[+] Файл {full_remote_path} сохранён как {local_file}")

    def ensure_dir(self, remote_dir: str):
        """
        Убеждается, что папка remote_dir существует на Яндекс.Диске,
        если нет — создаёт её, рекурсивно создавая отсутствующих родителей.
        """
        remote_dir = remote_dir.strip("/")

        if not remote_dir:
            return

        url = f"{self.base_url}/{remote_dir}"

        r = requests.request("MKCOL", url, auth=(self.login, self.password))

        if r.status_code == 201:
            print(f"[+] Папка {remote_dir} создана")
        elif r.status_code == 405:
            # 405 Method Not Allowed — папка уже есть
            print(f"[i] Папка {remote_dir} уже существует")
        elif r.status_code == 409:
            # 409 Conflict — родительская папка отсутствует
            parent = "/".join(remote_dir.split("/")[:-1])
            if parent:
                self.ensure_dir(parent)  # рекурсивно создаём родителя
            # После создания родителей пробуем ещё раз создать текущую папку
            self.ensure_dir(remote_dir)
        else:
            raise Exception(f"Ошибка создания папки {remote_dir}: {r.status_code} {r.text}")
