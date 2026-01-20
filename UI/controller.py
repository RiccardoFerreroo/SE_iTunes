import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

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
        self._view.dd_album.options= [ft.dropdown.Option(a.id) for a in self._model.lista_albums]
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"{len(self._model.G.nodes)} nodi, "
                                                                   f"{len(self._model.G.edges)} edges "))
        self._view.update()



        # TODO

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO