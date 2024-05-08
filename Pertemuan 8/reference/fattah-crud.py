#memasukkan library flet ke aplikasi
#import flet as ft
import datetime
import flet
from flet import *


#buat class form entri crud
class FormCrud(UserControl) :
    def build(crud) :
        #buat variabel untuk inputan crud
        crud.inputan_nama = TextField(
            border_color= "grey",
            label  = "Nama",
            hint_text = "Nama",
            autofocus=True,
            expand = True
        )

        #buat variabel untuk inputan crud2
        crud.inputan_jekel = Dropdown(
            border_color= "grey",
            hint_text = "Jenis Kelamin",
            expand = True,
            label="Jenis Kelamin",
            options=[
               dropdown.Option("Laki-Laki"),
               dropdown.Option("Perempuan"),
            ],
        )

        #buat variabel inputan tanggal lahir
        def ubah_tanggal_lahir(e):
            tgl_baru = crud.opsi_tanggal.value
            crud.inputan_tgl.value = tgl_baru.date()
            crud.update()

        def opsi_tanggal_lahir_dismissed(e):
            tgl_baru = crud.inputan_tgl.value
            crud.inputan_tgl.value = tgl_baru
            crud.update()

        crud.opsi_tanggal = DatePicker(
            on_change= ubah_tanggal_lahir,
            on_dismiss= opsi_tanggal_lahir_dismissed,
            first_date= datetime.datetime (1945, 1, 1),
            last_date= datetime.date.today(),
        )

        crud.inputan_tgl = TextField(
            border_color= "grey",
            label = "Tanggal Lahir",
            hint_text = "Tanggal Lahir",
            read_only = True,
            expand = True
        )

        #buat variabel inputan tanggal gabung member
        crud.inputan_tgl_member = TextField(
            border_color= "grey",
            label= "Tanggal Gabung Member",
            hint_text = "Tanggal Gabung Member",
            read_only = True,
            expand = True
        )

        def ubah_tanggal_member(e):
            tgl_baru = crud.opsi_tanggal_member.value
            crud.inputan_tgl_member.value = tgl_baru.date()
            crud.update()

        def opsi_tanggal_member_dismissed(e):
            tgl_baru = crud.inputan_tgl_member.value
            crud.inputan_tgl_member.value = tgl_baru
            crud.update()

        crud.opsi_tanggal_member = DatePicker(
            on_change= ubah_tanggal_member,
            on_dismiss= opsi_tanggal_member_dismissed,
            first_date= datetime.datetime (1945, 1, 1),
            last_date= datetime.date.today(),
        )

        crud.inputan_alamat = TextField(
            border_color= "grey",
            label= "Alamat",
            multiline= True,
            hint_text = "Alamat",
            max_lines= 3,
            expand = True
        )

        crud.inputan_telp = TextField(
            border_color= "grey",
            label= "No Telepon",
            multiline= True,
            hint_text = "No Telepon",
            max_lines= 3,
            expand = True
        )

        #buat notif snackbar
        crud.snack_bar = SnackBar(
            content= Text("Silahkan isi terlebih dahulu!"),
            bgcolor= colors.RED,
            close_icon_color= colors.WHITE,
            show_close_icon= True
        )

        #buat variabel utk layout data rekapan
        crud.layout_data = Column(
            
        )

        return Column(
            controls = [
                Row(
                controls = [
                    #field / inputan crud
                    crud.inputan_nama, 
                ]
            ),

                Row(
                controls = [
                    crud.inputan_jekel,
                    ]
                ),
                Row(
                controls = [
                    crud.inputan_tgl,
                     crud.opsi_tanggal,
                    FloatingActionButton(
                        "Pick date",
                        bgcolor = "blue",
                        icon=icons.CALENDAR_MONTH_ROUNDED,
                        on_click=lambda _: crud.opsi_tanggal.pick_date(),
                    )
                  ]
                ),

                Row(
                controls = [
                    crud.inputan_alamat,
                    ]
                ),

                Row(
                controls = [
                    crud.inputan_telp,
                    ]
                ),

                Row(
                controls = [
                    crud.inputan_tgl_member,
                     crud.opsi_tanggal_member,
                    FloatingActionButton(
                        "Pick date",
                        bgcolor = "blue",
                        icon=icons.CALENDAR_MONTH_ROUNDED,
                        on_click=lambda _: crud.opsi_tanggal_member.pick_date(),
                    )
                  ]
                ),

            Row(
                controls = [
                    #tombol tambah data 
                    FloatingActionButton( 
                        icon = icons.ADD,
                        text=("Tambah Data"),
                        bgcolor = "blue",
                        width = 340,
                    )
                    ]
                ),

            #layout rekapan data
            crud.layout_data,
            #snakbar
            crud.snack_bar,
            #tanggal
            crud.opsi_tanggal,
            ]  
        )
     

#function/fungsi utama 
def main (page : Page):
    #mengatur halaman
    page.title = "Aplikasi Note"
    page.window_width = 375
    page.window_height = 700
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = True
    page.scroll = "adaptive"
    page.theme_mode = ThemeMode.DARK

    #menampilkan objek 
    judul_aplikasi_1 = 'Fattah'
    judul_aplikasi_2 = 'Barbershop'
    judul_aplikasi_3 = '  '
    deskripsi_aplikasi = 'Aplikasi Input Membership Fattah Barbershop'

    form_aplikasi_note = FormCrud()

    page.add(
        Row (
            controls = [
                Text(judul_aplikasi_3,
                    size =15,
                    weight = "bold",
                    font_family="poppins",
                    color = "Blue"
                ),
            ],
            #aligment = MainAxisAlignment.END
            alignment = "center"
        ),
        Row (
            controls = [
                Text(judul_aplikasi_1,
                    size =30,
                    weight = "bold",
                    font_family="poppins",
                    color = "Blue"
                ),
                Text(judul_aplikasi_2,
                    size =30,
                    weight = "bold",
                    font_family="poppins",
                    color = "white"
                ), 
            ],
            #aligment = MainAxisAlignment.END
            alignment = "center"
        ),
        Row (
            controls = [

                Text(deskripsi_aplikasi,
                    size =12,
                    italic= True,
                    font_family="poppins",
                    color = "white"
                ),
                
            ],
            #aligment = MainAxisAlignment.END
            alignment = "center"
        ),
        Row (
            controls = [
                Text(judul_aplikasi_3,
                    size =15,
                    weight = "bold",
                    font_family="poppins",
                    color = "Blue"
                ),
            ],
            #aligment = MainAxisAlignment.END
            alignment = "center"
        ),
        form_aplikasi_note
    )

#mengatur output aplikasi
flet.app(target = main)
#ft.app(target = main, view = ft.AppView.WEB_BROWSER)