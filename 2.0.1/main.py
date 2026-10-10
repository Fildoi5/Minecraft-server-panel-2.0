import atexit
import time

import logging_module
import os
import installer
import web
import multiprocessing



class Main:
    def __init__(self):
        self.logger = logging_module.Logging(True, None)
        self.logger.write("Hello!", "INFO", "Start")

        atexit.register(self.exit_handler)


        self.installer_process = multiprocessing.Process(target=self.run_installer)
        self.web_process = multiprocessing.Process(target=self.run_web)
        self.check_installation()
    def check_installation(self):
        if os.path.exists("servers.json"):
            self.logger.write("Server is installed", "INFO", "Start")
            self.web_process.run()
            self.web_process.join()
        else:
            self.logger.write("Server is not installed", "WARN", "Start")

            self.installer_process.start()
            self.installer_process.join()
            time.sleep(1)
            self.web_process.run()
            self.web_process.join()

    def run_web(self):
        obj = web.Web()
        obj.run()

    def exit_handler(self):
        self.logger.write("Goodbye!", "INFO", "Ending")

    def run_installer(self):
        obj = installer.Installer()
        obj.run()


if __name__ == "__main__":
    main = Main()
