#TODO: change the cr search to allow for exactly, greater than, less than

import tkinter as tk
from tkinter import ttk
import MonsterDB as MonDB

font = ("Ariel", 9)
lg_font = ("Ariel", 11)

class MonsterDB(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.monsters = MonDB.monsters_like('Name', '_') # find all monsters in the database
        
        tk.Tk.__init__(self, *args, **kwargs)
        #tk.Tk.iconbitmap(self, default="-some.ico-")
        tk.Tk.wm_title(self, "A Simple Pathfinder Bestiary")

        container = tk.Frame(self) # create a frame for the window
        container.pack(side="top", fill="both", expand = True) #fill will stretch in both directions, expand allows change with window size
        container.grid_rowconfigure(0, weight=1) #0 is minimum number, weight suggests imporance?
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # a place to store the window layouts

        for F in (BrowsePage, SearchPage, MultiSearch): # for all the layouts add items to the frames dictionary
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MultiSearch) #call the function show_frame to show the search page

    def show_frame(self, cont):
        if cont==BrowsePage:
            self.frames[BrowsePage].prev_b.invoke() #refresh the browse page view with the new data
        frame = self.frames[cont]
        frame.tkraise()
        #set the current frame, then raise to be the focus
    
    


class SearchPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        #this needs to happen when this frame is created
        tk.Frame.__init__(self,parent) #initialize the Frame parent

        pg_label = ttk.LabelFrame(self, text="Pathfinder Bestiary Database")
        pg_label.grid(row=1, column=0, padx=4, pady=4)  #create a LabelFrame to house the search widgets

        selection_frame = ttk.LabelFrame(self, text="Search by:")
        selection_frame.grid(row=0, column=0, columnspan=3)
        self.ser_field = tk.StringVar()
        name_rad = ttk.Radiobutton(selection_frame, text="Name", variable=self.ser_field, value="Name", )
        name_rad.pack(side="left", padx=4, pady=4)
        name_rad.invoke()
        cr_rad = ttk.Radiobutton(selection_frame, text="CR", variable=self.ser_field, value="CR")
        cr_rad.pack(side="left", padx=4, pady=4)
        environ_rad = ttk.Radiobutton(selection_frame, text="Environment", variable=self.ser_field, value="Environment")
        environ_rad.pack(side="left", padx=4, pady=4)

        input_name = ttk.Entry(pg_label)
        input_name.grid(row=1, column=1, padx=4, pady=4)
        input_name.bind('<Return>', lambda _: self.send_search(input_name.get()))
        # entry widget for search term

        ent_label = ttk.Label(pg_label, text="Search term:")
        ent_label.grid(row=1, column=0, sticky="E")

        search_b = ttk.Button(pg_label, text="Search", command = lambda: self.send_search(input_name.get()))
        search_b.grid(row=2, column=1, padx=4, pady=4, sticky="E")
        #Button to run the search script

        self.result_count = ttk.Label(self, text="")
        self.result_count.grid(row=1, column=0, padx=4, pady=2, sticky="W")
        # result set quantity shown to help used refine / revise search

        self.to_browse = ttk.Button(pg_label, text="View")
        self.to_browse.grid(padx=4, pady=2, row=3, column=1, sticky="E")
        self.to_browse.state(["disabled"])
        self.to_browse['command'] = lambda: controller.show_frame(BrowsePage)
        #browse widget will be enabled if there are items in the found set

        self.adv_search = ttk.Button(self, text="Advanced Search") #navigate to search pane
        self.adv_search.grid(padx=4, pady=2, row=3, column=2, sticky="E")
        self.adv_search['command'] = lambda: self.controller.show_frame(MultiSearch)

        input_name.focus()
    
    def send_search(self, search_text): #this function searches the database and sets the app data
        self.controller.monsters = MonDB.monsters_like(self.ser_field.get(), search_text)
        # if self.ser_field.get() == "CR":
        #     self.controller.monsters = MonDB.monsters_like(self.ser_field.get(), float(search_text))
        # else:
        #     self.controller.monsters = MonDB.monsters_like(self.ser_field.get(), search_text)

        if len(self.controller.monsters) > 1:
            self.result_count["text"] = "There are " + str(len(self.controller.monsters)) + " matches."
            self.to_browse.state(["!disabled"])
        elif len(self.controller.monsters) == 1:
            self.result_count["text"] = "There was 1 match."
            self.to_browse.state(["!disabled"])
        else:
            self.result_count["text"] = "No matches! Try again."
            self.to_browse.state(["disabled"])


class BrowsePage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        #this needs to happen when this frame is created
        tk.Frame.__init__(self,parent) #initialize the Frame parent
        '''
        DB Fields: Name=0, CR=1, XP=2, Size=4, Type=5
        Init=7, Senses=8, AC=10, HP=12, Speed=26, Melee=28
        Reach=31, Environment=47, Description_Visual=50
        Description=53
        '''
        self.list_pos = 0 # tracks were you are in the found set
        
        but_frame = ttk.LabelFrame(self, text = 'Navigate Bestiary' ) #frame for buttons to navigate the found set
        but_frame.grid(column=0, row=0, columnspan=2, sticky='nsew', padx=5, pady=4)
        self.prev_b = ttk.Button(but_frame, text = '<', command=lambda: browse_monsters(self, "<", self.controller.monsters))
        self.prev_b.pack(side='left', padx=4, pady=4)
        self.next_b = ttk.Button(but_frame, text = '>', command=lambda: browse_monsters(self, ">", self.controller.monsters))
        self.next_b.pack(side='right', padx=4, pady=4)

        self.mon_desc_text = tk.Text(self, width=50, height=5, wrap=tk.WORD, font=font)
        self.mon_desc_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5 )
        self.mon_desc_text.config(state='normal') #container for the set data -- set state to normal so you can clear contents

        self.mon_cr_text = tk.Text(self, width=10, height=1)
        self.mon_cr_text.grid(row=3, column=0, padx=5, pady=5)
        self.mon_cr_text.config(state='normal')

        search_frm = ttk.LabelFrame(self, text='Back to Search')
        search_frm.grid(row=0, column=2, columnspan=2, sticky='nsew', padx=5, pady=4)

        self.to_search = ttk.Button(search_frm, text="Basic") #navigate to search pane
        self.to_search.grid(padx=4, pady=2, row=0, column=0, sticky="E")
        self.to_search['command'] = lambda: self.controller.show_frame(SearchPage)

        self.adv_search = ttk.Button(search_frm, text="Advanced") #navigate to search pane
        self.adv_search.grid(padx=4, pady=2, row=0, column=1, sticky="E")
        self.adv_search['command'] = lambda: self.controller.show_frame(MultiSearch)


        def work_with(monster_list, list_pos):
            # populate the monster description elements with data
            self.mon_desc_text.delete("1.0", 'end')
            self.mon_desc_text.insert("1.0", (monster_list[self.list_pos][0] + ": " + monster_list[self.list_pos][50]))
            self.mon_cr_text.delete("1.0", 'end')
            self.mon_cr_text.insert("1.0", monster_list[self.list_pos][1])
        
        
        def browse_monsters(self, button_name, monster_list): #navigate through the found set
            print(str(self.list_pos) + " / " + str(len(monster_list)))
            if button_name == ">" and self.list_pos < (len(monster_list)-1):
                self.list_pos += 1
            elif button_name == "<" and self.list_pos != 0:
                self.list_pos -= 1
            work_with(monster_list, self.list_pos)
        
        work_with(self.controller.monsters, 0) # show some data (first entry) when the window is initialized
        # this currently only shows the first entry from the full dataset when the app first inializes all frames


class MultiSearch(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        #this needs to happen when this frame is created
        tk.Frame.__init__(self,parent) #initialize the Frame parent

        self.n_var, self.cr_var, self.env_var, self.desc_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
        
        
        terms_frame = ttk.LabelFrame(self, text = "Complete these search criteria")
        terms_frame.pack()

        n_label = ttk.Label(terms_frame, text = 'Name or partial name:')
        n_label.grid(row=0, column=0, sticky='e')
        cr_label = ttk.Label(terms_frame, text='CR number:')
        cr_label.grid(row=1, column=0, sticky='e')
        desc_label = ttk.Label(terms_frame, text = 'Description:')
        desc_label.grid(row=3, column=0, sticky='e')
        env_label = ttk.Label(terms_frame, text='Environment:')
        env_label.grid(row=2, column=0, sticky='e')
        
        self.cr_term = ttk.Spinbox(terms_frame, from_=0, to=30, textvariable=self.cr_var)        
        self.cr_term.grid(row=1, column=1, sticky='w', padx=4, pady=4)

        self.env_term = ttk.Combobox(terms_frame, values = [
                'desert', 'swamp', 'forest', 'mountain', 'underground',
                'marsh', 'aquatic', 'ocean', 'costal', 'plain'], textvariable=self.env_var) 
        self.env_term.grid(row=2, column=1, sticky='w', padx=4, pady=4) 

        self.desc_term = ttk.Entry(terms_frame, textvariable=self.desc_var)
        self.desc_term.grid(row=3, column=1, sticky='w', padx=4, pady=4)

        self.input_name = ttk.Entry(terms_frame, textvariable=self.n_var)
        self.input_name.grid(row=0, column=1, padx=4, pady=4, sticky='w')  
        self.input_name.bind('<ButtonPress>', lambda _: self.input_name.delete(0, 'end') )  

        action_frame = ttk.LabelFrame(self)
        action_frame.pack()

        srh_button = ttk.Button(action_frame, text="Search", command = lambda: self.send_search())
        srh_button.grid(row=0, column=0, sticky='w')

        self.to_browse = ttk.Button(action_frame, text="View")
        self.to_browse.grid(padx=4, pady=2, row=0, column=3, sticky="E")
        self.to_browse.state(["disabled"])
        self.to_browse['command'] = lambda: controller.show_frame(BrowsePage)

        self.result_count = ttk.Label(action_frame, text = "")
        self.result_count.grid(row=1, column=0, columnspan=3)

    def send_search(self): #this function searches the database and sets the app data
        print(str(self.cr_var.get()))
        if self.n_var.get() == "":
            name_term = "_"
        else:
            name_term = self.n_var.get()

        if (str(self.cr_var.get()) == '') or (str(self.cr_var.get()) == "0"):
            cr_term = '0'
            cr_crit = '> '
        # elif (str(self.cr_term.get()) == '1'):
        #     cr_term = '2'
        #     cr_crit = '< '
        else:
            #cr_term = str(self.cr_var.get()) + '%\''
            cr_term = str(self.cr_var.get())
            cr_crit = '= '
            #cr_crit = 'LIKE \'%'

        if self.env_var.get() == '':
            env_term = '_'
        else:
            env_term = self.env_var.get()
        
        if self.desc_var.get() == '':
            desc_term = '_'
        else:
            desc_term = self.desc_var.get()
        
        self.controller.monsters = MonDB.monsters_all_terms(name_term, cr_term, cr_crit, env_term, desc_term)
        # if self.ser_field.get() == "CR":
        #     self.controller.monsters = MonDB.monsters_like(self.ser_field.get(), float(search_text))
        # else:
        #     self.controller.monsters = MonDB.monsters_like(self.ser_field.get(), search_text)

        if len(self.controller.monsters) > 1:
            self.result_count["text"] = "There are " + str(len(self.controller.monsters)) + " matches."
            self.to_browse.state(["!disabled"])
        elif len(self.controller.monsters) == 1:
            self.result_count["text"] = "There was 1 match."
            self.to_browse.state(["!disabled"])
        else:
            self.result_count["text"] = "No matches! Try again."
            self.to_browse.state(["disabled"])


app = MonsterDB()
app.mainloop()