#import libary flet ke aplikasi
import flet 
from flet import *

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

    #menampilkan objek
    judul_aplikasi = "Aplikasi Note"
    page.add(
        Row(
                controls = [
                Text(judul_aplikasi, 
                size = 30,
                weight= "bold",
                color = "white"   
            )
        ],
        alignment=MainAxisAlignment.CENTER

    )

)

#mengatur output aplikasi
flet.app(target = main)
