import os
import datetime

class Logging:
    def __init__(self, debug, wb=None, process="All"):
        self.debug = debug
        self.log_name = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".txt" # Vytvoření jména log souboru
        self.wb = wb
        self.process = process

        # Terminal colors
        self.RED = '\033[31m'
        self.GREEN = '\033[32m'
        self.YELLOW = '\033[33m'
        self.RESET = '\033[0m'

    def write(self, content,type_of_log, caller):
        if (self.debug and (type_of_log == "DEBUG")) or (type_of_log == "INFO") or (type_of_log == "ERROR") or (type_of_log == "WARN"):

            path = os.path.join(os.getcwd(), 'app-logs',self.log_name) # Udělání plné cesty k logu
            path_directory = os.path.join(os.getcwd(), 'app-logs') # Udělání plné cesty k složce

            if os.path.exists(path):
                with open(path, "a") as log:
                    log.write(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}\n")# Zapsání do logu

                    if type_of_log == "ERROR":
                        print(self.RED + f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}" + self.RESET)
                    elif type_of_log == "WARN":
                        print(self.YELLOW + f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}" + self.RESET)
                    elif type_of_log == "DEBUG":
                        print(self.GREEN + f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}" + self.RESET)
                    else:
                        print(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}")

                    if self.wb is not None:
                        if self.process == "All":
                            self.wb(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}")
                        else:
                            if self.process == caller:
                                self.wb(content)
            else:
                if not os.path.exists(path_directory):
                    os.mkdir(path_directory)
                with open(path, "w") as log:
                    log.write(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}\n") # Zapsání do logu
                    print(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}")
                    if self.wb is not None:
                        if self.process == "All":
                            self.wb(
                                f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{type_of_log}]: [{caller}] {content}")
                        else:
                            if self.process == type_of_log:
                                self.wb(content)

