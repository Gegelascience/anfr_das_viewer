""" App pour voir le das des smartphones valides par l'anfr """
from tkinter import Listbox, Scrollbar, StringVar, Tk, ttk, N,W,E,S
from helpers import anfr

class MyApp:
    """ Class encapsulant l'app"""

    def __init__(self, root_window: Tk):
        root_window.title("Visualisateur de DAS")
        self.mainframe = ttk.Frame(root_window, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root_window.columnconfigure(0, weight=1)
        root_window.rowconfigure(0, weight=1)

        self.anfr = anfr.AnfrConnector()
        self.original_records = []
        self.get_das_original_data()

        brands = self.get_brand_list()
        #brand_name_entry = ttk.Entry(self.mainframe, width=7, textvariable="marque")
        self.brand_name_entry =Listbox(self.mainframe,listvariable=brands)
        self.brand_name_entry.grid(
            column=2,
            row=1,
            sticky=(W, E))
        index_brand = 0
        for brand in brands:
            self.brand_name_entry.insert(index_brand, brand)
            index_brand+=1

        scrollbar_brands = Scrollbar(self.mainframe)
        scrollbar_brands.grid(
            column=3,
            row=1,
            sticky=(W, E))

        self.brand_name_entry.config(yscrollcommand = scrollbar_brands.set)

        scrollbar_brands.config(command = self.brand_name_entry.yview)



        ttk.Label(self.mainframe, text="Marque").grid(
            column=1,
            row=1,
            sticky=W)

        # résultat recherche
        self.info = StringVar()
        ttk.Label(self.mainframe, textvariable=self.info).grid(
            column=2,
            row=9,
            sticky=(W, E))


        ttk.Button(self.mainframe, text="Rechercher", command=self.search_mobile).grid(
            column=3,
            row=9,
            sticky=W)


        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.brand_name_entry.focus()


        # Gets the requested values of the height and widht.
        window_width = root_window.winfo_reqwidth()
        window_height = root_window.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        self.position_right = int(root_window.winfo_screenwidth()/2 - window_width/2)
        self.position_down = int(root_window.winfo_screenheight()/2 - window_height/2)

        # Positions the window in the center of the page.
		#root_window.geometry("+{}+{}".format(self.position_right, self.position_down))


    def get_das_original_data(self):
        """recuperation des datas de l'anfr"""
        dataset = self.anfr.search_dataset_by_name("das-telephonie-mobile")
        if dataset and len(dataset.get("resources")) > 0 :
            resource = self.anfr.get_resource_data(dataset.get("resources")[0].get("id"))
            if resource:
                self.original_records = resource.get("records")
                #print(self.original_records)

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

        brand_filter = self.brand_name_entry.get(selection_id)
        filtered_records = [mobile for mobile in self.original_records if mobile.get("marque") == brand_filter]

        concat_result = ""
        for record in filtered_records:
            concat_result = concat_result + record.get("modele") + "\r"

        self.info.set(concat_result)


if __name__ == "__main__":
    window = Tk()
    MyApp(window)
    window.mainloop()
