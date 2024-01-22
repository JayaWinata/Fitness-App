import customtkinter as ctk

class Title(ctk.CTkLabel):
    def __init__(self,text,anchor,master):
        super().__init__(master=master,text=text,font=('Bahnschrift SemiBold',20,'bold'),anchor=anchor)