from utils.vec2i import Vec2i

UP = Vec2i(0, 1)
DOWN = Vec2i(0, -1)
LEFT = Vec2i(-1, 0)
RIGHT = Vec2i(1, 0)


# given a grid with empty (None) and non-empty cells return a grid of vectors pointing to the nearest non-empty cell
def compute_nff(grid: [[]]):
    width = len(grid)
    height = len(grid[0])
    nff = [[None for i in range(height)] for j in range(width)]
    for sweep_dir in [UP, DOWN, RIGHT, LEFT]:
        transpose = sweep_dir is RIGHT or sweep_dir is LEFT
        reverse = sweep_dir is LEFT or sweep_dir is DOWN
        if sweep_dir is UP or sweep_dir is DOWN:
            dim1 = width
            dim2 = height
        else:
            dim1 = height
            dim2 = width
        for i in range(0, dim1):
            # Note: each iteration of this loop could be run entirely in parallel without any thread locks
            if sweep_dir is UP:
                nfv = [i][0]
            elif sweep_dir is DOWN:
                nfv = [i][height]
            elif sweep_dir is RIGHT:
                nfv = [0][i]
            else:
                nfv = [width][i]
            for j in range(dim2, 0, -1) if reverse else range(0, dim2):
                f = grid[j][i] if transpose else grid[i][j]
                if f is not None:
                    nfv = Vec2i(0, 0)
                elif nfv is not None:
                    nfv = nfv.sub(sweep_dir)
                prev_nfv = nff[j][i] if transpose else nff[i][j]
                if prev_nfv is None or nfv.x * nfv.x + nfv.y * nfv.y < prev_nfv.x * prev_nfv.x + prev_nfv.y * prev_nfv.y:
                    if transpose:
                        nff[j][i] = nfv
                    else:
                        nff[i][j] = nfv
    return nff


# given a grid and is barrier method return number of regions and grid labeled by region
def color_connected_regions(grid: [[]], is_barrier):
    width = len(grid)
    height = len(grid[0])
    colored_grid = [[-1 for i in range(height)] for j in range(width)]
    processed = set(Vec2i)
    region_num = -1
    for x in range(0, width):
        for y in range(0, height):
            pos = Vec2i(x, y)
            if processed.__contains__(pos):
                continue
            region_num += 1
            neighbors_to_process = [Vec2i]
            neighbors_to_process.add(pos)
            while len(neighbors_to_process) != 0:
                neighbor = neighbors_to_process.pop()
                colored_grid[neighbor.x][neighbor.y] = region_num
                processed.add(neighbor)
                for i in range(-1, 1):
                    for j in range(-1, 1):
                        if i is 0 and j is 0:
                            continue
                        if neighbor.x is 0 and i is -1 or neighbor.x is width and i is 1:
                            continue
                        if neighbor.y is 0 and j is -1 or neighbor.y is height and j is 1:
                            continue
                        new_neighbor = Vec2i(pos.x + i, pos.y + j)
                        if processed.__contains__(new_neighbor):
                            continue
                        if not is_barrier(grid[new_neighbor.x][new_neighbor.y]):
                            neighbors_to_process.add(new_neighbor)
    return region_num + 1, colored_grid
