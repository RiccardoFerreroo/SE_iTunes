import networkx as nx


from database.dao import DAO


class Model:
    def __init__(self):
        self._dao = DAO()
        self.G= nx.Graph()
        self.list_al_d = []
        self.mappa_aid_album={}
        self.mappa_aid_plyid={}
        self.albums_connected=[]

    def get_album_durata(self, durata):
        self.list_al_d =self._dao.get_album_durata(durata)
        self.mappa_aid_album = {a.id: a for a in self.list_al_d}
    def crea_grafo(self):
        self.G = nx.Graph()
        self.G.add_nodes_from(self.list_al_d)
        #print(self.G)
        self.mappa_aid_plyid=self._dao.get_edges_a_connessi(self.list_al_d)
        #print(self.mappa_aid_plyid)
        for i,a1 in enumerate(self.list_al_d):
            for a2 in self.list_al_d[i+1:]:
                if self.mappa_aid_plyid[a1.id] & self.mappa_aid_plyid[a2.id]:
                    #& = elemento di intersezione tra due inisemi {1,2,3}&{4,3,9} = {3}=TRUE
                    self.G.add_edge(a1, a2)
        return self.G.number_of_nodes(), self.G.number_of_edges()
    def get_comp_connessa(self, id_album):

        #print(self.mappa_aid_album[id_album])
        self.albums_connected =list(nx.node_connected_component(self.G,self.mappa_aid_album[id_album]))
        len_conn_comp = len(self.albums_connected)
        durata_tot = 0
        for comp in self.albums_connected:
            durata_tot += comp.durata
            #print(durata_tot, comp.id, comp.durata)
        return len_conn_comp, durata_tot

    def get_best_path(self, dtot, a1):
        d_max = dtot
        starting_node = a1
        sol_parziale = [a1]
        comp_rimasti = list(self.albums_connected)
        print(comp_rimasti)
        print(sol_parziale)


