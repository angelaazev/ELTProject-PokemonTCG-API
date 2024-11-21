import requests
import json
import os


def get_data_github(owner_repo, path):
    #Accessing the dir through GitHub API
    print(f"Accessing repository path: {path}")
    get_github_data = requests.get(f"https://api.github.com/repos/{owner_repo}/contents/{path}")
    get_github_data.raise_for_status()
    os.makedirs(f'{path}', exist_ok=True)

    #Getting dir files
    for file in get_github_data.json():
        file_link = file['download_url']
        file_name = file["name"]
        get_file_content = requests.get(file_link)

        #Writing the files into the path specified
        print(f"Writing file {file_name} into directory: {path}")
        with open (f"{path}/{file_name}", 'w') as write_json:
            json.dump(get_file_content.json(), write_json, indent=4)

    return path #('cards/en', 'decks/en', 'sets')
        

#Reading from the file 
    # with open('get_github_data_json.json') as json_file:
    #     data = json.load(json_file)
    #     for file in data:
    #         file_name = file["name"]
    #         print(file)
    #         file_link = file['download_url']
    #         get_file_content = requests.get(file_link)
                
            # with open (f"{path}/{file_name}", 'w') as write_json:
            #     json.dump(get_file_content.json(), write_json, indent=4)


        



