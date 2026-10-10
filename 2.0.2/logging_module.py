import os
import datetime


class Logging:
    def __init__(self, debug, wb):
        self.debug = debug
        self.log_name = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".txt" # Vytvoření jména log souboru
        self.wb = wb

    def write(self, content,type_of_log, caller):
        if (self.debug and (type_of_log == "DEBUG")) or (type_of_log == "INFO") or (type_of_log == "ERROR") or (type_of_log == "WARN"):

            path = os.path.join(os.getcwd(), 'app-logs',self.log_name) # Udělání plné cesty k logu
            path_directory = os.path.join(os.getcwd(), 'app-logs') # Udělání plné cesty k složce
            if os.path.exists(path):
                with open(path, "a") as log:
                    log.write(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}\n") # Zapsání do logu
                    print(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}")

                    if self.wb is not None:
                        self.wb(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}")
            else:
                if not os.path.exists(path_directory):
                    os.mkdir(path_directory)
                with open(path, "w") as log:
                    log.write(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}\n") # Zapsání do logu
                    print(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}")
                    if self.wb is not None:
                        self.wb(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}")

