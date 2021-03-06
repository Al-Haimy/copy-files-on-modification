
import watchdog.events
import watchdog.observers
import time
import shutil
import os


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, to_copy):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.php', "*.js", "*.map"],
                                                             ignore_directories=True, case_sensitive=False)
        self.to_copy = to_copy

    def on_created(self, event):
        print("Watchdog received created event - % s." % event.src_path)
        # Event is created, you can process it now

    def on_modified(self, event):
        print("Watchdog received modified event - % s." % event.src_path)
        # Source path
        source = event.src_path

        # Destination path
        path_to_copy = os.path.normpath(source)
        if "build" in source:
            destination = self.to_copy + \
                path_to_copy.split(os.sep)[-2] + \
                "\\" + path_to_copy.split(os.sep)[-1]
            self.copytodist(source, destination)
        elif "node_modules" in source:
            print("will not copy")
        else:
            destination = self.to_copy + path_to_copy.split(os.sep)[-1]
            self.copytodist(source, destination)

        # Copy the content of
        # source to destination

    def copytodist(self, source, destination):
        try:
            shutil.copy(source, destination)
            print("File copied successfully.")

        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")

        # For other errors
        except:
            print("Error occurred while copying file.")
            # Event is modified, you can process it now


if __name__ == "__main__":
    print("Hello I'm Here To Help you move your files when needed!")
    src_path = input("Enter folder path Please: ")
    copy_to = input("Enter Folder to copy the files to :")

    event_handler = Handler(copy_to)
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
