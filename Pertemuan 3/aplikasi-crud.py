# Import library flet ke aplikasi
import flet 
import datetime
from flet import *


# Buat class form entri catatan
class FormCatatan(UserControl) :
    def build(catatan):
        def ubah_tanggal(e):
            tgl_baru = catatan.opsi_tanggal.value
            catatan.inputan_tgl_baru.value = tgl_baru.date()
            catatan.update()
        def opsi_tanggal_dismissed(e):
            tgl_baru = catatan.inputan_tgl_baru.value
            catatan.inputan_tgl_baru.value = tgl_baru
            catatan.update()

        # Buat variabel untuk inputan catatan
        catatan.inputan_nama= TextField(
            hint_text= "Nama",
            label="Nama",
            expand=True
        )

        catatan.dropdown_jeniskelamin = Dropdown(
            width= 340,
            label="Jenis Kelamin",
            hint_text="Jenis Kelamin",
                options=[
                    dropdown.Option("Laki-Laki"),
                    dropdown.Option("Perempuan"),
                ],
            autofocus=False,
        )
        
        catatan.inputan_tgl_baru= TextField(
            label="Tanggal Lahir",
            hint_text= "Tanggal Lahir ",
            expand=True,
            read_only=True
        )
    
        catatan.opsi_tanggal = DatePicker(
            on_change=ubah_tanggal,
            on_dismiss=opsi_tanggal_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )


        catatan.inputan_alamat= TextField(
            label="Alamat",
            hint_text= "Alamat",
            expand=True,
        )

        #variabel untuk snackbar
        catatan.snackbar = SnackBar(
            content= Text("Data tidak boleh kosong"),
            bgcolor= colors.LIGHT_BLUE,
            close_icon_color= colors.WHITE,
            show_close_icon= True
        )

        # Buat variabel untuk layout data tampil
        catatan.layout_data = Column()

        return Column(
            controls= [
            Row(
                controls= [
                    # Inputan Nama
                    catatan.inputan_nama,
                ]
            ),
            Row(
                controls= [
                    catatan.dropdown_jeniskelamin
                ]
            ),
            Row(
                controls= [
                    # Field / inputan catatan
                    catatan.inputan_tgl_baru,
                    catatan.opsi_tanggal,
                    ElevatedButton(
                        "Pick date",
                        icon=icons.CALENDAR_MONTH,
                        on_click=lambda _: catatan.opsi_tanggal.pick_date(),
                    )
                ]
            ),
            Row(
                controls= [
                    # Field / inputan catatan
                    catatan.inputan_alamat,
                ]
            ),
            Row(
                controls= [
                    # Tombol tambah data
                    FloatingActionButton(
                        width=330,
                        icon= icons.ADD,
                        text=("Tambah Data"),
                        bgcolor= "blue",
                        on_click=catatan.tambah_catatan
                    )
                ]
            ),
            # Menampilkan layout catatan ke dalam column
            catatan.layout_data,
            catatan.snackbar
        ]
        )

    # Fungsi perintah tambah data
    def tambah_catatan (catatan, e) :
        if catatan.inputan_nama.value == "" or catatan.dropdown_jeniskelamin.value == "" or catatan.inputan_tgl_baru.value =="" or catatan.inputan_alamat.value =="" :
            catatan.snackbar.open = True
            catatan.update()

        elif catatan.inputan_nama.value != "" or catatan.dropdown_jeniskelamin.value != "" or catatan.inputan_tgl_baru.value != "" or catatan.inputan_alamat.value != "" :
            
            data_catatan_baru = FormDataCatatan(catatan.inputan_nama.value,catatan.dropdown_jeniskelamin.value , catatan.inputan_tgl_baru.value, catatan.inputan_alamat.value,catatan.hapus_catatan)
            catatan.layout_data.controls.append(data_catatan_baru)
            catatan.inputan_nama.value = ""
            catatan.dropdown_jeniskelamin.value = ""
            catatan.inputan_tgl_baru.value = ""
            catatan.inputan_alamat.value = ""
            catatan.update()

    # Fungsi perintah hapus data
    def hapus_catatan (catatan, data_catatan_masuk) :
        catatan.layout_data.controls.remove(data_catatan_masuk)
        catatan.update()


# Membuat class form data rekapan
class FormDataCatatan(UserControl) :
    def __init__(catatan, nama_catatan, jk_catatan, tgl_catatan, alamat_catatan, hapus_catatan):
        super().__init__()
        catatan.nama_catatan = nama_catatan
        catatan.jk_catatan = jk_catatan
        catatan.tgl_catatan = tgl_catatan
        catatan.alamat_catatan = alamat_catatan
        catatan.hapus_catatan = hapus_catatan

    def build(catatan):
        # catatan.data_catatan = Checkbox(value=False, label=catatan.isi_catatan)
        catatan.data_catatan = Text(catatan.nama_catatan + " (" + catatan.jk_catatan+ ", "+ str(catatan.tgl_catatan) +" )" )

        # Buat variabel untuk inputan ubah data
        catatan.inputan_catatan_ubah = TextField(expand=True)

        # Form untuk tampil data
        catatan.tampil_data = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                catatan.data_catatan,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="ubah",
                            on_click=catatan.ubah_data,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="hapus",
                            on_click=catatan.hapus_data,
                        ),
                    ]
                )
            ]
        )

        # Form untuk tampil ubah data
        catatan.tampil_ubah_data = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                catatan.inputan_catatan_ubah,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.DONE_OUTLINED,
                            tooltip="Simpan Perubahan",
                            on_click=catatan.simpan_ubah_data,
                        ),
                    ]
                )
            ]
        )
        return Column(controls=[catatan.tampil_data, catatan.tampil_ubah_data])

    # Fungsi untuk perintah simpan data
    def simpan_ubah_data(catatan, e):
        catatan.data_catatan.label = catatan.inputan_catatan_ubah.value
        catatan.tampil_data.visible = True
        catatan.tampil_ubah_data.visible = False
        catatan.update()

    # Fungsi untuk ubah form data update
    def ubah_data(catatan, e):
        catatan.inputan_catatan_ubah.value = catatan.data_catatan.label
        catatan.tampil_data.visible = False
        catatan.tampil_ubah_data.visible = True
        catatan.update()

    # Fungsi untuk hapus data
    def hapus_data(catatan, e):
        catatan.hapus_catatan(catatan)

# Function/fungsi utama
def main(page: Page):
    # Menampilkan title text aplikasi
    page.title = "Aplikasi Hello World"

    # Mengatur ukuran window aplikasi
    page.window_width = 375
    page.window_height = 700
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = True
    page.scroll = "adaptive"
    page.theme_mode = ThemeMode.DARK

    # Menampilkan objek
    judul_aplikasi_1 = "Aplikasi"
    judul_aplikasi_2 = "CRUD"

    form_aplikasi_note = FormCatatan()

    page.add(
        Row(
            controls=[
                Text(judul_aplikasi_1,
                     size=30,
                     weight="bold",
                     color="grey"
                     ),
                Text(judul_aplikasi_2,
                     size=30,
                     weight="bold",
                     color="white"
                     ),
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        # Memanggil aplikasi
        form_aplikasi_note
    )

# Mengatur output aplikasi
flet.app(target=main)
