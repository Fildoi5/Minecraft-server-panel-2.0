import json
import os
import requests
import sys
import subprocess
import threading
import shutil
import time

class InstallServer:
    def __init__(self, url, path, logger, javapath, command, dependencies, name, ram):
        self.url = url # Url to download server.jar
        self.path = os.path.join(os.getcwd(), path) # Path to server
        self.logger = logger # Logger object
        self.javapath = os.path.join(javapath, "bin", "java.exe") # Path to java
        self.command = command
        self.runcode = 0
        self.dependencies = dependencies
        self.name = name # Server name
        self.args = []
        self.ram = ram # Server ram

        self.check_folders()
        self.download_installer()

    def check_folders(self):
        self.logger.write("Installing Server", "INFO", "Installer")
        if not os.path.exists(self.path):

            self.logger.write(f"Server directory doesn't exist.", "WARN", "Installer")
            self.logger.write(f"Creating server directory: {self.path}", "INFO", "Installer")
            try:
                os.makedirs(self.path) # Create directories at the specified path if they do not exist.
            except Exception as e:
                self.logger.write(f"Creating server directory failed: {e}", "ERROR", "Installer")
                sys.exit() # Close application

            self.logger.write("Creating server directory is successful.", "INFO", "Installer")

    def download_installer(self):
        self.logger.write(f"Downloading server jar from: '{self.url}'", "INFO", "Installer")
        try:
            data = requests.get(self.url).content

            with open(os.path.join(self.path, "server.jar"), "wb") as file:
                file.write(data)
        except Exception as e:
            self.logger.write(f"Downloading server jar failed: {e}", "ERROR", "Installer")
            sys.exit() # Close application
        self.logger.write("Downloading server jar is successful.", "INFO", "Installer")

        self.runscript()

    def set_eula(self):
        # Eula
        self.logger.write(f"Rewriting EULA", "INFO", "Installer")
        try:

            with open(os.path.join(self.path, "eula.txt"), "w") as file:
                file.write("eula=true")
        except Exception as e:
            self.logger.write(f"Rewriting EULA failed: {e}", "ERROR", "Installer")
            sys.exit()  # Close application

        self.logger.write(f"Rewriting EULA is successful.", "INFO", "Installer")

    def set_server_data(self):
        # Save data about server
        self.logger.write(f"Editing file servers.json", "INFO", "Installer")
        try:

            # Opening servers.json
            with open("servers.json", "w") as file:
                dic = {
                    "name": self.name,
                    "path": self.path,
                    "java_path": self.javapath,
                    "command": self.args,
                    "ram": self.ram
                }
                json.dump(dic, file) # Save json to server.json
        except Exception as e:
            self.logger.write(f"Editing file servers.json failed: {e}", "ERROR", "Installer")
            sys.exit() # Close application

    def runscript(self):
        self.logger.write(f"Running server jar from: '{self.javapath}'", "INFO", "Installer")

        try:
            thread = threading.Thread(target=self.runthread)
            thread.start()
            thread.join()

            if self.runcode == 1:
                self.runcode = 0
                sys.exit()

        except Exception as e:
            self.logger.write(f"Running server jar failed: {e}", "ERROR", "Installer")
            sys.exit() # Close application

        self.logger.write("Running server jar is successful.", "INFO", "Installer")

        # if sys.platform == "win32":
        #     self.args = self.dependencies["run_command_windows"]
        # elif sys.platform == "linux":
        #     self.args = self.dependencies["run_command_linux"]

        # obj = run.Run(self.path, self.args, self.logger, self.javapath)
        # obj.run()

        self.set_eula()
        self.set_server_data()


    def runthread(self):
        try:
            process = subprocess.Popen([self.javapath, "-jar", os.path.join(self.path, "server.jar"),self.command],
                                       cwd=self.path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in process.stdout:
                self.logger.write(str(line), "INFO", "Minecraft")

            returncode = process.wait()
            if returncode  != 0:
                raise subprocess.CalledProcessError(returncode, process.args)

        except Exception as e:
            self.logger.write(f"Running server jar failed: {e}", "ERROR", "Installer")
            self.runcode = 1
            sys.exit()









