import customtkinter as ctk
from Assets.title import Title

ctk.set_default_color_theme('./Assets/theme.json')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('MyFitness')

        self.width = 400
        self.height = 500
        x = (self.winfo_screenwidth() - self.width) // 2 -50
        y = (self.winfo_screenheight() - self.height) // 2

        self.geometry(f'{self.height}x{self.width}+{x}+{y}')
        self.resizable(False,False)

    def getFont(self,size,weight,family='Adobe Gothic Std B',**kwargs):
        font =  ctk.CTkFont(family=family,size=size,weight=weight)
        for key,value in kwargs.items():
            font.configure(**{key: value})
        return font
    
class Dashboard(ctk.CTkFrame):
    def __init__(self,master: ctk.CTk):
        super().__init__(master)
        self.pack_configure(expand=1,fill='both',padx=10,pady=10)
        self.configure(fg_color='transparent')
        self.title = Title(master=self,anchor='w',text='Dashboard')
        self.title.pack_configure(fill='x',side='top',padx=20)
        
        self.plot_frame = ctk.CTkFrame(self,height=(master.winfo_height()/3))
        self.plot_frame.pack_configure(fill='x',side='top',padx=10,pady=10)
        self.plot_frame.bind('<Button-1>',lambda x: self.stats(master))

        self.schedule_frame = ctk.CTkFrame(self,width=(master.winfo_width()/2-10))
        self.schedule_frame.pack_configure(fill='y',side='left',padx=10,pady=10)
        self.schedule_frame.bind('<Button-1>',lambda x: self.schedule(master))

        self.report_frame = ctk.CTkFrame(self,width=(master.winfo_width()/2-10))
        self.report_frame.pack_configure(fill='y',side='left',padx=10,pady=10)

    def render_plot():
        pass

    def stats(self,master):
        self.destroy()
        Stats(master)

    def schedule(self,master):
        self.destroy()
        Schedule(master)

class Stats(ctk.CTkScrollableFrame):
    def __init__(self,master: ctk.CTk):
        super().__init__(master)
        self.pack(expand=1,fill='both',padx=10,pady=10)
        self.configure(fg_color='transparent')
        self.title = Title(self,text='Stats')
        self.title.pack_configure(fill='x',side='top',padx=20)

        self.body_weight_frame = ctk.CTkFrame(self,height=(master.winfo_height() / 3 -10))
        self.body_weight_frame.pack_configure(fill='x',side='top',padx=10,pady=10)
        
        self.calories_frame = ctk.CTkFrame(self,height=(master.winfo_height() / 3 -10))
        self.calories_frame.pack_configure(fill='x',side='top',padx=10,pady=10)
        
        self.body_fat_frame = ctk.CTkFrame(self,height=(master.winfo_height() / 3 -10))
        self.body_fat_frame.pack_configure(fill='x',side='top',padx=10,pady=10)

        self.back_lable = ctk.CTkLabel(master=self,text='<< Back',anchor='w',text_color='#5f5f5f')
        self.back_lable.pack_configure(padx=20,pady=10,fill='x',side='top')
        self.back_lable.bind('<Button-1>',lambda x: self.back(master))

    def back(self,master):
        self.pack_forget()
        self.destroy()
        Dashboard(master)

class Schedule(ctk.CTkScrollableFrame):
    def __init__(self,master: ctk.CTk):
        super().__init__(master)
        self.pack(expand=1,fill='both',padx=10,pady=10)
        self.configure(fg_color='transparent')
        self.title = Title(self,text='Schedule')
        self.title.pack_configure(fill='x',side='top',padx=20)

        self.days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        self.combo_box = ctk.CTkComboBox(self,values=self.days,border_width=0,dropdown_fg_color='#232D3F',dropdown_hover_color='#008170')
        self.combo_box.pack_configure(padx=10,pady=10,fill='x',side='top')

        self.list_frame = ctk.CTkFrame(master=self,fg_color='transparent',border_color='#5f5f5f',border_width=1)
        self.list_frame.pack_configure(fill='x',expand=1,padx=10,pady=10,side='top')
        self.temp = ['1','ttgertyrw','34546','34terfs','rwesf']
        for i in self.temp:
            ctk.CTkLabel(master=self.list_frame,text=i,anchor='w').pack_configure(padx=5,pady=2,fill='x',side='top')

        self.button_frame = ctk.CTkFrame(self,fg_color='transparent')
        self.button_frame.pack_configure(padx=10,pady=10,side='top',fill='x')
        self.new_button = ctk.CTkButton(self.button_frame,text='New',width=(master.winfo_width() / 4 +10))
        self.new_button.grid_configure(row=0,column=0,padx=5)
        self.edit_button = ctk.CTkButton(self.button_frame,text='Edit',width=(master.winfo_width() / 4 + 10))
        self.edit_button.grid_configure(row=0,column=1,padx=5)
        self.new_button = ctk.CTkButton(self.button_frame,text='Delete',width=(master.winfo_width() / 4 + 10))
        self.new_button.grid_configure(row=0,column=2,padx=5)

        self.back_lable = ctk.CTkLabel(master=self,text='<< Back',anchor='w',text_color='#5f5f5f')
        self.back_lable.pack_configure(padx=20,pady=10,fill='x',side='top')
        self.back_lable.bind('<Button-1>',lambda x: self.back(master))

    def back(self,master):
        self.pack_forget()
        self.destroy()
        Dashboard(master)

