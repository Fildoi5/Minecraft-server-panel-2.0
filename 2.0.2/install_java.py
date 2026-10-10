import zipfile
import requests
import os
import shutil
import sys

class InstallJava:
    def __init__(self, logger, path, url):
        self.url = url
        self.path = os.path.join(os.getcwd(), path)
        self.logger = logger


    def create_folders(self):
        shutil.rmtree(self.path, ignore_errors=True)
        if not os.path.exists(self.path):
            self.logger.write(f"Creating java directory: {self.path}", "INFO", "Installer-Java")
            try:
                os.mkdir(self.path)
            except Exception as e:
                self.logger.write(f"Creating java directory failed: {e}", "ERROR", "Installer-Java")
                sys.exit()

            self.logger.write("Creating java directory is successful.", "INFO", "Installer-Java")

    def download_java(self):
        self.create_folders()

        self.logger.write(f"Downloading java from: '{self.url}'", "INFO", "Installer-Java")
        try:
            data = requests.get(self.url).content
            with open(os.path.join(self.path, "java.zip"), "wb") as file:
                file.write(data)
        except Exception as e:
            self.logger.write(f"Downloading java failed: {e}", "ERROR", "Installer-Java")
            sys.exit()

        self.logger.write("Downloading java is successful.", "INFO", "Installer-Java")

        self.extract_java(os.path.join(self.path, "java.zip"))

    def extract_java(self,zip_path):
        self.logger.write("Extracting java", "INFO", "Installer-Java")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.path)
        except Exception as e:
            self.logger.write(f"Extracting java failed: {e}", "ERROR", "Installer-Java")
            sys.exit()

        self.logger.write("Extracting java is successful.", "INFO", "Installer-Java")

        self.logger.write("Deleting java zip file", "INFO", "Installer-Java")
        try:
            os.remove(zip_path)
        except Exception as e:
            self.logger.write(f"Deleting java zip file failed: {e}", "ERROR", "Installer-Java")
            sys.exit()

        self.logger.write("Deleting java zip file is successful.", "INFO", "Installer-Java")

    def get_java_directory(self):
        self.logger.write(f"Folder is: {self.path}", "DEBUG", "Installer-Java")
        dirs = next(os.walk(os.path.join(os.getcwd(), self.path)))[1]
        self.logger.write(f"All folders ('{self.path}'): {dirs}", "DEBUG", "Installer-Java")

        for i in dirs:
            if "jdk" in i:
                self.logger.write(f"Folder of java is: '{os.path.join(self.path, i)}'", "DEBUG", "Installer-Java")
                return os.path.join(self.path, i)

        return None