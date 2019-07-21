from maze_solver import MazeSolver
import requests
import json

def get_maze(maze_url):
    # MazeBot API for maze generation:
    URL = "https://api.noopschallenge.com"+maze_url
    # Get Maze:
    data = requests.get(url=URL)

    return data.json()

def solve_maze(maze_url):
    # Collect a maze and solve it using the MazeSolver object:
    maze = get_maze(maze_url)
    solution = MazeSolver(maze).execute()
    # Check solution and return the status:
    check_URL = "https://api.noopschallenge.com"+maze["mazePath"]
    reply = {"directions":solution}
    confirm = requests.post(check_URL,data=json.dumps(reply))

    return confirm.json()

def maze_racer():
    # MazeBot racer API:
    start_URL = "https://api.noopschallenge.com/mazebot/race/start"
    # Login name:
    git_login = {"login":"dionysius07"}
    # Posting login name:
    begin = requests.post(url=start_URL,data=json.dumps(git_login)).json()
    # Seed first maze:
    maze_url = begin["nextMaze"]
    # Start the race:
    print(begin["message"])
    response = None
    # Keep solving till the race ends:
    while True:
        confirm = solve_maze(maze_url)
        response = confirm["result"]
        print(response)
        if response == "finished":
            break
        maze_url = confirm["nextMaze"]
    # Print race details after it's done:
    print(confirm["message"])
    # Save certificate to file:
    cert = requests.get(url="https://api.noopschallenge.com"+confirm["certificate"])
    with open("mazebot/maze-solver/certificate.json","w") as certfile:
        json.dump(cert.json(),certfile,indent=2)
    
# MAIN:
if __name__ == "__main__":
    maze_racer()