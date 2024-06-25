import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_grafo(self, e):
        n=self._view.txt_canzoni.value
        if n=="":
            self._view.create_alert("Inserisci un valore numerico per il numero di canzoni di ogni album")
        grafo = self._model.creaGrafo(int(n))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        for album in grafo.nodes:
            self._view.dd_a1.options.append(ft.dropdown.Option(
                               text=album))
        self._view.update_page()
    def handle_adiacenze(self, e):
        album = self._view.dd_a1.value
        if album is None:
            self._view.create_alert("Seleziona un album")
            return
        lista=self._model.getBilancio(album)
        for (nodo, peso) in lista:
            self._view.txt_result.controls.append(ft.Text(f"{nodo}, bilancio={peso}"))

        self._view.update_page()