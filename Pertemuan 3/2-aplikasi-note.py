#import libary flet ke aplikasi
import flet 
from flet import *

#buat class form entri catatan
class FormCatatan(UserControl) :
    def build(catatan):
        #buat variabel untk inputan catatan
        catatan.inputan_catatan_baru= TextField(
            hint_text= "Text 1 ",
            expand=True
        )
        catatan.inputan_catatan_baru2= TextField(
            hint_text= "Text 2 ",
            expand=True
        )
        catatan.inputan_catatan_baru3= TextField(
            hint_text= "Text 3 ",
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
                ]
            ),
            Row(
                controls= [
                    #field / inputan catatan
                    catatan.inputan_catatan_baru2,
                ]
            ),
            Row(
                controls= [
                    #field / inputan catatan
                    catatan.inputan_catatan_baru3,
                ]
            ),
            Row(
                controls= [
                    #tombol tambah data
                    FloatingActionButton(
                        icon= icons.ADD,
                        text=("Tambah Data"),
                        bgcolor= "blue",
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
        data_catatan_baru = FormDataCatatan(catatan.inputan_catatan_baru.value+catatan.inputan_catatan_baru2.value+catatan.inputan_catatan_baru3.value, catatan.hapus_catatan)
        catatan.layout_data.controls.append(data_catatan_baru)


        catatan.inputan_catatan_baru.value = ""
        catatan.inputan_catatan_baru2.value = ""
        catatan.inputan_catatan_baru3.value = ""
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

            #buat variabel untuk inputan ubah data
            catatan.inputan_catatan_ubah = TextField(expand=True)

            #form untuk tampil data
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
                                on_click= catatan.ubah_data,
                            ),
                            IconButton(
                                icons.DELETE_OUTLINE,
                                tooltip = "hapus",
                                on_click= catatan.hapus_data,
                            ),
                        ]
                    )
                ]
            )

            #form untuk tampil ubah data
            catatan.tampil_ubah_data = Row(
                alignment="spaceBetween",
                vertical_alignment="center",
                controls=[
                    catatan.inputan_catatan_ubah,
                    Row(
                        spacing=0,
                        controls=[
                            IconButton(
                                icon=icons.DONE_OUTLINED,
                                tooltip = "Simpan Perubahan",
                                on_click = catatan.simpan_ubah_data,
                            ),
                        ]
                    )
                ]
            )
            return Column(controls=[catatan.tampil_data, catatan.tampil_ubah_data])

            #fungsi untuk perintah simpan data
        def simpan_ubah_data(catatan, e):
            catatan.data_catatan.label = catatan.inputan_catatan_ubah.value
            catatan.tampil_data.visible = True
            catatan.tampil_ubah_data.visible = False
            catatan.update()

            #fungsi untuk ubah form data update
        def ubah_data(catatan, e):
            catatan.inputan_catatan_ubah.value = catatan.data_catatan.label
            catatan.tampil_data.visible = False
            catatan.tampil_ubah_data.visible = True
            catatan.update()

            #fungsi untk hapus data
        def hapus_data(catatan, e):
            catatan.hapus_catatan(catatan)
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
