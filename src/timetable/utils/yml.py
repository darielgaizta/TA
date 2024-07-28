import yaml
from django.conf import settings

class Yml:
    def __init__(self, filename):
        self.filename = filename
        self.filepath = str(settings.RESULT_DIR / filename) + '.yaml'
    
    def read(self):
        with open(self.filepath, 'r') as file:
            return yaml.safe_load(file)
        
    def write(self, content):
        with open(self.filepath, 'a') as file:
            yaml.dump(content, file, sort_keys=False, default_flow_style=False)
        print('Write result in YAML success.')