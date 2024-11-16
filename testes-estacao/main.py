import flet as ft

import config.page
import config.routes

def main(page: ft.Page):


    config.routes.RouteConfig(page)
    config.page.PageConfig(page)
    # firebase = config.firebase.FirebaseConfig(page)


ft.app(target=main, assets_dir="assets")