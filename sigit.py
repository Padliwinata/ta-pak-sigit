from enum import Enum
import json
from json.decoder import JSONDecodeError
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
    variabel: str
    kode: str
    nama: str
    faktor: Faktor
    standar: int


class Pegawai(BaseModel):
    id_pegawai: str
    nama: str


class Skor(BaseModel):
    id_pegawai: str
    variabel: str
    skor: int


def read_variabel(file_path) -> List[Variabel]:
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []
    except JSONDecodeError:
        existing_data = []
    
    parsed_existing_data = [Variabel(**data) for data in existing_data]
    return parsed_existing_data

def read_sub_variabel(file_path) -> List[SubVariabel]:
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []
    except JSONDecodeError:
        existing_data = []
    
    parsed_existing_data = [SubVariabel(**data) for data in existing_data]
    return parsed_existing_data

def read_pegawai(file_path) -> List[Pegawai]:
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []
    except JSONDecodeError:
        existing_data = []
    
    parsed_existing_data = [Pegawai(**data) for data in existing_data]
    return parsed_existing_data


def store_variabel(file_path: str, json_data: List[Variabel] | List[SubVariabel] | List[Pegawai] | List[Skor]):
    if all(isinstance(item, str) for item in json_data):
        json_data_str = json.dumps(json_data)
    else:
        json_data_str = json.dumps([var.dict() for var in json_data], indent=4)
    with open(file_path, 'w') as json_file:
        json_file.write(json_data_str)


def search_variabel(existing_data: List[Variabel], nama: str) -> Variabel:
    for data in existing_data:
        if data.nama == nama:
            return data

def print_variabel():
    existing_data = read_variabel(VARIABEL_PATH)
    print("\n\n")
    print("====== DATA VARIABEL ======")
    if len(existing_data) == 0:
        print("Data kosong")
    else:
        for data in existing_data:
            print(f"Nama       : {data.nama}")
            print(f"Faktor     : {data.faktor.value}")
            print(f"Persentase : {data.persentase}")
            print("====== ====== ======")

def print_pegawai():
    existing_data = read_pegawai(PEGAWAI_PATH)
    print("\n\n")
    print("====== DATA PEGAWAI ======")
    if len(existing_data) == 0:
        print("Data kosong")
    else:
        for data in existing_data:
            print(f"ID Pegawai  : {data.id_pegawai}")
            print(f"Nama        : {data.nama}")
            print("====== ====== ======")

def print_subvariabel():
    existing_data = read_sub_variabel(SUB_VARIABEL_PATH)
    print("\n\n")
    print("====== DATA SUBVARIABEL ======")
    if len(existing_data) == 0:
        print("Data kosong")
    else:
        for data in existing_data:
            print(f"Variabel    : {data.variabel}")
            print(f"Kode        : {data.kode}")
            print(f"Nama        : {data.nama}")
            print(f"Faktor      : {data.faktor.value}")
            print(f"Standar     : {data.standar}")
            print("====== ====== ======")


VARIABEL_PATH = 'variabel.json'
SUB_VARIABEL_PATH = 'sub_variabel.json'
PEGAWAI_PATH = 'pegawai.json'
SKOR_PATH = 'skor.json'


def menu():
    print("\n\n")
    print("====== RECOMMENDER TRUK ======")
    print("1. Variabel")
    print("2. Sub Variabel")
    print("3. Pegawai")
    print("4. Mapping Data Pegawai")
    print("5. Hasil")
    chosen = int(input("Pilih salah satu dengan angka: "))
    if chosen == 1:
        chosen_menu = menu_variabel()
        if chosen_menu == 1:
            print("\n\n")
            new_data = create_variabel()

            existing_data = read_variabel(VARIABEL_PATH)
            existing_data.append(new_data)

            store_variabel(VARIABEL_PATH, existing_data)
            print("Data berhasil ditambahkan")
            menu()
        elif chosen_menu == 2:
            print("\n\n")
            updated_data = update_variabel()
            if updated_data:
                store_variabel(VARIABEL_PATH, updated_data)
            else:
                print('Data Tidak Ditemukan')
            menu()
        elif chosen_menu == 3:
            print_variabel()
            menu()
    elif chosen == 2:
        chosen_menu = menu_sub_variabel()
        if chosen_menu == 1:
            print("\n\n")
            new_data = create_sub_variabel()

            existing_data = read_sub_variabel(SUB_VARIABEL_PATH)
            existing_data.append(new_data)

            store_variabel(SUB_VARIABEL_PATH, existing_data)
            print("Data berhasil ditambahkan")
            menu()
        if chosen_menu == 2:
            print("\n\n")
            updated_data = update_sub_variabel()
            if updated_data:
                store_variabel(SUB_VARIABEL_PATH, updated_data)
            else:
                print("Data tidak ditemukan")
            menu()
        if chosen_menu == 3:
            print_subvariabel()
            menu()
    elif chosen == 3:
        chosen_menu = menu_pegawai()
        if chosen_menu == 1:
            print("\n\n")
            new_data = create_pegawai()

            existing_data = read_pegawai(PEGAWAI_PATH)
            existing_data.append(new_data)

            store_variabel(PEGAWAI_PATH, existing_data)
            print("Data berhasil ditambahkan")
            menu()
        if chosen_menu == 2:
            print("\n\n")
            updated_data = update_pegawai()
            if updated_data:
                store_variabel(PEGAWAI_PATH, updated_data)
            else:
                print("Data tidak ditemukan")
            menu()
        if chosen_menu == 3:
            print_pegawai()
            menu()
    elif chosen == 4:
        print_subvariabel()
        print_pegawai()

        existing_data_variabel = read_sub_variabel(SUB_VARIABEL_PATH)
        existing_data_pegawai = read_pegawai(PEGAWAI_PATH)

        id_pegawai = input("Masukkan id pegawai: ")
        found = None

        for data in existing_data_pegawai:
            if data.id_pegawai == id_pegawai:
                found = data
        
        if not found:
            print("Pegawai tidak ditemukan")
            menu()

        skor = []

        for variabel in existing_data_variabel:
            temp = int(input(f"Masukkan skor {variabel.nama} untuk {found.nama}: "))
            skor.append(Skor(id_pegawai=id_pegawai, variabel=variabel.nama, skor=temp))

        store_variabel(SKOR_PATH, skor)

        menu()




def menu_variabel():
    print("====== VARIABEL MENU ======")
    print("1. Create")
    print("2. Update")
    print("3. View")
    return int(input("Pilih salah satu dengan angka: "))

def menu_sub_variabel():
    print("====== SUB VARIABEL MENU ======")
    print("1. Create")
    print("2. Update")
    print("3. View")
    return int(input("Pilih salah satu dengan angka: "))

def menu_pegawai():
    print("====== PEGAWAI MENU ======")
    print("1. Create")
    print("2. Update")
    print("3. View")
    return int(input("Pilih salah satu dengan angka: "))

def menu_hasil():
    print("====== HASIL MENU ======")
    print("1. Perhitungan")
    print("2. Perankingan")
    return int(input("Pilih salah satu dengan angka: "))


def create_variabel() -> Variabel:
    nama = input("Masukkan nama variabel: ")
    faktor = input("Masukkan faktor variabel (Core/Secondary): ")
    persentase = int(input("Masukkan persentase variabel: "))

    return Variabel(nama=nama, faktor=faktor, persentase=persentase)


def update_variabel() -> List[Variabel] | None:
    find = input("Masukkan nama variabel yang akan diupdate: ")
    existing_data = read_variabel(VARIABEL_PATH)
    
    for data in existing_data:
        if data.nama == find:
            nama = input("Masukkan nama variabel: ")
            faktor = input("Masukkan faktor variabel (core/secondary): ")
            persentase = int(input("Masukkan persentase variabel: "))

            data.nama = nama
            data.faktor = faktor
            data.persentase = persentase

            return existing_data
    
    return None

def create_sub_variabel() -> SubVariabel:
    kode = input("Masukkan kode sub variabel: ")
    nama = input("Masukkan nama sub variabel: ")
    faktor = input("Masukkan faktor sub variabel (Core/Secondary): ")
    standar = int(input("Masukkan standar sub variabel: "))

    return SubVariabel(kode=kode, nama=nama, faktor=faktor, standar=standar)

def update_sub_variabel() -> List[SubVariabel] | None:
    find = input("Masukkan kode sub variabel yang akan diupdate: ")
    existing_data = read_sub_variabel()

    for data in existing_data:
        if data.kode == find:
            kode = input("Masukkan kode sub variabel: ")
            nama = input("Masukkan nama sub variabel: ")
            faktor = input("Masukkan faktor sub variabel (Core/Secondary): ")
            standar = int(input("Masukkan standar sub variabel: "))

            data.kode = kode
            data.nama = nama
            data.faktor = faktor
            data.standar = standar

            return existing_data
    
    return None

def create_pegawai() -> Pegawai:
    id_pegawai = input("Masukkan id pegawai: ")
    nama = input("Masukkan nama pegawai: ")

    return Pegawai(id_pegawai=id_pegawai, nama=nama)

def update_pegawai() -> List[Pegawai] | None:
    find = input("Masukkan id pegawai yang akan diupdate: ")
    existing_data = read_pegawai(PEGAWAI_PATH)

    for data in existing_data:
        if data.id_pegawai == find:
            id_pegawai = input("Masukkan id pegawai: ")
            nama = input("Masukkan nama pegawai: ")

            data.id_pegawai = id_pegawai
            data.nama = nama

            return existing_data
    
    return None



if __name__ == "__main__":
    menu()
