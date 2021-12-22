"""module de l'app"""
from tkinter import Listbox, Scrollbar, Tk, ttk, N,W,E,S, Toplevel, StringVar
from helpers import anfr


class Splash(Toplevel):
    """classe de la splash screen"""
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("Visualisateur de DAS")

        self.msg_info = StringVar()
        self.msg_info.set("Récupération des données en cours...")

        ttk.Label(self,textvariable=self.msg_info).grid(
            column=1,
            row=1,
            sticky=(W, E)
        )

        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)

        ## required to make window show before the program gets to the mainloop
        self.update()

    def update_failure_msg(self, msg:str):
        """ mise à jour du message"""
        self.msg_info.set(msg)


class MyApp(Tk):
    """ Class encapsulant l'app"""

    def __init__(self):
        Tk.__init__(self)
        self.withdraw()
        splash = Splash(self)


        self.title("Visualisateur de DAS")
        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.original_records = []
        self.filtered_records = []
        success = self.get_das_original_data()

        if success:

            ## finished loading so destroy splash
            splash.destroy()

            ## show window again
            self.deiconify()

            self.list_widget_result =[]

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



            ttk.Label(self.mainframe, text="Selectionner \r une marque").grid(
                column=3,
                row=1,
                sticky=W)

            # exemple label variable
            #self.info = StringVar()
            #ttk.Label(self.mainframe, textvariable=self.info).grid(
            #    column=2,
            #    row=6,
            #    sticky=(W, E))


            ttk.Button(self.mainframe, text="Rechercher", command=self.search_mobile).grid(
                column=3,
                row=5,
                sticky=W)


            #entetes des résultats
            ttk.Label(self.mainframe,text="Marque").grid(
                column=1,
                row=7,
                sticky=W
            )
            ttk.Label(self.mainframe,text="Modele").grid(
                column=2,
                row=7,
                sticky=W
            )
            ttk.Label(self.mainframe,text="Conforme ?").grid(
                column=3,
                row=7,
                sticky=W
            )
            ttk.Label(self.mainframe,text="Rapports").grid(
                column=4,
                row=7,
                sticky=W
            )


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
            print(dataset.get("resources")[0].keys())
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
        self.filtered_records = [mob for mob in self.original_records if mob.get("marque") == brand]

        print(self.filtered_records[0].keys())

        self.show_result()

    def show_result(self):
        """affiche les resultats"""

        for old_res in self.list_widget_result:
            old_res.destroy()

        index = 1
        for mob in self.filtered_records:

            #ajout de la colonne marque
            temp_brand_label =ttk.Label(self.mainframe,text=mob.get("marque"))
            temp_brand_label.grid(
            column=1,
            row=7 + index,
            sticky=W
            )
            self.list_widget_result.append(temp_brand_label)

            #ajout de la colonne nom du modele
            temp_mob_label = ttk.Label(self.mainframe,text=mob.get("modele"))
            temp_mob_label.grid(
                column=2,
                row=7 + index,
                sticky=W
            )
            self.list_widget_result.append(temp_mob_label)

            # ajout du lien de la conformité
            temp_mob_confort = ttk.Label(self.mainframe,text=mob.get("conformite_aux_normes", ""))
            temp_mob_confort.grid(
                column=3,
                row=7 + index,
                sticky=W
            )
            self.list_widget_result.append(temp_mob_confort)

            # ajout du lien des rapports
            temp_mob_rapport = ttk.Label(self.mainframe,text=mob.get("rapports", ""))
            temp_mob_rapport.grid(
                column=4,
                row=7 + index,
                sticky=W
            )
            self.list_widget_result.append(temp_mob_rapport)
            index+=1