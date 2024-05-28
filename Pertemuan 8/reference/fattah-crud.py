# memasukkan library flet ke aplikasi
# import flet as ft
import flet
from flet import *
import datetime
import mysql.connector

# buat koneksi ke database SQL
koneksi_db = mysql.connector.connect(host = "localhost", user = "root", password = "", database = "fattah_crud_mobile")
cursor = koneksi_db.cursor()

class FormMember(UserControl):
    # class untuk halaman mata kuliah
    def build(member) :

        def ubah_tanggal_lhr(e):
            tgl_baru = member.opsi_tanggal.value
            member.inputan_tgl_lahir.value = tgl_baru.date()
            member.update()
            
        def opsi_tanggal_lhr_dismissed(e):
            tgl_baru = member.inputan_tgl_lahir.value
            member.inputan_tgl_lhr_member.value = tgl_baru
            member.update()
        
        member.opsi_tanggal = DatePicker(
            on_change=ubah_tanggal_lhr,
            on_dismiss=opsi_tanggal_lhr_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )
        # buat variabel inputan
        member.inputan_id = TextField(visible = False, expand = True)
        member.inputan_nama = TextField(label = "NIDN Dosen", hint_text = "masukkan NIDN Dosen ", expand = True)
        member.inputan_jekel = Dropdown(label = "Jk", hint_text = "Lk or PR ", expand = True, options=[dropdown.Option("Laki-laki"), dropdown.Option("Perempuan")],)
        member.inputan_tgl_lahir = TextField(label = "Tanggal lahir", hint_text = "Tgl Lahir", expand = True)
        member.inputan_alamat = TextField(label = "Alamat Member", hint_text = "Alamat", expand = True)
        member.inputan_telp = TextField(label = "Telepon", hint_text = "Telepon", expand = True)
        member.inputan_tgl_member = TextField(label = "Tanggal Member", hint_text = "Tanggal Member", expand = True)
        member.snack_bar_berhasil = SnackBar( Text("Operasi berhasil"), bgcolor="green")

        # memuat tabel data
        def tampil_member(e):
            # Merefresh halaman & menampilkan notif
            member.data_member.rows.clear()
            cursor.execute("SELECT * FROM membership")
            result = cursor.fetchall()
            # menampilkan ulang data 
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]
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
                                    IconButton("delete", icon_color = "red", data = row, ),
                                    IconButton("create", icon_color = "grey", data = row, ),
                                ])
                            ),
                        ]
                        )
                    )

        # fungsi menampilkan dialog form entri
        def tampil_dialog_member(e):
            member.inputan_id.value = ''
            member.inputan_nama.value = ''
            member.inputan_jekel.value = ''
            member.inputan_tgl_lahir.value = ''
            member.inputan_alamat.value = ''
            member.inputan_telp.value = ''
            member.inputan_tgl_member.value = ''
            member.dialog.open = True
            member.update()

        def tampil_dialog_ubah_member(e):
            member.inputan_id.value = e.control.data['id']
            member.inputan_nama.value = e.control.data['nama']
            member.inputan_jekel.value = e.control.data['jekel']
            member.inputan_tgl_lahir.value = e.control.data['tgl_lahir']
            member.inputan_alamat.value = e.control.data['alamat']
            member.inputan_telp.value = e.control.data['telp']
            member.inputan_tgl_member.value = e.control.data['tgl_member']
            member.dialog.open = True
            member.update()

        # fungsi simpan data
        def simpan_member(e):
            try:
                if (dosen.inputan_id_dosen.value == '') :
                    sql = "INSERT INTO membership (id_dosen, nidn_dosen, nama_dosen, jk_dosen, tgl_lahir_dosen, alamat_dosen) VALUES(%s, %s, %s, %s, %s, %s)"
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
                dosen.opsi_tanggal
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
                        bgcolor = colors.BLUE_800, 
                        center_title = True,
                    ),
                    Column(
                        [
                            Image(src="img/Lambang.png",width=230 ),
                            # Icon(name = icons.CAST_FOR_EDUCATION, color = colors.BLUE, size = 180),
                            Column(
                                controls = [
                                    ElevatedButton("Menu Mata Kuliah", icon = icons.TABLE_ROWS, on_click = lambda _: page.go("/matakuliah"), width=205 ),
                                    ElevatedButton("Menu Dosen", icon = icons.PEOPLE_ROUNDED, on_click = lambda _: page.go("/dosen"), width=205 ),
                                    ElevatedButton("Menu Mahasiswa", icon = icons.PEOPLE_ROUNDED, on_click = lambda _: page.go("/mahasiswa"), width=205 ),
                                    ElevatedButton("Menu Jadwal Kuliah", icon = icons.SCHEDULE_ROUNDED, on_click = lambda _: page.go("/jadwalkuliah"), disabled=True, width=205 ),
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
