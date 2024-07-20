import yaml

def read(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)
    
def write(filepath, content):
    with open(filepath, 'a') as file:
        yaml.dump(content, file, sort_keys=False)
    print('Write YAML success.')