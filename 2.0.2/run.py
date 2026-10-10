import threading
import subprocess

class Run:
    def __init__(self, path, arguments, logger, javapath):
        self.process = None # Server process
        self.path = path # Path to the working directory
        self.arguments = arguments # Arguments for launching
        self.logger = logger # Logger object
        self.javapath = javapath # Java path
        self.runnning = False


    # Run function
    def run(self):
        thread = threading.Thread(target=self.runthread) # Server process thread
        thread.start() # Run thread

    def runthread(self):
        try:
            self.logger.write(f"Running server jar from: '{self.javapath}'", "INFO", "Run") # Write to the log
            self.runnning = True

            # Set arguments
            args = [self.javapath]
            for i in self.arguments:
                args.append(i)


            self.process = subprocess.Popen(args,cwd=self.path, stdin=subprocess.PIPE ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Create process

            # Read stdout
            for line in self.process.stdout:
                self.logger.write(line.decode("ascii").replace("\n", ""), "INFO", "Minecraft")# Write every line to the log
                if "Preparing spawn area: 100%" in line.decode("ascii"):
                    self.runnning = True

            returncode = self.process.wait()
            if returncode != 0:
                raise subprocess.CalledProcessError(returncode, self.process.args)

            self.runnning = False
        except Exception as e:
            self.logger.write(f"Running server jar failed: {e}", "ERROR", "Run") # Write to the log
            self.runnning = False

    def toogle_run(self):
        if self.runnning:
            self.logger.write(f"Shutting down server", "INFO", "Run") # Write to the log
            self.write(b'stop')
            return "OFFLINE" # Returns that the server is down
        else:
            self.logger.write(f"Running server", "INFO", "Run") # Write to the log
            self.run() # Run server
            return "ONLINE" # Returns that the server is up


    def write(self, text):
        self.logger.write(f"Writing to server console", "INFO", "Run") # Write to the log
        try:
            self.process.stdin.write(text + b'\n')
            self.process.stdin.flush()
        except Exception as e:
            self.logger.write(f"Writing to server console failed: {e}", "ERROR", "Run") # Write to the log

