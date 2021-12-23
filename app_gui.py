"""module de l'ui de l'app"""
from tkinter import Listbox, Scrollbar, Tk, ttk, N,W,E,S, END
from tkinter.constants import CENTER
from helpers import anfr
import app_popin




class MyApp(Tk):
    """ Class encapsulant l'app"""

    def __init__(self):
        Tk.__init__(self)
        self.withdraw()
        splash = app_popin.Splash(self)


        self.title("Visualisateur de DAS")
        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.srollbar_width = 0

        self.original_records = []
        success = self.get_das_original_data()

        if success:

            ## finished loading so destroy splash
            splash.destroy()

            ## show window again
            self.deiconify()

            self.list_widget_result =[]

            ttk.Label(self.mainframe, text="Selectionner \r une marque").grid(
                column=0,
                row=1,
                sticky=W)

            brands = self.get_brand_list()
            #brand_name_entry = ttk.Entry(self.mainframe, width=7, textvariable="marque")
            self.brand_name_entry =Listbox(self.mainframe,listvariable=brands)
            self.brand_name_entry.grid(
                column=1,
                row=1,
                sticky=(W, E))
            index_brand = 0
            for brand in brands:
                self.brand_name_entry.insert(index_brand, brand)
                index_brand+=1

            scrollbar_brands = Scrollbar(self.mainframe)
            scrollbar_brands.grid(
                column=2,
                row=1,
                sticky=(N,W, S))

            self.brand_name_entry.config(yscrollcommand = scrollbar_brands.set)

            scrollbar_brands.config(command = self.brand_name_entry.yview)


            ttk.Button(self.mainframe, text="Rechercher", command=self.search_mobile).grid(
                column=4,
                row=1,
                sticky=(W,E))


            columns = ("marque","modele","conformite_aux_normes","ref_dossier")
            self.result_table = ttk.Treeview(self.mainframe,column =columns,show="headings")
            self.result_table.grid(row=8, column=0, rowspan=11, columnspan=7, padx=5, pady=5)

            self.result_table.column("marque", anchor=CENTER, width=150)
            self.result_table.heading("marque", text="Marque")
            self.result_table.column("modele", anchor=CENTER)
            self.result_table.heading("modele", text="Modele")
            self.result_table.column("conformite_aux_normes", anchor=CENTER, width=100)
            self.result_table.heading("conformite_aux_normes", text="Conformité")
            self.result_table.column("ref_dossier", anchor=CENTER)
            self.result_table.heading("ref_dossier", text="Dossier")

            self.result_table.bind("<Double-1>",self.show_details)

            # Link a scrollbar to the canvas
            vsb = Scrollbar(self.mainframe, orient="vertical", command=self.result_table.yview)
            vsb.grid(row=8, column=8, rowspan=11, sticky=(N,S))
            self.result_table.configure(yscrollcommand=vsb.set)


            for child in self.mainframe.winfo_children():
                child.grid_configure(padx=5, pady=5)

            self.brand_name_entry.focus()


            # Gets the requested values of the height and widht.
            window_width = self.winfo_reqwidth()
            window_height = self.winfo_reqheight()

            # Gets both half the screen width/height and window width/height
            self.position_right = int(self.winfo_screenwidth()/2 - window_width/2)
            self.position_down = int(self.winfo_screenheight()/2 - window_height/2)

            # Positions the window in the center of the page.
            #self.geometry("+{}+{}".format(self.position_right, self.position_down))

        else:
            splash.update_failure_msg("Echec lors de la récupération des data de l'ANFR ")


    def get_das_original_data(self):
        """recuperation des datas de l'anfr"""
        anfr_connector = anfr.AnfrConnector()
        dataset = anfr_connector.search_dataset_by_name("das-telephonie-mobile")
        if dataset and len(dataset.get("resources")) > 0 :
            resource = anfr_connector.get_resource_data(dataset.get("resources")[0].get("id"),1000)
            if resource:
                self.original_records = resource.get("records")
                return True

        return False

    def get_brand_list(self):
        """recherche des marques des mobiles"""
        list_duplicate_brand = [item.get("marque") for item in self.original_records]
        brands = []
        for duplicate in list_duplicate_brand:
            if duplicate not in brands:
                brands.append(duplicate)

        return brands


    def search_mobile(self):
        """recherche des mobiles"""

        selection_id = self.brand_name_entry.curselection()

        brand = self.brand_name_entry.get(selection_id)
        filtered_records = [mob for mob in self.original_records if mob.get("marque") == brand]

        self.show_result(filtered_records)

    def show_result(self, list_resultats: list):
        """affiche les resultats"""

        for i in self.result_table.get_children():
            self.result_table.delete(i)

        for mob in list_resultats:
            row_data= (
                mob.get("marque"),
                mob.get("modele"),
                mob.get("conformite_aux_normes", ""),
                mob.get("ref_dossier")
                )
            self.result_table.insert('', END, values= row_data)


    def show_details(self, evt):
        """affiche la popin de details"""
        selection =self.result_table.selection()
        if len(selection) > 0:
            values = self.result_table.item(selection[0]).get("values")
            line_data = [mob for mob in self.original_records if mob.get("modele") == values[1]]
            if len(line_data) > 0:
                app_popin.DetailsDAS(self,line_data[0])
