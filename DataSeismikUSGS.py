#script ambil data seismik dari USGS
import requests
import csv
import pandas as pd

# URL API untuk mencari katalog gempa dari USGS
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Parameter pencarian
params = {
    'format': 'geojson',                    # Format data yang dikembalikan
    'starttime': datetime.date(2004, 1, 1), # Rentang waktu pencarian (mulai)
    'endtime': tanggal,                     # Sampai hari ini
    'minmagnitude': 5,                      # Magnitudo minimum
    'maxmagnitude': 8,                      # Magnitudo maksimum
    'mindepth': 1,                          # Kedalaman minimum (km)
    'maxdepth': 200,                        # Kedalaman maksimum (km)
    'minlatitude': -0.648,                  # Latitude minimum
    'maxlatitude': 4.325,                   # Latitude maksimum
    'minlongitude': 95.691,                 # Longitude minimum
    'maxlongitude': 100.481,                # Longitude maksimum
}

# Kirim permintaan ke API
response = requests.get(url, params=params)

# Memeriksa apakah respons berhasil
if response.status_code == 200:
    # Mengurai respons JSON
    data = response.json()
    
    # Membuka file CSV untuk menyimpan data
    with open('C:/arcpy map/data seismik/{} {} ({}).csv'.format 
    (hari,tanggal,jam.replace(':', '.')), mode='wb') as file:
        writer = csv.writer(file)
        
        # Tulis header CSV
        writer.writerow([
            'Time', 'Lat', 'Lon', 'Depth', 
            'Mag', 'Place'
        ])
        # Menyimpan data gempa dari API ke file CSV
        for feature in data['features']:
            properties = feature['properties']
            geometry = feature['geometry']
            time_log = dtt.utcfromtimestamp(properties['time'] / 1000).strftime
            ('%Y-%m-%d %H:%M:%S')
            latitude = geometry['coordinates'][1]
            longitude = geometry['coordinates'][0]
            depth = geometry['coordinates'][2]
            magnitude = properties['mag']
            place = properties['place']
            
            # Tulis baris data ke CSV
            writer.writerow([time_log, latitude, longitude, depth, magnitude, place])
    print('Data ke-'+str(i)+' berhasil disimpan ke data.csv')
else:
    print("Error fetching data: {}".format(response.status_code))

# Baca file Excel
file_path = 'C:/arcpy map/data seismik/{} {} ({}).csv'.format(hari,tanggal,jam.replace(':', '.'))
df = pd.read_csv(file_path)
df = df.sort_values(by='Depth', ascending=True)
df['Depth'] = df['Depth'].round(1)

# Simpan hasil ke file Excel 
df.to_csv('C:/arcpy map/data seismik/{} {} ({}).csv'.format(hari,tanggal,jam.replace(':', '.')))

#Nilai untuk variabel hari, tanggal, jam akan diambil dari script !MenjalankanPemetaanBerkala