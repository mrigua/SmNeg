from pathlib import Path


class HotFolder:
    def __init__(self, directory: Path, extensions: tuple[str, ...]):
        self.directory = directory
        self.extensions = extensions
        self.previous = {}

    def ready_files(self):
        current = {}
        for path in sorted(self.directory.iterdir()):
            if path.suffix.lower() not in self.extensions:
                continue
            try:
                stat = path.stat()
                if path.is_file() and stat.st_size:
                    current[path] = (stat.st_size, stat.st_mtime_ns)
            except OSError:
                continue
        ready = [path for path, signature in current.items()
                 if self.previous.get(path) == signature]
        self.previous = current
        return sorted(ready, key=lambda path: (current[path][1], path.name))
