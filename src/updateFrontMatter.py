
from os.path import dirname
from warnings import catch_warnings
import frontmatter
from markdown.core import markdown
import md2py
import os

class MdInfo: 
    def __init__(self):
        self.layout = "default"
        self.title = "default title"
        self.parent = None
        self.nav_order = 2
        self.has_children = False
        self.has_toc = False
        self.node_name = None
        self.node_path = None
        self.isDir = False

    def setDirName(self, dirName: str):
        self.isDir = True
        self.node_name = dirName.strip()

    def setFileName(self, fileName: str):
        self.isDir = False
        self.node_name = fileName.strip()


def getMdTitle(mdFileName: str) -> str:
    returnTitle = None
    mdFile = open(mdFileName, 'r')
    
    fileMd = markdown(mdFile.read())

    try:
        toc = md2py.md2py(fileMd)
        print(toc)
        returnTitle = toc.h1
    except TypeError:
        pass

    mdFile.close()

    return returnTitle

def parseFileName(path: str) -> str:
    fileName = os.path.split(path)[1]
    fileName = os.path.splitext(fileName)[0]
    return fileName

def updateFrontMatterBlock(mdInfo: MdInfo):

    mfb = frontmatter.load(testFile)

    mfb['layout'] = mdInfo.layout
    mfb['title'] = mdInfo.title
    if mdInfo.parent != None:
        mfb['parent'] = mdInfo.parent
    mfb['has_children'] = mdInfo.has_children
    mfb['nav_order'] = mdInfo.nav_order

    try:
        result = frontmatter.dumps(mfb)
        writeFile = open(testFile, 'w')
        writeFile.write(result)
    except Exception as err:
        print(err)
        pass

def find_md_files(startpath) -> dict[MdInfo]:
    mdFilesDict = dict()
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        dirName = '{}{}'.format(indent, os.path.basename(root))
        mdInfo = MdInfo()
        mdInfo.setDirName(dirName)
        mdInfo.node_path = '{}\\{}'.format(root, 'index.md')
        
        mdFilesDict[mdInfo.node_path] = mdInfo

        print(dirName + ':')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            fileName = '{}{}'.format(subindent, f)
            print(fileName)
            mdInfo = MdInfo()
            mdInfo.setFileName(fileName)
            mdInfo.node_path = '{}\\{}'.format(root, f)

            if mdFilesDict.get(mdInfo.node_path) == None:
                ext:str
                ext = os.path.splitext(f)[1]
                if ext.lower() == ".md":
                    print(ext)
                    print(dirName)
                    mdFilesDict[mdInfo.node_path] = mdInfo

    return mdFilesDict


mdDict = find_md_files("docs") 

# value: MdInfo
# for key, value in mdDict.items():
#     print('{}: {}'.format(key, value.__dict__))
#     print(parseFileName(value.node_name))

testFile = 'test_file.md'
testFile = 'docs\\test-folder1\\test-file1.md'

mdInfo = MdInfo()

fileTitle = getMdTitle(testFile)
fileName  = parseFileName(testFile)
if fileTitle is not None: 
    mdInfo.title = "{fname}: {title}".format(fname = fileName, title = fileTitle)
else:
    mdInfo.title = "{fname}: {title}".format(fname = fileName, title = mdInfo.title)

updateFrontMatterBlock(mdInfo)








