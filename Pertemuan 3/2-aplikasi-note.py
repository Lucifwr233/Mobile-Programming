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
        return Column(
            controls= [
            Row(
                controls= [
                    #field / inputan catatan
                    catatan.inputan_catatan_baru,
                    #tombol tambah data
                    FloatingActionButton(
                        icon= icons.ADD,
                        bgcolor= "purple"
                    )
                ]
            ),
        ]
        )

    #fungsi perintah tambah data
    def tambah_catatan (catatan, e) :
        catatan.inputan_catatan_baru.value = ""
        catatan.update()

    #fungsi perintah hapus data
    def hapus_catatan (catatan, data_catatan_masuk) :
        catatan.layout_data_controls.remove(data_catatan_masuk)
        catatan.update()

    #fungsi perintah ubah data
    def ubah_catatan (catatan, e) :
        catatan.inputan_catatan_ubah.value = catatan.data_catatan.label
        catatan.tampil_data.visible = False
        catatan.tampil_ubahdata.visible = True
        catatan.update()

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
