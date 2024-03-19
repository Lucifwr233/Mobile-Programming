#import libary flet ke aplikasi
import flet 
from flet import *

#buat class form entri catatan
class FormCatatan(UserControl) :
    def build(catatan):
        #buat variabel untk inputan catatan
        catatan.inputan_catatan_baru= TextField(
            hint_text= "masukkan catatan kamu .... ",
            expand=True
        )

        #buat variabel untuk layout data tampil
        catatan.layout_data = Column()


        return Column(
            controls= [
            Row(
                controls= [
                    #field / inputan catatan
                    catatan.inputan_catatan_baru,
                    #tombol tambah data
                    FloatingActionButton(
                        icon= icons.ADD,
                        bgcolor= "purple",
                        on_click=catatan.tambah_catatan
                    )
                ]
            ),
            #menampilkan layout catatan ke dalam column
            catatan.layout_data
        ]
        )

    #fungsi perintah tambah data
    def tambah_catatan (catatan, e) :
        data_catatan_baru = FormDataCatatan(catatan.inputan_catatan_baru.value, catatan.hapus_catatan)
        catatan.layout_data.controls.append(data_catatan_baru)

        catatan.inputan_catatan_baru.value = ""
        catatan.update()

    #fungsi perintah hapus data
    def hapus_catatan (catatan, data_catatan_masuk) :
        catatan.layout_data_controls.remove(data_catatan_masuk)
        catatan.update()

# membuat class form data rekapan
class FormDataCatatan(UserControl) :
        def __init__(catatan, isi_catatan, hapus_catatan):
            super().__init__()
            catatan.isi_catatan = isi_catatan
            catatan.hapus_catatan = hapus_catatan

        def build(catatan):
            catatan.data_catatan = Checkbox(value=False, label=catatan.isi_catatan)

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
                                tooltip = "ubah",
                            ),
                            IconButton(
                                icons.DELETE_OUTLINE,
                                tooltip = "hapus",
                            ),
                        ]
                    )
                ]
            )

            return Column(controls=[catatan.tampil_data])

#function/fungsi utama
def main (page : Page):

    #menampilkan title text aplikasi
    page.title = "Aplikasi Hello World"
    

    #mengatur ukuran window aplikasi
    page.window_width = 375
    page.window_height = 700
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = True
    page.scroll = "adaptive"
    page.theme_mode = ThemeMode.DARK

    #menampilkan objek
    judul_aplikasi_1 = "Aplikasi"
    judul_aplikasi_2 = "Note"

    form_aplikasi_note = FormCatatan()

    page.add(
        Row(
            controls = [
                Text(judul_aplikasi_1, 
                size = 30,
                weight= "bold",
                color = "grey"   
            ),
                Text(judul_aplikasi_2, 
                size = 30,
                weight= "bold",
                color = "white"   
            ),
        ],
        alignment=MainAxisAlignment.CENTER
    ),
    # memanggil aplikasi
    form_aplikasi_note
)

#mengatur output aplikasi
flet.app(target = main)
