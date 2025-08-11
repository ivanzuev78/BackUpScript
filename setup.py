from setuptools import setup, find_packages

setup(
    name="backup_scripts",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.0",
    ],
    author="Твоё имя",
    description="Набор скриптов для бэкапа в Яндекс через WebDav",
    url="https://github.com/ivanzuev78/BackUpScript",  # ссылка на репо
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
