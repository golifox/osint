import asyncio
import threading
from typing import Coroutine, Any

import customtkinter as ctk

from services.search_engine import SearchEngine
from src.db.database import db_session_manager, get_db
from src.db.models import Category, Link


class App(ctk.CTk):
    def __init__(self):
        db_session_manager.init()
        
        super().__init__()
        self.title("OSINT")
        self.geometry("750x430")
        self.minsize(750, 430)

        self.create_widgets()
        self.load_categories()
        self.load_links()

        self.categories: list[Category] = []
        self.links: list[Link] = []

    def create_widgets(self):
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, sticky="nsew")
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.top_frame)
        self.entry.pack(side="left", padx=10, pady=10)
        self.search_status_label = ctk.CTkLabel(self.top_frame, text="")
        self.search_status_label.pack(side="left", padx=10, pady=10)
        self.search_button = ctk.CTkButton(
            self.top_frame, text="Искать", command=self.on_search_click
        )
        self.search_button.pack(side="left", padx=10, pady=10)

    def load_categories(self):
        async def load():
            async for session in get_db():
                self.categories = await Category.get_all(session)

        self.thread_function(load)

    def load_links(self):
        # Загрузка ссылок из базы данных
        async def load():
            async for session in get_db():
                self.links = Link.get_all(session)

        self.thread_function(load)

    def activate_button(self, link_id):
        """Активирует кнопку и изменяет ее цвет на зеленый"""
        button = self.link_buttons.get(link_id)
        if button:
            button.configure(state="normal", fg_color="green")

    def on_search_click(self):
        nickname = self.entry.get()
        self.search_status_label.configure(text=f"Идет поиск никнейма @{nickname}...")

        threading.Thread(
            target=self.search_nickname_async, args=(nickname,), daemon=True
        ).start()

    def search_nickname_async(self, nickname):
        async def async_search():
            search_engine = SearchEngine(self.links)

            async for link, found in search_engine.search_nickname(nickname):
                if found:
                    self.activate_button(link.id)
                    self.search_status_label.configure(text="")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_search())
        loop.close()

    @staticmethod
    def thread_function(coroutine: Coroutine[Any, Any, None]):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coroutine())
        loop.close()


if __name__ == "__main__":
    app = App()
    app.mainloop()
