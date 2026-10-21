import os
import sys

class NonRoot:
    def __init__(self, logger):
        self.logger = logger

    def get_usr(self):
        try:
            self.logger.write("Creating args", "INFO", "NonRoot (create_args())") # Write to the log
            path = os.path.join(os.getcwd(),"user.usr")
            if sys.platform == "linux":
                if os.path.exists(path):
                    with open(path, "r") as file:
                        text = file.read()
                        if text.strip() != "":
                            return text.strip()
                        else:
                            return None
                else:
                    self.logger.write("user.usr doesn´t exist", "ERROR", "NonRoot (create_args())")  # Write to the log
                    return None

            else:
                return []
        except Exception as e:
            self.logger.write("Creating args failed", "ERROR", "NonRoot (create_args())")  # Write to the log