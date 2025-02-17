from setuptools import setup, find_packages
import os

# Funzione che legge e restituisce le dipendenze
def get_requires(fname:str="requirements.txt"):
    """Restituisce la lista di dipendenze del progetto."""
    if not os.path.isfile(fname):
        raise FileNotFoundError(f"File non trovato: \'{fname}\'. Impossibile proseguire con l'installazione.")
    with open(fname, 'r') as fd: return [r.strip() for r in fd if r.strip() and not r.startswith('#')]

# Informazioni pacchetto
PACKAGE_NAME = "GraboidRFC"
PACKAGE_VERSION = "0.6"
PYTHON_VERSION = ">=3.10"

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    packages=find_packages(include=["graboidrfc", "graboidrfc.*"]),
    install_requires=get_requires(),
    entry_points={
        "console_scripts": [
            "graboidrfc=graboidrfc.main:main",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=PYTHON_VERSION,
)