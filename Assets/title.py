import customtkinter as ctk

class Title(ctk.CTkLabel):
    def __init__(self,master,text='',anchor='w'):
        super().__init__(master=master,text=text,font=('Bahnschrift SemiBold',20,'bold'),anchor=anchor)

    def getFont(self):
        return self._font