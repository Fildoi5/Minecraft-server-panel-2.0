import os
import shutil

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
                # Finds "online mod"
                elif "online-mode" in line:
                    self.final_text += f"online-mode={self.data["onlinemode"]}\n"
                # Finds "difficulty"
                elif "difficulty" in line:
                    self.final_text += f"difficulty={self.data["difficulty"]}\n"
                else:
                    self.final_text += line

        with open(os.path.join(self.path,"server.properties"), "w") as file:
            file.write(self.final_text) # Writing to the final file

        if os.path.exists(os.path.join(os.getcwd(),"temp", "server-icon.png")):
            try:
                shutil.move(os.path.join(os.getcwd(),"temp", "server-icon.png"),os.path.join(self.path,"server-icon.png"))
            except Exception as e:
                print(e)

