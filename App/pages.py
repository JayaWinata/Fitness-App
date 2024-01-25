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

        self.data_frame = ctk.CTkFrame(self,width=(master.winfo_width()/2-10))
        self.data_frame.pack_configure(fill='y',side='left',padx=10,pady=10)
        self.data_frame.bind('<Button-1>',lambda x: self.data(master))

    def render_plot():
        pass

    def stats(self,master):
        self.destroy()
        Stats(master)

    def schedule(self,master):
        self.destroy()
        Schedule(master)

    def data(self,master):
        self.destroy()
        Data(master)

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

class Data(ctk.CTkScrollableFrame):
    def __init__(self,master: ctk.CTk):
        super().__init__(master)
        self.configure(fg_color='transparent')
        self.pack(expand=1,fill='both',padx=10,pady=10)
        self.title = Title(self,text='Report')
        self.title.pack_configure(fill='x',side='top',padx=20)

        self.calories_frame = ctk.CTkFrame(self,height=(master.winfo_height() / 4 -10))
        self.calories_frame.pack_configure(padx=10,pady=10,fill='x',side='top')
        self.change_calories_lable = ctk.CTkLabel(self.calories_frame,text='Change daily calories >>',text_color='#5f5f5f',anchor='e')
        self.change_calories_lable.pack_configure(side='bottom',fill='x',padx=10,pady=10)
        self.change_calories_lable.bind('<Button-1>',lambda x: self.input_calories())
        
        self.data_frame = ctk.CTkFrame(self,height=(master.winfo_height() * 3 / 4 -10))
        self.data_frame.pack_configure(padx=10,pady=10,fill='x',side='top')
        self.data_dict = {
            'Gender': 'Male',
            'Height':180,
            'Weight': 70,
            'Age':23,
            'Body Fat': 30,
        }

        for key,value in self.data_dict.items():
            frame = ctk.CTkFrame(self.data_frame,border_color='white',border_width=.5,fg_color='transparent')
            frame.pack_configure(fill='x',side='top',padx=10,pady=10)
            ctk.CTkLabel(frame,text=key).pack_configure(side='left',padx=10)
            ctk.CTkLabel(frame,text=value).pack_configure(side='right',padx=10)

        self.edit_button = ctk.CTkButton(self,text='Edit data',command=self.edit_data)
        self.edit_button.pack_configure(fill='x',side='top',padx=10,pady=10)
        self.back_lable = ctk.CTkLabel(master=self,text='<< Back',anchor='w',text_color='#5f5f5f')
        self.back_lable.pack_configure(padx=20,pady=10,fill='x',side='top')
        self.back_lable.bind('<Button-1>',lambda x: self.back(master))

    def back(self,master):
        self.pack_forget()
        self.destroy()
        Dashboard(master)
    
    def input_calories(self):
        input_dialog = ctk.CTkInputDialog(text='Input your daily calories:',title='',entry_fg_color='#232D3F')
        x = (input_dialog.winfo_screenwidth() - input_dialog.winfo_width()) // 2 -50
        y = (input_dialog.winfo_screenheight() - input_dialog.winfo_height()) // 2
        input_dialog.geometry(f'{input_dialog.winfo_width()}x{input_dialog.winfo_height()}+{x}+{y}')

    def edit_data(self):

        def save():
            frame.destroy()
            window.destroy()
        
        def cancel():
            frame.destroy()
            window.destroy()

        window = ctk.CTk()
        x = (window.winfo_screenwidth() - 250) // 2 -50
        y = (window.winfo_screenheight() - 300) // 2
        window.geometry(f'{250}x{300}+{x}+{y}')
        frame = ctk.CTkScrollableFrame(window)
        frame.configure(fg_color='transparent')
        frame.pack(expand=1,fill='both',padx=10,pady=10)

        for i in self.data_dict.keys():
            label = str(i + ": ")
            ctk.CTkLabel(frame,text=label,anchor='w').pack_configure(fill='x',side='top',padx=15,pady=5)
            if (i == 'Gender'):
                option = ['Male','Female']
                ctk.CTkComboBox(frame,values=option,border_width=0,dropdown_fg_color='#232D3F',dropdown_hover_color='#008170').pack_configure(padx=10,pady=10,fill='x',side='top')
            else:
                ctk.CTkEntry(frame,fg_color='#232D3F').pack_configure(fill='x',side='top',padx=10,pady=5)
        
        button_frame = ctk.CTkFrame(frame,fg_color='transparent')
        button_frame.pack_configure(side='top',fill='x',padx=10,pady=10)
        save_button = ctk.CTkButton(master=button_frame,width=(button_frame.winfo_width() / 2 - 10),text='Save',command=save)
        save_button.pack_configure(side='left',fill='y')
        ctk.CTkLabel(master=button_frame,text='').pack_configure(side='left',padx=10)
        cancel_button = ctk.CTkButton(master=button_frame,width=(button_frame.winfo_width() / 2 - 10),text='Cancel',command=cancel)
        cancel_button.pack_configure(side='left',fill='both')

        window.mainloop()