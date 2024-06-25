import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self._idMap = {}
        self._idMapNome = {}

    def creaGrafo(self, ncanzoni):
        self.nodi = DAO.getNodi(ncanzoni)
        self.grafo.add_nodes_from(self.nodi)
        for v in self.nodi:
            self._idMap[v.AlbumId] = v
        for v in self.nodi:
            self._idMapNome[v.Title] = v
        self.addEdges(ncanzoni)
        return self.grafo

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)

    def addEdges(self, durata):
        self.grafo.clear_edges()
        allEdges = DAO.getConnessioni(durata)
        for connessione in allEdges:
            nodo1 = self._idMap[connessione.v1]
            nodo2 = self._idMap[connessione.v2]
            if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes:
                if self.grafo.has_edge(nodo1, nodo2) == False:
                    if connessione.peso>0:
                        self.grafo.add_edge(nodo2, nodo1, weight=connessione.peso)
                    if connessione.peso<0:
                        self.grafo.add_edge(nodo1, nodo2, weight=abs(connessione.peso))

    def getBilancio(self, a1Titolo):
        album=self._idMapNome[a1Titolo]
        lista=[]
        for nodo in self.grafo.neighbors(album):
            lista.append((nodo.Title,self.bilancio(nodo)))
        return sorted(lista, key=lambda x:x[1], reverse=True)


    def bilancio(self,nodo):
        entranti=0
        uscenti=0
        for archientranti in self.grafo.in_edges(nodo):
            entranti+=self.grafo[archientranti[0]][archientranti[1]]["weight"]
        for archiuscenti in self.grafo.out_edges(nodo):
            uscenti += self.grafo[archiuscenti[0]][archiuscenti[1]]["weight"]
        return entranti-uscenti