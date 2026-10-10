import os

class Properties:
    def __init__(self, path, data):
        self.path = path
        self.data = data
        self.final_text = ""

    def create(self):
        with open(os.path.join(os.getcwd(),"assets","server.properties"), "r") as file: # It opens the file that will be edited.
            for line in file.readlines():
                # Finds "motd"
                if "motd" in line:
                    self.final_text += f"motd={self.data["motd"]}\n"
                # Finds "server ip"
                elif "server-ip" in line:
                    self.final_text += f"server-ip={self.data["ip"]}\n"
                else:
                    self.final_text += line

        with open(os.path.join(self.path,"server.properties"), "w") as file:
            file.write(self.final_text) # Writing to the final file
