# memasukkan library flet ke aplikasi
# import flet as ft
import flet
from flet import *
import datetime
import mysql.connector

# buat koneksi ke database SQL
koneksi_db = mysql.connector.connect(host = "localhost", user = "root", password = "", database = "mp_appcrudsql")
cursor = koneksi_db.cursor()

class FormMahasiswa(UserControl):
    # class untuk halaman mata kuliah
    def build(mahasiswa) :

        # buat variabel inputan
        mahasiswa.inputan_id_mahasiswa = TextField(visible = False, expand = True)
        mahasiswa.inputan_nama_mhs = TextField(label = "Nama", hint_text = "Nama ", expand = True)
        mahasiswa.inputan_age_mhs = TextField(label = "Umur", hint_text = "Umur", expand = True)
        mahasiswa.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")
        
        # memuat tabel data
        def tampil_data_mahasiswa(e):
            # Merefresh halaman & menampilkan notif
            mahasiswa.data_mahasiswa.rows.clear()
            cursor.execute("SELECT * FROM mahasiswa")
            result = cursor.fetchall()
            # menampilkan ulang data 
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
            for row in rows:
                mahasiswa.data_mahasiswa.rows.append(
                    DataRow(
                        cells = [
                            DataCell(Text(row['id'])),
                            DataCell(Text(row['name'])),
                            DataCell(Text(row['age'])),
                            DataCell(
                                Row([
                                    IconButton("delete", icon_color = "red", data = row, on_click = hapus_mahasiswa),
                                    IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_mahasiswa),
                                ])
                            ),
                        ]
                        )
                    )
        # fungsi menampilkan dialog form entri
        def tampil_dialog_mahasiswa(e):
            mahasiswa.inputan_id_mahasiswa.value = ''
            mahasiswa.inputan_nama_mhs.value = ''
            mahasiswa.inputan_age_mhs.value = ''
            mahasiswa.dialog.open = True
            mahasiswa.update()

        def tampil_dialog_ubah_mahasiswa(e):
            mahasiswa.inputan_id_mahasiswa.value = e.control.data['id']
            mahasiswa.inputan_nama_mhs.value = e.control.data['name']
            mahasiswa.inputan_age_mhs.value = e.control.data['age']
            mahasiswa.dialog.open = True
            mahasiswa.update()

        # fungsi simpan data
        def simpan_mahasiswa(e):
            try:
                if (mahasiswa.inputan_id_mahasiswa.value == '') :
                    sql = "INSERT INTO mahasiswa (name, age) VALUES(%s, %s)"
                    val = (mahasiswa.inputan_nama_mhs.value, mahasiswa.inputan_age_mhs.value)
                else :
                    sql = "UPDATE mahasiswa SET name = %s, age = %s WHERE id = %s"
                    val = (mahasiswa.inputan_nama_mhs.value, mahasiswa.inputan_age_mhs.value, mahasiswa.inputan_id_mahasiswa.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_data_mahasiswa(e)
                mahasiswa.dialog.open = False
                mahasiswa.snack_bar_berhasil.open = True
                mahasiswa.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # fungsi hapus data
        def hapus_mahasiswa(e):
            try:
                sql = "DELETE FROM mahasiswa WHERE id = %s"
                val = (e.control.data['id'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                mahasiswa.data_mahasiswa.rows.clear()
                
                tampil_data_mahasiswa(e)
                mahasiswa.dialog.open = False
                mahasiswa.snack_bar_berhasil.open = True
                mahasiswa.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # menampilkan semua data ke dalam tabel
        cursor.execute("SELECT * FROM mahasiswa")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        mahasiswa.data_mahasiswa = DataTable(
            columns = [
                DataColumn(Text("ID")),
                DataColumn(Text("Nama")),
                DataColumn(Text("Umur")),
                DataColumn(Text("Opsi")),
            ],
        )
        for row in rows:
            mahasiswa.data_mahasiswa.rows.append(
                DataRow(
                    cells = [
                        DataCell(Text(row['id'])),
                        DataCell(Text(row['name'])),
                        DataCell(Text(row['age'])),
                        DataCell(
                            Row([
                                IconButton("delete", icon_color = "red", data = row, on_click = hapus_mahasiswa),
                                IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_mahasiswa),
                            ])
                        ),
                    ]
                )
            )
        
        # buat variabel utk layout data rekapan
        mahasiswa.layout_data = Column()

        # buat form dialog untuk form entri data
        mahasiswa.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Entri Mahasiswa", weight = FontWeight.BOLD),
                        Row([ mahasiswa.inputan_id_mahasiswa ]),
                        Row([ mahasiswa.inputan_nama_mhs ]),
                        Row([ mahasiswa.inputan_age_mhs ]),
                        Row([
                            #tombol tambah data
                            ElevatedButton(
                                "Simpan Data",
                                    icon = "SAVE_AS",
                                    icon_color = "white",
                                    color = "white",
                                    bgcolor = "blue",
                                    width = 250,
                                    height = 50,
                                    on_click = simpan_mahasiswa,
                                )
                        ]),
                    ],
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    height = 500
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
        mahasiswa.layout_utama = Column(
            [
                Container(
                    Text(
                        "Rekap Data Mahasiswa",
                        size = 20,
                        color = "blue",
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
                        on_click = tampil_dialog_mahasiswa,
                    ),
                    alignment = alignment.center,
                    padding = 10,
                ),
                Row(
                    [mahasiswa.data_mahasiswa], scroll=ScrollMode.ALWAYS
                ),
                mahasiswa.layout_data,
                mahasiswa.snack_bar_berhasil,
                mahasiswa.dialog,
            ]
        )

        return mahasiswa.layout_utama

        # return Column(
        #     controls = [
        #         Row([ElevatedButton("Tambah Data", icon = icons.ADD, icon_color="white", color = "white", bgcolor = "blue", on_click = tampil_dialog_mahasiswa)], alignment = MainAxisAlignment.END),
        #         Row(
        #             [mahasiswa.data_mahasiswa], scroll=ScrollMode.ALWAYS
        #         ),
        #         mahasiswa.dialog, mahasiswa.snack_bar_berhasil
        #     ],
            
        # )

class FormMatakuliah(UserControl):
    # class untuk halaman mata kuliah
    def build(matakuliah) :

        # buat variabel inputan
        matakuliah.inputan_id_kuliah = TextField(visible = False, expand = True)
        matakuliah.inputan_mata_kuliah = TextField(label = "Mata Kuliah", hint_text = "masukkan mata kuliah ... ", expand = True)
        matakuliah.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")
        
        # memuat tabel data
        def tampil_data(e):
            # Merefresh halaman & menampilkan notif
            matakuliah.data_matakuliah.rows.clear()
            cursor.execute("SELECT * FROM mata_kuliah")
            result = cursor.fetchall()
            # menampilkan ulang data 
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
            for row in rows:
                matakuliah.data_matakuliah.rows.append(
                    DataRow(
                        cells = [
                            DataCell(Text(row['id_matakuliah'])),
                            DataCell(Text(row['mata_kuliah'])),
                            DataCell(
                                Row([
                                    IconButton("delete", icon_color = "red", data = row, on_click = hapus_matakuliah),
                                    IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah),
                                ])
                            ),
                        ]
                        )
                    )
        # fungsi menampilkan dialog form entri
        def tampil_dialog(e):
            matakuliah.inputan_id_kuliah.value = ''
            matakuliah.inputan_mata_kuliah.value = ''
            matakuliah.dialog.open = True
            matakuliah.update()

        def tampil_dialog_ubah(e):
            matakuliah.inputan_id_kuliah.value = e.control.data['id_matakuliah']
            matakuliah.inputan_mata_kuliah.value = e.control.data['mata_kuliah']
            matakuliah.dialog.open = True
            matakuliah.update()

        # fungsi simpan data
        def simpan_matakuliah(e):
            try:
                if (matakuliah.inputan_id_kuliah.value == '') :
                    sql = "INSERT INTO mata_kuliah (id_matakuliah, mata_kuliah) VALUES(%s, %s)"
                    val = ('', matakuliah.inputan_mata_kuliah.value)
                else :
                    sql = "UPDATE mata_kuliah SET mata_kuliah = %s WHERE id_matakuliah = %s"
                    val = (matakuliah.inputan_mata_kuliah.value, matakuliah.inputan_id_kuliah.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_data(e)
                matakuliah.dialog.open = False
                matakuliah.snack_bar_berhasil.open = True
                matakuliah.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # fungsi hapus data
        def hapus_matakuliah(e):
            try:
                sql = "DELETE FROM mata_kuliah WHERE id_matakuliah = %s"
                val = (e.control.data['id_matakuliah'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                matakuliah.data_matakuliah.rows.clear()
                
                tampil_data(e)
                matakuliah.dialog.open = False
                matakuliah.snack_bar_berhasil.open = True
                matakuliah.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # menampilkan semua data ke dalam tabel
        cursor.execute("SELECT * FROM mata_kuliah")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        matakuliah.data_matakuliah = DataTable(
            columns = [
                DataColumn(Text("ID")),
                DataColumn(Text("Mata Kuliah")),
                DataColumn(Text("Opsi")),
            ],
        )
        for row in rows:
            matakuliah.data_matakuliah.rows.append(
                DataRow(
                    cells = [
                        DataCell(Text(row['id_matakuliah'])),
                        DataCell(Text(row['mata_kuliah'])),
                        DataCell(
                            Row([
                                IconButton("delete", icon_color = "red", data = row, on_click = hapus_matakuliah),
                                IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah),
                            ])
                        ),
                    ]
                )
            )
        
        # buat variabel utk layout data rekapan
        matakuliah.layout_data = Column()

        # buat form dialog untuk form entri data
        matakuliah.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Entri Matakuliah", weight = FontWeight.BOLD),
                        Row([ matakuliah.inputan_id_kuliah ]),
                        Row([ matakuliah.inputan_mata_kuliah ]),
                        Row([
                            #tombol tambah data
                            ElevatedButton(
                                "Simpan Data",
                                    icon = "SAVE_AS",
                                    icon_color = "white",
                                    color = "white",
                                    bgcolor = "blue",
                                    width = 250,
                                    height = 50,
                                    on_click = simpan_matakuliah,
                                )
                        ]),
                    ],
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    height = 500
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
        matakuliah.layout_utama = Column(
            [
                Container(
                    Text(
                        "Rekap Data Mata Kuliah",
                        size = 19,
                        color = "blue",
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
                        on_click = tampil_dialog,
                    ),
                    alignment = alignment.center,
                    padding = 10,
                ),
                Row(
                    [matakuliah.data_matakuliah], scroll=ScrollMode.ALWAYS
                ),
                matakuliah.layout_data,
                matakuliah.snack_bar_berhasil,
                matakuliah.dialog,
            ]
        )

        return matakuliah.layout_utama

        # return Column(
        #     controls = [
        #         Row([ElevatedButton("Tambah Data", icon = icons.ADD, icon_color="white", color = "white", bgcolor = "blue", on_click = tampil_dialog)], alignment = MainAxisAlignment.END),
        #         Row(
        #             [matakuliah.data_matakuliah], scroll=ScrollMode.ALWAYS
        #         ),
        #         matakuliah.dialog, matakuliah.snack_bar_berhasil
        #     ],
            
        # )

class FormDosen(UserControl):
    # class untuk halaman mata kuliah
    def build(dosen) :

        def ubah_tanggal_lhr(e):
            tgl_baru = dosen.opsi_tanggal.value
            dosen.inputan_tgl_lhr_dosen.value = tgl_baru.date()
            dosen.update()
            
        def opsi_tanggal_lhr_dismissed(e):
            tgl_baru = dosen.inputan_tgl_lhr_dosen.value
            dosen.inputan_tgl_lhr_dosen.value = tgl_baru
            dosen.update()
        
        dosen.opsi_tanggal = DatePicker(
            on_change=ubah_tanggal_lhr,
            on_dismiss=opsi_tanggal_lhr_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )
        # buat variabel inputan
        dosen.inputan_id_dosen = TextField(visible = False, expand = True)
        dosen.inputan_nidn_dosen = TextField(label = "NIDN Dosen", hint_text = "masukkan NIDN Dosen ", expand = True)
        dosen.inputan_nama_dosen = TextField(label = "Nama Dosen", hint_text = "masukkan Nama Dosen ", expand = True)
        dosen.inputan_jk_dosen = Dropdown(label = "Jk Dosen", hint_text = "Lk or PR ", expand = True, options=[dropdown.Option("Laki-laki"), dropdown.Option("Perempuan")],)
        dosen.inputan_tgl_lhr_dosen = TextField(label = "Tanggal lahir", hint_text = "Tgl Lahir", expand = True)
        dosen.inputan_alamat_dosen = TextField(label = "Alamat Dosen", hint_text = "Alamat", expand = True)
        dosen.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")

        # memuat tabel data
        def tampil_data_dosen(e):
            # Merefresh halaman & menampilkan notif
            dosen.data_dosen.rows.clear()
            cursor.execute("SELECT * FROM dosen")
            result = cursor.fetchall()
            # menampilkan ulang data 
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
            for row in rows:
                dosen.data_dosen.rows.append(
                    DataRow(
                        cells = [
                            DataCell(Text(row['id_dosen'])),
                            DataCell(Text(row['nidn_dosen'])),
                            DataCell(Text(row['nama_dosen'])),
                            DataCell(Text(row['jk_dosen'])),
                            DataCell(Text(row['tgl_lahir_dosen'])),
                            DataCell(Text(row['alamat_dosen'])),
                            DataCell(
                                Row([
                                    IconButton("delete", icon_color = "red", data = row, ),
                                    IconButton("create", icon_color = "grey", data = row, ),
                                ])
                            ),
                        ]
                        )
                    )

        # fungsi menampilkan dialog form entri
        def tampil_dialog_dosen(e):
            dosen.inputan_id_dosen.value = ''
            dosen.inputan_nidn_dosen.value = ''
            dosen.inputan_nama_dosen.value = ''
            dosen.inputan_jk_dosen.value = ''
            dosen.inputan_tgl_lhr_dosen.value = ''
            dosen.inputan_alamat_dosen.value = ''
            dosen.dialog.open = True
            dosen.update()

        def tampil_dialog_ubah_dosen(e):
            dosen.inputan_id_dosen.value = e.control.data['id_dosen']
            dosen.inputan_nidn_dosen.value = e.control.data['nidn_dosen']
            dosen.inputan_nama_dosen.value = e.control.data['nama_dosen']
            dosen.inputan_jk_dosen.value = e.control.data['jk_dosen']
            dosen.inputan_tgl_lhr_dosen.value = e.control.data['tgl_lahir_dosen']
            dosen.inputan_alamat_dosen.value = e.control.data['alamat_dosen']
            dosen.dialog.open = True
            dosen.update()

        # fungsi simpan data
        def simpan_dosen(e):
            try:
                if (dosen.inputan_id_dosen.value == '') :
                    sql = "INSERT INTO dosen (id_dosen, nidn_dosen, nama_dosen, jk_dosen, tgl_lahir_dosen, alamat_dosen) VALUES(%s, %s, %s, %s, %s, %s)"
                    val = (dosen.inputan_id_dosen.value, dosen.inputan_nidn_dosen.value, dosen.inputan_nama_dosen.value, dosen.inputan_jk_dosen.value, dosen.inputan_tgl_lhr_dosen.value, dosen.inputan_alamat_dosen.value)
                else :
                    sql = "UPDATE dosen SET nidn_dosen = %s, nama_dosen = %s, jk_dosen = %s, tgl_lahir_dosen = %s, alamat_dosen = %s WHERE id_dosen = %s"
                    val = (dosen.inputan_nidn_dosen.value, dosen.inputan_nama_dosen.value, dosen.inputan_jk_dosen.value, dosen.inputan_tgl_lhr_dosen.value, dosen.inputan_alamat_dosen.value,  dosen.inputan_id_dosen.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_data_dosen(e)
                dosen.dialog.open = False
                dosen.snack_bar_berhasil.open = True
                dosen.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")


        # fungsi hapus data
        def hapus_dosen(e):
            try:
                sql = "DELETE FROM dosen WHERE id_dosen = %s"
                val = (e.control.data['id_dosen'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                dosen.data_dosen.rows.clear()
                
                tampil_data_dosen(e)
                dosen.dialog.open = False
                dosen.snack_bar_berhasil.open = True
                dosen.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")

        # menampilkan semua data ke dalam tabel
        cursor.execute("SELECT * FROM dosen")
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        dosen.data_dosen = DataTable(
            columns = [
                DataColumn(Text("ID Dosen")),
                DataColumn(Text("NIDN")),
                DataColumn(Text("Nama")),
                DataColumn(Text("JK")),
                DataColumn(Text("Tanggal Lahir")),
                DataColumn(Text("Alamat")),
                DataColumn(Text("Opsi")),
            ],
        )
        for row in rows:
            dosen.data_dosen.rows.append(
                DataRow(
                    cells = [
                            DataCell(Text(row['id_dosen'])),
                            DataCell(Text(row['nidn_dosen'])),
                            DataCell(Text(row['nama_dosen'])),
                            DataCell(Text(row['jk_dosen'])),
                            DataCell(Text(row['tgl_lahir_dosen'])),
                            DataCell(Text(row['alamat_dosen'])),
                        DataCell(
                            Row([
                                IconButton("delete", icon_color = "red", data = row, on_click = hapus_dosen ),
                                IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_dosen),
                            ])
                        ),
                    ]
                )
            )

        # buat variabel utk layout data rekapan
        dosen.layout_data = Column()

        # buat form dialog untuk form entri data
        dosen.dialog = BottomSheet(
            Container(
                Column(
                    [
                        Text("Form Entri Data Dosen", weight = FontWeight.BOLD),
                        Row([ dosen.inputan_id_dosen ]),
                        Row([ dosen.inputan_nidn_dosen ]),
                        Row([ dosen.inputan_nama_dosen ]),
                        Row([ dosen.inputan_jk_dosen ]),
                        Row([ dosen.inputan_tgl_lhr_dosen, FloatingActionButton(icon=icons.CALENDAR_MONTH, on_click=lambda _: dosen.opsi_tanggal.pick_date()) ]),
                        Row([ dosen.inputan_alamat_dosen ]),
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
                                    on_click = simpan_dosen,
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
        dosen.layout_utama = Column(
            [
                Container(
                    Text(
                        "Rekap Data Dosen",
                        size = 25,
                        color = "blue",
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
                        on_click = tampil_dialog_dosen,
                    ),
                    alignment = alignment.center,
                    padding = 10,
                ),
                Row(
                    [dosen.data_dosen], scroll=ScrollMode.ALWAYS
                ),
                dosen.layout_data,
                dosen.snack_bar_berhasil,
                dosen.dialog,
            ]
        )

        return dosen.layout_utama

# fungsi utama
def main (page : Page):
    # mengatur halaman
    page.title = "Kelas A - Aplikasi CRUD (Menu & SQL)"
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
                        title = Text("Aplikasi CRUD Jadwal Kuliah", size = 18, weight = FontWeight.BOLD, color = colors.WHITE), 
                        bgcolor = colors.BLUE, 
                        center_title = True,
                    ),
                    Column(
                        [
                            Icon(name = icons.CAST_FOR_EDUCATION, color = colors.BLUE, size = 180),
                            Column(
                                controls = [
                                    ElevatedButton("Menu Mata Kuliah", icon = icons.TABLE_ROWS, on_click = lambda _: page.go("/matakuliah")),
                                    ElevatedButton("Menu Dosen", icon = icons.PEOPLE_ROUNDED, on_click = lambda _: page.go("/dosen")),
                                    ElevatedButton("Menu Mahasiswa", icon = icons.PEOPLE_ROUNDED, on_click = lambda _: page.go("/mahasiswa")),
                                    ElevatedButton("Menu Jadwal Kuliah", icon = icons.SCHEDULE_ROUNDED, on_click = lambda _: page.go("/jadwalkuliah"), disabled=True),
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
                            Text('Mobile Programming @2024', size = 12)
                        ],
                        horizontal_alignment = CrossAxisAlignment.CENTER,
                    ),
                    
                ],
            )
        )
        if page.route == "/mahasiswa":
            page.views.append(
                View("/mahasiswa",
                    [
                        AppBar(title = Text("Menu Mahasiswa", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT),
                        FormMahasiswa()
                    ],
                )
            )
        if page.route == "/matakuliah":
            page.views.append(
                View("/matakuliah",
                    [
                        AppBar(title = Text("Menu Kuliah", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT),
                        FormMatakuliah()
                    ],
                )
            )
        if page.route == "/dosen":
            page.views.append(
                View("/dosen",
                    [
                        AppBar(title = Text("Menu Dosen", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT),
                        FormDosen()
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
