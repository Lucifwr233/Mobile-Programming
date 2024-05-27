# memasukkan library flet ke aplikasi
# import flet as ft
import flet
from flet import *
import mysql.connector

# buat koneksi ke database SQL
koneksi_db = mysql.connector.connect(host = "localhost", user = "root", password = "", database = "mp_appcrudsql")
cursor = koneksi_db.cursor()

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
                                    bgcolor = "teal",
                                    width = 280,
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
            bgcolor = colors.GREY_50
            #on_dismiss=bs_dismissed,
        )
    
        return Column(
            controls = [
                Row([ElevatedButton("Tambah Data", icon = icons.ADD, icon_color="white", color = "white", bgcolor = "teal", on_click = tampil_dialog)], alignment = MainAxisAlignment.END),
                matakuliah.data_matakuliah, matakuliah.dialog, matakuliah.snack_bar_berhasil
            ],
            
        )

class FormDosen(UserControl):
    # class untuk halaman mata kuliah
    def build(dosen) :

        # buat variabel inputan
        dosen.inputan_id_dosen = TextField(visible = False, expand = True)
        dosen.inputan_nidn_dosen = TextField(label = "NIDN Dosen", hint_text = "masukkan NIDN Dosen ", expand = True)
        dosen.inputan_nama_dosen = TextField(label = "Nama Dosen", hint_text = "masukkan Nama Dosen ", expand = True)
        dosen.inputan_jk_dosen = TextField(label = "Jk Dosen", hint_text = "Lk or PR ", expand = True)
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
                    val = ('', dosen.inputan_nidn_dosen.value)
                    val = ('', dosen.inputan_nama_dosen.value)
                    val = ('', dosen.inputan_jk_dosen.value)
                    val = ('', dosen.inputan_tgl_lhr_dosen.value)
                    val = ('', dosen.inputan_alamat_dosen.value)
                else :
                    sql = "UPDATE dosen SET nidn_dosen, nama_dosen, jk_dosen, tgl_lahir_dosen, alamat_dosen = %s %s %s %s %s WHERE id_dosen = %s"
                    val = (dosen.inputan_nidn_dosen.value, dosen.inputan_nidn_dosen.value, dosen.inputan_nama_dosen.value, dosen.inputan_jk_dosen.value, dosen.inputan_tgl_lhr_dosen.value, dosen.inputan_alamat_dosen.value)
                    
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
                                IconButton("create", icon_color = "grey", data = row,on_click = tampil_dialog_ubah_dosen),
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
                        Row([ dosen.inputan_tgl_lhr_dosen ]),
                        Row([ dosen.inputan_alamat_dosen ]),
                        Row([
                            #tombol tambah data
                            ElevatedButton(
                                "Simpan Data",
                                    icon = "SAVE_AS",
                                    icon_color = "white",
                                    color = "white",
                                    bgcolor = "teal",
                                    width =  250,
                                    height = 100,
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
            bgcolor = colors.GREY_50
            #on_dismiss=bs_dismissed,
        )


        return Column(
            controls = [
                Row([ElevatedButton("Tambah Data", icon = icons.ADD, icon_color="white", color = "white", bgcolor = "teal", on_click = tampil_dialog_dosen)], alignment = MainAxisAlignment.END),
                Row(
                    [dosen.data_dosen], scroll=ScrollMode.ALWAYS
                ),
                dosen.dialog, dosen.snack_bar_berhasil
            ],
            
        )

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
                        title = Text("Aplikasi CRUD Jadwal Kuliah", size = 18, weight = FontWeight.BOLD, color = colors.WHITE), 
                        bgcolor = colors.TEAL, 
                        center_title = True,
                        actions = [
                            IconButton(icons.WB_SUNNY_OUTLINED, on_click = mode_tema),
                        ],
                    ),
                    Column(
                        [
                            Icon(name = icons.CALENDAR_MONTH_ROUNDED, color = colors.TEAL, size = 180),
                            Column(
                                controls = [
                                    ElevatedButton("Menu Mata Kuliah", icon = icons.TABLE_ROWS, icon_color="black", color = "black", on_click = lambda _: page.go("/matakuliah")),
                                    ElevatedButton("Menu Dosen", icon = icons.PEOPLE_ROUNDED, icon_color="black", color = "black", on_click = lambda _: page.go("/dosen")),
                                    ElevatedButton("Menu Jadwal Kuliah", icon = icons.SCHEDULE_ROUNDED, icon_color="black", color = "black", on_click = lambda _: page.go("/jadwalkuliah")),
                                ],
                                width = 375,
                                horizontal_alignment = CrossAxisAlignment.CENTER,
                            ),
                            Text('Mobile Programming @2024', size = 12)
                        ],
                        height = 500,
                        width = 375,
                        alignment = MainAxisAlignment.SPACE_AROUND,
                        horizontal_alignment = CrossAxisAlignment.CENTER,
                    ),
                    
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
