#import libary flet ke aplikasi
import flet as ft

#function/fungsi utama
def main (page : ft.page):

    #menampilkan title text aplikasi
    page.title = "Aplikasi Hello World"
    

    #mengatur ukuran window aplikasi
    page.window_width = 375
    page.window_height = 700
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = True
    page.scroll = "adaptive"

    #menampilkan text dalam aplikasi
    page.add(
        ft.Row(
            controls = [
                ft.Text("Hello World",
                size=30,
                color="white")
            ],
            alignment = ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            controls = [
                ft.Text("Natasya Aditiya")
            ],
            alignment = ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            controls = [
                ft.Text("202153032")
            ],
            alignment = ft.MainAxisAlignment.CENTER
        )
    )
    
    #Menampilkan ICON dalam aplikasi
    page.add(
        ft.Row(
            controls = [
                    ft.Icon(
                    name = ft.icons.PERSON,
                    color ="teal",
                    size=100
                ),
                    ft.Icon(
                    name = ft.icons.BEACH_ACCESS,
                    color ="red",
                    size=100
                    ),
                    ft.Icon(
                    name = ft.icons.AUDIOTRACK,
                    color ="white",
                    size=100
                    )
            ],
             alignment = ft.MainAxisAlignment.CENTER
        )
    )

    #Menampilkan gambar dalam aplikasi
    page.add(
        ft.Image(
            src="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTXMIZTJcW9kGnK7JD5Ml4ZdqpqxyjoxtBPsIzdgJpISkP_JAtk",
            width=300,
            height=250,
        ),
        ft.Container(
            content=ft.Text("JohnCena"),
            image_src="gambar1.webp",
            width=300,
            height=250,
            image_fit= ft.ImageFit.COVER,
            border_radius =10
        ),
        ft.Container(
            content=ft.Text("JohnCena"),
            image_src="gambar1.webp",
            width=300,
            height=250,
            border= ft.border.all(2, ft.colors.AMBER),
            image_fit= ft.ImageFit.COVER,
            border_radius =10
        )
    )
    

    #menampilkan avatar dalam aplikasi
    page.add(
        ft.Stack(
            [
                ft.CircleAvatar(
                    foreground_image_url="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTXMIZTJcW9kGnK7JD5Ml4ZdqpqxyjoxtBPsIzdgJpISkP_JAtk",
                    width=300,
                    height=250,
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.colors.GREEN, radius=15),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=160,
            height=150
        ),

        ft.CircleAvatar(
            content=ft.Icon(ft.icons.PERSON_ADD, size=150),
            color = ft.colors.WHITE,
            bgcolor= ft.colors.TEAL,
            width=200,
            height=200
        )
    )

#mengatur output aplikasi
ft.app(target = main)
# ft.app(target = main, view=ft.AppView.WEB_BROWSER)