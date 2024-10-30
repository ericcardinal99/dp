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
    result = {}
    prev = {}
    for vertex in edges.keys():
        result[vertex] = float('inf')
        prev[vertex] = float('inf')
    
    result[start_vertex] = 0
    for i in range (len(edges.keys())):
        for tail, heads in edges.items():
            for head in heads:
                weight = head[1] + result[tail]
                if weight < result[head[0]]:
                    head_vertex = head[0]
                    result[head_vertex] = weight 
                    prev[head_vertex] = tail     
    return result, prev
    
def createOutputFile(result, prev):
    output_file = open("017856202.txt", "w")
    shortest_path_string = ""
    weight_path_string = ""
    
    for current, weight in result.items():
        weight_path_string += str(round(weight, 2)) + " " 
    
    cur = goal_vertex
    while cur != start_vertex:
        shortest_path_string = str(cur) + " " + shortest_path_string
        cur = prev[cur]

    shortest_path_string = str(cur) + " " + shortest_path_string

    output_file.write(shortest_path_string[:-1]) # removing last character because it will be a space from the loop
    output_file.write("\n")
    output_file.write(weight_path_string[:-1]) # removing last character because it will be a space from the loop

    output_file.close()

def main() :
    readInputFile()
    result , prev= dp()
    createOutputFile(result, prev)

main()