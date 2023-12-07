# ---- Clase VERTICE ------ ------------------------------------ 
class Vertex:
    # Constructor
    def __init__(self, name):
        self.name = name

    # Obtener datos de la clase
    def __str__(self):
        return self.name
    
    # Gets and sets
    def get_name(self):
        return self.name
    
# ---- Clase ARISTA ------ ------------------------------------
class Edge:
    # Constructor
    def __init__(self, vertex_1, vertex_2, weight):
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2
        self.weight = weight

    # Obtener datos de la clase
    def __str__(self):
        return self.vertex_1.get_name() + " ---> " + self.vertex_2.get_name()

    # Gets and sets
    def get_vertex_1(self):
        return self.vertex_1
    
    def get_vertex_2(self):
        return self.vertex_2

    def get_weight(self):
        return self.weight

# ---- Clase GRAFO ------ ------------------------------------
class Graph:
    # Constructor, crea un grafo con un diccionario
    def __init__(self, directed=True):
        self.graph_dict = {}
        self.directed = directed
        self.colors = {}

    # Obtener datos del grafo
    def __str__(self):
        graph_dict = ""
        for vertex, neighbors in self.graph_dict.items():
            for neighbor, weight in neighbors:
                if self.directed:
                    graph_dict += f"{vertex.get_name()} ---({weight})---> {neighbor.get_name()}\n"
                else:
                    graph_dict += f"{vertex.get_name()} ---({weight})--- {neighbor.get_name()}\n"
        return graph_dict

    # Añade un vértice al grafo (él vertice debe estár creado)
    def add_vertex(self, vertex):
        if vertex in self.graph_dict:
            return print("El Vertice ya está en el grafo:",vertex)
        self.graph_dict[vertex] = []
        print(f"el vertice: {vertex} se agregó al grafo")

    # Añade una arista al grafo (la arista debe estár creada)
    def add_edge(self, edge):
        vertex_1 = edge.get_vertex_1()
        vertex_2 = edge.get_vertex_2()
        weight = edge.get_weight()
        self.graph_dict[vertex_1].append((vertex_2, weight))
        if not self.directed:
            self.graph_dict[vertex_2].append((vertex_1, weight)) 

    # verificar si un vertice existe
    def get_vertex(self, vertex_name):
        for v in self.graph_dict:
            if vertex_name == v.get_name():
                return print("existe ", v)
        print(f"{vertex_name} no existe")

    def print_graph(self):
        print("graph_dict = {")
        for vertice, vecinos in self.graph_dict.items():
            print(f"    '{vertice}': [", end="")
            for idx, (vecino, peso) in enumerate(vecinos):
                print(f"('{vecino}', {peso})", end="")
                if idx < len(vecinos) - 1:
                    print(", ", end="")
            print("],")
        print("}")

#-- BFS ------ ------------------------------------
    def BFS(self, start, order=None):
        print("Algoritmo BFS: \n")
        visited = []
        queue = []

        if order is None:
            order = []

        visited.append(start)
        queue.append(start)

        while queue:
            s = queue.pop(0)
            order.append(s.get_name())

            for neighbour in self.graph_dict[s]:
                neighbour = neighbour[0]
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.append(neighbour)
        return order

#-- DFS ------ ------------------------------------
    def DFS(self, start, stack=None, visited=None, order=None):
        print("Algoritmo DFS: \n")
        if visited is None:
            visited = set()
        if stack is None:
            stack = []
        if order is None:
            order = []

        if start not in visited:
            order.append(start.get_name())
            visited.add(start)

            for neighbour in self.graph_dict[start]:
                neighbour = neighbour[0]
                if neighbour not in visited:
                    self.DFS(neighbour, stack, visited, order)

            stack.append(start.get_name())
        return order

#-- Topological Sort ------ ------------------------------------
    def topological_sort(self):
        print("Algoritmo de Topological Sort: \n")
        if self.directed == True:
            stack = []
            visited = set()

            for vertex in self.graph_dict:
                if vertex not in visited:
                    self.DFS(vertex, stack, visited)

            ordering = []
            while stack:
                ordering.append(stack.pop())
            return ordering
        else:
            return "El grafo no es DAG"

#-- Dijkstra ------ -------------------------------------------
    def dijkstra(self, initial):
            print("Algoritmo Dijkstra: \n")
            visited = {initial.get_name(): 0}
            path = {}

            nodes = set(self.graph_dict.keys())

            while nodes:
                min_node = None
                for node in nodes:
                    if node.get_name() in visited:
                        if min_node is None:
                            min_node = node
                        elif visited[node.get_name()] < visited[min_node.get_name()]:
                            min_node = node

                if min_node is None:
                    break

                nodes.remove(min_node)
                current_weight = visited[min_node.get_name()]

                for neighbor, weight in self.graph_dict[min_node]:
                    total_weight = current_weight + weight
                    if neighbor.get_name() not in visited or total_weight < visited[neighbor.get_name()]:
                        visited[neighbor.get_name()] = total_weight
                        path[neighbor.get_name()] = min_node.get_name()

            return visited, path

#-- Bellman forn ------ -------------------------------------------
    def bellman_ford(self, source):
        print("Algoritmo Bellman Ford: \n")
        distance = {vertex.get_name(): float('inf') for vertex in self.graph_dict}
        distance[source.get_name()] = 0

        for _ in range(len(self.graph_dict) - 1):
            for vertex in self.graph_dict:
                for neighbour, weight in self.graph_dict[vertex]:
                    if distance[vertex.get_name()] != float('inf') and distance[vertex.get_name()] + weight < distance[neighbour.get_name()]:
                        distance[neighbour.get_name()] = distance[vertex.get_name()] + weight

        for vertex in self.graph_dict:
            for neighbour, weight in self.graph_dict[vertex]:
                if distance[vertex.get_name()] != float('inf') and distance[vertex.get_name()] + weight < distance[neighbour.get_name()]:
                    print("El grafo contiene un ciclo de peso negativo")
                    return

        return distance

#-- Prim ------ -------------------------------------------
    
    def prim(self, initial):
        if self.directed:
            print("El algoritmo de Prim solo se puede ejecutar en grafos no dirigidos.")
            return None, None
        
        print("Algoritmo Prim: \n")
        visitados = set()
        arbolSM = []
        suma_total = 0

        cola = [(0, None, initial)]

        while cola:
            cola.sort(key=lambda x: x[0])
            peso, origen, nodo_actual = cola.pop(0)

            if nodo_actual not in visitados:
                visitados.add(nodo_actual)
                if origen is not None:
                    arbolSM.append((origen.get_name(), nodo_actual.get_name(), peso))
                    suma_total += peso

                if nodo_actual in self.graph_dict:
                    for vecino, peso_vecino in self.graph_dict[nodo_actual]:
                        if vecino not in visitados:
                            cola.append((peso_vecino, nodo_actual, vecino))
        return arbolSM, suma_total
    
#-- Kruskal ------ -------------------------------------------    
    def kruskal(self):
        if self.directed:
            print("El algoritmo de Kruskal solo se puede ejecutar en grafos no dirigidos.")
            return None, None
        
        print("Algoritmo Kruskal: \n")
        edges = []#almacena aristas
        for vertex, neighbors in self.graph_dict.items():#recorre el grafo
            for neighbor, weight in neighbors:
                edges.append((weight, vertex, neighbor))#añade como tupla el peso y los vertices que forman la arista

        edges.sort(key=lambda edge: edge[0])#ordena las aristas en orden ascendente

        parent = {vertex: vertex for vertex in self.graph_dict}

        def find(v):# encuentra la raíz del conjunto al que pertenece un vértice
            if parent[v] != v:
                parent[v] = find(parent[v])
            return parent[v]

        def union(v1, v2):#une dos conjuntos disjuntos especificando sus representantes.
            root1 = find(v1)
            root2 = find(v2)
            parent[root1] = root2

        minimum_spanning_tree = []#arbol de expansion minima
        total_weight = 0#peso total

        for edge in edges:#
            weight, vertex_1, vertex_2 = edge
            if find(vertex_1) != find(vertex_2):#VERIFICA si son del mismo conjunto disconjunto(estudiar)
                union(vertex_1, vertex_2)#si no es asi los une y agrega al arbol de expansion minima
                minimum_spanning_tree.append((vertex_1.get_name(), vertex_2.get_name(), weight))
                total_weight += weight#y suma el peso

        return minimum_spanning_tree, total_weight
    
#-- Floyd Warshall ------ -------------------------------------------      
    def floyd_warshall(self):
        print("Algoritmo Floyd Warshall: \n")
        num_vertices = len(self.graph_dict)
        distance = [[float('inf')]*num_vertices for _ in range(num_vertices)]#repren todos a inf

        # Iniciar la matriz de distancias con los pesos de las aristas existentes
        for vertex, neighbors in self.graph_dict.items():#clave valor| vertex = vertice | neighbors = lista vecinos cn peso(vecino-peso)
            vertex_index = list(self.graph_dict.keys()).index(vertex)#obt vertice actual indicex
            distance[vertex_index][vertex_index] = 0  # Asegurar que la diagonal principal sea cero
            print("vertice actual:",vertex)
            for neighbor, weight in neighbors:#se itera sobre neighbor(vecino-peso)
                print("vecino",neighbor)
                print("su peso:",weight)
                neighbor_index = list(self.graph_dict.keys()).index(neighbor)
                distance[vertex_index][neighbor_index] = weight

        # Aplicar el algoritmo de Floyd-Warshall
        for k in range(num_vertices):#
            print("matriz formada:",distance)
            for i in range(num_vertices):
                for j in range(num_vertices):
                    if distance[i][k] + distance[k][j] < distance[i][j]:#si la distancia de i a j por k es menor a ij
                        distance[i][j] = distance[i][k] + distance[k][j]#actualiza  

        # Imprimir la solución
        print('Distancia más corta entre cada par de nodos:')
        for i in range(num_vertices):
            print("\n-------------------------------------------------------------------")
            for j in range(num_vertices):
                if distance[i][j] == float('inf'):
                    print(f"{list(self.graph_dict.keys())[i]} ---> {list(self.graph_dict.keys())[j]}: INF", end='  | ')
                else:
                    print(f"{list(self.graph_dict.keys())[i]} ---> {list(self.graph_dict.keys())[j]}: {distance[i][j]}", end='  | ')
            print()
        print("\n-------------------------------------------------------------------")
        return distance

#-- Greedy o Voraz (Es lo mismo)------ -------------------------------------------     
    def greedy_coloring(self):
        # Sólo para grafo no dirigido
        if self.directed:
            return print ("El algoritmo Greedy sólo se puede ejecutar en grafos no dirigidos")

        color_counter = 0

        for vertex in self.graph_dict: # Para cada vertice del grafo...
            neighbor_colors = set() # recopilo colores
            for neighbor, _ in self.graph_dict[vertex]: # ... reviso sus vecinos
                neighbor_color = self.colors.get(neighbor) # obtengo el color del vecino
                if neighbor_color is not None: # ¿Tiene color asignado? 
                    neighbor_colors.add(neighbor_color) # guardo color del vecino

            # Busco si hay algun color existente en los vecinos para saber que color asignar al vertice
            vertex_color = None
            for color in range(color_counter):
                if color not in neighbor_colors:
                    vertex_color = color
                    break

            # En caso de que el color es nada, pues se crea un nuevo color (para numero cromatico)
            if vertex_color is None:
                vertex_color = color_counter
                color_counter += 1

            # Se asigna el color al vertice
            self.colors[vertex] = vertex_color

        # Número cromático (cantidad minima de colores para colorear el grafo)
        numero_cromatico = color_counter

        # Imprimir resultados
        print("Número cromático:", numero_cromatico)
        print("Colores asignados:")
        for vertex, color in self.colors.items():
            print(f"{vertex.get_name()}: {color}")

        return numero_cromatico, self.colors

# -----------------------Programa principal y vertices --------------------------------
graph = Graph(directed=False)

#  Vertices
a = Vertex('A')
b = Vertex('B')
c = Vertex('C')
d = Vertex('D')
e = Vertex('E')
f = Vertex('F')
g = Vertex('G')
h = Vertex('H')
i = Vertex('I')
j = Vertex('J')
k = Vertex('K')

# --Ejemplos BFS, DFS y Dijkstra --------------

graph.add_vertex(a)
graph.add_vertex(b)
graph.add_vertex(c)
graph.add_vertex(d)
graph.add_vertex(e)
graph.add_vertex(f)
graph.add_vertex(g)
graph.add_vertex(h)
graph.add_vertex(i)
graph.add_vertex(j)
graph.add_vertex(k)

graph.add_edge(Edge(a, b, 5))
graph.add_edge(Edge(a, c, 5))
graph.add_edge(Edge(a, d, 6))
graph.add_edge(Edge(b, e, 3))
graph.add_edge(Edge(b, f, 6))
graph.add_edge(Edge(c, g, 3))
graph.add_edge(Edge(d, g, 4))
graph.add_edge(Edge(d, h, 7))
graph.add_edge(Edge(f, i, 8))
graph.add_edge(Edge(f, j, 9))
graph.add_edge(Edge(g, k, 7))
graph.add_edge(Edge(j, k, 4))

graph.print_graph()

graph.greedy_coloring()
# print(graph.BFS(a))
# print(graph.DFS(a))
# print(graph.dijkstra(a))
# print(graph.topological_sort())

# arbol_expansion_minima, suma_total = graph.prim(a)
# print("Árbol de expansión mínima:", arbol_expansion_minima)
# print("Suma total del árbol:", suma_total)

# arbol_expansion_minima, suma_total = graph.kruskal()
# print("Árbol de expansión mínima:", arbol_expansion_minima)
# print("Suma total del árbol:", suma_total)

# distance_matrix = graph.floyd_warshall()
# print("\nMatriz de distancias después de aplicar Floyd-Warshall:")
# for row in distance_matrix:
#     print(row)

# --Ejemplos con Greedy o Voraz ----------------------------------------------------------
# graph.add_vertex(a)
# graph.add_vertex(b)
# graph.add_vertex(c)
# graph.add_vertex(d)
# graph.add_vertex(e)
# graph.add_vertex(f)

# #graph.add_edge(Edge(a, b, 3))
# #graph.add_edge(Edge(b, c, 3))
# graph.add_edge(Edge(c, d, 3))

# graph.add_edge(Edge(c, d, 3))

# graph.add_edge(Edge(d, e, 3))

# #graph.add_edge(Edge(c, a, 3))

# #graph.add_edge(Edge(e, f, 3))

# print(graph)

# graph.greedy_coloring()

# ---------------------------------------