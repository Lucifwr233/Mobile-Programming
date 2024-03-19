import flet as ft
def main (page : ft.page):
    #menampilkan title text aplikasi
    page.title = "UI Form"

    #mengatur ukuran window aplikasi
    page.window_width = 375
    page.window_height = 700
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = True
    page.scroll = "adaptive"

    #form inputan
    field_input_1 = ft.TextField(label = "Standard")
    field_input_2 = ft.TextField(label = "Disable", disabled=True, value="Nama Depan")
    field_input_3 = ft.TextField(label = "Read Only", read_only=True, value="Nama Belakang")
    field_input_4 = ft.TextField(label = "Dengan Placeholder", hint_text="silahkan isi")
    field_input_5 = ft.TextField(label = "Dengan sebuah Icon", icon=ft.icons.EMOJI_EMOTIONS)

    page.add(
        field_input_1, field_input_2,
        field_input_3, field_input_4,
        field_input_5,

        ft.TextField(label = "nim")
    )

    text_output = ft.Text()
    def textbox_changed(e):
            text_output.value = e.control.value
            page.update()
    field_contoh = ft.TextField(
        label="Textbox dengan function output",
        on_change=textbox_changed
    )
    page.add(
        field_contoh,
        text_output
    )

    #button elevated icon
    page.add(
        ft.ElevatedButton("Button Elevated", icon="chair_outlined"),
        ft.ElevatedButton(
            "Button dengan colorfull icon",
            icon="park_rounded",
            icon_color="green400"
        )   
    )

    #button outlined version
    page.add(
        ft.ElevatedButton("Button Elevated", icon="chair_outlined"),
        ft.OutlinedButton(
            "Button dengan colorfull icon",
            icon="park_rounded",
            icon_color="green400"
        )   
    )

ft.app(target = main)