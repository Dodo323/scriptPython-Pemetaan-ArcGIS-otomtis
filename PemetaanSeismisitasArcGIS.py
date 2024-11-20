import arcpy
import time

# Inisiasi variabel
xy_table = 'C:/arcpy map/data seismik/{} {} ({}).csv'.format(hari,tanggal,jam.replace(':', '.'))
spatial_reference = arcpy.SpatialReference(4326) #tentukan koordinat sistem referensi (misalnya WGS 1984)
out_layer = 'Sebaran Gempa' #nama layer xy
x_field = 'Lon' #tentukan nama field untuk koordinat x dan y
y_field = 'Lat'
#Variabel Peta Wilayah 
arcpy.env.workspace = 'C:/arcpy map/'
mapName = 'map/template peta2.mxd'
sumut_marker = 'C:/arcpy map/layer data/kb_sumut_penanda.lyr'
sumatera = 'C:/arcpy map/layer data/DEM_sumatera.lyr'
sumatera_marker = 'C:/arcpy map/layer data/sumatera.lyr'
batimetri = 'C:/arcpy map/layer data/bathy.dem.lyr'
grs_pantai = 'C:/arcpy map/layer data/IND_PNT_polyline.lyr'
QBC_lyr = 'C:/arcpy map/layer data/Quantity by Category.lyr'
#Nilai variabel dapat disesuaikan 

#Buat layer dari data XY
arcpy.MakeXYEventLayer_management(xy_table, x_field, y_field, out_layer, spatial_reference)

# Inisiasi MapDocument dan objek DataFrame 
mxd = arcpy.mapping.MapDocument(arcpy.env.workspace + '/' + mapName) 
dfs = arcpy.mapping.ListDataFrames(mxd)

#Mendapatkan data frame pertama
df = dfs[0]

#atur ukuran data frame
df.elementPositionX = 0.9693 
df.elementPositionY = 6.6226 
df.elementWidth = 26.0246  
df.elementHeight = 13.6653 
arcpy.RefreshActiveView()

#Zoom in ke daerah sumut
new_extent = df.extent
new_extent.XMin = 95.331570  
new_extent.XMax = 100.607108  
new_extent.YMin = -0.296682 
new_extent.YMax = 4.645273 
df.extent = new_extent

# Inisiasi objek layer
layerObj1 = arcpy.mapping.Layer(sumatera)
layerObj2 = arcpy.mapping.Layer(batimetri)
layerObj3 = arcpy.mapping.Layer(grs_pantai)
xy_layer = arcpy.mapping.Layer(out_layer)

# Menambahkan layer baru kedalam map
arcpy.mapping.AddLayer(df, layerObj1)
arcpy.mapping.AddLayer(df, layerObj2)
arcpy.mapping.AddLayer(df, layerObj3)
arcpy.mapping.AddLayer(df, xy_layer)
arcpy.RefreshActiveView()

#akses objek tiap layer
Layers = arcpy.mapping.ListLayers(mxd,'',df)
lyr_xy = Layers [0]
lyr_xytemp = Layers [1]
lyr_pantai = Layers [2]
lyr_batimeteri = Layers [3]
lyr_sumatera = Layers [4]

#terapkan atribut multi simbol ke layer data gempa/xy
arcpy.ApplySymbologyFromLayer_management(lyr_xy, QBC_lyr)
arcpy.RefreshActiveView()
#menghilangkan nama layer data xy agar legend rapi
lyr_xy.name = ''

#Mengatur Layout
for elem in arcpy.mapping.ListLayoutElements(mxd):
    #Mengatur Judul
    if "Title" in elem.name:
        title = elem
        # Mengganti teks title
        title.text = "Peta Seismisitas Wilayah Sumatera Utara"  
        title.fontSize = 17  # Mengubah ukuran font
        title.font = "Arial"  # Mengubah jenis font
        title.bold = True
        arcpy.RefreshActiveView()
        title.elementWidth = 27
        title.elementHeight = 0.7
        title.elementPositionX = 14.1647
        title.elementPositionY = 21.2296
    #Mengatur background judul
    elif "Background judul" in elem.name:
        bckgnd = elem
        bckgnd.elementWidth = 28
        bckgnd.elementHeight = 0.7
        bckgnd.elementPositionX = 13.9585 
        bckgnd.elementPositionY = 21.259  
    #Mengatur Logo di Peta    
    elif "logo UINSU" in elem.name:
        picture = elem
        picture.elementWidth = 4.7153 
        picture.elementHeight = 3.9804 
        picture.elementPositionX = 16.247  
        picture.elementPositionY = 3.3113 
    #Mengatur mata angin
    elif "North Arrow" in elem.name:
        arrow = elem
        arrow.elementWidth = 2.5427  
        arrow.elementHeight = 2.6215 
        arrow.elementPositionX = 23.8778 
        arrow.elementPositionY = 17.3152  
    #Mengatur bar skala
    elif "Alternating Scale Bar" in elem.name:
        scale_bar = elem
        scale_bar.elementWidth = 7.5949 
        scale_bar.elementHeight = 0.7335 
        scale_bar.elementPositionX = 1.9268 
        scale_bar.elementPositionY = 7.072 
    #Mengatur data frame pulau sumatera
    elif "Data Frame" in elem.name:
        df_smtr = elem
        df_smtr.elementWidth = 7.6887   
        df_smtr.elementHeight = 5.2335 
        df_smtr.elementPositionX = 19.2339  
        df_smtr.elementPositionY = 0.6297 
        lyr_dfsmtr = arcpy.mapping.Layer(sumatera_marker)
        marker_sumut = arcpy.mapping.Layer(sumut_marker)
        arcpy.mapping.AddLayer(df_smtr, lyr_dfsmtr)       
        arcpy.mapping.AddLayer(df_smtr, marker_sumut)
        desc = arcpy.Describe(lyr_dfsmtr)
        extent = desc.extent
        new_extent = df_smtr.extent
        new_extent.XMin = extent.XMin
        new_extent.XMax = extent.XMax
        new_extent.YMin = extent.YMin
        new_extent.YMax = extent.YMax
        df_smtr.extent = new_extent 
        #Mengatur legend
    elif "Legend" in elem.name:
        legend = elem
        legend.removeItem (lyr_sumatera)
        legend.removeItem (lyr_xytemp)
        arcpy.mapping.RemoveLayer(df,lyr_xytemp) 
        legend.removeItem (lyr_batimeteri)
        legend.removeItem (lyr_pantai)
        legend.adjustColumnCount (3)
        legend.elementWidth = 10.3451     
        legend.elementHeight = 4.1622 
        legend.elementPositionX = 7.2932  
        legend.elementPositionY = 3.3196  
arcpy.RefreshActiveView()        

#Finishing
copyName = 'C:/arcpy map/map/peta seismisitas.mxd'
mxd.saveACopy(copyName)# Save a copy of the map.

imageName = 'C:/arcpy map/image/gambar peta/{} {} ({}).csv'
.format(hari,tanggal,jam.replace(':', '.'))
arcpy.mapping.ExportToPNG(mxd, imageName)
print('Gambar peta ke-'+str(i)+' berhasil disimpan')

arcpy.Delete_management(out_layer) #Delete xy_layer
del mxd # Delete the MapDocument object to release the map.