import yaml

CONFIG_PATH = "config/config.yaml"

# Loads the YAML file as a dictionary
def load_config():
    """Loads the config.yaml file as a dictionary."""
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

# Saves the YAML file from its dictionary form
def save_config(data):
    """Writes updated dictionary back to config.yaml."""
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False)

if __name__ == "__main__":
    CONFIG = load_config()
    print(CONFIG)
    CONFIG["role_selection"]["selector_message_id"] = 5244165414654
    save_config(CONFIG) 
    CONFIG = load_config()
    print(CONFIG)
    CONFIG["role_selection"]["selector_message_id"] = 1349066107893583903
    save_config(CONFIG) 