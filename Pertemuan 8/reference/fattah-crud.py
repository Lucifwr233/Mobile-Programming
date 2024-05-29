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

        # tgl lhr member
        def ubah_tanggal_lhr(e):
            tgl_baru = member.opsi_tanggal.value
            member.inputan_tgl_lahir.value = tgl_baru.date()
            member.update()
            
        def opsi_tanggal_lhr_dismissed(e):
            tgl_baru = member.inputan_tgl_lahir.value
            member.inputan_tgl_lahir.value = tgl_baru
            member.update()
        
        member.opsi_tanggal = DatePicker(
            on_change=ubah_tanggal_lhr,
            on_dismiss=opsi_tanggal_lhr_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        # tgl member join
        def ubah_tanggal_lhr_member(e):
            tgl_baru = member.opsi_tanggal_member.value
            member.inputan_tgl_member.value = tgl_baru.date()
            member.update()
            
        def opsi_tanggal_lhr_dismissed_member(e):
            tgl_baru = member.inputan_tgl_member.value
            member.inputan_tgl_member.value = tgl_baru
            member.update()
        
        member.opsi_tanggal_member = DatePicker(
            on_change=ubah_tanggal_lhr_member,
            on_dismiss=opsi_tanggal_lhr_dismissed_member,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )
        # buat variabel inputan
        member.inputan_id = TextField(visible = False, expand = True)
        member.inputan_nama = TextField(label = "Nama", hint_text = "Nama", expand = True)
        member.inputan_jekel = Dropdown(label = "JeKel", hint_text = "Lk or PR ", expand = True, options=[dropdown.Option("Laki-laki"), dropdown.Option("Perempuan")],)
        member.inputan_tgl_lahir = TextField(label = "Tanggal lahir", hint_text = "Tgl Lahir", expand = True)
        member.inputan_alamat = TextField(label = "Alamat Member", hint_text = "Alamat Member", expand = True)
        member.inputan_telp = TextField(label = "Telepon", hint_text = "Telepon", expand = True)
        member.inputan_tgl_member = TextField(label = "Tanggal Member", hint_text = "Tanggal Gabung Member", expand = True)
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
                if (member.inputan_id.value == '') :
                    sql = "INSERT INTO membership (id, nama, jekel, tgl_lahir, alamat, telp, tgl_member) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                    val = (member.inputan_id.value, member.inputan_nama.value, member.inputan_jekel.value, member.inputan_tgl_lahir.value, member.inputan_alamat.value, member.inputan_telp.value, member.inputan_tgl_member.value)
                else :
                    sql = "UPDATE membership SET nama = %s, jekel = %s, tgl_lahir = %s, alamat = %s, telp = %s, tgl_member = %s WHERE id = %s"
                    val = (member.inputan_nama.value, member.inputan_jekel.value, member.inputan_tgl_lahir.value, member.inputan_alamat.value, member.inputan_telp.value, member.inputan_tgl_member.value,  member.inputan_id.value)
                    
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "Data di simpan!")

                tampil_member(e)
                member.dialog.open = False
                member.snack_bar_berhasil.open = True
                member.update()
            except Exception as e:
                print(e)
                print("Ada yang error!")


        # fungsi hapus data
        def hapus_member(e):
            try:
                sql = "DELETE FROM membership WHERE id = %s"
                val = (e.control.data['id'],)
                cursor.execute(sql, val)
                koneksi_db.commit()
                print(cursor.rowcount, "data di hapus!")
                member.data_member.rows.clear()
                
                tampil_member(e)
                member.dialog.open = False
                member.snack_bar_berhasil.open = True
                member.update()
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
                                IconButton("delete", icon_color = "red", data = row, on_click = hapus_member ),
                                IconButton("create", icon_color = "grey", data = row, on_click = tampil_dialog_ubah_member),
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

# fungsi utama
def main (page : Page):
    # mengatur halaman
    page.title = "Fattah Barbershop"
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
                        title = Text("Aplikasi CRUD Fattah Barbershop", size = 18, weight = FontWeight.BOLD, color = colors.WHITE), 
                        bgcolor = colors.BLUE_800, 
                        center_title = True,
                    ),
                    Column(
                        [
                            Image(src="img/fattahbarbershop.png",width=180 ),
                            # Icon(name = icons.CAST_FOR_EDUCATION, color = colors.BLUE, size = 180),
                            Column(
                                controls = [
                                    ElevatedButton("Menu Mata Kuliah", icon = icons.TABLE_ROWS, on_click = lambda _: page.go("/matakuliah"), width=205, disabled= True ),
                                    ElevatedButton("Menu Membership", icon = icons.PEOPLE_ROUNDED, on_click = lambda _: page.go("/member"), width=205 ),
                                    ElevatedButton("Menu Mahasiswa", icon = icons.PEOPLE_ROUNDED, on_click = lambda _: page.go("/mahasiswa"), width=205, disabled= True ),
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
        if page.route == "/matakuliah":
            page.views.append(
                View("/matakuliah",
                    [
                        AppBar(title = Text("Menu Kuliah", size = 14, weight = FontWeight.BOLD), bgcolor = colors.SURFACE_VARIANT ),
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
