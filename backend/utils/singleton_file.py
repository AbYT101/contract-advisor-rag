class SingletonFile:
    _instance = None
    _file_content = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonFile, cls).__new__(cls)
        return cls._instance

    def set_file_content(self, content):
        self._file_content = content

    def get_file_content(self):
        return self._file_content
