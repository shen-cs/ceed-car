import json
from queue import PriorityQueue
import sys

def pathfinding(start, goal):
    with open(sys.argv[1]) as map_json:
        map_dict = json.load(map_json)

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        for next in map_dict[current]:
            new_cost = cost_so_far[current] + map_dict[current][next][0]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    path = []
    path_dict = {}
    if goal in came_from:
        path.append(goal)
        i = came_from[goal]
        while i != start:
            path.append(str(i))
            i = came_from[i]
    path = path[::-1]

    path_dict['header'] = {'start': start, 'end': goal}
    path_dict[start] = {'prev': '', 'next': path[0]}
    if len(path) > 1:
        path_dict[path[0]] = {'prev': start, 'next': path[1]}
        for i in range(1, len(path)-1):
            path_dict[path[i]] = {'prev':path[i-1], 'next':path[i+1]}
        path_dict[goal] = {'prev': path[-2], 'next': ''}
    else:
        path_dict[goal] = {'prev': path[0], 'next': ''}

    with open(sys.argv[4], 'w') as path_json:
        json.dump(path_dict, path_json)
    print(json.dumps(path_dict))

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('<map> <starting point> <destination> <path file name>')
        exit(-1)
    pathfinding(sys.argv[2], sys.argv[3])
