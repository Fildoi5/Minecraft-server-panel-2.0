import json
import os
import requests
import sys
import subprocess
import threading
import properties


class InstallServer:
    def __init__(self, url, path, logger, javapath, command, name, ram, motd, ip, onlinemode,difficulty,run_args):
        self.url = url  # Url to download server.jar
        self.path = os.path.join(os.getcwd(), path)  # Path to server
        self.logger = logger  # Logger object
        self.javapath = None

        if sys.platform == "win32":
            self.javapath = os.path.join(javapath, "bin", "java.exe")  # Path to java
        elif sys.platform == "linux":
            self.javapath = os.path.join(javapath, "bin", "java")  # Path to java

        self.command = command
        self.runcode = 0
        self.name = name  # Server name
        self.args = run_args
        self.ram = ram  # Server ram
        self.motd = motd  # Server motd
        self.ip = ip  # Server ip
        self.onlinemode = onlinemode # Server online mode
        self.difficulty = difficulty # Server difficulty

        self.check_folders()
        self.download_installer()

    def check_folders(self):
        self.logger.write("Installing Server", "INFO", "Server-Installer")
        if not os.path.exists(self.path):

            self.logger.write(f"Server directory doesn't exist.", "WARN", "Server-Installer")
            self.logger.write(f"Creating server directory: {self.path}", "INFO", "Server-Installer")
            try:
                os.makedirs(self.path)  # Create directories at the specified path if they do not exist.
            except Exception as e:
                self.logger.write(f"Creating server directory failed: {e}", "ERROR", "Server-Installer")

            self.logger.write("Creating server directory is successful.", "INFO", "Server-Installer")

    # Download installer
    def download_installer(self):
        self.logger.write(f"Downloading server jar from: '{self.url}'", "INFO", "Server-Installer")
        try:
            data = requests.get(self.url).content

            with open(os.path.join(self.path, "server.jar"), "wb") as file:
                file.write(data)
        except Exception as e:
            self.logger.write(f"Downloading server jar failed: {e}", "ERROR", "Server-Installer")

        self.logger.write("Downloading server jar is successful.", "INFO", "Server-Installer")

        self.runscript()  # Run server

    def set_eula(self):
        # Eula
        self.logger.write(f"Rewriting EULA", "INFO", "Server-Installer")
        try:

            with open(os.path.join(self.path, "eula.txt"), "w") as file:
                file.write("eula=true")
        except Exception as e:
            self.logger.write(f"Rewriting EULA failed: {e}", "ERROR", "Server-Installer")
            sys.exit()  # Close application

        self.logger.write(f"Rewriting EULA is successful.", "INFO", "Server-Installer")

    def set_server_data(self):
        # Save data about server
        self.logger.write(f"Editing file servers.json", "INFO", "Server-Installer")
        try:
            dic = {
                "name": self.name,
                "path": self.path,
                "java_path": self.javapath,
                "args": self.args,
                "ram": self.ram,
                "motd": self.motd,
                "ip": self.ip,
                "onlinemode": self.onlinemode,
                "difficulty": self.difficulty
            }
            # Opening server.json
            with open("server.json", "w") as file:
                json.dump(dic, file)  # Save json to server.json

        except Exception as e:
            self.logger.write(f"Editing file servers.json failed: {e}", "ERROR", "Server-Installer")
            sys.exit()  # Close application

    def set_server_properties(self):
        # Create server properties
        self.logger.write(f"Editing file server.properties", "INFO", "Server-Installer")
        try:
            # Opening server.json
            with open("server.json", "r") as file:
                prop = properties.Properties(self.path, json.load(file)) # Loading server information
                prop.create()
        except Exception as e:
            self.logger.write(f"Editing file server.properties failed: {e}", "ERROR", "Server-Installer")
            sys.exit()  # Close application

    def runscript(self):
        self.logger.write(f"Running server jar from: '{self.javapath}'", "INFO", "Server-Installer")

        try:
            thread = threading.Thread(target=self.runthread)
            thread.start()
            thread.join()

            if self.runcode == 1:
                self.runcode = 0
                sys.exit()

        except Exception as e:
            self.logger.write(f"Running server jar failed: {e}", "ERROR", "Server-Installer")
            sys.exit()  # Close application

        self.logger.write("Running server jar is successful.", "INFO", "Server-Installer")

        self.set_eula()
        self.set_server_data()
        self.set_server_properties()

    def runthread(self):
        try:

            process = subprocess.Popen([self.javapath, "-jar", os.path.join(self.path, "server.jar"), self.command],
                                       cwd=self.path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in process.stdout:
                self.logger.write(str(line), "INFO", "Minecraft")

            returncode = process.wait()
            if returncode != 0:
                raise subprocess.CalledProcessError(returncode, process.args)

        except Exception as e:
            self.logger.write(f"Running server jar failed: {e}", "ERROR", "Server-Installer")
            self.runcode = 1
            sys.exit()
