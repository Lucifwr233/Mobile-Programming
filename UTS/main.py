#memasukkan library flet ke aplikasi
#import flet as ft
import datetime
import flet
from flet import *

#buat class form entri catatan
class FormCatatan(UserControl) :
    def build(catatan) :
        #buat variabel untuk inputan catatan
        catatan.inputan_nama = TextField(
            border_color= "grey",
            label  = "Nama",
            hint_text = "Nama",
            autofocus=True,
            expand = True
        )

        #buat variabel untuk inputan catatan2
        catatan.inputan_jekel = Dropdown(
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
            tgl_baru = catatan.opsi_tanggal.value
            catatan.inputan_tgl.value = tgl_baru.date()
            catatan.update()

        def opsi_tanggal_lahir_dismissed(e):
            tgl_baru = catatan.inputan_tgl.value
            catatan.inputan_tgl.value = tgl_baru
            catatan.update()

        catatan.opsi_tanggal = DatePicker(
            on_change= ubah_tanggal_lahir,
            on_dismiss= opsi_tanggal_lahir_dismissed,
            first_date= datetime.datetime (1945, 1, 1),
            last_date= datetime.date.today(),
        )

        catatan.inputan_tgl = TextField(
            border_color= "grey",
            label = "Tanggal Lahir",
            hint_text = "Tanggal Lahir",
            read_only = True,
            expand = True
        )

        #buat variabel inputan tanggal gabung member
        catatan.inputan_tgl_member = TextField(
            border_color= "grey",
            label= "Tanggal Gabung Member",
            hint_text = "Tanggal Gabung Member",
            read_only = True,
            expand = True
        )

        def ubah_tanggal_member(e):
            tgl_baru = catatan.opsi_tanggal_member.value
            catatan.inputan_tgl_member.value = tgl_baru.date()
            catatan.update()

        def opsi_tanggal_member_dismissed(e):
            tgl_baru = catatan.inputan_tgl_member.value
            catatan.inputan_tgl_member.value = tgl_baru
            catatan.update()

        catatan.opsi_tanggal_member = DatePicker(
            on_change= ubah_tanggal_member,
            on_dismiss= opsi_tanggal_member_dismissed,
            first_date= datetime.datetime (1945, 1, 1),
            last_date= datetime.date.today(),
        )

        catatan.inputan_alamat = TextField(
            border_color= "grey",
            label= "Alamat",
            multiline= True,
            hint_text = "Alamat",
            max_lines= 3,
            expand = True
        )

        catatan.inputan_telp = TextField(
            border_color= "grey",
            label= "No Telepon",
            multiline= True,
            hint_text = "No Telepon",
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
        catatan.layout_data = Column(
            
        )

        return Column(
            controls = [
                Row(
                controls = [
                    #field / inputan catatan
                    catatan.inputan_nama, 
                ]
            ),

                Row(
                controls = [
                    catatan.inputan_jekel,
                    ]
                ),
                Row(
                controls = [
                    catatan.inputan_tgl,
                     catatan.opsi_tanggal,
                    FloatingActionButton(
                        "Pick date",
                        bgcolor = "blue",
                        icon=icons.CALENDAR_MONTH_ROUNDED,
                        on_click=lambda _: catatan.opsi_tanggal.pick_date(),
                    )
                  ]
                ),

                Row(
                controls = [
                    catatan.inputan_alamat,
                    ]
                ),

                Row(
                controls = [
                    catatan.inputan_telp,
                    ]
                ),

                Row(
                controls = [
                    catatan.inputan_tgl_member,
                     catatan.opsi_tanggal_member,
                    FloatingActionButton(
                        "Pick date",
                        bgcolor = "blue",
                        icon=icons.CALENDAR_MONTH_ROUNDED,
                        on_click=lambda _: catatan.opsi_tanggal_member.pick_date(),
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
        if catatan.inputan_nama.value == "" or catatan.inputan_jekel.value == "" or catatan.inputan_tgl.value == "" or catatan.inputan_alamat.value == "" or catatan.inputan_telp.value == "" or catatan.inputan_tgl_member.value == "" :
           catatan.snack_bar.open = True
           catatan.update()
        
        elif catatan.inputan_nama.value != "" or catatan.inputan_jekel.value != "" or catatan.inputan_tgl.value != "" or catatan.inputan_alamat.value != "" or catatan.inputan_telp.value != "" or catatan.inputan_tgl_member.value != "" :
             data_catatan_baru = FormDataCatatan(catatan.inputan_nama.value, catatan.inputan_jekel.value, catatan.inputan_tgl.value, catatan.inputan_alamat.value, catatan.inputan_telp.value, catatan.inputan_tgl_member.value, catatan.hapus_catatan)
             catatan.layout_data.controls.append(data_catatan_baru)
             catatan.inputan_nama.value = ""
             catatan.inputan_jekel.value = ""
             catatan.inputan_tgl.value = ""
             catatan.inputan_alamat.value = ""
             catatan.inputan_telp.value = ""
             catatan.inputan_tgl_member.value = ""
             catatan.update()
    
    #fungsi utk perintah hapus data
    def hapus_catatan (catatan, data_catatan_masuk) :
        catatan.layout_data.controls.remove(data_catatan_masuk)
        catatan.update()

#buat class form data rekapan/histori catatan
class FormDataCatatan(UserControl) :
    def __init__(catatan, nama_catatan, jk_catatan, tgl_catatan, alamat_catatan, telp_catatan, tglmem_catatan, hapus_catatan):
        super().__init__()
        catatan.nama_catatan = nama_catatan
        catatan.jk_catatan = jk_catatan
        catatan.tgl_catatan = tgl_catatan
        catatan.alamat_catatan = alamat_catatan
        catatan.telp_catatan = telp_catatan
        catatan.tglmem_catatan = tglmem_catatan
        catatan.hapus_catatan = hapus_catatan

    def build(catatan):
        #buat variabel untuk checkbox
        # catatan.data_catatan_nama = Checkbox(value = False, label = catatan.nama_catatan, label_position=LabelPosition.LEFT  )
        catatan.data_catatan_nama = Text(catatan.nama_catatan)
        # catatan.data_jk_catatan = Checkbox(value= False, label= str(catatan.jk_catatan), label_position=LabelPosition.LEFT )
        catatan.data_jk_catatan = Text(str(catatan.jk_catatan) )
        # catatan.data_catatan_tgl = Checkbox(value = False, label = str(catatan.tgl_catatan), label_position=LabelPosition.LEFT  )
        catatan.data_catatan_tgl = Text(str(catatan.tgl_catatan))
        # catatan.data_catatan_alamat = Checkbox(value = False, label = str(catatan.alamat_catatan), label_position=LabelPosition.LEFT  )
        catatan.data_catatan_alamat = Text(str(catatan.alamat_catatan))
        catatan.data_catatan_telp = Text(str(catatan.telp_catatan) )
        catatan.data_catatan_tglmem = Text(str(catatan.tglmem_catatan))
        # catatan.data_catatan = Text(catatan.nama_catatan + " ( " + catatan.jk_catatan+ " )")

        #buat variable utk inputan/field ubah data
        catatan.inputan_catatan_nama = TextField(label = "Nama", border_color= "grey", expand = True)
        catatan.inputan_catatan_jk = TextField(label = "Jenis Kelamin", border_color= "grey", expand = True)
        catatan.inputan_catatan_tgl = TextField(label = "Tanggal Lahir", border_color= "grey", expand=True)
        catatan.inputan_catatan_alamat= TextField(label = "Alamat", border_color= "grey", expand=True)
        catatan.inputan_catatan_telp= TextField(label = "Nomor Telepon", border_color= "grey", expand=True)
        catatan.inputan_catatan_tglmem= TextField(label = "Tanggal Member", border_color= "grey", expand=True)

        #buat form rekapan data yang berhasil di simpan
        catatan.tampil_data = Row(
            alignment = "spaceBetween",
            vertical_alignment = "center",
            controls = [
                Row(
                    controls= [
                        catatan.data_catatan_nama,
                    ]

                ),
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
        
        catatan.tampil_ubahdata = Column(
            visible = False,
            controls = [
                #field / inputan catatan
                Row(
                    controls= [
                        Text(" ",
                            size =20,
                            font_family="poppins",
                            color = "white"
                        ),
                    ]

                ),
                Row(
                    controls= [
                        Text(" Data ",
                            size =20,
                            weight="bold",
                            font_family="poppins",
                            color = "white"
                        ),
                    ]

                ),
                Row(
                    controls= [
                        catatan.inputan_catatan_nama,
                    ]

                ),
                Row(
                    controls= [
                        catatan.inputan_catatan_jk,
                    ]

                ),
                Row(
                    controls= [
                        catatan.inputan_catatan_tgl,

                    ]

                ),
                Row(
                    controls= [
                        catatan.inputan_catatan_alamat,

                    ]

                ),
                Row(
                    controls= [
                        catatan.inputan_catatan_telp,

                    ]

                ),
                Row(
                    controls=[
                        catatan.inputan_catatan_tglmem,
                    ]
                ),
                Row(
                    controls=[
                        #tombol ubah data
                        FloatingActionButton( 
                        icon = icons.CHANGE_CIRCLE,
                        text=("Simpan Perubahan"),
                        bgcolor = "blue",
                        width = 340,
                        on_click = catatan.simpan_ubah_data
                    )
                    ]
                ),
            ],
        )
        return Column(controls = [catatan.tampil_data, catatan.tampil_ubahdata ])

    #fungsi utk perintah simpan ubah data
    def simpan_ubah_data(catatan, e):
        catatan.data_catatan_nama.value = catatan.inputan_catatan_nama.value
        catatan.data_catatan_tgl.value = catatan.inputan_catatan_tgl.value
        catatan.data_catatan_alamat.value = catatan.inputan_catatan_alamat.value
        catatan.data_catatan_telp.value = catatan.inputan_catatan_telp.value
        catatan.data_catatan_tglmem.value = catatan.inputan_catatan_tglmem.value
        catatan.tampil_data.visible = True
        catatan.tampil_ubahdata.visible = False
        catatan.update()

    #fungsi utk perintah form ubah data
    def ubah_data(catatan, e):
        catatan.inputan_catatan_nama.value = catatan.data_catatan_nama.value
        catatan.inputan_catatan_jk.value = catatan.data_jk_catatan.value
        catatan.inputan_catatan_tgl.value = catatan.data_catatan_tgl.value
        catatan.inputan_catatan_alamat.value = catatan.data_catatan_alamat.value
        catatan.inputan_catatan_telp.value = catatan.data_catatan_telp.value
        catatan.inputan_catatan_tglmem.value = catatan.data_catatan_tglmem.value
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

    form_aplikasi_note = FormCatatan()

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