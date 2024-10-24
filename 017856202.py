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
        if create_video:
            current_vertex_x, current_vertex_y = coordinates[current_vertex]
            axis.scatter(current_vertex_x, current_vertex_y, s=30, color='deepskyblue', zorder=2)
            plt.draw()
            writer.grab_frame()

        current_vertex_edges = edges[current_vertex]
        
        for edge in current_vertex_edges:
            edge_head = edge[0]
            edge_weight = edge[1]
            
            if edge_head in unvisited_vertices:
                new_vertex_weight = round(current_weight+edge_weight, 2)
                
                if new_vertex_weight < unvisited_vertices[edge_head]:
                    unvisited_vertices[edge_head] = new_vertex_weight
                    previous_vertices[edge_head] = current_vertex
            
            if create_video:
                current_vertex_x, current_vertex_y = coordinates[current_vertex]
                head_x, head_y = coordinates[edge_head]
                axis.plot([current_vertex_x, head_x], [current_vertex_y, head_y], 'aqua', linestyle='-', linewidth=1, zorder=0)
                plt.draw()
                writer.grab_frame()
                plt.pause(0.01)

    return total_weight, previous_vertices, axis

def getShortestPathAndWeight(previous_vertices, total_weight):
    shortest_path = [goal_vertex]
    current_vertex = goal_vertex
    weight_path = [total_weight]
    current_weight = total_weight

    while current_vertex != start_vertex:
        previous_vertex = current_vertex
        current_vertex_x, current_vertex_y = coordinates[current_vertex]
        current_vertex = previous_vertices[current_vertex]

        for edge in edges[previous_vertex]:
            if edge[0] == current_vertex:
                current_weight = round(current_weight-edge[1], 2)
                weight_path.insert(0, current_weight)

        shortest_path.insert(0, current_vertex)
        if create_video:
            previous_vertex_x, previous_vertex_y = coordinates[current_vertex]
            axis.scatter(current_vertex_x, current_vertex_y, s=30, color='lime', zorder=3)
            axis.plot([current_vertex_x, previous_vertex_x], [current_vertex_y, previous_vertex_y], 'lime', linestyle='-', linewidth=1, zorder=4)
            plt.draw()
            writer.grab_frame()
            plt.pause(0.3)
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

def createGraph():
    graph = {}

    for edge in edges.items():
        tail_coordinate = coordinates[edge[0]]
        
        for head in edge[1]:
            head_coordinate = head[0]

            if tail_coordinate in graph:
                graph[tail_coordinate].append(coordinates[head_coordinate])

            else:
                graph[tail_coordinate] = [coordinates[head_coordinate]]
    return graph

def plotGraph(unvisited_graph):
    unvisited_vertices = list(unvisited_graph.keys())
    graph_edges = []
    
    for vertex, edge in unvisited_graph.items():
        for neighbor in edge:
            graph_edges.append((vertex, neighbor))

    # Draw edges
    for (vertex1, vertex2) in graph_edges:
        x_coords = [vertex1[0], vertex2[0]]
        y_coords = [vertex1[1], vertex2[1]]
        axis.plot(x_coords, y_coords, 'grey', linestyle='-', linewidth=1, zorder=0)

    # Draw vertices
    x_coords, y_coords = zip(*unvisited_vertices)
    axis.scatter(x_coords, y_coords, s=30, color='black', zorder=1)

    # Make start and goal vertices different from the rest
    start_x_coords = [coordinates[start_vertex][0]]
    start_y_coords = [coordinates[start_vertex][1]]
    axis.scatter(start_x_coords, start_y_coords, s=30, color='lime', zorder=3)
    end_x_coords = [coordinates[goal_vertex][0]]
    end_y_coords = [coordinates[goal_vertex][1]]
    axis.scatter(end_x_coords, end_y_coords, s=30, color='red', zorder=3)

    axis.set_aspect('equal')

    # Show plot
    plt.grid(False)
    plt.draw()
    writer.grab_frame()
    return axis

def main() :
    readInputFile()
    readCoordinateFile()

    if create_video:
        with writer.saving(fig, "017856202.mp4", 100): 
            total_weight, previous_vertices, axis = dijkstra()
            shortest_path, weight_path = getShortestPathAndWeight(previous_vertices, total_weight)
    else:
        total_weight, previous_vertices, axis = dijkstra()
        shortest_path, weight_path = getShortestPathAndWeight(previous_vertices, total_weight)
    createOutputFile(shortest_path, weight_path)

main()