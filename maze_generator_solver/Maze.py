import random
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from matplotlib.animation import FuncAnimation


def generate_maze(size):
    maze = np.ones((size, size), dtype=int)

    stack = [(1, 1)]
    maze[1, 1] = 0

    while stack:
        x, y = stack[-1]

        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        found = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 < nx < size - 1 and 0 < ny < size - 1:
                if maze[ny, nx] == 1:
                    maze[y + dy // 2, x + dx // 2] = 0
                    maze[ny, nx] = 0
                    stack.append((nx, ny))
                    found = True
                    break

        if not found:
            stack.pop()

    maze[1, 0] = 0
    maze[size - 2, size - 1] = 0

    return maze


def solve_maze(maze):
    size = len(maze)
    start = (1, 1)
    end = (size - 2, size - 2)

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == end:
            return path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy

            if (0 <= nx < size and 0 <= ny < size
                    and maze[ny, nx] == 0
                    and (nx, ny) not in visited):

                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    return []


def animate_maze(maze, path):
    fig, ax = plt.subplots(figsize=(9, 9))

    ax.imshow(maze, cmap="binary", interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])

    ax.scatter(1, 1, color="green", s=100, label="Start")
    ax.scatter(len(maze) - 2, len(maze) - 2,
               color="blue", s=100, label="Finish")

    dot, = ax.plot([], [], "ro", markersize=9)

    ax.legend()

    def update(frame):
        x, y = path[frame]
        dot.set_data([x], [y])
        return dot,

    animation = FuncAnimation(
        fig,
        update,
        frames=len(path),
        interval=100,
        repeat=False,
        blit=True
    )

    plt.show()


size = int(input("Enter maze size (odd number, minimum 5): "))

if size < 5 or size % 2 == 0:
    print("Please enter an odd number of at least 5.")
else:
    maze = generate_maze(size)
    solution = solve_maze(maze)

    print("Maze generated!")
    print("Solving maze...")

    if solution:
        print("Solution found!")
        print("Path length:", len(solution))
        animate_maze(maze, solution)
    else:
        print("No solution found!")
