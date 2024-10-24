total_vertices = -1
start_vertex = -1
goal_vertex = -1
edges = {}

def readInputFile():
    input_data_file = open("input.txt", "r")
    input_data_array = input_data_file.read().split('\n')
    input_data_file.close()
    
    global total_vertices
    total_vertices = int(input_data_array.pop(0))
    
    global start_vertex
    start_vertex = int(input_data_array.pop(0))
    
    global goal_vertex
    goal_vertex = int(input_data_array.pop(0))
    
    getEdges(input_data_array)
    
def getEdges(input_edges):
    for tuple in input_edges: 
        edge_values = tuple.split(' ')
        
        if len(edge_values) == 3:
            edge_tail = int(edge_values[0])
            edge_head = int(edge_values[1])
            edge_weight = float(edge_values[2])
            
            if edge_tail in edges:
                edges[edge_tail].append((edge_head, edge_weight))
            
            else:
                edges[edge_tail] = [(edge_head, edge_weight)]

def dp():
    total_weight = float('inf')
    unvisited_vertices = {}
    previous_vertices = {}
    
    while len(unvisited_vertices) > 0:
        vertex_weights = list(unvisited_vertices.values())
    
        if vertex_weights.count(float('inf')) == len(vertex_weights):
            break
        
        current_weight = min(vertex_weights)
        current_vertex = [i for i in unvisited_vertices if unvisited_vertices[i] == current_weight][0]
        
        if current_vertex == goal_vertex:
            total_weight = current_weight
            break
        
        del unvisited_vertices[current_vertex]

        current_vertex_edges = edges[current_vertex]
        
        for edge in current_vertex_edges:
            edge_head = edge[0]
            edge_weight = edge[1]
            
            if edge_head in unvisited_vertices:
                new_vertex_weight = round(current_weight+edge_weight, 2)
                
                if new_vertex_weight < unvisited_vertices[edge_head]:
                    unvisited_vertices[edge_head] = new_vertex_weight
                    previous_vertices[edge_head] = current_vertex

    return total_weight, previous_vertices

def getShortestPathAndWeight(previous_vertices, total_weight):
    shortest_path = [goal_vertex]
    current_vertex = goal_vertex
    weight_path = [total_weight]
    current_weight = total_weight

    while current_vertex != start_vertex:
        previous_vertex = current_vertex
        current_vertex = previous_vertices[current_vertex]

        for edge in edges[previous_vertex]:
            if edge[0] == current_vertex:
                current_weight = round(current_weight-edge[1], 2)
                weight_path.insert(0, current_weight)

        shortest_path.insert(0, current_vertex)
        
    return shortest_path, weight_path
    
def createOutputFile(shortest_path, weight_path):
    output_file = open("017856202.txt", "w")
    shortest_path_string = ""
    weight_path_string = ""
    
    for vertex in shortest_path:
        shortest_path_string += str(vertex) + " "
    
    for weight in weight_path: 
        weight_path_string += str(weight) + " "
    
    output_file.write(shortest_path_string[:-1]) # removing last character because it will be a space from the loop
    output_file.write("\n")
    output_file.write(weight_path_string[:-1]) # removing last character because it will be a space from the loop

    output_file.close()

def main() :
    readInputFile()
    total_weight, previous_vertices = dp()
    shortest_path, weight_path = getShortestPathAndWeight(previous_vertices, total_weight)
    createOutputFile(shortest_path, weight_path)

main()