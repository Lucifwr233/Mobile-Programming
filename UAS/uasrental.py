# memasukkan library flet ke aplikasi
# import flet as ft
import flet
from flet import *
import mysql.connector
import datetime

# buat koneksi ke database SQL
koneksi_db = mysql.connector.connect(host = "localhost", user = "root", password = "", database = "rentaly")
cursor = koneksi_db.cursor()

class FormDurasiSewa(UserControl):
    def build(durasisewa) :

        # buat variabel inputan
        durasisewa.inputan_id_durasi = TextField(visible = False, expand = True)
        durasisewa.inputan_durasi_sewa = TextField(label = "Durasi Sewa", hint_text = "masukkan Durasi Jam ... ", expand = True)
        durasisewa.inputan_harga_sewa = TextField(label = "Harga Sewa", hint_text = "masukkan Harga Sewa ... ", expand = True)
        durasisewa.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")
        
        # memuat tabel data
        def tampil_data(e):
            # Merefresh halaman & menampilkan notif
            durasisewa.data_durasisewa.rows.clear()
            cursor.execute("SELECT * FROM durasi_sewa ORDER BY id_durasi DESC")
            
            result = cursor.fetchall()
            # menampilkan ulang data 
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
            for row in rows:
                durasisewa.data_durasisewa.rows.append(
                    DataRow(
                        cells = [
                            DataCell(Text(row['id_durasi'])),
                            DataCell(Text(row['durasi_sewa'])),
                            DataCell(Text(row['harga_sewa'])),
                            DataCell(
                                Row([
                                    IconButton("delete", icon_color = "#4968B8", data = row, on_click = hapus_durasisewa),
                                    IconButton("create", icon_color = "#4968B8", data = row, on_click = tampil_dialog_ubah),
                                ])
                            ),
                        ]
                        )
                    )
        # fungsi menampilkan dialog form entri
        def tampil_dialog(e):
            durasisewa.inputan_id_durasi.value = ''
            durasisewa.inputan_durasi_sewa.value = ''
            durasisewa.inputan_harga_sewa.value = ''
            durasisewa.dialog.open = True
            durasisewa.update()

        def tampil_dialog_ubah(e):
            durasisewa.inputan_id_durasi.value = e.control.data['id_durasi']
            durasisewa.inputan_durasi_sewa.value = e.control.data['durasi_sewa']
            durasisewa.inputan_harga_sewa.value = e.control.data['harga_sewa']
            durasisewa.dialog.open = True
            durasisewa.update()

        # fungsi simpan data
        def simpan_durasisewa(e):
            try:
                if (durasisewa.inputan_id_durasi.value == '') :
                    sql = "INSERT INTO durasi_sewa (id_durasi, durasi_sewa, harga_sewa) VALUES(%s, %s, %s)"
                    val = ('', durasisewa.inputan_durasi_sewa.value, durasisewa.inputan_harga_sewa.value )
                else :
                    sql = "UPDATE durasi_sewa SET durasi_sewa = %s, harga_sewa = %s WHERE id_durasi = %s"
                    val = (durasisewa.inputan_durasi_sewa.value, durasisewa.inputan_harga_sewa.value, durasisewa.inputan_id_durasi.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_data(e)
                durasisewa.dialog.open = False
                durasisewa.snack_bar_berhasil.open = True
                durasisewa.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # fungsi hapus data
        def hapus_durasisewa(e):
            try:
                sql = "DELETE FROM durasi_sewa WHERE id_durasi = %s"
                val = (e.control.data['id_durasi'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                durasisewa.data_durasisewa.rows.clear()
                
                tampil_data(e)
                durasisewa.dialog.open = False
                durasisewa.snack_bar_berhasil.open = True
                durasisewa.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # menampilkan semua data ke dalam tabel
        durasisewa.data_durasisewa = DataTable(
            columns = [
                DataColumn(Text("ID")),
                DataColumn(Text("Durasi Sewa")),
                DataColumn(Text("Harga Sewa")),
                DataColumn(Text("Opsi")),
            ],
        )
        cursor.execute("SELECT * FROM durasi_sewa ORDER BY id_durasi DESC")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        for row in rows:
            durasisewa.data_durasisewa.rows.append(
                DataRow(
                    cells = [
                        DataCell(Text(row['id_durasi'])),
                        DataCell(Text(row['durasi_sewa'])),
                        DataCell(Text(row['harga_sewa'])),
                        DataCell(
                            Row([
                                IconButton("delete", icon_color = "red", data = row, on_click = hapus_durasisewa),
                                IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah),
                            ])
                        ),
                    ]
                )
            )
        
        # buat variabel utk layout data rekapan
        durasisewa.layout_data = Column()

        # buat form dialog untuk form entri data
        durasisewa.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Tambah Durasi Sewa", weight = FontWeight.BOLD),
                        Row([ durasisewa.inputan_id_durasi ]),
                        Row([ durasisewa.inputan_durasi_sewa ]),
                        Row([ durasisewa.inputan_harga_sewa ]),
                        Row([
                            #tombol tambah data
                            ElevatedButton(
                                "SIMPAN",
                                    icon = "SAVE_AS",
                                    icon_color = "white",
                                    color = "white",
                                    bgcolor = "GREEN",
                                    width = 280,
                                    height = 50,
                                    on_click = simpan_durasisewa,
                                )
                        ]),
                    ],
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    height = 500,
                    scroll = ScrollMode.ALWAYS
                    #tight = True,
                ),
                padding = 40,
                width = 378,
                height = 500
            ),
            open = False,
            bgcolor = colors.GREY_50
        )
    
        return Column(
            controls = [
                Row([ElevatedButton("Tambah", icon = icons.ADD, icon_color="white", color = "white", bgcolor = "RED", on_click = tampil_dialog)], alignment = MainAxisAlignment.END),
                Row([durasisewa.data_durasisewa], scroll = ScrollMode.ALWAYS),             
                durasisewa.dialog, durasisewa.snack_bar_berhasil
            ],
            
        )

class FormMobil(UserControl):
    def build(mobil) :

        # buat variabel inputan
        mobil.inputan_id_mobil = TextField(visible = False, expand = True)
        mobil.inputan_kode_mobil = TextField(label = "Kode Mobil", hint_text = "masukkan Kode Mobil ... ", expand = True)
        mobil.inputan_nama_mobil = TextField(label = "Nama Mobil", hint_text = "masukkan Nama Mobil ... ", expand = True)
        mobil.inputan_keterangan = TextField(label = "Keterangan", hint_text = "masukkan Keterangan ... ", expand = True)

        mobil.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")

        # memuat tabel data
        def tampil_data(e):
            # Merefresh halaman & menampilkan notif
            mobil.data_mobil.rows.clear()
            cursor.execute("SELECT * FROM mobil ORDER BY id_mobil DESC")
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
            for row in rows:
                mobil.data_mobil.rows.append(
                    DataRow(
                        cells = [
                            DataCell(Text(row['id_mobil'])),
                            DataCell(Text(row['kode_mobil'])),
                            DataCell(Text(row['nama_mobil'])),
                            DataCell(Text(row['keterangan'])),
                            DataCell(
                                Row([
                                    IconButton("delete", icon_color = "red", data = row, on_click = hapus_mobil),
                                    IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah),
                                ])
                            ),
                        ]
                    )
                )
        # fungsi menampilkan dialog form entri
        def tampil_dialog(e):
            mobil.inputan_id_mobil.value = ''
            mobil.inputan_kode_mobil.value = ''
            mobil.inputan_nama_mobil.value = ''
            mobil.inputan_keterangan.value = ''
            mobil.dialog.open = True
            mobil.update()

        def tampil_dialog_ubah(e):
            mobil.inputan_id_mobil.value = e.control.data['id_mobil']
            mobil.inputan_kode_mobil.value = e.control.data['kode_mobil']
            mobil.inputan_nama_mobil.value = e.control.data['nama_mobil']
            mobil.inputan_keterangan.value = e.control.data['keterangan']
            mobil.dialog.open = True
            mobil.update()

        # fungsi simpan data
        def simpan_mobil(e):
            try:
                if (mobil.inputan_id_mobil.value == '') :
                    sql = "INSERT INTO mobil (id_mobil, kode_mobil, nama_mobil, keterangan) VALUES(%s, %s, %s, %s)"
                    val = ('', mobil.inputan_kode_mobil.value, mobil.inputan_nama_mobil.value, mobil.inputan_keterangan.value)
                else :
                    sql = "UPDATE mobil SET kode_mobil =  %s, nama_mobil =  %s, keterangan =  %s  WHERE id_mobil = %s"
                    val = (mobil.inputan_kode_mobil.value, mobil.inputan_nama_mobil.value, mobil.inputan_keterangan.value, mobil.inputan_id_mobil.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_data(e)
                mobil.dialog.open = False
                mobil.snack_bar_berhasil.open = True
                mobil.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # fungsi hapus data
        def hapus_mobil(e):
            try:
                sql = "DELETE FROM mobil WHERE id_mobil = %s"
                val = (e.control.data['id_mobil'],)
                cursor.execute(sql, val) 
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                mobil.data_mobil.rows.clear()
                
                tampil_data(e)
                mobil.dialog.open = False
                mobil.snack_bar_berhasil.open = True
                mobil.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        mobil.data_mobil = DataTable(
            columns = [
                DataColumn(Text("ID")),
                DataColumn(Text("Kode Mobil")),
                DataColumn(Text("Nama Mobil")),
                DataColumn(Text("Keterangan")),
                DataColumn(Text("Opsi")),
            ],
        )
        cursor.execute("SELECT * FROM mobil ORDER BY id_mobil DESC")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        for row in rows:
            mobil.data_mobil.rows.append(
                DataRow(
                    cells = [
                        DataCell(Text(row['id_mobil'])),
                        DataCell(Text(row['kode_mobil'])),
                        DataCell(Text(row['nama_mobil'])),
                        DataCell(Text(row['keterangan'])),
                        DataCell(
                            Row([
                                IconButton("delete", icon_color = "red", data = row, on_click = hapus_mobil),
                                IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah),
                            ])
                        ),
                    ]
                )
            )
        
        # buat variabel utk layout data rekapan
        mobil.layout_data = Column()

        # buat form dialog untuk form entri data
        mobil.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Tambah Jenis Mobil", weight = FontWeight.BOLD),
                        Row([ mobil.inputan_id_mobil ]),
                        Row([ mobil.inputan_kode_mobil ]),
                        Row([ mobil.inputan_nama_mobil ]),
                        Row([ mobil.inputan_keterangan ]),
                        Row([
                            #tombol tambah data
                            ElevatedButton(
                                "SIMPAN",
                                    icon = "SAVE_AS",
                                    icon_color = "white",
                                    color = "white",
                                    bgcolor = "GREEN",
                                    width = 280,
                                    height = 50,
                                    on_click = simpan_mobil,
                                )
                        ]),
                        
                    ],
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    scroll = ScrollMode.AUTO
                    #tight = True,
                ),
                padding = 40,
                width = 378,
                height = 500
            ),
            open = False,
            bgcolor = colors.GREY_50
        )

        return Column(
            controls = [
                Row([ElevatedButton("Tambah", on_click = tampil_dialog, icon = icons.ADD, icon_color="white", color = "white", bgcolor = "RED")], alignment = MainAxisAlignment.END),
                Row([mobil.data_mobil], scroll = ScrollMode.ALWAYS),
                mobil.dialog, mobil.snack_bar_berhasil
            ],
            scroll = ScrollMode.ALWAYS
            
        )

class FormJadwalRental(UserControl):
    def build(jadwalrental) :

        # buat variabel inputan
        jadwalrental.inputan_id_jadwalrental = TextField(visible = False, expand = True)
        jadwalrental.inputan_hari_rental = Dropdown(label = "Hari Rental", hint_text = "pilih hari rental ... ", expand = True,
            options=[
                dropdown.Option("Senin"),
                dropdown.Option("Selasa"),
                dropdown.Option("Rabu"),
                dropdown.Option("Kamis"),
                dropdown.Option("Jumat"),
                dropdown.Option("Sabtu"),
                dropdown.Option("Minggu"),
            ],
        )

        # TimePicker untuk jam mulai
        def ubah_jam_mulai(e):
            jam_mulai = str(time_picker_jam_mulai.value)
            jadwalrental.inputan_jam_mulai_rental.value = jam_mulai[:5]
            jadwalrental.update()

        def dismissed_jam_mulai(e):
            jadwalrental.update()

        time_picker_jam_mulai = TimePicker(
            confirm_text = "Konfirmasi",
            cancel_text = "Batal",
            error_invalid_text = "Waktu di luar jangkauan",
            help_text = "Pilih waktu",
            on_change = ubah_jam_mulai,
            on_dismiss = dismissed_jam_mulai,
        )

        # TimePicker untuk jam selesai
        def ubah_jam_selesai(e):
            jam_selesai = str(time_picker_jam_selesai.value)
            jadwalrental.inputan_jam_selesai_rental.value = jam_selesai[:5]
            jadwalrental.update()

        def dismissed_jam_selesai(e):
            jadwalrental.update()

        time_picker_jam_selesai = TimePicker(
            confirm_text = "Konfirmasi",
            error_invalid_text = "Waktu di luar jangkauan",
            help_text = "Pilih waktu",
            on_change = ubah_jam_selesai,
            on_dismiss = dismissed_jam_selesai,
        )

        jadwalrental.inputan_jam_mulai_rental = TextField(label = "Jam Mulai Rental", hint_text = "masukkan jam mulai ... ", expand = True, on_change = lambda _: time_picker_jam_mulai.pick_time())
        jadwalrental.inputan_jam_selesai_rental = TextField(label = "Jam Selesai Rental", hint_text = "masukkan jam selesai ... ", expand = True, on_change = lambda _: time_picker_jam_selesai.pick_time())
        jadwalrental.inputan_lokasi = TextField(
            label = "Lokasi",
            hint_text = "masukkan Lokasi... ",
            expand = True,
            multiline = True,
            max_lines = 3,
            min_lines = 2
        )
        
        cursor.execute("SELECT * FROM mobil ORDER BY id_mobil DESC")
        jadwalrental.inputan_mobil = Dropdown(label = "Jenis Mobil", hint_text = "Pilih jenis mobil ... ", expand = True,
            options=[
            dropdown.Option(row[0], row[2] + ' - ' + row[3]) for row in cursor.fetchall()],
        )

        cursor.execute("SELECT * FROM durasi_sewa ORDER BY id_durasi DESC")
        jadwalrental.inputan_durasisewa = Dropdown(label = "Durasi Sewa", hint_text = "Pilih Durasi Sewa ... ", expand = True,
            options=[
            dropdown.Option(row[0], row[1] + ' - ' + row[2]) for row in cursor.fetchall()],
        )

        jadwalrental.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")

        # memuat tabel data
        def tampil_data(e):
            # Merefresh halaman & menampilkan notif
            jadwalrental.data_jadwalrental.rows.clear()
            cursor.execute("SELECT * FROM jadwal_rental, mobil, durasi_sewa WHERE jadwal_rental.id_mobil = mobil.id_mobil AND jadwal_rental.id_durasi = durasi_sewa.id_durasi ORDER BY id_jadwalrental DESC")
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
            for row in rows:
                jadwalrental.data_jadwalrental.rows.append(
                    DataRow(
                        cells = [
                            DataCell(Text(row['id_jadwalrental'])),
                            DataCell(Text(row['hari_rental'] + ', ' + row['jam_rental'])),
                            DataCell(Text(row['lokasi'])),
                            DataCell(Text(row['durasi_sewa'] + ' (' + row['nama_mobil'] + '(' + row['harga_sewa'] + ')' )),
                            DataCell(
                                Row([
                                    IconButton("delete", icon_color = "red", data = row, on_click = hapus_jadwalrental),
                                    IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah),
                                ])
                            ),
                        ]
                    )
                )
        # fungsi menampilkan dialog form entri
        def tampil_dialog(e):
            jadwalrental.inputan_id_jadwalrental.value = ''
            jadwalrental.inputan_hari_rental.value = ''
            jadwalrental.inputan_jam_mulai_rental.value = ''
            jadwalrental.inputan_jam_selesai_rental.value = ''
            jadwalrental.inputan_lokasi.value = ''
            jadwalrental.inputan_mobil.value = ''
            jadwalrental.inputan_durasisewa.value = ''
            jadwalrental.dialog.open = True
            jadwalrental.update()

        def tampil_dialog_ubah(e):
            jadwalrental.inputan_id_jadwalrental.value = e.control.data['id_jadwalrental']
            jadwalrental.inputan_hari_rental.value = e.control.data['hari_rental']
            jadwalrental.inputan_jam_mulai_rental.value = e.control.data['jam_rental'][:5]
            jadwalrental.inputan_jam_selesai_rental.value = e.control.data['jam_rental'][-5:]
            jadwalrental.inputan_lokasi.value = e.control.data['lokasi']
            jadwalrental.inputan_mobil.value = e.control.data['id_mobil']
            jadwalrental.inputan_durasisewa.value = e.control.data['id_durasi']
            jadwalrental.dialog.open = True
            jadwalrental.update()

        # fungsi simpan data
        def simpan_jadwalrental(e):
            waktu_rental = jadwalrental.inputan_jam_mulai_rental.value + ' sampai ' + jadwalrental.inputan_jam_selesai_rental.value
            try:
                if (jadwalrental.inputan_id_jadwalrental.value == '') :
                    sql = "INSERT INTO jadwal_rental (id_jadwalrental, hari_rental, jam_rental, lokasi, id_mobil, id_durasi) VALUES(%s, %s, %s, %s, %s, %s)"
                    val = ('', jadwalrental.inputan_hari_rental.value, str(waktu_rental), jadwalrental.inputan_lokasi.value, jadwalrental.inputan_mobil.value, jadwalrental.inputan_durasisewa.value)
                else :
                    sql = "UPDATE jadwal_rental SET hari_rental =  %s, jam_rental =  %s, lokasi =  %s, id_mobil =  %s, id_durasi =  %s WHERE id_jadwalrental = %s"
                    val = (jadwalrental.inputan_hari_rental.value, str(waktu_rental), jadwalrental.inputan_lokasi.value, jadwalrental.inputan_mobil.value, jadwalrental.inputan_durasisewa.value, jadwalrental.inputan_id_jadwalrental.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_data(e)
                jadwalrental.dialog.open = False
                jadwalrental.snack_bar_berhasil.open = True
                jadwalrental.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # fungsi hapus data
        def hapus_jadwalrental(e):
            try:
                sql = "DELETE FROM jadwal_rental WHERE id_jadwalrental = %s"
                val = (e.control.data['id_jadwalrental'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                jadwalrental.data_jadwalrental.rows.clear()
                
                tampil_data(e)
                jadwalrental.dialog.open = False
                jadwalrental.snack_bar_berhasil.open = True
                jadwalrental.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        jadwalrental.data_jadwalrental = DataTable(
            columns = [
                DataColumn(Text("ID")),
                DataColumn(Text("Waktu Rental")),
                DataColumn(Text("Lokasi Rental")),
                DataColumn(Text("Jenis Rental")),
                DataColumn(Text("Opsi")),
            ],
        )
        cursor.execute("SELECT * FROM jadwal_rental, mobil, durasi_sewa WHERE jadwal_rental.id_mobil = mobil.id_mobil AND jadwal_rental.id_durasi = durasi_sewa.id_durasi ORDER BY id_jadwalrental DESC")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        for row in rows:
            jadwalrental.data_jadwalrental.rows.append(
                DataRow(
                    cells = [
                        DataCell(Text(row['id_jadwalrental'])),
                        DataCell(Text(row['hari_rental'] + ', ' + row['jam_rental'])),
                        DataCell(Text(row['lokasi'])),
                        DataCell(Text(row['durasi_sewa'] + ' (' + row['nama_mobil'] + '(' + row['harga_sewa'] + ')' )),
                        DataCell(
                            Row([
                                IconButton("delete", icon_color = "red", data = row, on_click = hapus_jadwalrental),
                                IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah),
                            ])
                        ),
                    ]
                )
            )
        
        # buat variabel utk layout data rekapan
        jadwalrental.layout_data = Column()

        # buat form dialog untuk form entri data
        jadwalrental.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Tambah Jadwal Rental", weight = FontWeight.BOLD),
                        Row([ jadwalrental.inputan_id_jadwalrental ]),
                        Row([ jadwalrental.inputan_hari_rental ]),
                        Row([ jadwalrental.inputan_jam_mulai_rental, jadwalrental.inputan_jam_selesai_rental, time_picker_jam_mulai, time_picker_jam_selesai ]),
                        Row([ jadwalrental.inputan_lokasi ]),
                        Row([ jadwalrental.inputan_mobil ]),
                        Row([ jadwalrental.inputan_durasisewa ]),
                        
                        Row([
                            #tombol tambah data
                            ElevatedButton(
                                "SIMPAN",
                                    icon = "SAVE_AS",
                                    icon_color = "white",
                                    color = "white",
                                    bgcolor = "RED",
                                    width = 280,
                                    height = 50,
                                    on_click = simpan_jadwalrental,
                                )
                        ]),
                        
                    ],
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    scroll = ScrollMode.AUTO
                    #tight = True,
                ),
                padding = 40,
                width = 378,
                height = 500
            ),
            open = False,
            bgcolor = colors.GREY_50
        )

        # Fungsi untuk mencari data berdasarkan input pengguna
        def inputsearch(e):
            query = jadwalrental.inputan_cari.value.lower()
            jadwalrental.data_jadwalrental.rows.clear()
            cursor.execute("SELECT * FROM jadwal_rental, mobil, durasi_sewa WHERE jadwal_rental.id_mobil = mobil.id_mobil AND jadwal_rental.id_durasi = durasi_sewa.id_durasi ORDER BY id_jadwalrental DESC")
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns, row)) for row in result]
            for row in rows:
                if query in row['durasi_sewa'].lower():
                    jadwalrental.data_jadwalrental.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(row['id_jadwalrental'])),
                                DataCell(Text(row['hari_rental'] + ', ' + row['jam_rental'])),
                                DataCell(Text(row['lokasi'])),
                                DataCell(Text(row['durasi_sewa'] + ' (' + row['nama_mobil'] +  '(' + row['harga_sewa'] + ')' )),
                                DataCell(
                                    Row([
                                        IconButton("delete", icon_color="red", data=row, on_click=hapus_jadwalrental),
                                        IconButton("create", icon_color="grey", data=row, on_click=tampil_dialog_ubah),
                                    ])
                                ),
                            ]
                        )
                    )
            jadwalrental.update()

        jadwalrental.inputan_cari = TextField(
            label="Cari Data",
            hint_text="masukkan kata kunci ... ",
            expand=True,
            on_change=inputsearch
        )

        return Column(
            controls = [

                Row([jadwalrental.inputan_cari, ElevatedButton("Tambah Jadwal Rental", on_click = tampil_dialog, icon = icons.ADD, icon_color="white", color = "white", bgcolor = "RED")], alignment = MainAxisAlignment.END),
                Row([jadwalrental.data_jadwalrental], scroll = ScrollMode.ALWAYS),
                jadwalrental.dialog, jadwalrental.snack_bar_berhasil
            ],
            scroll = ScrollMode.ALWAYS
            
        )


# fungsi utama
def main (page : Page):
    # mengatur halaman
    page.title = "Aplikasi RENTALYUK"
    page.window_width = 375
    page.window_height = 612
    page.window_resizable = False
    page.window_maximizable = True
    page.window_minimizable = False
    page.scroll = "adaptive"
    #page.theme_mode = "light"
    page.theme_mode = ThemeMode.LIGHT

    # fungsi untuk mode halaman dark/light
    def mode_tema(e):
        page.theme_mode = "light" if page.theme_mode =="dark" else "dark"
        page.update()

    # fungsi untuk routing / pembagian halaman
    def route_change(route):
        page.views.clear()
        page.views.append(
            View("/",
                [
                    AppBar(
                        title = Text("RENTALYUK", size = 18, weight = FontWeight.BOLD, color = colors.WHITE), 
                        bgcolor = 'RED', 
                        center_title = True,
                        actions = [
                            IconButton(icons.WB_SUNNY_OUTLINED, on_click = mode_tema),
                        ],
                    ),
                    Column(
                        [
                            Image(src="rental.png", width=250, height=250),
                            Column(
                                controls = [
                                    ElevatedButton("Durasi Sewa", icon = icons.SCHEDULE_ROUNDED, icon_color="RED", color = "RED", on_click = lambda _: page.go("/durasisewa")),
                                    ElevatedButton("Jenis Mobil", icon = icons.CAR_RENTAL_OUTLINED, icon_color="RED", color = "RED", on_click = lambda _: page.go("/mobil")),
                                    ElevatedButton("Jadwal Rental", icon = icons.CALENDAR_TODAY_ROUNDED, icon_color="RED", color = "RED", on_click = lambda _: page.go("/jadwalrental")),
                                ],
                                width = 375,
                                horizontal_alignment = CrossAxisAlignment.CENTER,
                            ),
                            Text('RENTALYUK @Mobile Programming 2024', size = 12)
                        ],
                        height = 500,
                        #width = 375,
                        alignment = MainAxisAlignment.SPACE_AROUND,
                        horizontal_alignment = CrossAxisAlignment.CENTER,
                    ),
                    
                ],
            )
        )
        if page.route == "/durasisewa":
            page.views.append(
                View("/durasisewa",
                    [
                        AppBar(title = Text("Durasi Sewa", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT),
                        FormDurasiSewa()
                    ],
                )
            )
        elif page.route == "/mobil":
            page.views.append(
                View("/mobil",
                    [
                        AppBar(title = Text("Jenis Mobil", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT),
                        FormMobil()
                    ],
                )
            )
        elif page.route == "/jadwalrental":
            page.views.append(
                View("/jadwalrental",
                    [
                        AppBar(title = Text("Menu Jadwal Rental", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT),
                        FormJadwalRental()
                    ],
                )
            )
        
        page.update()

    # fungsi untuk pop up halaman
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


# mengatur output aplikasi
flet.app(target = main)

