class Parser:
   def __init__(self, path):
        self.path = path
        self.headers = []
        self.data = []

   def getData(self, separator, lineSeparator):
        file = open(self.path, encoding='utf8')
        txt = file.read()

        #split data into lines
        arr = txt.split(lineSeparator)

        #get headers from the first line
        self.headers = arr[0].split(separator)

        #loop over remaining lines and put them into list of dictionaries
        for line in arr[1:]:
            split = line.split(separator)

            #continue parsing only if the data is correct (same number of items as headers)
            if len(split) == len(self.headers):
                temp = []
                for i in range(len(self.headers)):
                    temp.append(split[i])
                self.data.append(dict(zip(self.headers, temp)))
        return self.data

