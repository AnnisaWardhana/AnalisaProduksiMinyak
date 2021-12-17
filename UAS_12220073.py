#Ujian Akhir Semester Pemrograman Komputer
#Nama   : Annisa Nur Syifa Wardhana
#NIM    : 12220073

import streamlit as st
import pandas as pd
import altair as alt
#import matplotlib.pyplot as plt

#Fungsi Menuliskan Menu Pilihan Aplikasi
def Menu_Utama(data_produksi):
    st.header("Aplikasi Analisis Produksi Minyak Dunia")
    st.subheader("Annisa Nur Syifa Wardhana")
    st.subheader("")

    #Menampilkan pilihan fitur aplikasi
    
    pilihan_fitur = st.selectbox("Pilihan Fitur Aplikasi : ", ["Fitur 1 - Trend Produksi Tahunan Negara",
           "Fitur 2 - Produksi Terbesar","Fitur 3 - Produksi Kumulatif Terbesar","Fitur 4 - Informasi Negara"])
    
    
    #Mendefinisikan dictionary untuk menghitung produksi kumulatif setiap negara
    produksi_kumulatif = dict()

    #Menghitung produksi kumulatif untuk setiap negara ke dalam dictionary
    for item in data_produksi_clean:
        produksi_kumulatif[item[0]] = produksi_kumulatif.get(item[0], 0) + item[2]

    if (pilihan_fitur == "Fitur 1 - Trend Produksi Tahunan Negara"):
        Produksi_Tahunan(data_produksi)
    elif (pilihan_fitur == "Fitur 2 - Produksi Terbesar"):
        TopXTerbesarPerTahun(data_produksi)
    elif (pilihan_fitur == "Fitur 3 - Produksi Kumulatif Terbesar"):
        TopXTerbesarKumulatif(produksi_kumulatif)
    elif (pilihan_fitur == "Fitur 4 - Informasi Negara"):
           
        #Menyajikan pilihan fitur informasi

        pilihan_info = st.selectbox("Pilihan Informasi : ", ["Info 1 - Negara dengan Produksi Terbesar","Info 2 - Negara dengan Produksi Terkecil","Info 3 - Negara dengan Produksi Nol"])
    
        #st.write("Fitur yang dipilih adalah : ", pilihan_info)

        if (pilihan_info == "Info 1 - Negara dengan Produksi Terbesar"):
            InfoTerbesarTahun(data_produksi_clean)
            InfoTerbesarKumulatif(produksi_kumulatif)
        elif (pilihan_info == "Info 2 - Negara dengan Produksi Terkecil"):
            InfoTerkecilTahun(data_produksi_clean)
            InfoTerkecilKumulatif(produksi_kumulatif)
        elif (pilihan_info == "Info 3 - Negara dengan Produksi Nol"):
            InfoProdZeroTahun(data_produksi_clean)    
            InfoKumulatifZero(produksi_kumulatif)

    return

#Fungsi Menu 1 - Menampilkan Grafik Jumlah Produksi Minyak Mentah Terhadap Tahun dari negara yang dipilih
def Produksi_Tahunan(data_produksi):
   
    # Memasukkan data produksi yang sudah dibersihkan ke dalam data frame
    df = pd.DataFrame(data_produksi, columns=['negara','tahun','produksi','nama_negara'])

   
    # Menampilkan dropdownbox untuk memilih negara
    pilihan_negara = [st.selectbox("Pilihan Negara : ", df["nama_negara"].unique())]

    # Memperkecil data frame hanya untuk negara yang dipilih    
    df_negara_pilihan = df[df["nama_negara"].isin(pilihan_negara)]

   
    # Menampilkan grafik produksi tahunan hanya untuk negara yang dipilih
    chart = alt.Chart(df_negara_pilihan).mark_line().encode(
        x=alt.X("tahun", title = "Tahun"),
        y=alt.Y("produksi", title = "Produksi"),
        color =alt.Color("nama_negara")
    ).properties(title = "Trend Produksi Tahunan")

    st.altair_chart(chart, use_container_width = True)

    return

#Fungsi Menu 2 - Menampilkan Top-X Negara dengan Produksi Minyak Mentah Terbesar pada suatu tahun 

def TopXTerbesarPerTahun(data_produksi):

    #Menerima input pilihan tahun produksi    
    pil_tahun = str(st.slider("Pilih tahun produksi :",1971,2015))
    
    #Menerima input pilihan jumlah negara yang ingin ditampilkan
    top_negara = st.slider("Jumlah negara yang ingin ditampilkan : ",1,20)
    
    # Memasukkan data produksi yang sudah dibersihkan ke dalam data frame
    df = pd.DataFrame(data_produksi, columns=['negara','tahun','produksi','nama_negara'])

    # Memperkecil data frame hanya untuk tahun produksi yang dipilih
    df_tahun_pilihan = df[df["tahun"].isin([pil_tahun])]
    #st.write(df_tahun_pilihan)

    # Mengurutkan data berdasarkan produksi dari terbesar sampai terkecil (descending)    
    df_tahun_pilihan.sort_values(by=['produksi'], inplace = True, ascending = False) 
    #st.write(df_tahun_pilihan)

    # Memperkecil data frame hanya diambil Top-X negara yang produksinya terbesar (berdasarkan input user)    
    df_top = df_tahun_pilihan.head(top_negara)
    
    judul = "Top " + str(top_negara) + " Produksi Minyak Terbesar pada tahun " + pil_tahun

    st.subheader(judul)
    st.write(df_top)
    
    # Menampilkan grafik
    chart = alt.Chart(df_top).mark_bar().encode(
        x=alt.X("nama_negara", title = "Negara"),
        y=alt.Y("produksi", title = "Produksi"),
        color =alt.Color("nama_negara")
    ).properties(title = judul)

    st.altair_chart(chart, use_container_width = True)

    return

#Fungsi Menu 3 - Menampilkan Top-X Negara dengan Produksi Kumulatif terbesar keseluruhan tahun

def TopXTerbesarKumulatif(dict_kumulatif):
    #Menerima input pilihan jumlah negara yang ingin ditampilkan
    top_negara = st.slider("Jumlah negara yang ingin ditampilkan : ",1,20)
    #st.write(top_negara)
    
    #Membuat dataframe dari dictionary
    df_dict = pd.DataFrame.from_dict(dict_kumulatif,orient='index')
    df_dict.columns = ['prod_kumulatif']
    df_dict.sort_values(by=['prod_kumulatif'], inplace = True, ascending = False)
    #st.write(df_dict)

    df_top = df_dict.head(top_negara)
    
    judul = "Top " + str(top_negara) + " Negara dengan Produksi Minyak Kumulatif terbesar"

    st.subheader(judul)
    st.write(df_top)
    
    #st.write(alt.Chart(data).mark_bar().encode(
    #    x = alt.X('negara',sort=None),
    #    y = 'produksi minyak kumulatif',
    #))

    st.bar_chart(df_top)

    return

#Fungsi menuliskan informasi negara dengan streamlit
def TulisInfoNegara(alpha3,master_negara):
    found = False
    for item in master_negara:
            if alpha3 == item['alpha-3']:
                found = True
                st.subheader(item['name'])
                st.caption("Kode Alpha-3:" + item['alpha-3'])
                st.caption("Kode Negara :" + item['country-code'])
                st.caption("Region      :" + item['region'])
                st.caption("Sub Region  :" + item['sub-region'])
                st.caption(" ")
                return
    if found is False:
        st.caption("Data negara tidak ditemukan")
        return 

#4.1a - Info Negara dengan Jumlah produksi terbesar pada tahun yang dipilih
def InfoTerbesarTahun(data_produksi):

    #Menerima input pilihan tahun produksi    
    pil_tahun = str(st.slider("Pilih tahun produksi :",1971,2015))
    
    # Memasukkan data produksi yang sudah dibersihkan ke dalam data frame
    df = pd.DataFrame(data_produksi, columns=['negara','tahun','produksi','nama_negara'])

    # Memperkecil data frame hanya untuk tahun produksi yang dipilih
    df_tahun_pilihan = df[df["tahun"].isin([pil_tahun])]
    
    #df_tahun_pilihan.sort_values(by=['produksi'], inplace = True, ascending = False)
    #st.write(df_tahun_pilihan)

    #Mengekstrak item dengan produksi tahunan terbesar    
    df_max = df_tahun_pilihan[df_tahun_pilihan['produksi'] == df_tahun_pilihan['produksi'].max()]
    #st.write(df_max)
    
    negara_max = df_max['negara'].values[0]
    #st.write(negara_max)

    st.subheader("Informasi 1A. Produksi Minyak Terbesar per Tahun")
    st.caption("Jumlah produksi terbesar untuk tahun produksi " + pil_tahun + " adalah : " + str(df_max['produksi'].values[0]) )
    st.caption("Negara dengan jumlah produksi minyak terbesar untuk tahun produksi " + pil_tahun + " adalah : ")

    TulisInfoNegara(negara_max,data_negara) 

    return

#4.1b - Info Negara dengan Jumlah produksi terbesar pada keseluruhan tahun 
def InfoTerbesarKumulatif(dict_kumulatif):
    
    max_key = max(dict_kumulatif, key=dict_kumulatif.get)

    st.subheader("Informasi 1B. Produksi Minyak Terbesar Kumulatif")
    st.caption("Negara dengan jumlah produksi minyak terbesar kumulatif untuk keseluruhan tahun adalah : ")
    
    TulisInfoNegara(max_key,data_negara) 
    
    return 

#4.2a - Info Negara dengan Jumlah produksi terkecil (tapi tidak nol) pada tahun yang dipilih
def InfoTerkecilTahun(data_produksi):

    #Menerima input pilihan tahun produksi    
    pil_tahun = str(st.slider("Pilih tahun produksi :",1971,2015))
    
    # Memasukkan data produksi yang sudah dibersihkan ke dalam data frame
    df = pd.DataFrame(data_produksi, columns=['negara','tahun','produksi','nama_negara'])

    # Memperkecil data frame hanya untuk tahun produksi yang dipilih
    df_tahun_pilihan = df[df["tahun"].isin([pil_tahun])]
    
    df_tahun_pilihan.sort_values(by=['produksi'], inplace = True, ascending = True)
    #st.write(df_tahun_pilihan)

    #Mengekstrak item dengan produksi tahunan terkecil non zero    
    df_nz = df_tahun_pilihan[df_tahun_pilihan["produksi"].ne(0)]
    #st.write(df_nz)
    
    #Mengekstrak item dengan produksi tahunan terbesar    
    df_min = df_nz[df_nz['produksi'] == df_nz['produksi'].min()]
    #st.write(df_min)

    negara_min = df_min['negara'].values[0]
    #st.write(negara_min)

    st.subheader("Informasi 2A. Produksi Minyak Terkecil per Tahun")
    st.caption("Jumlah produksi terkecil untuk tahun produksi " + pil_tahun + " adalah : " + str(df_nz['produksi'].min()))
    st.caption("Negara dengan jumlah produksi minyak terkecil non zero untuk tahun produksi " + pil_tahun + " adalah : ")

    TulisInfoNegara(negara_min,data_negara) 

    return

#4.2b - Info Negara dengan Jumlah produksi terkecil (tapi tidak nol)  pada keseluruhan tahun
def InfoTerkecilKumulatif(dict_kumulatif):
    
    max_key = max(dict_kumulatif, key=dict_kumulatif.get)

    terkecil = dict_kumulatif[max_key]
    min_key = max_key

    for key in dict_kumulatif:        
        if (float(dict_kumulatif[key]) != 0.0000):
            if float(dict_kumulatif[key] < terkecil) :
                terkecil = float(dict_kumulatif[key])
                min_key = key

    st.subheader("Informasi 2B. Produksi Minyak Terkecil Kumulatif")
    st.caption("Jumlah produksi terkecil untuk keseluruhan tahun produksi adalah : " + str(terkecil))
    st.caption("Negara dengan jumlah produksi minyak terkecil untuk keseluruhan tahun adalah : ")
        
    TulisInfoNegara(min_key,data_negara) 
    
    return 


#4.3a - Info Negara dengan Jumlah produksi nol pada tahun yang dipilih

def InfoProdZeroTahun(data_produksi):

    #Menerima input pilihan tahun produksi    
    pil_tahun = str(st.slider("Pilih tahun produksi :",1971,2015))
    
    # Memasukkan data produksi yang sudah dibersihkan ke dalam data frame
    df = pd.DataFrame(data_produksi, columns=['negara','tahun','produksi','nama_negara'])

    # Memperkecil data frame hanya untuk tahun produksi yang dipilih
    df_tahun_pilihan = df[df["tahun"].isin([pil_tahun])]
    
    df_tahun_pilihan.sort_values(by=['produksi'], inplace = True, ascending = True)
    #st.write(df_tahun_pilihan)

    #Mengekstrak item dengan produksi tahunan  zero    
    df_z = df_tahun_pilihan[df_tahun_pilihan["produksi"] == 0]
    st.write(df_z)
    
    #for 

    #negara_z = df_z['negara'].values[i]
    #st.write(negara_min)

    st.subheader("Informasi 3A. Produksi Zero Per Tahun")
    st.caption("Negara yang tidak memiliki produksi minyak untuk tahun produksi " + pil_tahun + " adalah : ")

    for index,row in df_z.iterrows():
        TulisInfoNegara(row["negara"],data_negara) 

    return


#4.3b - Info Negara dengan Jumlah produksi nol  pada keseluruhan tahun
def InfoKumulatifZero(dict_kumulatif):
    
    st.subheader("Informasi 3B. Produksi Kumulatif Zero")
    st.caption("Negara yang tidak memiliki produksi minyak untuk keseluruhan tahun adalah : ")
    
    for key in dict_kumulatif:
        if (float(dict_kumulatif[key]) == 0.0000):
           TulisInfoNegara(key,data_negara) 
    
    return 

# START EKSEKUSI PROGRAM
#Membuka file "kode_negara_lengkap.json" dan extract data ke dalam tabel "data_negara"
import json
with open('kode_negara_lengkap.json') as json_file:
  data_negara = json.load(json_file)

#Definisi list data_produksi_clean untuk menyimpan data produksi hanya dari negara yang ada di master negara

data_produksi_clean = []

# Membuka File "produksi_minyak_mentah.csv"
import csv

with open('produksi_minyak_mentah.csv') as csv_file:
    produksi_tahunan = csv.reader(csv_file, delimiter=",")
        
    for data in produksi_tahunan:
        found = False
        nama_negara = ""
        data_temp = ["","",0.0,""]

        for item in data_negara:
            if data[0] == item['alpha-3']:
                found = True
                nama_negara = item['name']

        #Bila kode_negara ada di dalam tabel "data_negara", simpan data produksi kedalam tabel "Produksi Tahunan"
        if found is True:
            data_temp[0] = data[0]          #Kode Alpha 3
            data_temp[1] = data[1]          #Tahun
            data_temp[2] = float(data[2])   #Produksi
            data_temp[3] = nama_negara          
            
            data_produksi_clean.append(data_temp)


# Menampilkan Menu Utama - Pilihan Fitur untuk Pengguna
Menu_Utama(data_produksi_clean)

# Menutup file-file yang dibuka
csv_file.close()
json_file.close()