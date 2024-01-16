from enum import Enum
import json
from pydantic import BaseModel
from typing import List


class Faktor(str, Enum):
    core = "Core"
    secondary = "Secondary"


class Variabel(BaseModel):
    nama: str
    faktor: Faktor
    persentase: int


class SubVariabel(BaseModel):
    kode: str
    nama: str
    faktor: Faktor
    standar: int


class Pegawai(BaseModel):
    nama: str


class Skor(BaseModel):
    pegawai: Pegawai
    variabel: Variabel
    skor: int


def read_variabel(file_path) -> List[Variabel]:
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []
    
    parsed_existing_data = [Variabel(**data) for data in existing_data]
    return parsed_existing_data


def store_variabel(file_path: str, json_data: List[Variabel]):
    json_data_str = json.dumps([var.dict() for var in json_data], indent=4)
    with open(file_path, 'w') as json_file:
        json_file.write(json_data_str)


def search_variabel(existing_data: List[Variabel], nama: str) -> Variabel:
    for data in existing_data:
        if data.nama == nama:
            return data


VARIABEL_PATH = 'variabel.json'


def menu():
    print("====== RECOMMENDER TRUK ======")
    print("1. Variabel")
    print("2. Sub Variabel")
    print("3. Pegawai")
    print("4. Mapping Data Pegawai")
    print("5. Hasil")
    chosen = int(input("Pilih salah satu dengan angka:"))
    if chosen == 1:
        chosen_menu = menu_variabel()
        if chosen_menu == 1:
            new_data = create_variabel()

            existing_data = read_variabel(VARIABEL_PATH)
            existing_data.append(new_data)

            store_variabel(VARIABEL_PATH, existing_data)

def menu_variabel():
    print("====== VARIABEL MENU ======")
    print("1. Create")
    print("2. Update")
    print("3. View")
    return int(input("Pilih salah satu dengan angka:"))

def menu_sub_variabel():
    print("====== SUB VARIABEL MENU ======")
    print("1. Create")
    print("2. Update")
    print("3. View")
    return int(input("Pilih salah satu dengan angka:"))

def menu_pegawai():
    print("====== PEGAWAI MENU ======")
    print("1. Create")
    print("2. Update")
    print("3. View")
    return int(input("Pilih salah satu dengan angka:"))

def menu_hasil():
    print("====== HASIL MENU ======")
    print("1. Perhitungan")
    print("2. Perankingan")
    return int(input("Pilih salah satu dengan angka:"))


def create_variabel():
    nama = input("Masukkan nama variabel: ")
    faktor = input("Masukkan faktor variabel (core/secondary): ")
    persentase = int(input("Masukkan persentase variabel: "))
    return Variabel(nama=nama, faktor=faktor, persentase=persentase)


def update_variabel(variabel: Variabel):
    nama = input("Masukkan nama variabel: ")
    faktor = input("Masukkan faktor variabel (core/secondary): ")
    persentase = int(input("Masukkan persentase variabel: "))
    


if __name__ == "__main__":
    menu()
