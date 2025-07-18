import json
import os

def AddCfg(typeCfg, cfg, dir):
    """
    This function adds a new config.
    The function determines where to sort the files that meet the specified criteria.
    
    Input:
        - typeCfg: The type of the config (must match a key in the JSON file).
        - cfg: The name of the configuration to add.
        - dir: The directory to associate with the config.
    Output:
        - A status message (string).
    """
    project_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(project_dir, 'cfg.json')
    data = {}
    print(cfg_path)
    if not os.path.exists(cfg_path):
        return "Error: config file does not exist."

    try:
        with open(cfg_path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return "Error: config file is not a valid JSON."

    if typeCfg not in data:
        return f"Error: config type '{typeCfg}' not found in JSON."
    types = data[typeCfg]
    if cfg in types:
        return "This config already exists."

    data[typeCfg].append(cfg)
    data["directories"][cfg] = dir
    with open(cfg_path, 'w') as file:
        json.dump(data, file, indent=4)

    return "Config added successfully."

def main():
    print(AddCfg("type", "jsoFn", "fvfvfvfvfv"))


if __name__ == "__main__":
    main()