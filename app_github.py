from PySide2 import QtWidgets    # Possède différentes fonctions qui permettent de créer des interfaces graphiques
import currency_converter

class App(QtWidgets.QWidget): #  On indique que l'on veut "hériter" de la classe QWidget, contenue dans QtWidgets
    def __init__(self):
        super().__init__()  # Permet d'appeler la methode __init__ de QWidget
                            # Permet d'initialiser QWidget à l'intérieur de la classe App()

        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de Devises")    # Permet d'indiquer un Titre à la fenêtre
        self.setup_ui()    # Permet d'appeler la methode setup_ui() =  Création des Widgets
        self.setup_connections()
        self.set_default_values()  # Toujours mettre ces 2 dernières lignes après setup_ui
        self.setup_css()
        self.resize(500, 5)

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)    # self ici indique que l'on fait reference au "parent" (la fenêtre principale)
        self.cbb_devisesFrom = QtWidgets.QComboBox()  # le préfixe cbb_ pour plus de clarté = "combobox" (Menu déroulant)
        self.spn_montant = QtWidgets.QSpinBox()     # spn_ = SpinBox
        self.cbb_devisesTo = QtWidgets.QComboBox()   # ComboBox
        self.spn_montantConverti = QtWidgets.QSpinBox()  # SpinBox
        self.btn_inverser = QtWidgets.QPushButton("Inverser Devises")  # Button

        self.layout.addWidget(self.cbb_devisesFrom)         # Permet d'afficher le widget dans le layout
        self.layout.addWidget(self.spn_montant)             # Permet d'afficher le widget dans le layout
        self.layout.addWidget(self.cbb_devisesTo)          # Permet d'afficher le widget dans le layout
        self.layout.addWidget(self.spn_montantConverti)     # Permet d'afficher le widget dans le layout
        self.layout.addWidget(self.btn_inverser)            # Permet d'afficher le widget dans le layout

    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies))) # self.c n'est pas une liste mais un SET
                                                                       # On le transforme donc en liste avec list()
                                                                       # Puis on trie cette liste par ordre Alphab.
        self.cbb_devisesTo.addItems(sorted(list(self.c.currencies)))


        ## On fixe les valeurs par défaut :

        self.cbb_devisesFrom.setCurrentText("EUR")  # On spécifie une Devise par défaut, ici "EUR"
        self.cbb_devisesTo.setCurrentText("EUR")    # On spécifie une Devise par défaut, ici "EUR"

        # On fixe le "Range" des valeurs (MIN, MAX)
        self.spn_montant.setRange(1, 1000000)
        self.spn_montantConverti.setRange(1, 1000000)
        # On fixe une valeur par défaut inclue dans le "Range" (voir au-dessus)
        self.spn_montant.setValue(100)
        self.spn_montantConverti.setValue(100)

    def setup_connections(self ):
        self.cbb_devisesFrom.activated.connect(self.compute) # On connecte le SIGNAL "activated" sur le widget "cbb_devisesFrom"
        self.cbb_devisesTo.activated.connect(self.compute)   # S'executera à chaque changement de devise

        self.spn_montant.valueChanged.connect(self.compute) # S'executera au changement d'une/des valeur(s)
        self.btn_inverser.clicked.connect(self.inverser_devises)

    def setup_css(self):                        # Méthode qui va permettre de changer le CSS du convertisseur :
        self.setStyleSheet("""                          
        background-color: rgb(4, 30, 30);
        color: rgb(240, 240, 240);
        border: none;
        """)                                            # On modifie le background de l'application entière
                                                        # On modifie la couleur du texte
                                                        # On supprime les bordures



    def compute(self):  # Cest la méthode que l'on va appeler pour modifier la valeur ou la devise pour pouvoir calculer la conversion
        montant = self.spn_montant.value()
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        try:                                                                # On gère les erreurs avec try/catch
            resultat = self.c.convert(montant, devise_from, devise_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion n'a pas fonctionné !")
        else:
            self.spn_montantConverti.setValue(resultat)

    def inverser_devises(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)

        self.compute()



app = QtWidgets.QApplication([])   # On créé une QApplication, que l'on execute ensuite (app.exec_() )
win = App()    # On créé une instance de la classe App() que l'on récupère dans la variable "win"
win.show()    # Permet d'afficher la fenêtre


app.exec_