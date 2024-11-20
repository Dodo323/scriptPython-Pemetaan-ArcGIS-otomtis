import time
from datetime import datetime as dtt
import datetime
from datetime import timedelta

# Jumlah iterasi
n = int(raw_input('Jumlah iterasi (default = 10): '))
if n > 10 or n == None:
    n = 10

# Rentang waktu (dalam detik) antara setiap eksekusi
interval = int(raw_input('Masukkan rentang waktu (default = 600s): '))
if interval > 600 or interval == None :
    interval = 600

#Perlungan tergantung jumlah iterasi dan rentang waktu
for i in range(1,n+1):
    sekarang = datetime.datetime.now()
    tanggal = sekarang.strftime('%Y-%m-%d')  # Format: Tahun-Bulan-Hari
    hari = sekarang.strftime('%A')  # Nama hari dalam bahasa Inggris
    jam = sekarang.strftime('%H:%M:%S')  # Format: Jam:Menit:Detik
    
    execfile('C:/arcpy map/script/DataGempaUSGS.py')
    execfile('C:/arcpy map/script/PemetaanSeismisitas.py')
    
    time.sleep(interval)  # Tunggu selama interval sebelum menjalankan perintah lagi

