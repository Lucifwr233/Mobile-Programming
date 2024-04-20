# Memasukkan Library Flet
# import flet as ft
import flet
import datetime
from flet import *


# Membuat Class Form Entry Catatan
class FormCatatan(UserControl):
    def build(catatan):
        # Variabel Inputan
        catatan.inputan_nama_baru = TextField(
            label="Nama", hint_text="Masukkan Nama Kamu ....", expand=True
        )
        # Variabel Inputan
        catatan.inputan_jk_baru = Dropdown(
            label="Jenis Kelamin",
            options=[dropdown.Option("Laki-Laki"), dropdown.Option("Perempuan")],
            expand=True,
        )
        # Variabel Inputan
        catatan.inputan_tgl_baru = TextField(
            label="Tanggal Lahir",
            hint_text="Masukkan Tanggal Lahir ....",
            read_only=True,
            expand=True,
        )

        # Variabel Tanggal
        def ubah_tanggal(e):
            tgl_baru = catatan.opsi_tanggal.value
            catatan.inputan_tgl_baru.value = tgl_baru.date()
            catatan.update()

        def opsi_tanggal_dismissed(e):
            tgl_baru = catatan.inputan_tgl_baru.value
            catatan.inputan_tgl_baru.value = tgl_baru
            catatan.update()

        catatan.opsi_tanggal = DatePicker(
            on_change=ubah_tanggal,
            on_dismiss=opsi_tanggal_dismissed,
            first_date=datetime.datetime(1945, 1, 1),
            last_date=datetime.date.today(),
        )

        # Variabel Inputan
        catatan.inputan_alamat_baru = TextField(
            label="Alamat",
            hint_text="Masukkan Alamat ....",
            expand=True,
            multiline=True,
            max_lines=3,
        )

        # Variabel Notif SnackBar
        catatan.snack_bar = SnackBar(
            content=Text("Input Data Terlebih Dahulu"),
            bgcolor=colors.RED,
            close_icon_color=colors.WHITE,
            show_close_icon=True,
        )

        # Buat Data Variabel Untuk Data Rekapan
        catatan.layout_data = Column()

        return Column(
            controls=[
                Row(
                    controls=[
                        # Field / Inputan Catatan
                        catatan.inputan_nama_baru,
                    ]
                ),
                Row(
                    controls=[
                        # Field / Inputan Catatan
                        catatan.inputan_jk_baru,
                    ]
                ),
                Row(
                    controls=[
                        # Field / Inputan Catatan
                        catatan.inputan_tgl_baru,
                        IconButton(
                            icon=icons.CALENDAR_MONTH,
                            bgcolor="Blue",
                            tooltip="Pilih Tanggal",
                            on_click=lambda _: catatan.opsi_tanggal.pick_date(),
                        ),
                    ]
                ),
                Row(
                    controls=[
                        # Field / Inputan Catatan
                        catatan.inputan_alamat_baru,
                    ]
                ),
                Row(
                    controls=[
                        # Tombol Tambah Data
                        CupertinoButton(
                            "Simpan",
                            icon=icons.SAVE_AS,
                            bgcolor="Blue",
                            expand=True,
                            on_click=catatan.tambah_catatan,
                        )
                    ]
                ),
                # Layout Rekapan Data
                catatan.layout_data,
                # Snackbar
                catatan.snack_bar,
                # Opsi Tanggal
                catatan.opsi_tanggal,
            ]
        )

    # Fungsi Untuk Perintah Tambah Data
    def tambah_catatan(catatan, e):
        if catatan.inputan_nama_baru.value == "":
            catatan.snack_bar.open = True
            catatan.update()

        elif (
            catatan.inputan_nama_baru.value != ""
            or catatan.inputan_jk_baru.value != ""
            or catatan.inputan_tgl_baru.value != ""
            or catatan.inputan_alamat_baru != ""
        ):
            data_catatan_baru = FormDataCatatan(
                catatan.inputan_nama_baru.value,
                catatan.inputan_jk_baru.value,
                catatan.hapus_catatan,
            )
            catatan.layout_data.controls.append(data_catatan_baru)
            catatan.inputan_nama_baru.value = ""
            catatan.inputan_jk_baru.value = ""
            catatan.inputan_tgl_baru.value = ""
            catatan.inputan_alamat_baru.value = ""
            catatan.update()

    # Fungsi Hapus Data
    def hapus_catatan(catatan, data_catatan_masuk):
        catatan.layout_data.controls.remove(data_catatan_masuk)
        catatan.update()


# Class Form Data Rekapan
class FormDataCatatan(UserControl):
    def _init_(catatan, nama_catatan, jk_catatan, alamat_catatan, hapus_catatan):
        super()._init_()
        catatan.nama_catatan = nama_catatan
        catatan.jk_catatan = jk_catatan
        catatan.alamat_catatan = alamat_catatan
        catatan.hapus_catatan = hapus_catatan

    def build(catatan):
        # Variabel Checkbox
        catatan.data_catatan = Text(
            catatan.nama_catatan + " (" + catatan.jk_catatan + ")"
        )


        # Variabel Ubah Data
        catatan.inputan_catatan_ubah = TextField(expand=True)
        catatan.inputan_catatan_ubah1 = TextField(expand=True)

        # Form Rekapan Data
        catatan.tampil_data = Row(
            alignment="spaceBetween",
            vertical_alignment="Center",
            controls=[
                catatan.data_catatan,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Ubah",
                            on_click=catatan.ubah_data,
                        ),
                        IconButton(
                            icon=icons.DELETE_OUTLINED,
                            tooltip="Hapus",
                            on_click=catatan.hapus_data,
                        ),
                    ],
                ),
            ],
        )
        # Form Entry Perubahan Data
        catatan.tampil_ubahdata = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                # Field
                catatan.inputan_catatan_ubah,
                catatan.inputan_catatan_ubah1,
                # Tombol Ubah
                IconButton(
                    icon=icons.DONE,
                    icon_color=colors.BLUE,
                    tooltip="Simpan Perubahan Data",
                    on_click=catatan.simpan_ubah_data,
                ),
            ],
        )
        return Column(
            controls=[
                catatan.tampil_data,
                catatan.tampil_ubahdata,
            ]
        )

    # Fungsi Simpan Data
    def simpan_ubah_data(catatan, e):
        catatan.data_catatan.label = (
            catatan.inputan_catatan_ubah.value + catatan.inputan_catatan_ubah1.value
        )
        catatan.tampil_data.visible = True
        catatan.tampil_ubahdata.visible = False
        catatan.update()

    # Fungsi Ubah Data
    def ubah_data(catatan, e):
        catatan.inputan_catatan_ubah.value = catatan.data_catatan.label
        catatan.inputan_catatan_ubah1.value = catatan.data_catatan.label
        catatan.tampil_data.visible = False
        catatan.tampil_ubahdata.visible = True
        catatan.update()

    # Fungsi Hapus Data
    def hapus_data(catatan, e):
        catatan.hapus_catatan(catatan)


# Function Atau Fungsi Utama
def main(page: Page):
    # Mengatur Halaman
    page.title = "Aplikaasi "
    page.window_width = 375
    page.window_height = 612
    page.window_resizable = True
    page.window_maximizable = True
    page.window_minimizable = True
    page.scroll = "Adaptive"
    page.theme_mode = ThemeMode.SYSTEM

    # Menampilkan Objek
    judul_aplikasi_1 = "Aplikasi"
    judul_aplikasi_2 = "CRUD"
    page.add(
        Row(
            controls=[
                Icon(name=icons.PERSON, color="teal", size=50),
            ],
            alignment=MainAxisAlignment.CENTER,
        ))

    form_aplikasi_note = FormCatatan()
    page.add(
        Row(
            controls=[
                Text(judul_aplikasi_1, size=30, weight=FontWeight.BOLD, color="Black"),
                Text(judul_aplikasi_2, size=18, weight=FontWeight.BOLD, color="Blue"),
            
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        form_aplikasi_note,
    )


# Mengatur Output Aplikasi
flet.app(target=main)