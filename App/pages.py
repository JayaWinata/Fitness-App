import sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageFilter
sys.path.append('../')
from Database import db
from BodyGauge import gauge
from Assets.title import Title
from Assets import plot

ctk.set_default_color_theme('../Assets/theme.json')

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
        self.data_frame.pack_configure(fill='both',side='left',padx=10,pady=10,expand=1)
        self.data_frame.bind('<Button-1>',lambda x: self.data(master))

        self.show_plot(master)
        self.show_schedule(master)
        self.show_data(master)

    def show_plot(self,master):
        plot.plot_data('weight',10)
        raw_image = Image.open('../Assets/Image/weight.png')
        raw_image = raw_image.filter(ImageFilter.DETAIL)
        image = ctk.CTkImage(dark_image=raw_image,size=(450,120))
        image = ctk.CTkLabel(master=self.plot_frame,image=image,text='')
        image.pack_configure(padx=5,pady=5)
        image.bind('<Button-1>',lambda x: self.stats(master))

    def show_schedule(self,master):
        title = Title(master=self.schedule_frame,text='Today Schedule')
        title.configure(font=('Bahnschrift SemiBold',20,'bold'))
        title.pack(padx=30,pady=10,side='top',fill='x')
        data = db.get_current_schedule()
        if data:
            for i in data[:3]:
                label = ctk.CTkLabel(self.schedule_frame,text=f'{i[0]}. {i[1]}',anchor='w')
                label.pack(padx=10,pady=1,fill='x',side='top')
                label.bind('<Button-1>',lambda x: self.schedule(master))
        else:
            for i in range(3):
                label = ctk.CTkLabel(self.schedule_frame,text='',anchor='w')
                label.pack(padx=10,pady=1,fill='x',side='top')
                label.bind('<Button-1>',lambda x: self.schedule(master))
        more_label = ctk.CTkLabel(self.schedule_frame,text='More >>',text_color='#5f5f5f',anchor='e')
        more_label.pack_configure(padx=20,pady=5,side='bottom',fill='x')
        more_label.bind('<Button-1>',lambda x: self.schedule(master))

    def show_data(self,master):
        bmi_label = ctk.CTkLabel(self.data_frame,anchor='w',text='Your BMI score:')
        bmi_label.pack_configure(padx=20,fill='x',pady=5,side='top')
        temp_text = f'{round(gauge.get_bmi()[0],2)} ({gauge.get_bmi()[1]})'
        bmi_score = ctk.CTkLabel(self.data_frame,anchor='w',text=temp_text,font=('TkDefaultFont',15, 'bold'))
        bmi_score.pack_configure(padx=20,fill='x',side='top')
        
        add_label = ctk.CTkLabel(self.data_frame,anchor='w',text='Add calories:')
        add_label.pack_configure(padx=20,fill='x',pady=5,side='top')
        add_frame = ctk.CTkFrame(self.data_frame, height=(self.data_frame.winfo_height() / 2))
        add_frame.pack_configure(side='top',fill='x',padx=20)
        add_entry = ctk.CTkEntry(add_frame, fg_color='#232D3F')
        add_entry.pack_configure(side='left',fill='y',padx=2)

        def add_cal():
            db.add_calories(int(add_entry.get()))
            add_entry.delete(0,tk.END)
        add_button = ctk.CTkButton(add_frame,text='+',command=add_cal)
        add_button.pack_configure(side='left',fill='both',padx=2)

        more_label = ctk.CTkLabel(self.data_frame,text='More >>',text_color='#5f5f5f',anchor='e')
        more_label.pack_configure(padx=20,pady=5,side='bottom',fill='x')
        for i in self.data_frame.winfo_children():
            i.bind('<Button-1>',lambda x: self.data(master))


    def stats(self,master):
        self.pack_forget()
        self.destroy()
        Stats(master)

    def schedule(self,master):
        self.pack_forget()
        self.destroy()
        Schedule(master)

    def data(self,master):
        self.pack_forget()
        self.destroy()
        Data(master)

class Stats(ctk.CTkScrollableFrame):
    def __init__(self,master: ctk.CTk):
        super().__init__(master)
        self.pack(expand=1,fill='both',padx=10,pady=10)
        self.configure(fg_color='transparent')
        self.title = Title(self,text='Stats')
        self.title.pack_configure(fill='x',side='top',padx=20)

        self.show_stats(master)

        self.back_lable = ctk.CTkLabel(master=self,text='<< Back',anchor='w',text_color='#5f5f5f')
        self.back_lable.pack_configure(padx=20,pady=10,fill='x',side='top')
        self.back_lable.bind('<Button-1>',lambda x: self.back(master))

    def show_stats(self,master):
        for i in plot.column_name:
            parent = ctk.CTkFrame(self,height=(master.winfo_height() / 3 -10))
            parent.pack_configure(fill='x',side='top',padx=10,pady=10)
            raw_image = Image.open(f'../Assets/Image/{i}.png')
            raw_image = raw_image.filter(ImageFilter.DETAIL)
            image = ctk.CTkImage(dark_image=raw_image,size=(420,120))
            image = ctk.CTkLabel(master=parent,image=image,text='')
            image.pack_configure(padx=5,pady=5)

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
        self.show_button = ctk.CTkButton(self,text='Show Schedule',command=self.show_schedule)
        self.show_button.pack_configure(padx=10,pady=10,fill='x',side='top')
        self.selected_day = ctk.CTkLabel(self,text='Selected day:',anchor='w')
        self.selected_day.pack_configure(fill='x',side='top',padx=20,pady=5)

        self.list_frame = ctk.CTkFrame(master=self,height=100,border_color='#5f5f5f',border_width=1,fg_color='transparent')
        self.list_frame.pack_configure(fill='x',padx=10,pady=10,side='top')

        self.button_frame = ctk.CTkFrame(self,fg_color='transparent')
        self.button_frame.pack_configure(padx=10,pady=10,side='top',fill='x')
        self.new_button = ctk.CTkButton(self.button_frame,text='New',width=(master.winfo_width() / 4 +10),command=lambda: self.add(master))
        self.new_button.grid_configure(row=0,column=0,padx=5)
        self.edit_button = ctk.CTkButton(self.button_frame,text='Edit',width=(master.winfo_width() / 4 + 10),command=self.edit)
        self.edit_button.grid_configure(row=0,column=1,padx=5)
        self.delete_button = ctk.CTkButton(self.button_frame,text='Delete',width=(master.winfo_width() / 4 + 10),command=self.delete)
        self.delete_button.grid_configure(row=0,column=2,padx=5)

        self.additional_frame = ctk.CTkFrame(self,fg_color='transparent',height=35)
        self.additional_frame.pack_configure(fill='x',side='top',padx=20,pady=5)

        self.error = ctk.CTkLabel(self,text='',anchor='w')
        self.error.pack_configure(fill='x',side='top',padx=20,pady=10)

        self.back_lable = ctk.CTkLabel(master=self,text='<< Back',anchor='w',text_color='#5f5f5f')
        self.back_lable.pack_configure(padx=20,pady=10,fill='x',side='top')
        self.back_lable.bind('<Button-1>',lambda x: self.back(master))

    def show_schedule(self):
        self.selected_day.configure(text=f'Selected day: {self.combo_box.get()}')
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.list_frame.configure(height=100)
        self.data = db.get_schedule(self.combo_box.get())
        if self.data:
            for i in self.data:
                ctk.CTkLabel(master=self.list_frame,text=f'{i[0]}. {i[1]}',anchor='w').pack_configure(padx=5,pady=2,fill='x',side='top')

    def edit(self):
        self.clear_frame()
        self.additional_frame.pack_configure(fill='x',side='top',padx=20)
        order_entry = ctk.CTkEntry(master=self.additional_frame,placeholder_text='List number',width=self.additional_frame.winfo_width() / 5,fg_color='#232D3F',border_width=0)
        order_entry.pack_configure(fill='y',side='left',padx=5)
        value_entry = ctk.CTkEntry(master=self.additional_frame,placeholder_text='Value',fg_color='#232D3F',border_width=0,width=(self.additional_frame.winfo_width()*3/5))
        value_entry.pack_configure(fill='y',side='left',padx=5)

        def apply():
            order = order_entry.get()
            value = value_entry.get()
            order_list = [i[0] for i in self.data] if self.data else []
            if (int(order) in order_list) and value:
                db.update_schedule([order,value,self.combo_box.get()])
                self.error.configure(text='Please re-enter this page to see updated data!')
                self.clear_frame()
            else:
                self.error.configure('Error occured!')

        apply_button = ctk.CTkButton(self.additional_frame,width=(self.additional_frame.winfo_width()/5),text='Apply',command=apply)
        apply_button.pack_configure(fill='y',side='left',padx=5)
    
    def add(self,master):
        self.clear_frame()
        self.additional_frame.pack_configure(fill='x',side='top',padx=20)
        order_entry = ctk.CTkEntry(master=self.additional_frame,placeholder_text='List number',width=self.additional_frame.winfo_width() / 5,fg_color='#232D3F',border_width=0)
        order_entry.pack_configure(fill='y',side='left',padx=5)
        value_entry = ctk.CTkEntry(master=self.additional_frame,placeholder_text='Value',fg_color='#232D3F',border_width=0,width=(self.additional_frame.winfo_width()*3/5))
        value_entry.pack_configure(fill='y',side='left',padx=5)

        def apply():
            order = order_entry.get()
            value = value_entry.get()
            order_list = [i[0] for i in self.data] if self.data else []
            if (int(order) not in order_list) and value:
                db.add_schedule((order,value,self.combo_box.get()))
                ctk.CTkLabel(master=self.list_frame,text=f'{order}. {value}',anchor='w').pack_configure(padx=5,pady=2,fill='x',side='top')
                self.error.configure(text='')
                self.clear_frame()
            else:
                self.error.configure(text='The list number must be unique, and value must be filled!')

        apply_button = ctk.CTkButton(self.additional_frame,width=(self.additional_frame.winfo_width()/5),text='Apply',command=apply)
        apply_button.pack_configure(fill='y',side='left',padx=5)

    def delete(self):
        self.clear_frame()
        self.additional_frame.pack_configure(fill='x',side='top',padx=20)
        order_entry = ctk.CTkEntry(master=self.additional_frame,placeholder_text='List number',width=self.additional_frame.winfo_width() / 5,fg_color='#232D3F',border_width=0)
        order_entry.pack_configure(fill='y',side='left',padx=5)

        def apply():
            order = order_entry.get()
            order_list = [i[0] for i in self.data] if self.data else []
            if (int(order) in order_list):
                db.delete_schedule((order,self.combo_box.get()))
                self.error.configure(text='Please re-enter this page to check the deleted data!')
                self.clear_frame()
            else:
                self.error.configure(text='Error occured!')


        apply_button = ctk.CTkButton(self.additional_frame,width=(self.additional_frame.winfo_width()*4/5),text='Delete',command=apply)
        apply_button.pack_configure(fill='y',side='left',padx=5)

    def clear_frame(self):
        widget_list = self.additional_frame.winfo_children()
        for i in widget_list:
            i.destroy()

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
        ctk.CTkLabel(self.calories_frame,text='Your calories today:',anchor='w').pack_configure(padx=20,pady=5,fill='y',side='left')
        text = f'{db.get_calories()} / {db.get_calories_limit()}'
        self.cal_desc = ctk.CTkLabel(self.calories_frame,text=text,anchor='e',font=('TkDefaultFont',16,'bold'))
        self.cal_desc.pack_configure(fill='y',padx=20,pady=5,side='right')

        
        self.data_frame = ctk.CTkFrame(self,height=(master.winfo_height() * 3 / 4 -10))
        self.data_frame.pack_configure(padx=10,pady=10,fill='x',side='top')

        for key,value in gauge.get_body_metrics().items():
            frame = ctk.CTkFrame(self.data_frame,border_color='white',border_width=.5,fg_color='transparent')
            frame.pack_configure(fill='x',side='top',padx=10,pady=10)
            ctk.CTkLabel(frame,text=key).pack_configure(side='left',padx=10)
            ctk.CTkLabel(frame,text=value).pack_configure(side='right',padx=10)

        self.change_button = ctk.CTkButton(self,text='Change calories limit',command=self.input_calories)
        self.change_button.pack_configure(fill='x',side='top',padx=10,pady=10)
        self.edit_button = ctk.CTkButton(self,text='Edit data',command=lambda: self.edit_data(master))
        self.edit_button.pack_configure(fill='x',side='top',padx=10,pady=10)

        self.back_lable = ctk.CTkLabel(master=self,text='<< Back',anchor='w',text_color='#5f5f5f')
        self.back_lable.pack_configure(padx=20,pady=10,fill='x',side='top')
        self.back_lable.bind('<Button-1>',lambda x: self.back(master))

    def back(self,master):
        self.pack_forget()
        self.destroy()
        Dashboard(master)

    def edit_data(self,master):
        self.pack_forget()
        self.destroy()
        EditData(master)
    
    def input_calories(self):
        input_dialog = ctk.CTkInputDialog(text='Input your daily calories:',title='',entry_fg_color='#232D3F')
        x = (input_dialog.winfo_screenwidth() - input_dialog.winfo_width()) // 2 -50
        y = (input_dialog.winfo_screenheight() - input_dialog.winfo_height()) // 2
        input_dialog.geometry(f'{input_dialog.winfo_width()}x{input_dialog.winfo_height()}+{x}+{y}')
        db.set_calories_limit(input_dialog.get_input())
        text = f'{db.get_calories()} / {db.get_calories_limit()}'
        self.cal_desc.configure(text=text)

class EditData(ctk.CTkScrollableFrame):
        def __init__(self,master: ctk.CTk):
            super().__init__(master)
            self.configure(fg_color='transparent')
            self.pack(expand=1,fill='both',padx=10,pady=10)
            self.title = Title(self,'Edit Data')
            self.title.pack_configure(side='top',fill='x',padx=20,pady=5)

            self.gender_label = ctk.CTkLabel(self,text='Gender:',anchor='w')
            self.gender_label.pack_configure(fill='x',side='top',padx=45,pady=5)
            option = ['Male','Female']
            self.gender_cb = ctk.CTkComboBox(self,values=option,border_width=0,dropdown_fg_color='#232D3F',dropdown_hover_color='#008170',variable=ctk.StringVar(value=gauge.get_body_metrics()['Gender']))
            self.gender_cb.pack_configure(padx=40,pady=5,fill='x',side='top')

            self.age_label = ctk.CTkLabel(self,text='Age:',anchor='w')
            self.age_label.pack_configure(fill='x',side='top',padx=45,pady=5)
            self.age_entry = ctk.CTkEntry(self,fg_color='#232D3F',textvariable=ctk.StringVar(value=gauge.get_body_metrics()['Age']))
            self.age_entry.pack_configure(fill='x',side='top',padx=40,pady=5)

            self.weight_label = ctk.CTkLabel(self,text='Weight:',anchor='w')
            self.weight_label.pack_configure(fill='x',side='top',padx=45,pady=5)
            self.weight_entry = ctk.CTkEntry(self,fg_color='#232D3F', textvariable=ctk.StringVar(value=gauge.get_body_metrics()['Weight']))
            self.weight_entry.pack_configure(fill='x',side='top',padx=40,pady=5)

            self.height_label = ctk.CTkLabel(self,text='Height:',anchor='w')
            self.height_label.pack_configure(fill='x',side='top',padx=45,pady=5)
            self.height_entry = ctk.CTkEntry(self,fg_color='#232D3F',textvariable=ctk.StringVar(value=gauge.get_body_metrics()['Height']))
            self.height_entry.pack_configure(fill='x',side='top',padx=40,pady=5)
            
            activity_list = [value for _,value in gauge.get_activity_mapper().items()]
            self.activity_label = ctk.CTkLabel(self,text='Activity:',anchor='w')
            self.activity_label.pack_configure(fill='x',side='top',padx=45,pady=5)
            self.activity_cb = ctk.CTkComboBox(self,values=activity_list,border_width=0,dropdown_fg_color='#232D3F',dropdown_hover_color='#008170',variable=ctk.StringVar(value=gauge.get_body_metrics()['Activity']))
            self.activity_cb.pack_configure(padx=40,pady=5,fill='x',side='top')

            ctk.CTkLabel(self,text='Please restart the app after edit your data!',anchor='w').pack_configure(padx=45,pady=10,side='top',fill='x')
            
            button_frame = ctk.CTkFrame(self,fg_color='transparent')
            button_frame.pack_configure(side='top',fill='x',padx=40,pady=20)
            save_button = ctk.CTkButton(master=button_frame,width=(button_frame.winfo_width() / 2 - 10),text='Save',command=self.save)
            save_button.pack_configure(side='left',fill='y')
            ctk.CTkLabel(master=button_frame,text='').pack_configure(side='left',padx=10)
            cancel_button = ctk.CTkButton(master=button_frame,width=(button_frame.winfo_width() / 2 - 10),text='Cancel',command=lambda:self.cancel(master))
            cancel_button.pack_configure(side='left',fill='both')

        def save(self):
            data_tuple = (self.gender_cb.get(),self.age_entry.get(),self.weight_entry.get(),self.height_entry.get(),gauge.get_activity_mapper(self.activity_cb.get(),reversed=True))
            db.insert_data(data_tuple)

        def cancel(self,master):
            self.pack_forget()
            self.destroy()
            Data(master)