import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


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
    print("sleeping")
    await asyncio.sleep(5)
    print("sleep end")
    await watch_task


if __name__ == "__main__":
    asyncio.run(main())
