import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.album_selezionato= False
        self.lista_a_connessi = []
        self.album_selezionato = None
    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            durata_minima = float(self._view.txt_durata.value)
        except ValueError:
            self._view.show_alert("mettere valore valido!!! CAMI TI AMO <3")
            return
        self._model.carica_albums(durata_minima)
        self._model.album_playlist_in_comune()
        self._model.crea_grafo()

        self._view.dd_album.options.clear()
        self._view.dd_album.options= [ft.dropdown.Option(a.title) for a in self._model.lista_albums]
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"{len(self._model.G.nodes)} nodi, "
                                                                   f"{len(self._model.G.edges)} edges "))
        self._view.update()





    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        title = e.control.value
        self.album_selezionato = next((a for a in self._model.lista_albums if a.title == title), None)



    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        if not self.album_selezionato:
            self._view.show_alert("CAMILLA E' PROPRIO BELLA\n" 
                                    "selezionare album!!")
            return
        lista_a_connessi = self._model.cerca_grafo(self.album_selezionato)
        durata_totale, lunghezza_a_connessi = self._model.calcola_durata_a_connessi(lista_a_connessi)


        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensione componente: {lunghezza_a_connessi}\n "
                                                                  f"Durata totalecomponenti connesse: {durata_totale} min "))
        self._view.update()



    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        print('handler chiamato')
        try :
            dTOT = float(self._view.txt_durata_totale.value)

        except ValueError:
            self._view.show_alert("RIKI AMA CAMI\n ..(metti valore valido)")
            return
        print('except passato')
        soluzione_best = self._model.cerca_grafo_dTOT(dTOT, self.album_selezionato)
        len_soluzione_best = len(soluzione_best)

        durata_complessiva = sum(a.durata for a in soluzione_best)


        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Set trovato({len_soluzione_best} album,"
                                                                   f" durata {durata_complessiva}minuti):\n"))
        for a in soluzione_best:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"- {a.title} ("
                                                                       f"{a.durata}min)\n"))

        self._view.update()



        # TODO