import csv
from datetime import datetime

riwayat_transaksi = []

class Kasir:
    def __init__(self):
        self.kasir = None
        self.pembeli = None
        self.tanggal = None
        self.daftar_harga = {
            1: {"nama": "Apel", "harga": 4850},
            2: {"nama": "Pisang", "harga": 2690},
            3: {"nama": "Mangga", "harga": 3990},
            4: {"nama": "Anggur", "harga": 9490},
            5: {"nama": "Pear", "harga": 4990},
            6: {"nama": "Naga", "harga": 5590},
            7: {"nama": "Jeruk", "harga": 2750},
        }
        self.buah_list = []
        self.satuan_list = []

    def input_data(self):
        print("---------- Program Kasir ----------")
        self.kasir = input("Masukkan nama Kasir: ")
        self.pembeli = input("Nama Pembeli: ")
        try:
            tanggal_input = input("Tanggal (DD/MM/YYYY): ")
            self.tanggal = datetime.strptime(tanggal_input, "%d/%m/%Y")
        except ValueError:
            print("Format tanggal salah.")
            exit()

    def tampilkan_menu_buah(self):
        print("\n--- Daftar Buah ---")
        for nomor, detail in self.daftar_harga.items():
            print(f"{nomor}. {detail['nama']} - Rp {detail['harga']}")

    def proses_pembelian(self):
        while True:
            self.tampilkan_menu_buah()
            try:
                nomor = int(input("Pilih buah (nomor): "))
                if nomor not in self.daftar_harga:
                    print("Pilihan tidak valid.")
                    continue
                satuan = int(input(f"Jumlah {self.daftar_harga[nomor]['nama']}: "))
                self.buah_list.append(self.daftar_harga[nomor]['nama'])
                self.satuan_list.append(satuan)
                lanjut = input("Beli lagi? (y/n): ").lower()
                if lanjut != 'y':
                    break
            except ValueError:
                print("Input tidak valid.")

    def hitung_total(self):
        total = 0
        for i, nama in enumerate(self.buah_list):
            harga = next(item['harga'] for item in self.daftar_harga.values() if item['nama'] == nama)
            total += harga * self.satuan_list[i]
        return total

    def cetak_struk(self, total, uang):
        print("\n========== STRUK ==========")
        print(f"Kasir     : {self.kasir}")
        print(f"Nama      : {self.pembeli}")
        print(f"Tanggal  : {self.tanggal.strftime('%d/%m/%Y')}")
        for i, nama in enumerate(self.buah_list):
            jumlah = self.satuan_list[i]
            harga = next(item['harga'] for item in self.daftar_harga.values() if item['nama'] == nama)
            print(f"{i+1}. {jumlah} {nama} x Rp {harga} = Rp {harga * jumlah}")
        print(f"Total     : Rp {total}")
        print(f"Dibayar   : Rp {uang}")
        print(f"Kembalian : Rp {uang - total}")
        print("===========================")

    def simpan_ke_csv(self, filename='transaksi.csv'):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            for buah, jumlah in zip(self.buah_list, self.satuan_list):
                writer.writerow([self.tanggal.strftime('%d/%m/%Y'), buah, jumlah])
        print("Data transaksi disimpan.")

    def jalankan(self):
        self.input_data()
        self.proses_pembelian()
        total = self.hitung_total()
        try:
            uang = int(input(f"Total: Rp {total} | Uang tunai: Rp "))
        except ValueError:
            print("Input tidak valid.")
            return
        self.cetak_struk(total, uang)
        self.simpan_ke_csv()
        riwayat_transaksi.append({
            "tanggal": self.tanggal.strftime('%d/%m/%Y'),
            "total": total
        })


# === Fungsi Tambahan ===

def menu_pengelolaan():
    while True:
        print("\n=== MENU PENGELOLAAN ===")
        print("1. Lihat Belanjaan")
        print("2. Tambah Belanjaan")
        print("3. Edit Belanjaan")
        print("4. Hapus Belanjaan")
        print("5. Keluar")
        pilihan = input("Pilih: ")
        if pilihan == "1":
            lihat_belanjaan()
        elif pilihan == "2":
            tambah_belanjaan()
        elif pilihan == "3":
            edit_belanjaan()
        elif pilihan == "4":
            hapus_belanjaan()
        elif pilihan == "5":
            break

buah_list = []
jumlah_list = []

def lihat_belanjaan():
    if not buah_list:
        print("Belum ada belanjaan.")
        return
    for i, (buah, jumlah) in enumerate(zip(buah_list, jumlah_list), 1):
        print(f"{i}. {buah} - {jumlah} buah")

def tambah_belanjaan():
    buah = input("Nama buah: ")
    jumlah = int(input("Jumlah: "))
    buah_list.append(buah)
    jumlah_list.append(jumlah)

def edit_belanjaan():
    lihat_belanjaan()
    idx = int(input("Edit nomor: ")) - 1
    if 0 <= idx < len(buah_list):
        jumlah_baru = int(input("Jumlah baru: "))
        jumlah_list[idx] = jumlah_baru

def hapus_belanjaan():
    lihat_belanjaan()
    idx = int(input("Hapus nomor: ")) - 1
    if 0 <= idx < len(buah_list):
        buah_list.pop(idx)
        jumlah_list.pop(idx)

def cek_total_per_tanggal():
    tanggal_input = input("Cek total transaksi pada tanggal (DD/MM/YYYY): ")
    total = sum(trx["total"] for trx in riwayat_transaksi if trx["tanggal"] == tanggal_input)
    print(f"Total transaksi pada {tanggal_input}: Rp {total}")


# === Menu Utama ===
def main():
    while True:
        print("\n==== MENU UTAMA ====")
        print("1. Jalankan Kasir")
        print("2. Pengelolaan Belanjaan")
        print("3. Cek Total Transaksi per Tanggal")
        print("4. Keluar")
        pilih = input("Pilih menu (1-4): ")
        if pilih == "1":
            kasir = Kasir()
            kasir.jalankan()
        elif pilih == "2":
            menu_pengelolaan()
        elif pilih == "3":
            cek_total_per_tanggal()
        elif pilih == "4":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
    kasir = Kasir()
kasir.jalankan()
