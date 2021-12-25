"""module des popin de l'app"""
from tkinter import Toplevel, StringVar, ttk, W,E
import webbrowser

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
            child.grid_configure(padx=10, pady=15)


         # Gets the requested values of the height and widht.
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        position_right = int(self.winfo_screenwidth()/2 - window_width/2)
        position_down = int(self.winfo_screenheight()/2 - window_height/2)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(position_right, position_down))

        # required to make window show before the program gets to the mainloop
        self.update()

    def update_failure_msg(self, msg:str):
        """ mise à jour du message"""
        self.msg_info.set(msg)


class DetailsDAS(Toplevel):
    """classe encapsulant la fenetre de details"""

    def __init__(self,parent, raw_data):
        Toplevel.__init__(self,parent)
        self.title("Détails DAS")

        self.reports_url = raw_data.get("rapports")
        # modele
        ttk.Label(self,text="Modèle: ").grid(
            column=0,
            row=1,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("modele")).grid(
            column=1,
            row=1,
            sticky=(W, E)
        )

        # marque
        ttk.Label(self,text="Marque: ").grid(
            column=0,
            row=2,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("marque")).grid(
            column=1,
            row=2,
            sticky=(W, E)
        )

        # conformité
        ttk.Label(self,text="Conformité: ").grid(
            column=0,
            row=3,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("conformite_aux_normes")).grid(
            column=1,
            row=3,
            sticky=(W, E)
        )

        # dossier anfr
        ttk.Label(self,text="Dossier: ").grid(
            column=0,
            row=4,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("ref_dossier")).grid(
            column=1,
            row=4,
            sticky=(W, E)
        )

        # date de contrôle
        ttk.Label(self,text="Date de contrôle: ").grid(
            column=0,
            row=5,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("date_controle")).grid(
            column=1,
            row=5,
            sticky=(W, E)
        )

        # Reglementation
        ttk.Label(self,text="Reglementation: ").grid(
            column=0,
            row=6,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("Règlementation applicable")).grid(
            column=1,
            row=6,
            sticky=(W, E)
        )

        # DAS Tête (NF EN 50360)
        ttk.Label(self,text="DAS Tête (NF EN 50360): ").grid(
            column=0,
            row=7,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("das_tete_norme_nf_en_50360")).grid(
            column=1,
            row=7,
            sticky=(W, E)
        )

        # DAS Tronc (NF EN 50566)
        ttk.Label(self,text="DAS Tronc (NF EN 50566): ").grid(
            column=0,
            row=8,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("das_tronc_norme_nf_en_50566")).grid(
            column=1,
            row=8,
            sticky=(W, E)
        )

        # Distance mesure (mm)
        ttk.Label(self,text="Distance mesure (mm): ").grid(
            column=0,
            row=9,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("distance_mesure_mm")).grid(
            column=1,
            row=9,
            sticky=(W, E)
        )

        # DAS Membre (EN 50566)
        ttk.Label(self,text="DAS Membre (EN 50566): ").grid(
            column=0,
            row=10,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("das_membre_norme_en_50566")).grid(
            column=1,
            row=10,
            sticky=(W, E)
        )

        # DAS tronc (5mm)
        ttk.Label(self,text="DAS tronc (5mm): ").grid(
            column=0,
            row=11,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("das_tronc_a_5mm")).grid(
            column=1,
            row=11,
            sticky=(W, E)
        )

        # DAS tronc au contact
        ttk.Label(self,text="DAS tronc au contact: ").grid(
            column=0,
            row=12,
            sticky=(W, E)
        )
        ttk.Label(self,text=raw_data.get("das_tronc_au_contact")).grid(
            column=1,
            row=12,
            sticky=(W, E)
        )

        # Rapports

        ttk.Button(self, text="Accès aux rapports", command=self.show_reports).grid(
                column=2,
                row=1,
                rowspan=12,
                sticky=(W,E))


        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)


        # Gets the requested values of the height and widht.
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        position_right = int(self.winfo_screenwidth()/2 - window_width/2)
        position_down = int(self.winfo_screenheight()/2 - window_height/2)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(position_right, position_down))

    def show_reports(self):
        """ouvre le navigateur sur les rapports"""
        webbrowser.open(self.reports_url)
