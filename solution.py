from logging import raiseExceptions
from math import fabs
import sys
from queue import Queue
import heapq
import operator
#--ss prijelazi adj_list , --h hueristike
#python3 solution.py --alg --ss --h --check-optimistic --check-consistent
#
#
#
#1. BFS ALGO
def bfs_algo(path):
    adj_list = {}
    d = []
    data = []
    with open(path, "r") as x:
        d = x.readlines()
    for line in d:
        if( "#" not in line):
            data.append(line)
    starting_node = data[0].rstrip()
    if " " in data[1].rstrip():
        gnode = data[1].rstrip().split(" ")
    else:
        gnode = data[1].rstrip()

    for index in range(2,len(data)):
            node_info = data[index].rstrip().split(" ")
            node = node_info[0].replace(":","")
            neighbours = []
            sorted_n = {}
            for index in range(1,len(node_info)):
                struct = node_info[index].split(",")
                sorted_n[struct[0]]=int(struct[1])
            sorted_neightbours = sorted(sorted_n)
            for value in sorted_neightbours:
                value = value+","+str(sorted_n[value])
                neighbours.append(value)
            adj_list[node] = neighbours

    visited = {}
    level = {}
    parent = {}
    bfs_traversal_output = []
    queue = Queue()
    for node in adj_list.keys():
        visited[node] = False
        parent[node] = None
        level[node] = -1

    visited[starting_node] = True
    level[starting_node] = float(0)
    queue.put(starting_node)

    while not queue.empty():
        u = queue.get()
        bfs_traversal_output.append(u)
        if u in gnode:
            path = []
            gn = u
            while gn is not None:
                path.append(gn)
                gn = parent[gn]
            path.reverse()
            print("# BFS")
            if(path):
                print("[FOUND_SOLUTION]: yes")
                print("[STATES_VISITED]: "+str(len(bfs_traversal_output)))
                print("[PATH_LENGTH]: "+str(len(path)))
                print("[TOTAL_COST]: "+str(float(level[u])))
                final_path = ""
                for node in path:
                    final_path += node +" => "
                print("[PATH]: "+final_path[0:len(final_path)-3])
            return True
        
        for v in adj_list[u]:
            point = v.split(",")
            if not visited[point[0]]:         
                visited[point[0]] = True
                parent[point[0]] = u
                level[point[0]] = float(level[u]) + float(point[1])
                queue.put(point[0])
    return False
#
#
#
#
#
#
# 2. UCS ALGO
def ucs_algo(path):
    adj_list = {}
    d = []
    data = []
    with open(path, "r") as x:
        d = x.readlines()
    for line in d:
        if( "#" not in line):
            data.append(line)
    starting_node = data[0].rstrip()
    if " " in data[1].rstrip():
        goal_node = data[1].rstrip().split(" ")
    else:
        goal_node = data[1].rstrip()
    for index in range(2,len(data)):
            node_s = data[index].rstrip().split(":")
            node = node_s[0]
            if(node_s[1] != ''):
                next_nodes = node_s[1].strip().split(" ")
                us_nodes = {}
                neighbours = []
                for i in next_nodes:
                    prim = i.split(",")
                    us_nodes[prim[0]]=int(prim[1])
                sortedList = {k: v for k,v in sorted(us_nodes.items(), key=operator.itemgetter(1))}
                for key in sortedList.keys():
                    neighbours.append(str(key+","+str(sortedList[key])))
                adj_list[node] = neighbours
            else:
                adj_list[node] = []

    visited = {}
    vrijednost = {}
    parent = {}
    for node in adj_list.keys():
        visited[node] = False
        parent[node] = None
        vrijednost[node] = 99999999
    visited[starting_node] = True
    vrijednost[starting_node] = 0
    que = []
    heapq.heappush(que, (0, starting_node))
    while len(que) > 0 :
        node = heapq.heappop(que)
        visited[node[1]] = True
        if node[1] in goal_node:
            path = []
            states = 0
            for i in visited.keys():
                if(visited[i]):
                    states += 1
            gn = node[1]
            while gn is not None:
                path.append(gn)
                gn = parent[gn]
            path.reverse()
            print("# UCS")
            if(path):
                print("[FOUND_SOLUTION]: yes")
                print("[STATES_VISITED]: "+str(states))
                print("[PATH_LENGTH]: "+str(len(path)))
                print("[TOTAL_COST]: "+str(float(vrijednost[node[1]])))
                final_path = ""
                for node in path:
                    final_path += node +" => "
                print("[PATH]: "+final_path[0:len(final_path)-3])
            return True

        for neighbour in adj_list[node[1]]:
            n = neighbour.split(",")
            node_name = n[0]
            node_value = float(n[1])
            if not visited[node_name]:
                node_value += float(node[0])
                if(float(vrijednost[node_name]) > node_value):
                    vrijednost[node_name] = node_value 
                    parent[node_name] = node[1]
                    heapq.heappush(que, (node_value, node_name))
    return False
#
#
#
#
# A-STAR (A*)
def astar_algo(data_path, hueristic_path):
    d = []
    data = []
    with open(data_path, "r") as x:
        d = x.readlines()
    for line in d:
        if( "#" not in line):
            data.append(line)
    start_node = data[0].rstrip()

    if "," in data[1].rstrip():
            goal = data[1].rstrip().split(",")
    else:
            goal = data[1].rstrip()
    adj_list = {}
    hueristic_cost = {}
    with open(hueristic_path, "r") as f:
        hueristic_data = f.readlines()
        for line in hueristic_data:
            node = line.rstrip().split(": ")
            hueristic_cost[node[0]]=int(node[1])
    for index in range(2,len(data)):
            node = data[index].rstrip().split(":")
            node_state = node[0]
            if(node[1] != ''):
                adj_nodes = node[1].strip().split(" ")
                neighbours = []
                for adj in adj_nodes:
                    prim = adj.split(",")
                    heapq.heappush(neighbours, (prim[1],prim[0]))
                n2 = []
                for el in neighbours:
                    n2.append(str(el[1])+","+str(el[0]))
                adj_list[node_state] = n2
            else:
                adj_list[node_state] = []

    open_set = []
    open_hash = {}
    closed_set = {}
    g_cost = {}
    f_cost = {}
    parent = {}

    for node in adj_list:
        g_cost[node] = 9999
        f_cost[node] = 0
        closed_set[node] = False
        open_hash[node] = False

    heapq.heappush(open_set, (float(0), start_node))
    g_cost[start_node] = float(0)
    parent[start_node] = None

    while len(open_set) > 0:
        open_node = heapq.heappop(open_set)
        closed_set[open_node[1]] = True
        if(open_node[1] in goal):
            print("# A-STAR ",str(hueristic_path))
            path = []
            state_visited = 0
            for a in closed_set.keys():
                if(closed_set[a]):
                    state_visited += 1
            gn = open_node[1]
            while gn is not None:
                path.append(gn)
                gn = parent[gn]
            path.reverse()
            print("[FOUND_SOLUTION]: yes")
            print("[STATES_VISITED]: "+str(state_visited))
            print('[PATH_LENGTH] {}'.format(len(path)))
            print("[TOTAL_COST]: ",str((g_cost[open_node[1]])))
            final_path = ""
            for node in path:
                final_path += node + " => "
            print("[PATH]: "+final_path[0:len(final_path)-3])
            return True
        for m in adj_list[open_node[1]]:   
            m = m.split(",")     
            if  not open_hash[m[0]] and not closed_set[m[0]]:
                
                parent[m[0]]=open_node[1]
                g_cost[m[0]]=g_cost[open_node[1]] + float(m[1])
                f_cost[m[0]]=g_cost[m[0]] + float(hueristic_cost[m[0]])
                open_hash[m[0]] = True
                heapq.heappush(open_set, (f_cost[m[0]], m[0]))
            else:
                if g_cost[open_node[1]] + float(m[1]) < g_cost[m[0]]:
                    parent[m[0]] = open_node[1]
                    g_cost[m[0]] =  g_cost[open_node[1]] + float(m[1])
                    f_cost[m[0]] = g_cost[m[0]] + float(hueristic_cost[m[0]])
                    if closed_set[m[0]]:
                        closed_set[m[0]] = False
                        open_hash[m[0]] = True
                        heapq.heappush(open_set, (f_cost[m[0]], m[0]))
    return False
#
#
#
#
#4.HUERISTIC-OPTIMISTIC = UCS 
def optimistic_algo(path,hueristic_path):
    adj_list = {}
    d = []
    data = []
    with open(path, "r") as x:
        d = x.readlines()
    for line in d:
        if( "#" not in line):
            data.append(line)
    hueristic_cost = {}
    with open(hueristic_path, "r") as f:
        hueristic_data = f.readlines()
        for line in hueristic_data:
            node = line.rstrip().split(": ")
            hueristic_cost[node[0]]=int(node[1])
    
    starting_node = data[0].rstrip()
    if " " in data[1].rstrip():
        goal_node = data[1].rstrip().split(" ")
    else:
        goal_node = data[1].rstrip()
    for index in range(2,len(data)):
            node_s = data[index].rstrip().split(":")
            node = node_s[0]
            if(node_s[1] != ''):
                next_nodes = node_s[1].strip().split(" ")
                us_nodes = {}
                neighbours = []
                for i in next_nodes:
                    prim = i.split(",")
                    us_nodes[prim[0]]=int(prim[1])
                sortedList = {k: v for k,v in sorted(us_nodes.items(), key=operator.itemgetter(1))}
                for key in sortedList.keys():
                    neighbours.append(str(key+","+str(sortedList[key])))
                adj_list[node] = neighbours
            else:
                adj_list[node] = []
    adj_list = {k: v for k,v in sorted(adj_list.items(), key=operator.itemgetter(0))}
    flag = True
    for starting_node in adj_list:
            visited = {}
            vrijednost = {}
            parent = {}
            for node in adj_list.keys():
                visited[node] = False
                parent[node] = None
                vrijednost[node] = 99999999
            visited[starting_node] = True
            vrijednost[starting_node] = 0
            que = []
            heapq.heappush(que, (0, starting_node))
            while len(que) > 0 :
                node = heapq.heappop(que)
                visited[node[1]] = True
                if node[1] in goal_node: 
                    if(hueristic_cost[starting_node] <= vrijednost[node[1]]):
                        print("[CONDITION]: [OK] h("+starting_node+") <= h*: "+str(float(hueristic_cost[starting_node]))+" <= "+str(float( vrijednost[node[1]])))
                    else:
                        print("[CONDITION]: [ERR] h("+starting_node+") <= h*: "+str(float(hueristic_cost[starting_node]))+" <= "+str(float(vrijednost[node[1]])))
                        flag = False
                    que.clear()
                for neighbour in adj_list[node[1]]:
                    n = neighbour.split(",")
                    node_name = n[0]
                    node_value = float(n[1])
                    if not visited[node_name]:
                        node_value += float(node[0])
                        if(float(vrijednost[node_name]) > node_value):
                            vrijednost[node_name] = node_value 
                            parent[node_name] = node[1]
                            heapq.heappush(que, (node_value, node_name))
            continue
    return flag

#
#
#
#
#
#5.CONSISTENT ALGO
def const_algo(path,hueristic_path):
    adj_list = {}
    d = []
    data = []
    with open(path, "r") as x:
        d = x.readlines()
    for line in d:
        if( "#" not in line):
            data.append(line)
   
    fl = False
    if " " in data[1].rstrip():
        goal_node = data[1].rstrip().split(" ")
        fl = True
    else:
        goal_node = data[1].rstrip()
    hueristic_cost = {}
    with open(hueristic_path, "r") as f:
        hueristic_data = f.readlines()
        for line in hueristic_data:
            node = line.rstrip().split(": ")
            hueristic_cost[node[0]]=int(node[1])

    for index in range(2,len(data)):
            node_s = data[index].rstrip().split(":")
            node = node_s[0]
            if(node_s[1] != ''):
                next_nodes = node_s[1].strip().split(" ")
                us_nodes = {}
                neighbours = []
                
                for i in next_nodes:
                    prim = i.split(",")
                    us_nodes[prim[0]]=int(prim[1])
                sortedList = {k: v for k,v in sorted(us_nodes.items(), key=operator.itemgetter(0))}
                for key in sortedList.keys():
                    neighbours.append(str(key+","+str(sortedList[key])))
                adj_list[node] = neighbours
            else:
                adj_list[node] = []
    print("# HEURISTIC-CONSISTENT ",hueristic_path)
    flag = True
    adj_list = {k: v for k,v in sorted(adj_list.items(), key=operator.itemgetter(0))}
    for node in adj_list:
        for adj in adj_list[node]:
            adj = adj.split(",")
            if(float(hueristic_cost[node]) <= float(hueristic_cost[adj[0]]) + float(adj[1])):
                print("[CONDITION]: [OK] h(" + node + ") <= h(" + adj[0] + ") + c: " + str(float(hueristic_cost[node])) +" <= " + str(float(hueristic_cost[adj[0]]))+ " + " + str(float(adj[1])))
            else:
                print("[CONDITION]: [ERR] h(" + node + ") <= h(" + adj[0] + ") + c: " + str(float(hueristic_cost[node])) +" <= " + str(float(hueristic_cost[adj[0]]))+ " + " + str(float(adj[1])))
                flag = False
    return flag


##MAIN PROG
## daj sve argumente 
a = " ".join(sys.argv).split(" ")
path = ""
path_hueristic = ""
algo = ""
conistent = False
optimistic = False
for i in range(1,len(a)):
    
    if(a[i] == "--ss"):
        path = a[i+1]

    elif(a[i] == "--h"):
        path_hueristic = a[i+1]

    elif(a[i] == "--alg"):
        algo = a[i+1]

    elif(a[i] == "--check-optimistic"):
        optimistic = True

    elif(a[i] == "--check-consistent"):
        conistent = True

try:
    if(algo == "bfs"): 
        try:
            value = bfs_algo(path)
            if not value:
                print("# BFS")
                print("[FOUND_SOLUTION]: no")
        except:
                print("ERROR IN FUNCTION BFS!")
    elif(algo == "ucs"):  
        try:
            value = ucs_algo(path)
            if not value:
                print("# UCS")
                print("[FOUND_SOLUTION]: no")
        except:
            print("ERROR IN FUNCTION USC!")
    elif(algo == "astar"):
        try:
            value = astar_algo(path, path_hueristic)
            if not value:
                print("# A-STAR ",str(sys.argv[6]))
                print("[FOUND_SOLUTION]: no")
        except:
            print("ERROR IN FUNCTION A-STAR!")
    #python3 solution.py (0) --ss ista.txt --h istra_hueristic.txt --check-optimistic / --check-consistent
    elif(optimistic):
        try:
            print("# HEURISTIC-OPTIMISTIC ",path_hueristic)
            value = optimistic_algo(path,path_hueristic)
            if value:
                print("[CONCLUSION]: Heuristic is optimistic.")
            else:
                print("[CONCLUSION]: Heuristic is not optimistic.")
        except:
            print("ERROR IN FUNCTION CHECK-OPTIMISTIC!")
    # python3 solution.py --ss ai.txt --h ai_pass.txt --check-consistent
    elif(conistent):
        try:
            print("# HEURISTIC-CONSISTENT ",path_hueristic)
            value = const_algo(path, path_hueristic)
            if value:
                print("[CONCLUSION]: Heuristic is consistent.")
            else:
                print("[CONCLUSION]: Heuristic is not consistent.")
        except:
            print("ERROR IN FUNCTION CHECK-CONSISTENT!")
    
    else:
        raise
    

except:
    print("Wrong arguments!")