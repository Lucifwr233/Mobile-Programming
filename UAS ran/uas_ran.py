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
        def format_rupiah(angka):
            return f"Rp {angka:,.0f}".replace(',', '.')
        # buat variabel inputan
        sembako.inputan_id_sembako = TextField(visible = False, expand = True)
        sembako.inputan_nama_sembako = TextField(label = "Nama Sembako", hint_text = "Nama Sembako", expand = True)
        sembako.inputan_harga = TextField(label = "Harga", hint_text = "Harga", expand = True)
        sembako.inputan_quantity = TextField(label = "Quantity", hint_text = "Quantity", expand = True)
        sembako.inputan_satuan = Dropdown(label = "Satuan", hint_text = "Satuan", expand = True, options=[dropdown.Option("Kg"), dropdown.Option("L")],)
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
                            DataCell(Text(format_rupiah(row['harga']))),
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
                    sql = "INSERT INTO sembako (id_sembako, nama_sembako, harga, quantity, satuan) VALUES(%s, %s, %s, %s, %s)"
                    val = (sembako.inputan_id_sembako.value, sembako.inputan_nama_sembako.value, sembako.inputan_harga.value, sembako.inputan_quantity.value, sembako.inputan_satuan.value)
                else :
                    sql = "UPDATE sembako SET nama_sembako = %s, harga = %s, quantity = %s, satuan = %s WHERE id_sembako= %s"
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
        cursor.execute("SELECT * FROM sembako")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        sembako.data_sembako = DataTable(
            columns = [
                DataColumn(Text("ID Sembako")),
                DataColumn(Text("Nama Sembako")),
                DataColumn(Text("Harga")),
                DataColumn(Text("Quantity")),
                DataColumn(Text("Satuan")),
                DataColumn(Text("Opsi")),
            ],
        )
        for row in rows:
            sembako.data_sembako.rows.append(
                DataRow(
                    cells = [
                            DataCell(Text(row['id_sembako'])),
                            DataCell(Text(row['nama_sembako'])),
                            DataCell(Text(format_rupiah(row['harga']))),
                            DataCell(Text(row['quantity'])),
                            DataCell(Text(row['satuan'])),
                        DataCell(
                            Row([
                                IconButton("EDIT_OUTLINED", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_sembako),
                                IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row, on_click = hapus_sembako ),
                            ])
                        ),
                    ]
                )
            )

        # buat variabel utk layout data rekapan
        sembako.layout_data = Column()

        # buat form dialog untuk form entri data
        sembako.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Entri Data Sembako", weight = FontWeight.BOLD),
                        Row([ sembako.inputan_id_sembako ]),
                        Row([ sembako.inputan_nama_sembako ]),
                        Row([ sembako.inputan_harga ]),
                        Row([ sembako.inputan_quantity ]),
                        Row([ sembako.inputan_satuan ]),
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
                                    on_click = simpan_sembako,
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

        # Fungsi untuk mencari data berdasarkan input pengguna
        def inputsearch(e):
            query = sembako.inputan_cari.value.lower()
            sembako.data_sembako.rows.clear()
            cursor.execute("SELECT * FROM sembako ORDER BY id_sembako DESC")
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns, row)) for row in result]
            for row in rows:
                if query in row['nama_sembako'].lower():
                    sembako.data_sembako.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(row['id_sembako'])),
                                DataCell(Text(row['nama_sembako'])),
                                DataCell(Text(format_rupiah(row['harga']))),
                                DataCell(Text(row['quantity'])),
                                DataCell(Text(row['satuan'])),
                                DataCell(
                                    Row([
                                        IconButton("EDIT_OUTLINED", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_sembako),
                                        IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row, on_click = hapus_sembako ),
                                    ])
                                ),
                            ]
                        )
                    )
            sembako.update()

        sembako.inputan_cari = TextField(
            label="Cari Data",
            hint_text="Masukkan Nama Sembako",
            expand=True,
            on_change=inputsearch
        )

   # buat variabel tampilan layout utama
        sembako.layout_utama = Column(
            [
                Container(
                    Text(
                        "Rekap Data Sembako",
                        size = 25,
                        # color = "white",
                        weight = FontWeight.BOLD,
                    ),
                    alignment = alignment.center,
                    padding = 30,
                ),
                Container(
                    sembako.inputan_cari,
                ),
                Container(
                    ElevatedButton(
                        "Tambah Data",
                        icon = "ADD",
                        icon_color = "white",
                        color = "white",
                        bgcolor = "blue",
                        width = 200,
                        on_click = tampil_dialog_sembako,
                    ),
                    alignment = alignment.center,
                    padding = 10,
                ),
                Row(
                    [sembako.data_sembako], scroll=ScrollMode.ALWAYS
                ),
                sembako.layout_data,
                sembako.snack_bar_berhasil,
                sembako.dialog,
            ]
        )

        return sembako.layout_utama


class FormPenjualan(UserControl):
    # class untuk halaman mata kuliah
    def build(penjualan) :

        def format_rupiah(angka):
            return f"Rp {angka:,.0f}".replace(',', '.')

        # tgl lhr penjualan
        def ubah_tanggal_lhr(e):
            tgl_baru = penjualan.opsi_tanggal.value
            penjualan.inputan_tanggal_penjualan.value = tgl_baru.date()
            penjualan.update()
            
        def opsi_tanggal_lhr_dismissed(e):
            tgl_baru = penjualan.inputan_tanggal_penjualan.value
            penjualan.inputan_tanggal_penjualan.value = tgl_baru
            penjualan.update()
        
        penjualan.opsi_tanggal = DatePicker(
            on_change=ubah_tanggal_lhr,
            on_dismiss=opsi_tanggal_lhr_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        # #input jam
        # def ubah_jam(e):
        #     jam_baru = reservasi.opsi_jam.value
        #     reservasi.inputan_waktu_reservasi.value = jam_baru.strftime('%H:%M')
        #     reservasi.update()

        # def ubah_jam_dismissed(e):
        #     jam_baru = reservasi.inputan_waktu_reservasi.value
        #     reservasi.inputan_waktu_reservasi.value = jam_baru
        #     reservasi.update()

        # reservasi.opsi_jam = TimePicker(
        #     confirm_text="Confirm",
        #     error_invalid_text="Time out of range",
        #     help_text="Pick your time slot",
        #     on_change=ubah_jam,
        #     on_dismiss=ubah_jam_dismissed,
        # )

        # buat variabel inputan
        penjualan.inputan_id_penjualan= TextField(visible = False, expand = True)
        penjualan.inputan_tanggal_penjualan = TextField(label = "Tanggal Penjualan", hint_text = "Tanggal Penjualan", expand = True)
        penjualan.inputan_kasir = TextField(label = "Kasir", hint_text = "Kasir", expand = True)

        cursor.execute("SELECT * FROM pembeli")
        penjualan.inputan_id_pembeli= Dropdown(label = "Nama Pembeli", hint_text = "Nama Pembeli", expand = True, options=[dropdown.Option(row[0], f"{row[1]} - {row[2]}") for row in cursor.fetchall()],)

        cursor.execute("SELECT * FROM sembako")
        penjualan.inputan_id_sembako = Dropdown(label = "Nama Sembako", hint_text = "Nama Sembako", expand = True, options=[dropdown.Option(row[0], f"{row[1]} - {row[2]}") for row in cursor.fetchall()])
        penjualan.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")

        # memuat tabel data
        def tampil_penjualan(e):
            # Merefresh halaman & menampilkan notif
            penjualan.data_penjualan.rows.clear()
            cursor.execute("""
                SELECT penjualan.id_penjualan, penjualan.tanggal, penjualan.kasir, 
                    pembeli.id_pembeli, pembeli.nama_pembeli,
                    sembako.id_sembako, sembako.nama_sembako
                FROM penjualan
                JOIN pembeli ON penjualan.id_pembeli = pembeli.id_pembeli
                JOIN sembako ON penjualan.id_sembako = sembako.id_sembako
            """)
            result = cursor.fetchall()
            # menampilkan ulang data 
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
            for row in rows:
                penjualan.data_penjualan.rows.append(
                    DataRow(
                        cells = [
                            DataCell(Text(row['id_penjualan'])),
                            DataCell(Text(row['tanggal'])),
                            DataCell(Text(row['kasir'])),
                            DataCell(Text(f"({row['nama_pembeli']})")), 
                            DataCell(Text(f"({row['nama_sembako']})")),
                            DataCell(
                            Row([
                                IconButton("EDIT_OUTLINED", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_penjualan ),
                                IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row, on_click = hapus_penjualan ),
                            ])),
                        ]
                        )
                    )

        # fungsi menampilkan dialog form entri
        def tampil_dialog_penjualan(e):
            penjualan.inputan_id_penjualan.value = ''
            penjualan.inputan_tanggal_penjualan.value = ''
            penjualan.inputan_kasir.value = ''
            penjualan.inputan_id_pembeli.value = ''
            penjualan.inputan_id_sembako.value = ''
            penjualan.dialog.open = True
            penjualan.update()

        def tampil_dialog_ubah_penjualan(e):
            penjualan.inputan_id_penjualan.value = e.control.data['id_penjualan']
            penjualan.inputan_tanggal_penjualan.value = e.control.data['tanggal']
            penjualan.inputan_kasir.value = e.control.data['kasir']
            penjualan.inputan_id_pembeli.value = e.control.data['id_pembeli']
            penjualan.inputan_id_sembako.value = e.control.data['id_sembako']
            penjualan.dialog.open = True
            penjualan.update()


        # fungsi simpan data
        def simpan_penjualan(e):
            try:
                if (penjualan.inputan_id_penjualan.value == '') :
                    sql = "INSERT INTO penjualan (id_penjualan, tanggal, kasir, id_pembeli , id_sembako) VALUES(%s, %s, %s, %s, %s)"
                    val = (penjualan.inputan_id_penjualan.value, penjualan.inputan_tanggal_penjualan.value, penjualan.inputan_kasir.value, penjualan.inputan_id_pembeli.value, penjualan.inputan_id_sembako.value)
                else :
                    sql = "UPDATE penjualan SET tanggal = %s, kasir = %s, id_pembeli = %s, id_sembako = %s WHERE id_penjualan = %s"
                    val = (penjualan.inputan_tanggal_penjualan.value, penjualan.inputan_kasir.value, penjualan.inputan_id_pembeli.value, penjualan.inputan_id_sembako.value, penjualan.inputan_id_penjualan.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_penjualan(e)
                penjualan.dialog.open = False
                penjualan.snack_bar_berhasil.open = True
                penjualan.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")


        # fungsi hapus data
        def hapus_penjualan(e):
            try:
                sql = "DELETE FROM penjualan WHERE id_penjualan = %s"
                val = (e.control.data['id_penjualan'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                penjualan.data_penjualan.rows.clear()
                
                tampil_penjualan(e)
                penjualan.dialog.open = False
                penjualan.snack_bar_berhasil.open = True
                penjualan.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # menampilkan semua data ke dalam tabel
        cursor.execute("""
            SELECT penjualan.id_penjualan, penjualan.tanggal, penjualan.kasir, 
                pembeli.id_pembeli, pembeli.nama_pembeli,
                sembako.id_sembako, sembako.nama_sembako
            FROM penjualan
            JOIN pembeli ON penjualan.id_pembeli = pembeli.id_pembeli
            JOIN sembako ON penjualan.id_sembako = sembako.id_sembako
        """)
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        penjualan.data_penjualan = DataTable(
            columns = [
                DataColumn(Text("ID Penjualan")),
                DataColumn(Text("Tanggal")),
                DataColumn(Text("Kasir")),
                DataColumn(Text("ID Pembeli")),
                DataColumn(Text("ID Sembako")),
                DataColumn(Text("Opsi")),
            ],
        )
        for row in rows:
            penjualan.data_penjualan.rows.append(
                DataRow(
                    cells = [
                            DataCell(Text(row['id_penjualan'])),
                            DataCell(Text(row['tanggal'])),
                            DataCell(Text(row['kasir'])),
                            DataCell(Text(f"{row['nama_pembeli']}")), 
                            DataCell(Text(f"{row['nama_sembako']}")),
                            DataCell(
                                Row([
                                    IconButton("EDIT_OUTLINED", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_penjualan ),
                                    IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row, on_click = hapus_penjualan ),
                                ])
                                ),
                    ]
                )
            )

        # buat variabel utk layout data rekapan
        penjualan.layout_data = Column()


        # buat form dialog untuk form entri data
        penjualan.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Entri Data Penjualan", weight = FontWeight.BOLD),
                        Row([ penjualan.inputan_id_penjualan ]),
                        Row([ penjualan.inputan_tanggal_penjualan, FloatingActionButton(icon=icons.CALENDAR_MONTH, on_click=lambda _: penjualan.opsi_tanggal.pick_date())  ]),
                        Row([ penjualan.inputan_kasir ]),
                        # Row([ penjualan.inputan_waktu_reservasi,FloatingActionButton(icon=icons.ACCESS_TIME, on_click=lambda _: reservasi.opsi_jam.pick_time()) ]),
                        Row([ penjualan.inputan_id_pembeli ]),
                        Row([ penjualan.inputan_id_sembako ]),
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
                                    on_click = simpan_penjualan,
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


        # Fungsi untuk mencari data berdasarkan input pengguna
        def inputsearch(e):
            query = penjualan.inputan_cari.value.lower()
            penjualan.data_penjualan.rows.clear()
            cursor.execute("""
                SELECT penjualan.id_penjualan, penjualan.tanggal, penjualan.kasir, 
                    pembeli.id_pembeli, pembeli.nama_pembeli,
                    sembako.id_sembako, sembako.nama_sembako
                FROM penjualan
                JOIN pembeli ON penjualan.id_pembeli = pembeli.id_pembeli
                JOIN sembako ON penjualan.id_sembako = sembako.id_sembako
            """)
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns, row)) for row in result]
            for row in rows:
                if query in row['kasir'].lower():
                    penjualan.data_penjualan.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(row['id_penjualan'])),
                                DataCell(Text(row['tanggal'])),
                                DataCell(Text(row['kasir'])),
                                DataCell(Text(f"{row['nama_pembeli']}")), 
                                DataCell(Text(f"{row['nama_sembako']}")),
                                DataCell(
                                    Row([
                                        IconButton("EDIT_OUTLINED", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_penjualan ),
                                        IconButton("DELETE_OUTLINE_OUTLINED", icon_color = "red", data = row, on_click = hapus_penjualan ),
                                    ])
                                ),
                            ]
                        )
                    )
            penjualan.update()

        penjualan.inputan_cari = TextField(
            label="Cari Data",
            hint_text="Masukkan Nama Kasir",
            expand=True,
            on_change=inputsearch
        )


   # buat variabel tampilan layout utama
        penjualan.layout_utama = Column(
            [
                Container(
                    Text(
                        "Rekap Data Penjualan",
                        size = 23,
                        # color = "white",
                        weight = FontWeight.BOLD,
                    ),
                    alignment = alignment.center,
                    padding = 30,
                ),
                Container(
                    penjualan.inputan_cari,
                ),
                Container(
                    ElevatedButton(
                        "Tambah Data",
                        icon = "ADD",
                        icon_color = "white",
                        color = "white",
                        bgcolor = "blue",
                        width = 200,
                        on_click = tampil_dialog_penjualan,
                    ),
                    alignment = alignment.center,
                    padding = 10,
                ),

                Row(
                    [penjualan.data_penjualan], scroll=ScrollMode.ALWAYS
                ),
                penjualan.layout_data,
                penjualan.opsi_tanggal,
                # penjualan.opsi_jam,
                penjualan.snack_bar_berhasil,
                penjualan.dialog,
            ]
        )

        return penjualan.layout_utama


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

        # Fungsi untuk mencari data berdasarkan input pengguna
        def inputsearch(e):
            query = pembeli.inputan_cari.value.lower()
            pembeli.data_pembeli.rows.clear()
            cursor.execute("SELECT * FROM pembeli ORDER BY id_pembeli DESC")
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns, row)) for row in result]
            for row in rows:
                if query in row['nama_pembeli'].lower():
                    pembeli.data_pembeli.rows.append(
                        DataRow(
                            cells=[
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
            pembeli.update()

        pembeli.inputan_cari = TextField(
            label="Cari Data",
            hint_text="Masukkan Nama Pembeli",
            expand=True,
            on_change=inputsearch
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
                    pembeli.inputan_cari,
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
                            Image(src="image.png",width=200 ),
                            # Icon(name = icons.CAST_FOR_EDUCATION, color = colors.BLUE, size = 180),
                            Column(
                                controls = [
                                    ElevatedButton("Menu Penjualan", icon = icons.TABLE_ROWS, on_click = lambda _: page.go("/penjualan"), width=205),
                                    ElevatedButton("Menu Sembako", icon = icons.PEOPLE_ROUNDED, on_click = lambda _: page.go("/sembako"), width=205 ),
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
                            Text('Mobile Programming - Sembako @2024', size = 12)
                        ],
                        horizontal_alignment = CrossAxisAlignment.CENTER,
                    ),
                    
                ],
            )
        )
        if page.route == "/sembako":
            page.views.append(
                View("/sembako",
                    [
                        AppBar(title = Text("Menu Sembako", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT ),
                        FormSembako()
                    ],
                )
            )
        if page.route == "/penjualan":
            page.views.append(
                View("/penjualan",
                    [
                        AppBar(title = Text("Menu Penjualan", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT ),
                        FormPenjualan()
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
