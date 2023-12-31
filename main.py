import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
import psutil


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print("Got it!")
            print(event.src_path)


async def watch_directory(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print("Watching directory: {}".format(path))
    try:
        while True:
            await asyncio.sleep(1)
    finally:
        observer.stop()
        observer.join()


async def main():
    watch_task = asyncio.create_task(watch_directory("./tmp"))
    print("running")

    print("run subprocess")
    processes = []
    processes.append(subprocess.Popen(["sleep", "1000"]))
    processes.append(subprocess.Popen(["sleep", "1000"]))
    processes.append(subprocess.Popen(["sleep", "1000"]))

    print("show children")
    pid = os.getpid()
    parent_prcess = psutil.Process(pid)
    children = parent_prcess.children(recursive=True)

    for child in children:
        print(f"child pid is {child.pid}")
        child.kill()
        child.wait()
        print(f"killed {child.pid}")

    print("awaiting")
    await watch_task


if __name__ == "__main__":
    asyncio.run(main())
