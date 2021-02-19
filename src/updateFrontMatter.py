
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

    def __str__(self) -> str:
        return ''


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

def updateFrontMatterBlock(mdInfo: MdInfo):

    mfb = frontmatter.load(testFile)

    mfb['layout'] = mdInfo.layout
    mfb['title'] = mdInfo.title
    if mdInfo.parent != None:
        mfb['parent'] = mdInfo.parent
    
    try:
        result = frontmatter.dumps(mfb)
        writeFile = open(testFile, 'w')
        writeFile.write(result)
    except Exception as err:
        print(err)
        pass

def list_files(startpath) -> list[MdInfo]:
    returnList = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        dirName = '{}{}'.format(indent, os.path.basename(root))
        mdInfo = MdInfo()
        mdInfo.setDirName(dirName)
        mdInfo.node_path = '{}\\{}'.format(root, 'index.md')
        returnList.append(mdInfo)

        print(dirName + ':')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            fileName = '{}{}'.format(subindent, f)
            print(fileName)
            mdInfo = MdInfo()
            mdInfo.setFileName(fileName)
            mdInfo.node_path = '{}\\{}'.format(root, f)
            returnList.append(mdInfo)

    return returnList


mdList = list_files("docs") 
for md in mdList:
    print(md.__dict__)

testFile = 'test_file.md'

mdInfo = MdInfo()

fileTitle = getMdTitle(testFile)
if fileTitle is not None: 
    fileName = os.path.splitext(testFile)[0]
    mdInfo.title = "{fname}: {title}".format(fname = fileName, title = fileTitle)

updateFrontMatterBlock(mdInfo)








