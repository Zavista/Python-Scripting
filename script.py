import os
import json
import shutil
from subprocess import PIPE, run
import sys


GAME_DIR_PATTERN = "game"

def find_all_game_paths(source): #finds all the game paths in source
    game_paths = []

    for root, dirs, files in os.walk(source): #walk recursively  finds all root, dir and files from source
        for directory in dirs: 
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
            
        break
        
    return game_paths

def get_name_from_paths(paths, to_strip):
    new_names = []

    for path in paths:
        _,  dir_name = os.path.split(path) # gives us the game dir names like hello_world_game
        new_dir_name = dir_name.replace(to_strip, "") #removes game
        new_names.append(new_dir_name)
    
    return new_names

def create_dir(path): #creates a new dir
    if not os.path.exists(path):
        os.mkdir(path)


def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest) #recursively deletes everything in dest
    
    shutil.copytree(source, dest) #copies everything from source to dest


def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }

    with open(path, "w") as f: #open the file and  write to it
        json.dump(data, f)

def main(source, target): #entry point
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source) # os.path.join works for all operating systems
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "game")
    
    create_dir(target_path)

    for src, dest in zip(game_paths, new_game_dirs): #zip just combines them together so that each corresponding element are tupled together
        dest_path  = os.path.join(target_path, dest) #creates a path in target with dest
        copy_and_overwrite(src, dest_path) #copies the src path to the dest path

    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)
    
    

if __name__ == "__main__": #only runs when script is being executed directly
    args = sys.argv #stores command-line args in args as a list
    
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only.")
    
    source, target = args[1], args[2]   
    main(source, target)