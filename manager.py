import os
import json
import datetime

customize = {}  


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
    This function sorts a single file to a new directory based on the current customize order.
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

        def sortByType():
            extension = nameParts[TYPE]
            types = data.get("type", {})
            if extension in types:
                baseNewPath = directories[extension]
                newPath = os.path.join(baseNewPath, fileName)
                os.replace(path, newPath)
                return f"Successfully sorted {fileName}."
            return "failed."

        def sortByDate():
            creationDate = get_creation_date_str(path)
            date = data.get("date", {})
            if creationDate in date:
                baseNewPath = directories[creationDate]
                newPath = os.path.join(baseNewPath, fileName)
                os.replace(path, newPath)
                return f"Successfully sorted {fileName}."
            return "failed."

        def sortBySize():
            sizeOfFile = str(int(os.path.getsize(path) / 1024))
            size = data.get("size", {})
            if sizeOfFile in size:
                baseNewPath = directories[size]
                newPath = os.path.join(baseNewPath, fileName)
                os.replace(path, newPath)
                return f"Successfully sorted {fileName}."
            return "failed."

        pointerToFunctions = {
            "type": sortByType,
            "date": sortByDate,
            "size": sortBySize
        }

        for key in ["1", "2", "3"]:
            sort_type = customize.get(key)
            if sort_type:
                msg = pointerToFunctions[sort_type]()
                if "Successfully" in msg:
                    return msg

        return f"failed sorted {fileName}."

    except Exception as e:
        return f"Error: {e}"


def initializeSettings(first, second, third):
    """
    This function initializes the filter order to organize by.
    Input:
        - first: first condition.
        - second: second condition.
        - third: third condition.
    Output:
        - None
    """
    customize["1"] = first
    customize["2"] = second
    customize["3"] = third


def SortDir(dir):
    """
    This function sorts all files in a directory to new directories.
    Input:
        - dir: path to the directory whose files should be sorted.
    Output:
        - A status list: [success_files, failed_files]
    """
    SUCCESS = 0
    FAILD = 1
    results = [[], []]

    with os.scandir(dir) as dirfiles:
        for file in dirfiles:
            if file.is_file():
                path = os.path.join(dir, file.name)
                result = SortSingleFile(path)
                if "Successfully" in result:
                    results[SUCCESS].append(file.name)
                else:
                    results[FAILD].append(file.name)
    return results
