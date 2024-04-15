#memasukkan library flet ke aplikasi
#import flet as ft
import datetime
import flet
from flet import *

#buat class form entri catatan
class FormCatatan(UserControl) :
    def build(catatan) :
        #buat variabel untuk inputan catatan
        catatan.inputan_catatan_baru = TextField(
            hint_text = "Nama",
            expand = True
        )

        #buat variabel untuk inputan catatan2
        catatan.inputan_catatan_baru_2 = Dropdown(
            hint_text = "Jenis Kelamin",
            expand = True,
            label="Jenis Kelamin",
            options=[
               dropdown.Option("Laki-Laki"),
               dropdown.Option("Perempuan"),
            ],
            autofocus=True,
        )

        #buat variabel inputan tanggal
        def ubah_tanggal(e):
            tgl_baru = catatan.opsi_tanggal.value
            catatan.inputan_catatan_baru_3.value = tgl_baru.date()
            catatan.update()

        def opsi_tanggal_dismissed(e):
            tgl_baru = catatan.inputan_catatan_baru_3.value
            catatan.inputan_catatan_baru_3.value = tgl_baru
            catatan.update()

        catatan.opsi_tanggal = DatePicker(
            on_change= ubah_tanggal,
            on_dismiss= opsi_tanggal_dismissed,
            first_date= datetime.datetime (1945, 1, 1),
            last_date= datetime.date.today(),
        )

        catatan.inputan_catatan_baru_3 = TextField(
            hint_text = "Tanggal Lahir",
            expand = True
        )

        catatan.inputan_catatan_baru_4 = TextField(
            label= "Alamat",
            multiline= True,
            hint_text = "Alamat",
            max_lines= 3,
            expand = True
        )

        #buat notif snackbar
        catatan.snack_bar = SnackBar(
            content= Text("Silahkan isi terlebih dahulu!"),
            bgcolor= colors.RED,
            close_icon_color= colors.WHITE,
            show_close_icon= True
        )

        #buat variabel utk layout data rekapan
        catatan.layout_data = Column()

        return Column(
            controls = [
                Row(
                controls = [
                    #field / inputan catatan
                    catatan.inputan_catatan_baru, 
                ]
            ),

                Row(
                controls = [
                    #field / inputan catatan2
                    catatan.inputan_catatan_baru_2,
                    ]
                ),
                Row(
                controls = [
                    #field / inputan catatan
                    catatan.inputan_catatan_baru_3,
                     catatan.opsi_tanggal,
                    FloatingActionButton(
                        bgcolor = "#D895DA",
                        icon=icons.CALENDAR_MONTH_ROUNDED,
                        on_click=lambda _: catatan.opsi_tanggal.pick_date(),
                    )
                  ]
                ),

                Row(
                controls = [
                    #field / inputan catatan2
                    catatan.inputan_catatan_baru_4,
                    ]
                ),

            Row(
                controls = [
                    #tombol tambah data 
                    FloatingActionButton( 
                        icon = icons.SAVE_AS,
                        bgcolor = "#BC7FCD",
                        width = 340,
                        on_click = catatan.tambah_catatan
                    )
                    ]
                ),

            #layout rekapan data
            catatan.layout_data,
            #snakbar
            catatan.snack_bar,
            #tanggal
            catatan.opsi_tanggal,
            ]  
        )
    
    #fungsi utk perintah tambah data
    def tambah_catatan (catatan, e) :
        if catatan.inputan_catatan_baru.value == "" or catatan.inputan_catatan_baru_2.value == "" or catatan.inputan_catatan_baru_3.value == "" or catatan.inputan_catatan_baru_4.value == ""  :
           catatan.snack_bar.open = True
           catatan.update()
        
        elif catatan.inputan_catatan_baru.value != "" or catatan.inputan_catatan_baru_2.value != "" or catatan.inputan_catatan_baru_3.value != "" or catatan.inputan_catatan_baru_4.value != "" :
             data_catatan_baru = FormDataCatatan(catatan.inputan_catatan_baru.value, catatan.inputan_catatan_baru_2.value, catatan.hapus_catatan)
             catatan.layout_data.controls.append(data_catatan_baru)
             catatan.inputan_catatan_baru.value = ""
             catatan.inputan_catatan_baru_2.value = ""
             catatan.inputan_catatan_baru_3.value = ""
             catatan.inputan_catatan_baru_4.value = ""
             catatan.update()
    
    #fungsi utk perintah hapus data
    def hapus_catatan (catatan, data_catatan_masuk) :
        catatan.layout_data.controls.remove(data_catatan_masuk)
        catatan.update()

#buat class form data rekapan/histori catatan
class FormDataCatatan(UserControl) :
    def __init__(catatan, nama_catatan, jk_catatan, hapus_catatan):
        super().__init__()
        catatan.nama_catatan = nama_catatan
        catatan.jk_catatan = jk_catatan
        catatan.hapus_catatan = hapus_catatan

    def build(catatan):
        #buat variabel untuk checkbox
        #catatan.data_catatan = Checkbox(value = False, label = catatan.isi_catatan)
        catatan.data_catatan = Text(catatan.nama_catatan + " (" + catatan.jk_catatan+ " )" )

        #buat variable utk inputan/field ubah data
        catatan.inputan_catatan_ubah = TextField(expand = True)

        #buat form rekapan data yang berhasil di simpan
        catatan.tampil_data = Row(
            alignment = "spaceBetween",
            vertical_alignment = "center",
            controls = [
                catatan.data_catatan,
                Row(
                    spacing = 0,
                    controls = [
                        IconButton(
                            icon = icons.CREATE_OUTLINED,
                            tooltip = "Ubah",
                            on_click = catatan.ubah_data,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip = "Hapus",
                            on_click = catatan.hapus_data,
                        ),
                    ],
                ),
            ],
        )

        #buat form entri untuk perubahan data
        catatan.tampil_ubahdata = Row(
            visible = False,
            alignment = "spaceBetween",
            vertical_alignment = "center",
            controls = [
                #field / inputan catatan
                catatan.inputan_catatan_ubah,
                #tombol ubah data
                IconButton(
                    icon = icons.DONE_OUTLINE_OUTLINED,
                    icon_color = colors.GREEN,
                    tooltip = "Simpan Perubahan",
                    on_click = catatan.simpan_ubah_data,
                ),
            ],
        )
        return Column(controls = [catatan.tampil_data, catatan.tampil_ubahdata ])

    #fungsi utk perintah simpan ubah data
    def simpan_ubah_data(catatan, e):
        catatan.data_catatan.label = catatan.inputan_catatan_ubah.value
        catatan.tampil_data.visible = True
        catatan.tampil_ubahdata.visible = False
        catatan.update()

    #fungsi utk perintah form ubah data
    def ubah_data(catatan, e):
        catatan.inputan_catatan_ubah.value = catatan.data_catatan.label
        catatan.tampil_data.visible = False
        catatan.tampil_ubahdata.visible = True
        catatan.update()

    #fungsi utk perintah hapus catatan
    def hapus_data(catatan, e):
        catatan.hapus_catatan(catatan)        

#function/fungsi utama 
def main (page : Page):
    #mengatur halaman
    page.title = "Aplikasi Note"
    page.window_width = 375
    page.window_height = 612
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = False
    page.scroll = "adaptive"

    #menampilkan objek 
    judul_aplikasi_1 = 'Aplikasi'
    judul_aplikasi_2 = 'Note'

    form_aplikasi_note = FormCatatan()

    page.add(
        Row (
            controls = [
                Text(judul_aplikasi_1,
                    size =30,
                    #weight = FontWeight.W_400
                    weight = "bold",
                    #color = colors.AMBER
                    color = "black"
                ),
                Text(judul_aplikasi_2,
                    size =30,
                    #weight = FontWeight.W_400
                    weight = "bold",
                    #color = colors.AMBER
                    color = "purple"
                )
            ],
            #aligment = MainAxisAlignment.END
            alignment = "center"
        ),
        form_aplikasi_note
    )

#mengatur output aplikasi
flet.app(target = main)
#ft.app(target = main, view = ft.AppView.WEB_BROWSER)