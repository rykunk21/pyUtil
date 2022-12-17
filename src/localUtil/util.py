import os
import time
# from bs4 import BeautifulSoup
import urllib.request

def addInit():
    # Set the directory you want to start from
    rootDir = '.'

    for dirName, subdirList, fileList in os.walk(rootDir):
        for subdir in subdirList:
            # Construct the path to the subdirectory
            subdirPath = os.path.join(dirName, subdir)

            # Check if the subdirectory already has an __init__.py file
            if not os.path.exists(os.path.join(subdirPath, '__init__.py')):
                # Create the __init__.py file if it doesn't exist
                with open(os.path.join(subdirPath, '__init__.py'), 'w') as f:
                    f.write('')
                
    
class Connection:
    """
    This is a class for making HTTP connections and downloading data from a specified URL.

    :param url: (str): The URL to connect to.
    :param data: (bytes): The data downloaded from the URL.
    """

    def __init__(self, url: str):
        """
        The constructor for Connection.
        
        :param:url (str): The URL to connect to.
        """
        self.url = url
        self._download()

    def changeUrl(self, newUrl: str):
        """
        This method changes the URL and downloads data from the new URL.
        
        :param: newUrl (str): The new URL to connect to.
        """
        self.url = newUrl
        self._download()

    def _download(self):
        """
        This method downloads data from the specified URL.
        """
        try:
            with urllib.request.urlopen(self.url) as response:
                self.data = response.read()
        except urllib.error.HTTPError as err:
            print(f"An error occurred: {err}")
            self.data = None

    def add_params(self, params: dict):
        """
        This method adds query parameters to the URL and downloads data from the updated URL.
        
        :param params: The query parameters to add to the URL.
        """
        url = urllib.parse.urlparse(self.url)
        query = urllib.parse.parse_qs(url.query)
        query.update(params)
        url = url._replace(query=urllib.parse.urlencode(query, doseq=True))
        self.url = url.geturl()
        self._download()

    def findById(self, elementId: str):
        """
        This method finds an HTML element with the specified ID in the downloaded data.
        
        :param elementId: The ID of the element to find.
        :return: The first element with the specified ID, or None if no such element was found.
        """
        if self.data:
            soup = BeautifulSoup(self.data, "html.parser")
            element = soup.find(id=elementId)
            return element

    def findByClass(self, elementClass: str):
        """
        This method finds all HTML elements with the specified class in the downloaded data.

        :param elementClass (str): The class of the elements to find.
        :return: A list of elements with the specified class, or an empty list if no such elements were found.
        """
        if self.data:
            soup = BeautifulSoup(self.data, "html.parser")
            elements = soup.find_all(class_=elementClass)
            return elements


class TestCase:
    """A class representing a test case, with an ID, expected value, actual value, and result."""

    def __init__(self, id, expected, actual, result):
        self.id = id
        self.expected = expected
        self.actual = actual
        self.result = result


class TestHelper:
    """A class that provides useful methods for testing another class."""

    def __init__(self):
        """Initialize the TestHelper instance with an empty list of test cases and a current ID of 0."""
        self.testCases = []
        self.currentId = 0

    def assertEquals(self, expected, actual):
        """Assert that the expected and actual values are equal.
        
        If the values are equal, a new TestCase object is added to the testCases list with a result of True.
        If the values are not equal, a new TestCase object is added to the testCases list with a result of False.
        The currentId is incremented by 1 each time this method is called.
        
        Args:
            expected: The expected value.
            actual: The actual value.
        """
        result = expected == actual
        testCase = TestCase(self.currentId, expected, actual, result)
        self.testCases.append(testCase)

def PyPrettify(fileName):
    """
    Improves the readability of a Python file by adding blank lines between paragraphs and sentences, and by adding appropriate indentation.

    Args:
        fileName (str): The name of the file to improve.
    """
    # Read the file into a list of lines.
    with open(fileName) as file:
        lines = file.readlines()

    # Add blank lines between paragraphs and sentences, and add appropriate indentation.
    indentLevel = 0
    newLines = []
    for line in lines:
        # Add a blank line between paragraphs.
        if line.strip() == "":
            newLines.append(line)
        else:
            # Add a blank line after each sentence.
            for sentence in line.split(". "):
                # Add appropriate indentation.
                indent = "    " * indentLevel
                newLines.append(indent + sentence + ".\n")
                newLines.append("\n")

            # Increase the indent level if the line is a loop or an if statement, and decrease it if the line starts with "return" or "pass".
            if line.strip().startswith(("for ", "while ", "if ", "elif ", "else")):
                indentLevel += 1
            elif line.strip().startswith(("return", "pass")):
                indentLevel -= 1
                
    with open(fileName, "w") as file:
        file.writelines(newLines)


class Node:
    def __init__(self, fileName, fileType, dateAdded):
        self.fileName = fileName
        self.fileType = fileType
        self.dateAdded = dateAdded
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
    def __repr__(self):
        out = ''
        current = self.head
        i=0
        while not current is None:
            out += f'i: {i}\nName: {current.fileName}\nType: {current.fileType}\nDate: {current.dateAdded}\n'
            current = current.next
            i += 1
        return out

    def __str__(self):
        return self.__repr__()

    def addNode(self, fileName, fileType, dateAdded):
        node = Node(fileName, fileType, dateAdded)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node

    def removeNode(self, fileName):
        current = self.head
        if current is not None and current.fileName == fileName:
            self.head = current.next
        else:
            while current is not None:
                if current.fileName == fileName:
                    break
                previous = current
                current = current.next
            if current is None:
                return
            previous.next = current.next


def scanDirectory(directory):
    linkedList = LinkedList()
    for fileName in os.listdir(directory):
        if ('.') in fileName:
            fileType = fileName.split(".")[-1]
        else:
            fileType = 'DIR'
        dateAdded = time.ctime(os.path.getctime(fileName))
        linkedList.addNode(fileName, fileType, dateAdded)
    return linkedList
    
    
    
    
    
    
    
    
    
    
    
    
 
# Create a Connection object and download the contents of the page
conn = Connection("https://www.python.org")

# Find all elements on the page with the given class
elements = conn.findByClass("python-list")
print(elements)
