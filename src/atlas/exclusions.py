import fnmatch


class ExclusionRules:
    def __init__(self, config):
        self.excluded_names = {name.lower() for name in config["excluded_folder_names"]}
        self.excluded_paths = [path.lower() for path in config["excluded_paths"]]
        self.excluded_patterns = [pattern.lower() for pattern in config["excluded_file_patterns"]]

    def is_folder_excluded(self, name: str, path: str):
        if name.lower() in self.excluded_names:
            return True
        path_lower = path.lower()
        return any(path_lower.startswith(path) for path in self.excluded_paths)

    def is_file_excluded(self, name: str):
        name_lower = name.lower()
        return any(fnmatch.fnmatch(name_lower, pattern) for pattern in self.excluded_patterns)
