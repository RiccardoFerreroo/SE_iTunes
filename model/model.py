import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G=nx.Graph()
        self._dao= DAO
        self.lista_albums = []
        self.album_lista_playlists = {}
        self.soluzione_best = []

    def carica_albums(self, durata_minima):
        self.lista_albums = self._dao.carica_albums(durata_minima)#lista di oggetti album con durata>d_min
        #print(self.lista_albums)

    def album_playlist_in_comune(self):#per ogni album vedo in quali playlist è
        self.album_lista_playlists=self._dao.album_playlist_map(self.lista_albums)
        #print(self.album_lista_playlists)

    def crea_grafo(self):
        self.G.add_nodes_from(self.lista_albums)
        for (i,a1) in enumerate(self.lista_albums):
            for a2 in self.lista_albums[i+1:]:
                if a1 != a2:
                    if self.album_lista_playlists[a1] & self.album_lista_playlists[a2]:
                            self.G.add_edge(a1, a2)

        #print(self.G)
        return self.G
    def cerca_grafo(self, album_selezionato):
        if album_selezionato not in self.G.nodes():
            return []
        lista_a_connessi = list(nx.node_connected_component(self.G, album_selezionato))
        return lista_a_connessi

    def calcola_durata_a_connessi(self, lista_a_connessi):
        durata_totale = sum(a.durata for a in lista_a_connessi)
        lunghezza_a_connessi = len(lista_a_connessi)
        return durata_totale, lunghezza_a_connessi



    def cerca_grafo_dTOT(self, max_duration, start_album):
        """Ricerca ricorsiva del set massimo di album nella componente connessa"""
        component = self.cerca_grafo(start_album)
        self.soluzione_best = []
        self._ricorsione(component, [start_album], start_album.durata, max_duration)

        return self.soluzione_best


    def _ricorsione(self, albums, current_set, current_duration, max_duration):
        if len(current_set) > len(self.soluzione_best):
            self.soluzione_best = current_set[:]

        for album in albums:
            if album in current_set:
                continue
            new_duration = current_duration + album.durata
            if new_duration <= max_duration:
                current_set.append(album)
                self._ricorsione(albums, current_set, new_duration, max_duration)
                current_set.pop()








