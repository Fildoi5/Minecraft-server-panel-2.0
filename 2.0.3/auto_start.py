import json
import datetime
import os


class AutoStart:
    def __init__(self, logger):
        self.logger = logger
        self.path = os.path.join(os.getcwd(), "assets", "time_config.json")
        self.configdic = self.load_config()

    # Load server data
    def load_config(self):
        self.logger.write("Loading time config", "INFO", "Time")
        try:
            if os.path.exists(self.path):
                with open(self.path, "r") as raw_file:
                    j = json.load(raw_file)
                    self.logger.write("Time configuration loading was successful.", "INFO", "Time")
                    return j
            else:
                self.logger.write("Time config doesn't exist.", "WARN", "Time")
                return self.create_config()
        except Exception as e:
            self.logger.write(f"Loading time config failed: {e}", "ERROR", "Time")

    def create_config(self):
        self.logger.write("Creating time config", "INFO", "Time")
        try:

            dic = {
                "startup": {"Monday": None, "Tuesday": None, "Wednesday": None, "Thursday": None, "Friday": None,
                            "Saturday": None, "Sunday": None},
                "shutdown": {"Monday": None, "Tuesday": None, "Wednesday": None, "Thursday": None, "Friday": None,
                             "Saturday": None, "Sunday": None}
            }
            with open(self.path, "w") as file:
                json.dump(dic, file)
            return dic

        except Exception as e:
            self.logger.write(f"Creating time config failed: {e}", "ERROR", "Time")

    def create_own_config(self, dic):
        self.logger.write("Creating time config", "INFO", "Time")
        try:

            with open(self.path, "w") as file:
                json.dump(dic, file)
            self.configdic = dic

        except Exception as e:
            self.logger.write(f"Creating time config failed: {e}", "ERROR", "Time")

    def check_startup_time(self):
        current_time = datetime.datetime.now()
        day = current_time.strftime("%A")
        time = current_time.strftime("%H:%M")
        startup_time = self.configdic.get("startup").get(str(day))

        if startup_time == time:
            self.logger.write(f"It is: {time} Starting server", "INFO", "Time")
            return True
        else:
            return False

    def check_shutdown_time(self):
        current_time = datetime.datetime.now()
        day = current_time.strftime("%A")
        time = current_time.strftime("%H:%M")
        shutdown_time = self.configdic.get("shutdown").get(str(day))

        if shutdown_time == time:
            self.logger.write(f"It is: {time} Shutting down the server", "INFO", "Time")
            return True
        else:
            return False
