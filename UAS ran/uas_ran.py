# memasukkan library flet ke aplikasi
# import flet as ft
import flet
from flet import *
import datetime
import mysql.connector

# buat koneksi ke database SQL
koneksi_db = mysql.connector.connect(host = "localhost", user = "root", password = "", database = "mp_uas")
cursor = koneksi_db.cursor()

class FormSembako(UserControl):
    # class untuk halaman mata kuliah
    def build(sembako) :
        # buat variabel inputan
        sembako.inputan_id_sembako = TextField(visible = False, expand = True)
        sembako.inputan_nama_sembako = TextField(label = "Nama Sembako", hint_text = "Nama Sembako", expand = True)
        sembako.inputan_harga = TextField(label = "Harga", hint_text = "Harga", expand = True)
        sembako.inputan_quantity = TextField(label = "Quantity", hint_text = "Quantity", expand = True)
        member.inputan_satuan = Dropdown(label = "Satuan", hint_text = "Satuan", expand = True, options=[dropdown.Option("Kg"), dropdown.Option("Ltr")],)
        sembako.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")

        # memuat tabel data
        def tampil_sembako(e):
            # Merefresh halaman & menampilkan notif
            sembako.data_sembako.rows.clear()
            cursor.execute("SELECT * FROM sembako")
            result = cursor.fetchall()
            # menampilkan ulang data 
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
            for row in rows:
                sembako.data_sembako.rows.append(
                    DataRow(
                        cells = [
                            DataCell(Text(row['id_sembako'])),
                            DataCell(Text(row['nama_sembako'])),
                            DataCell(Text(row['harga'])),
                            DataCell(Text(row['quantity'])),
                            DataCell(Text(row['satuan'])),
                            DataCell(
                                Row([
                                    IconButton("EDIT_OUTLINED", icon_color = "grey", data = row,on_click=tampil_dialog_ubah_sembako ),
                                    IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row,on_click=hapus_sembako ),
                                ])
                            ),
                        ]
                        )
                    )

        # fungsi menampilkan dialog form entri
        def tampil_dialog_sembako(e):
            sembako.inputan_id_sembako.value = ''
            sembako.inputan_nama_sembako.value = ''
            sembako.inputan_harga.value = ''
            sembako.inputan_quantity.value = ''
            sembako.inputan_satuan.value = ''
            sembako.dialog.open = True
            sembako.update()

        def tampil_dialog_ubah_sembako(e):
            sembako.inputan_id_sembako.value = e.control.data['id_sembako']
            sembako.inputan_nama_sembako.value = e.control.data['nama_sembako']
            sembako.inputan_harga.value = e.control.data['harga']
            sembako.inputan_quantity.value = e.control.data['quantity']
            sembako.inputan_satuan.value = e.control.data['satuan']
            sembako.dialog.open = True
            sembako.update()

        # fungsi simpan data
        def simpan_sembako(e):
            try:
                if (sembako.inputan_id_sembako.value == '') :
                    sql = "INSERT INTO membership (id_sembako, nama_sembako, harga, quantity, satuan) VALUES(%s, %s, %s, %s, %s)"
                    val = (sembako.inputan_id_sembako.value, sembako.inputan_nama_sembako.value, sembako.inputan_harga.value, sembako.inputan_quantity.value, sembako.inputan_satuan.value)
                else :
                    sql = "UPDATE membership SET nama_sembako = %s, harga = %s, quantity = %s, satuan = %s, WHERE id_sembako = %s"
                    val = (sembako.inputan_nama_sembako.value, sembako.inputan_harga.value, sembako.inputan_quantity.value, sembako.inputan_satuan.value, sembako.inputan_id_sembako.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_sembako(e)
                sembako.dialog.open = False
                sembako.snack_bar_berhasil.open = True
                sembako.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")


        # fungsi hapus data
        def hapus_sembako(e):
            try:
                sql = "DELETE FROM sembako WHERE id = %s"
                val = (e.control.data['id_sembako'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                sembako.data_sembako.rows.clear()
                
                tampil_sembako(e)
                sembako.dialog.open = False
                sembako.snack_bar_berhasil.open = True
                sembako.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # menampilkan semua data ke dalam tabel
        cursor.execute("SELECT * FROM membership")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        member.data_member = DataTable(
            columns = [
                DataColumn(Text("ID")),
                DataColumn(Text("Nama")),
                DataColumn(Text("Jenis Kelamin")),
                DataColumn(Text("Tgl Lahir")),
                DataColumn(Text("Alamat")),
                DataColumn(Text("Telp")),
                DataColumn(Text("Tgl Member")),
                DataColumn(Text("Opsi")),
            ],
        )
        for row in rows:
            member.data_member.rows.append(
                DataRow(
                    cells = [
                            DataCell(Text(row['id'])),
                            DataCell(Text(row['nama'])),
                            DataCell(Text(row['jekel'])),
                            DataCell(Text(row['tgl_lahir'])),
                            DataCell(Text(row['alamat'])),
                            DataCell(Text(row['telp'])),
                            DataCell(Text(row['tgl_member'])),
                        DataCell(
                            Row([
                                IconButton("EDIT_OUTLINED", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_member),
                                IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row, on_click = hapus_member ),
                            ])
                        ),
                    ]
                )
            )

        # buat variabel utk layout data rekapan
        member.layout_data = Column()

        # buat form dialog untuk form entri data
        member.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Entri Data Member", weight = FontWeight.BOLD),
                        Row([ member.inputan_id ]),
                        Row([ member.inputan_nama ]),
                        Row([ member.inputan_jekel ]),
                        Row([ member.inputan_alamat ]),
                        Row([ member.inputan_tgl_lahir, FloatingActionButton(icon=icons.CALENDAR_MONTH, on_click=lambda _: member.opsi_tanggal.pick_date())  ]),
                        Row([ member.inputan_telp ]),
                        Row([ member.inputan_tgl_member, FloatingActionButton(icon=icons.CALENDAR_MONTH, on_click=lambda _: member.opsi_tanggal_member.pick_date()) ]),
                        Row([
                            #tombol tambah data
                            ElevatedButton(
                                "Simpan Data",
                                    icon = "SAVE_AS",
                                    icon_color = "white",
                                    color = "white",
                                    bgcolor = "blue",
                                    width =  250,
                                    height = 50,
                                    on_click = simpan_member,
                                )
                        ]),
                    ],
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    height = 500,
                    scroll= ScrollMode.ALWAYS,
                    #tight = True,
                    

                ),
                padding = 40,
                width = 378,
                height = 500
            ),
            open = False,
            #on_dismiss=bs_dismissed,
        )

   # buat variabel tampilan layout utama
        member.layout_utama = Column(
            [
                Container(
                    Text(
                        "Rekap Data Member",
                        size = 25,
                        # color = "white",
                        weight = FontWeight.BOLD,
                    ),
                    alignment = alignment.center,
                    padding = 30,
                ),
                Container(
                    ElevatedButton(
                        "Tambah Data",
                        icon = "ADD",
                        icon_color = "white",
                        color = "white",
                        bgcolor = "blue",
                        width = 200,
                        on_click = tampil_dialog_member,
                    ),
                    alignment = alignment.center,
                    padding = 10,
                ),
                Row(
                    [member.data_member], scroll=ScrollMode.ALWAYS
                ),
                member.layout_data,
                member.snack_bar_berhasil,
                member.dialog,
                member.opsi_tanggal,
                member.opsi_tanggal_member
            ]
        )

        return member.layout_utama


class Reservasi(UserControl):
    # class untuk halaman mata kuliah
    def build(reservasi) :

        def format_rupiah(angka):
            return f"Rp {angka:,.0f}".replace(',', '.')

        # tgl lhr reservasi
        def ubah_tanggal_lhr(e):
            tgl_baru = reservasi.opsi_tanggal.value
            reservasi.inputan_tanggal_reservasi.value = tgl_baru.date()
            reservasi.update()
            
        def opsi_tanggal_lhr_dismissed(e):
            tgl_baru = reservasi.inputan_tanggal_reservasi.value
            reservasi.inputan_tanggal_reservasi.value = tgl_baru
            reservasi.update()
        
        reservasi.opsi_tanggal = DatePicker(
            on_change=ubah_tanggal_lhr,
            on_dismiss=opsi_tanggal_lhr_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        #input jam
        def ubah_jam(e):
            jam_baru = reservasi.opsi_jam.value
            reservasi.inputan_waktu_reservasi.value = jam_baru.strftime('%H:%M')
            reservasi.update()

        def ubah_jam_dismissed(e):
            jam_baru = reservasi.inputan_waktu_reservasi.value
            reservasi.inputan_waktu_reservasi.value = jam_baru
            reservasi.update()

        reservasi.opsi_jam = TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=ubah_jam,
            on_dismiss=ubah_jam_dismissed,
        )

        # buat variabel inputan
        reservasi.inputan_id_reservasi= TextField(visible = False, expand = True)

        cursor.execute("SELECT * FROM membership")
        reservasi.inputan_id_pelanggan = Dropdown(label = "Nama Pelanggan", hint_text = "Nama Pelanggan", expand = True, options=[dropdown.Option(row[0],row[1] + " - " + row[2]) for row in cursor.fetchall()])
        reservasi.inputan_tanggal_reservasi = TextField(label = "Tanggal Reservasi", hint_text = "Tanggal Reservasi", expand = True)
        reservasi.inputan_waktu_reservasi = TextField(label = "Waktu Reservasi", hint_text = "Waktu Reservasi", expand = True)

        cursor.execute("SELECT * FROM layanan")
        reservasi.inputan_jenis_layanan= Dropdown(label = "Jenis Layanan", hint_text = "Jenis", expand = True, options=[dropdown.Option(row[0], f"{row[1]} - {row[2]}") for row in cursor.fetchall()],)
        reservasi.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")

        # memuat tabel data
        def tampil_reservasi(e):
            # Merefresh halaman & menampilkan notif
            reservasi.data_reservasi.rows.clear()
            cursor.execute("""
                SELECT reservasi.id_reservasi, reservasi.id_pelanggan, membership.nama AS nama_pelanggan, 
                    reservasi.tanggal_reservasi, reservasi.waktu_reservasi, 
                    reservasi.jns_layanan, layanan.jns_layanan AS nama_layanan,
                    layanan.hrg_layanan AS harga_layanan
                FROM reservasi
                JOIN membership ON reservasi.id_pelanggan = membership.id
                JOIN layanan ON reservasi.jns_layanan = layanan.id_layanan
            """)
            result = cursor.fetchall()
            # menampilkan ulang data 
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
            for row in rows:
                reservasi.data_reservasi.rows.append(
                    DataRow(
                        cells = [
                            DataCell(Text(row['id_reservasi'])),
                            DataCell(Text(f"{row['id_pelanggan']} - ({row['nama_pelanggan']})")), 
                            DataCell(Text(row['tanggal_reservasi'])),
                            DataCell(Text(row['waktu_reservasi'])),
                            DataCell(Text(f"{row['jns_layanan']} - ({row['nama_layanan']})")),
                            DataCell(Text(format_rupiah(row['harga_layanan']))),
                            DataCell(
                            Row([
                                IconButton("EDIT_OUTLINED", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_reservasi ),
                                IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row, on_click = hapus_reservasi ),
                            ])),
                        ]
                        )
                    )

        # fungsi menampilkan dialog form entri
        def tampil_dialog_reservasi(e):
            reservasi.inputan_id_reservasi.value = ''
            reservasi.inputan_id_pelanggan.value = ''
            reservasi.inputan_tanggal_reservasi.value = ''
            reservasi.inputan_waktu_reservasi.value = ''
            reservasi.inputan_jenis_layanan.value = ''
            reservasi.dialog.open = True
            reservasi.update()

        def tampil_dialog_ubah_reservasi(e):
            reservasi.inputan_id_reservasi.value = e.control.data['id_reservasi']
            reservasi.inputan_id_pelanggan.value = e.control.data['id_pelanggan']
            reservasi.inputan_tanggal_reservasi.value = e.control.data['tanggal_reservasi']
            reservasi.inputan_waktu_reservasi.value = e.control.data['waktu_reservasi']
            reservasi.inputan_jenis_layanan.value = e.control.data['jns_layanan']
            reservasi.dialog.open = True
            reservasi.update()


        # fungsi simpan data
        def simpan_reservasi(e):
            try:
                if (reservasi.inputan_id_reservasi.value == '') :
                    sql = "INSERT INTO reservasi (id_reservasi, id_pelanggan, tanggal_reservasi, waktu_reservasi, jns_layanan) VALUES(%s, %s, %s, %s, %s)"
                    val = (reservasi.inputan_id_reservasi.value, reservasi.inputan_id_pelanggan.value, reservasi.inputan_tanggal_reservasi.value, reservasi.inputan_waktu_reservasi.value, reservasi.inputan_jenis_layanan.value)
                else :
                    sql = "UPDATE reservasi SET id_pelanggan = %s, tanggal_reservasi = %s, waktu_reservasi = %s, jns_layanan = %s WHERE id_reservasi = %s"
                    val = (reservasi.inputan_id_pelanggan.value, reservasi.inputan_tanggal_reservasi.value, reservasi.inputan_waktu_reservasi.value, reservasi.inputan_jenis_layanan.value, reservasi.inputan_id_reservasi.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_reservasi(e)
                reservasi.dialog.open = False
                reservasi.snack_bar_berhasil.open = True
                reservasi.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")


        # fungsi hapus data
        def hapus_reservasi(e):
            try:
                sql = "DELETE FROM reservasi WHERE id_reservasi = %s"
                val = (e.control.data['id_reservasi'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                reservasi.data_reservasi.rows.clear()
                
                tampil_reservasi(e)
                reservasi.dialog.open = False
                reservasi.snack_bar_berhasil.open = True
                reservasi.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # menampilkan semua data ke dalam tabel
        cursor.execute("""
            SELECT reservasi.id_reservasi, reservasi.id_pelanggan, membership.nama AS nama_pelanggan, 
                reservasi.tanggal_reservasi, reservasi.waktu_reservasi, 
                reservasi.jns_layanan, layanan.jns_layanan AS nama_layanan,
                layanan.hrg_layanan AS harga_layanan
            FROM reservasi
            JOIN membership ON reservasi.id_pelanggan = membership.id
            JOIN layanan ON reservasi.jns_layanan = layanan.id_layanan
        """)
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        reservasi.data_reservasi = DataTable(
            columns = [
                DataColumn(Text("ID Reservasi")),
                DataColumn(Text("ID Pelanggan")),
                DataColumn(Text("Tanggal Reservasi")),
                DataColumn(Text("Waktu Reservasi")),
                DataColumn(Text("Jenis Layanan")),
                DataColumn(Text("Total Harga")),
                DataColumn(Text("Opsi")),
            ],
        )
        for row in rows:
            reservasi.data_reservasi.rows.append(
                DataRow(
                    cells = [
                            DataCell(Text(row['id_reservasi'])),
                            DataCell(Text(f"{row['id_pelanggan']} - ({row['nama_pelanggan']})")), 
                            DataCell(Text(row['tanggal_reservasi'])),
                            DataCell(Text(row['waktu_reservasi'])),
                            DataCell(Text(f"{row['jns_layanan']} - ({row['nama_layanan']})")),
                            DataCell(Text(format_rupiah(row['harga_layanan']))),
                            DataCell(
                                Row([
                                    IconButton("EDIT_OUTLINED", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_reservasi ),
                                    IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row, on_click = hapus_reservasi ),
                                ])
                                ),
                    ]
                )
            )

        # buat variabel utk layout data rekapan
        reservasi.layout_data = Column()


        # buat form dialog untuk form entri data
        reservasi.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Entri Data Reservasi", weight = FontWeight.BOLD),
                        Row([ reservasi.inputan_id_reservasi ]),
                        Row([ reservasi.inputan_id_pelanggan ]),
                        Row([ reservasi.inputan_tanggal_reservasi, FloatingActionButton(icon=icons.CALENDAR_MONTH, on_click=lambda _: reservasi.opsi_tanggal.pick_date())  ]),
                        Row([ reservasi.inputan_waktu_reservasi,FloatingActionButton(icon=icons.ACCESS_TIME, on_click=lambda _: reservasi.opsi_jam.pick_time()) ]),
                        Row([ reservasi.inputan_jenis_layanan ]),
                        Row([
                            #tombol tambah data
                            ElevatedButton(
                                "Simpan Data",
                                    icon = "SAVE_AS",
                                    icon_color = "white",
                                    color = "white",
                                    bgcolor = "blue",
                                    width =  250,
                                    height = 50,
                                    on_click = simpan_reservasi,
                                )
                        ]),
                    ],
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    height = 500,
                    scroll= ScrollMode.ALWAYS,
                    #tight = True,
                    

                ),
                padding = 40,
                width = 378,
                height = 500
            ),
            open = False,
            #on_dismiss=bs_dismissed,
        )


   # buat variabel tampilan layout utama
        reservasi.layout_utama = Column(
            [
                Container(
                    Text(
                        "Rekap Data Reservasi",
                        size = 23,
                        # color = "white",
                        weight = FontWeight.BOLD,
                    ),
                    alignment = alignment.center,
                    padding = 30,
                ),
                Container(
                    ElevatedButton(
                        "Tambah Data",
                        icon = "ADD",
                        icon_color = "white",
                        color = "white",
                        bgcolor = "blue",
                        width = 200,
                        on_click = tampil_dialog_reservasi,
                    ),
                    alignment = alignment.center,
                    padding = 10,
                ),

                Row(
                    [reservasi.data_reservasi], scroll=ScrollMode.ALWAYS
                ),
                reservasi.layout_data,
                reservasi.opsi_tanggal,
                reservasi.opsi_jam,
                reservasi.snack_bar_berhasil,
                reservasi.dialog,
            ]
        )

        return reservasi.layout_utama


class FormPembeli(UserControl):
    # class untuk halaman mata kuliah
    def build(pembeli) :

        def format_rupiah(angka):
            return f"Rp {angka:,.0f}".replace(',', '.')

        # buat variabel inputan
        pembeli.inputan_id_pembeli= TextField(visible = False, expand = True)
        pembeli.inputan_nama_pembeli= TextField(label = "Nama Pembeli", hint_text = "Nama", expand = True )
        pembeli.inputan_jk_pembeli = Dropdown(label = "Jenis Kelamin", hint_text = "Jk", expand = True, options=[dropdown.Option("pria"), dropdown.Option("wanita")])
        pembeli.inputan_alamat = TextField(label = "Alamat", hint_text = "Alamat", expand = True)
        pembeli.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")

        # memuat tabel data
        def tampil_pembeli(e):
            # Merefresh halaman & menampilkan notif
            pembeli.data_pembeli.rows.clear()
            cursor.execute("SELECT * FROM pembeli")
            result = cursor.fetchall()
            # menampilkan ulang data 
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
            for row in rows:
                pembeli.data_pembeli.rows.append(
                    DataRow(
                        cells = [
                            DataCell(Text(row['id_pembeli'])),
                            DataCell(Text(row['nama_pembeli'])),
                            DataCell(Text(row['jk_pembeli'])),
                            DataCell(Text(row['alamat'])),
                            DataCell(
                                Row([
                                    IconButton("EDIT_OUTLINED", icon_color = "grey", data = row, on_click=tampil_dialog_ubah_pembeli ),
                                    IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row, on_click=hapus_pembeli ),
                                ])
                            ),
                        ]
                        )
                    )

        # fungsi menampilkan dialog form entri
        def tampil_dialog_pembeli(e):
            pembeli.inputan_id_pembeli.value = ''
            pembeli.inputan_nama_pembeli.value = ''
            pembeli.inputan_jk_pembeli.value = ''
            pembeli.inputan_alamat.value = ''
            pembeli.dialog.open = True
            pembeli.update()

        def tampil_dialog_ubah_pembeli(e):
            pembeli.inputan_id_pembeli.value = e.control.data['id_pembeli']
            pembeli.inputan_nama_pembeli.value = e.control.data['nama_pembeli']
            pembeli.inputan_jk_pembeli.value = e.control.data['jk_pembeli']
            pembeli.inputan_alamat.value = e.control.data['alamat']
            pembeli.dialog.open = True
            pembeli.update()

        # fungsi simpan data
        def simpan_pembeli(e):
            try:
                if (pembeli.inputan_id_pembeli.value == '') :
                    sql = "INSERT INTO pembeli (id_pembeli, nama_pembeli, jk_pembeli, alamat ) VALUES(%s, %s, %s, %s)"
                    val = (pembeli.inputan_id_pembeli.value, pembeli.inputan_nama_pembeli.value, pembeli.inputan_jk_pembeli.value, pembeli.inputan_alamat.value)
                else :
                    sql = "UPDATE pembeli SET nama_pembeli = %s, jk_pembeli = %s, alamat = %s WHERE id_pembeli = %s"
                    val = (pembeli.inputan_nama_pembeli.value, pembeli.inputan_jk_pembeli.value, pembeli.inputan_alamat.value, pembeli.inputan_id_pembeli.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_pembeli(e)
                pembeli.dialog.open = False
                pembeli.snack_bar_berhasil.open = True
                pembeli.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")


        # fungsi hapus data
        def hapus_pembeli(e):
            try:
                sql = "DELETE FROM pembeli WHERE id_pembeli = %s"
                val = (e.control.data['id_pembeli'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                pembeli.data_pembeli.rows.clear()
                
                tampil_pembeli(e)
                pembeli.dialog.open = False
                pembeli.snack_bar_berhasil.open = True
                pembeli.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # menampilkan semua data ke dalam tabel
        cursor.execute("SELECT * FROM pembeli")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        pembeli.data_pembeli = DataTable(
            columns = [
                DataColumn(Text("ID Pembeli")),
                DataColumn(Text("Nama Pembeli")),
                DataColumn(Text("JK Pembeli")),
                DataColumn(Text("Alamat")),
                DataColumn(Text("Opsi")),
            ],
        )
        for row in rows:
            pembeli.data_pembeli.rows.append(
                DataRow(
                    cells = [
                            DataCell(Text(row['id_pembeli'])),
                            DataCell(Text(row['nama_pembeli'])),
                            DataCell(Text(row['jk_pembeli'])),
                            DataCell(Text(row['alamat'])),
                        DataCell(
                            Row([
                                IconButton("EDIT_OUTLINED", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_pembeli),
                                IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row, on_click = hapus_pembeli ),
                            ])
                        ),
                    ]
                )
            )

        # buat variabel utk layout data rekapan
        pembeli.layout_data = Column()

        # buat form dialog untuk form entri data
        pembeli.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Entri Data Pembeli", weight = FontWeight.BOLD),
                        Row([ pembeli.inputan_id_pembeli ]),
                        Row([ pembeli.inputan_nama_pembeli ]),
                        Row([ pembeli.inputan_jk_pembeli ]),
                        Row([ pembeli.inputan_alamat ]),
                        Row([
                            #tombol tambah data
                            ElevatedButton(
                                "Simpan Data",
                                    icon = "SAVE_AS",
                                    icon_color = "white",
                                    color = "white",
                                    bgcolor = "blue",
                                    width =  250,
                                    height = 50,
                                    on_click = simpan_pembeli,
                                )
                        ]),
                    ],
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    height = 500,
                    scroll= ScrollMode.ALWAYS,
                    #tight = True,
                    

                ),
                padding = 40,
                width = 378,
                height = 500
            ),
            open = False,
            #on_dismiss=bs_dismissed,
        )

   # buat variabel tampilan layout utama
        pembeli.layout_utama = Column(
            [
                Container(
                    Text(
                        "Rekap Data Pembeli",
                        size = 25,
                        # color = "White",
                        weight = FontWeight.BOLD,
                    ),
                    alignment = alignment.center,
                    padding = 30,
                ),
                Container(
                    ElevatedButton(
                        "Tambah Data",
                        icon = "ADD",
                        icon_color = "white",
                        color = "white",
                        bgcolor = "blue",
                        width = 200,
                        on_click = tampil_dialog_pembeli,
                    ),
                    alignment = alignment.center,
                    padding = 10,
                ),
                Row(
                    [pembeli.data_pembeli], scroll=ScrollMode.ALWAYS
                ),
                pembeli.layout_data,
                pembeli.snack_bar_berhasil,
                pembeli.dialog,
            ]
        )

        return pembeli.layout_utama



# fungsi utama
def main (page : Page):
    # mengatur halaman
    page.title = "Penjualan Sembako"
    page.window_width = 350
    page.window_height = 700
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = True
    page.scroll = "adaptive"
    #page.theme_mode = "light"
    page.theme_mode = ThemeMode.DARK

    # fungsi untuk mode halaman dark/light
    def mode_tema(e):
        page.theme_mode = "dark" if page.theme_mode =="light" else "light"
        page.update()

    # fungsi untuk routing / pembagian halaman
    def route_change(route):
        page.views.clear()
        page.views.append(
            View("/",
                [
                    AppBar(
                        title = Text("Aplikasi CRUD Penjualan Sembako", size = 18, weight = FontWeight.BOLD, color = colors.WHITE), 
                        bgcolor = colors.BLUE_800, 
                        center_title = True,
                    ),
                    Column( 
                        [
                            Image(src="reference/ssss.png",width=180 ),
                            # Icon(name = icons.CAST_FOR_EDUCATION, color = colors.BLUE, size = 180),
                            Column(
                                controls = [
                                    ElevatedButton("Menu Reservasi", icon = icons.TABLE_ROWS, on_click = lambda _: page.go("/reservasi"), width=205),
                                    ElevatedButton("Menu Membership", icon = icons.PEOPLE_ROUNDED, on_click = lambda _: page.go("/member"), width=205 ),
                                    ElevatedButton("Menu Pembeli", icon = icons.PEOPLE_ROUNDED, on_click = lambda _: page.go("/pembeli"), width=205 ),
                                    ElevatedButton("Menu Jadwal Kuliah", icon = icons.SCHEDULE_ROUNDED, on_click = lambda _: page.go("/jadwalkuliah"), disabled=True, width=205, visible=False ),
                                ],
                                width = 375,
                                horizontal_alignment = CrossAxisAlignment.CENTER,
                            ),

                        ],
                        height = 500,
                        width = 375,
                        alignment = MainAxisAlignment.SPACE_AROUND,
                        horizontal_alignment = CrossAxisAlignment.CENTER,
                    ),
                    Column(
                        [
                            Column(
                                controls = [
                                    ElevatedButton("Mode Warna", icon = icons.WB_SUNNY_OUTLINED, on_click = mode_tema),
                                ],
                                width = 375,
                                horizontal_alignment = CrossAxisAlignment.CENTER,
                            ),
                            Text('Mobile Programming - Fattah Barbershop @2024', size = 12)
                        ],
                        horizontal_alignment = CrossAxisAlignment.CENTER,
                    ),
                    
                ],
            )
        )
        if page.route == "/member":
            page.views.append(
                View("/member",
                    [
                        AppBar(title = Text("Menu Membership", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT ),
                        FormMember()
                    ],
                )
            )
        if page.route == "/reservasi":
            page.views.append(
                View("/reservasi",
                    [
                        AppBar(title = Text("Menu Reservasi", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT ),
                        Reservasi()
                    ],
                )
            )
        if page.route == "/pembeli":
            page.views.append(
                View("/pembeli",
                    [
                        AppBar(title = Text("Menu Layanan", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT),
                        FormPembeli()
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
