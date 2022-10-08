class FilterFile:
    def __init__(self, file_name, keywords, encoding="UTF-8"):
        self.file = open(file_name, encoding=encoding)
        # self.len = len(self.file)
        self.keywords = set(keyword.lower() for keyword in keywords)
        self.file_closed = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.file_closed:
            raise StopIteration

        for string in self.file:
            words = set(word for word in string.lower().split(" "))
            matched_words = words & self.keywords

            if matched_words != set():
                return string

        self.file.close()
        self.file_closed = True
        raise StopIteration
