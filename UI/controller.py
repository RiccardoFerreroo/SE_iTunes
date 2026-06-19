from logging import exception

import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.id_album_dd= None
    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            durata = float(self._view.txt_durata.value)
            if durata < 0:
                raise Exception
        except Exception:
            self._view.show_alert('metti valore valido')
            pass
        self._model.get_album_durata(durata)
        nodi, edges = self._model.crea_grafo()
        self._view.lista_visualizzazione_1.clean()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo creato:{nodi} nodi, {edges} archi"))

        self._view.dd_album.options = [ft.dropdown.Option(key=a.id, text=a.title) for a in self._model.list_al_d]
        self._view.update()


    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        self.id_album_dd = int(self._view.dd_album.value)

        # TODO

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        len_conn_comp, durata_tot = self._model.get_comp_connessa(self.id_album_dd)
        self._view.lista_visualizzazione_2.clean()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensione componente"
                                                                   f":{len_conn_comp} \n"
                                                                   f"Durata totale: {durata_tot}minuti"))
        self._view.update()


    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        try:
            d_tot = float(self._view.txt_durata_totale.value)
            if d_tot < 0:
                raise Exception
        except Exception:
            self._view.show_alert('metti valore valido')
            pass
        self._model.get_best_path(d_tot, self.id_album_dd)

        # TODO