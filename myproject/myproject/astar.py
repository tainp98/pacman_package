from pygame.math import Vector2 as vec
from .settings import *

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def get_pix_pos(position):
    cell_width = MAZE_WIDTH//55
    cell_height = MAZE_HEIGHT//30
    return vec(position.x*cell_width+cell_width//2,
                position.y*cell_height+cell_height//2)
def astar(start, end, walls):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    cell_width = MAZE_WIDTH//55
    cell_height = MAZE_HEIGHT//30
    # Create start and end node
    # start = get_pix_pos(start)
    end = get_pix_pos(end)
    #print(start,end)
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)
    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            #pos_current_node = App.pacman.get_pix_pos(current_node.position)
            node_position = (current_node.position[0] + new_position[0]*cell_width, current_node.position[1] + new_position[1]*cell_height)

            # Make sure within range
            if node_position[0] > MAZE_WIDTH or node_position[0] < 0 or node_position[1] > MAZE_HEIGHT or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            break0 = False
            for wall in walls:
                pix_wall = get_pix_pos(wall)
                if node_position == pix_wall:
                    break0 = True
                    break
            if break0 == True: 
                continue
            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            break1 = False
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    break1 = True
                    break
            if break1 == True:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position.x) ** 2) + ((child.position[1] - end_node.position.y) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            break2 = False
            for open_node in open_list:
                if child.position[0] == open_node.position[0] and child.position[1] == open_node.position[1]:
                    break2 = True
                    break
            if break2 == True:
                continue
            # Add the child to the open list
            open_list.append(child)


