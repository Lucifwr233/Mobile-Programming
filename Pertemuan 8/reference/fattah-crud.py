#memasukkan library flet ke aplikasi
#import flet as ft
import datetime
import flet
from flet import *
import mysql.connector

# CONECTION TO DB
mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "",
	database = "fattah_crud_mobile"
)
cursor = mydb.cursor()

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

        crud.data_member = DataTable(
            columns=[
                DataColumn(Text("ID")),
                DataColumn(Text("Nama")),
                DataColumn(Text("Jenis Kelamin")),
                DataColumn(Text("Tanggal Lahir")),
                DataColumn(Text("Alamat")),
                DataColumn(Text("Telepon")),
                DataColumn(Text("Tanggal Gabung Member")),
            ],
            rows= []
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
                        on_click= crud.simpan_data_baru,
                    )
                    ]
                ),

            #layout rekapan data
            crud.layout_data,
            #tanggal
            crud.opsi_tanggal,
            ]  
        )

            # DELETE FUNCTION
        def hapus_data(e):
            print("you selected id is = ", e.control.data['id'])
            try:
                sql = "DELETE FROM membership WHERE id = %s"
                val = (e.control.data['id'],)
                cursor.execute(sql, val)
                mydb.commit()
                print("you deleted !")
                data_mahasiswa.rows.clear()
                tampil_data_mahasiswa()

                # AND SHOW SNACKBAR
                page.snack_bar = SnackBar(
                    Text("Data success Deleted",size = 30),
                    bgcolor = "red"
                )
                page.snack_bar.open = True
                page.update()
            except Exception as e:
                print(e)
                print("error you code for delete")

        def tampil_data_member():
            # GET ALL DATA FROM DATABASE AND PUSH TO DATATABLE
            cursor.execute("SELECT * FROM membership")
            result = cursor.fetchall()

            # AND PUSH DATA TO DICT
            columns = [column[0] for column in cursor.description]
            rows = [dict(zip(columns,row)) for row in result]

            # LOOP AND PUSH
            for row in rows:
                data_member.rows.append(
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
                                    IconButton("delete",icon_color = "red",
                                        data = row,
                                        on_click = hapus_data
                                    ),
                                    IconButton("create",icon_color = "red",
                                        data = row,
                                        on_click = tampil_ubah_data
                                    ),
                                ])
                            ),
                        ]
                    )

                )
            page.update()
            # calling data from database when app open for the first time
            tampil_data_member()

            def simpan_data_baru(e):
                try:
                    sql = "INSERT INTO membership (nama,jekel,tgl_lahir,alamat,telp,tgl_member) VALUES(%s,%s)"
                    val = (crud.inputan_nama.value,crud.inputan_jekel.value,crud.inputan_tgl.value,crud.inputan_alamat.value,crud.inputan_telp.value,crud.inputan_tgl_member.value)
                    cursor.execute(sql,val)
                    mydb.commit()
                    print(cursor.rowcount,"YOU RECORD INSERT !!!")

                    # AND CLEAR ROWS IN TABLE AND PUSH FROM DATABASE AGAIN
                    data_member.rows.clear()
                    tampil_data_member()

                    # AND SHOW SNACKBAR
                    page.snack_bar = SnackBar(
                        Text("Data success add",size = 30),
                        bgcolor="green"

                    )
                    page.snack_bar.open = True
                    page.update()
                except Exception as e:
                    print(e)
                    print("error you CODE !!!!")
     

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
        FormCrud()
    )

#mengatur output aplikasi
flet.app(target = main)
#ft.app(target = main, view = ft.AppView.WEB_BROWSER)