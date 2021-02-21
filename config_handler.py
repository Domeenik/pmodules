import json
import sys

#ToDo: add different file formats: yaml, xml, conf

class ConfigHandler():
    def __init__(self, path):
        self.path_to_config = path
        self.reload()
    
    def reload(self):
        with open(self.path_to_config, 'r') as f:
            try:
                self.json_unparsed = json.load(f)
            except:
                print("[ERROR] could not read {}".format(self.path_to_config))
                raise IOError("could not read file")

    def get(self, *args, **kwargs):
        try:
            if len(args) == 0:
                return self.json_unparsed
            elif len(args) == 1:
                return self.json_unparsed[args[0]]
            elif len(args) == 2:
                return self.json_unparsed[args[0]][args[1]]
            elif len(args) == 3:
                return self.json_unparsed[args[0]][args[1]][args[2]]
            
            # if length > 3 use a less effective way
            # but otherwise the function will get too long
            elif len(args) > 3:
                tmp_dict = self.json_unparsed
                for i in range(len(args)-1):
                    tmp_dict = tmp_dict[args[i]]
                return tmp_dict[args[-1]]
        except KeyError as err:
            print(f"[ERROR] key {err} does not exist")

    def print(self, *args, **kwargs):
        print(json.dumps(self.get(*args), indent=4))

    def set(self, topic, option, value=""):
        if not value == "":
            self.json_unparsed[str(topic)][str(option)] = value
        else:
            self.json_unparsed[str(topic)] = option
        self.save()

    def save(self,):
        try:
            with open(self.path_to_config, 'w') as f:
                json.dump(self.json_unparsed, f, indent=4)
        except:
            print("[ERROR] could not save file")