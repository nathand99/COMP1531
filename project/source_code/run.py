import file_path
from routes import app, system
import sys, os, socket
from contextlib import closing

# Courtesy to saaj, Dominic Rodger
# https://stackoverflow.com/questions/1365265/on-localhost-how-do-i-pick-a-free-port-number
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


if __name__ == '__main__':
    # SIGINT to stop (Ctrl + C)
    try:
        app.run(debug=True,port=8000)
    except:
        print("Cannot run on port 8000. Trying to run on a free port")
        app.run(debug=True,port=find_free_port())
    
        

    


