import os
import json
import datetime
def get_creation_date_str(filepath):
    """
    Returns the creation date of the file in YYYY-MM-DD format.
    Input:
        - filepath: A string containing the full path to the file.
    Output:
        - A string in YYYY-MM-DD date format.
    """

    timestamp = os.path.getctime(filepath)
    creation_date = datetime.datetime.fromtimestamp(timestamp)
    return creation_date.strftime("%Y-%m-%d")


def SortSingleFile(path):
    """
    This function sort a file to new directory.
    Input:
        - path: path of file to sort.
    Output:
        - A status message (string).
    """
    fileName = os.path.basename(path)
    nameParts = fileName.split('.')
    TYPE = len(nameParts) - 1
   
    project_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(project_dir, 'cfg.json')

    try:
        with open(cfg_path, 'r', encoding="utf-8") as cfg_file:
            data = json.load(cfg_file)

        directories = data["directories"]
        types = data["type"]
        extension = nameParts[TYPE]
        if extension in types:
            baseNewPath = directories[extension]
            newPath = os.path.join(baseNewPath, fileName)
            os.replace(path, newPath)
            return f"Successfully sorted {fileName}."
        
        creationDate = get_creation_date_str(path)
        date = data["date"]
        if creationDate in date:
            baseNewPath = directories[creationDate]
            newPath = os.path.join(baseNewPath, fileName)
            os.replace(path, newPath)
            return f"Successfully sorted {fileName}."
        
        sizeOfFile = str(int(os.path.getsize(path)/1024))
        size = data["size"]
        if sizeOfFile in size:
            baseNewPath = directories[creationDate]
            newPath = os.path.join(baseNewPath, fileName)
            os.replace(path, newPath)
            return f"Successfully sorted {fileName}."
        return f"faild sorted {fileName}."

    except Exception as e:
        return f"Error: {e}"
    
def SortDir(dir):
    """
    This function sort a files to new directory.
    Input:
        - dir: path to the directory whose files should be sorted.
    Output:
        - A status files(list success - 0, faild - 1).
    """
    SUCCESS = 0
    FAILD = 1
    results = [[],[]]
    with os.scandir(dir) as dirfiles:
        for file in dirfiles:
            if file.is_file():
                fileName = file.name
                path =  os.path.join(dir,fileName)
                result = SortSingleFile(path)
                if "Successfully" in result:
                    results[SUCCESS].append(fileName)
                else:
                    results[FAILD].append(fileName)
    return results
