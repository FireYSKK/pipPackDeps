import requests
import graphviz

# Name of a package
packageName = input("Введите название пакета: ")
# Graph object
dot = graphviz.Digraph(f'{packageName} requirements')
# root of the graph
dot.node(packageName, packageName, color='black', fillcolor='green', style='filled')

# blacklist
# some package cause extremely long dependency chains (probably documentation error)
blacklist = ["six", "boto3-stubs", "wheel", "attrs", "mypy", "hypothesis", "pytest", "sphinx", "html5lib", "furo",
             "setuptools", "virtualenv", "backports-functools-lru-cache", "zope", "rich", "pep517", "ipython",
             "twisted", "pyparsing", "scipy", "numbagg", "scanpydoc", "fsspec"]

# set of checked packages
allPackages = set(blacklist)
allPackages.add(packageName)

# color preset
colors = ['aliceblue', 'antiquewhite', 'deepskyblue', 'aquamarine', 'blue', 'blueviolet', 'chartreuse', 'chocolate',
          'crimson', 'cyan', 'violet', 'gold', 'green', 'hotpink', 'magenta', 'orange', 'red', 'pink',
          'yellow']
colorIndex = 0

def getPackageName(requirement: str) -> str:
    if requirement.find("pytest") != -1: return "pytest"
    if requirement.find("sphinx") != -1: return "sphinx"
    for i in range(1, len(requirement)):
        if not (requirement[i].isalnum() or requirement[i] == "-" or requirement[i] == "_" or requirement[i] == "."):
            return requirement[:i]
    return requirement


def getPackageRequirements(packageName: str) -> None:
    allPackages.add(packageName)
    json1 = requests.get(f"https://pypi.org/pypi/{packageName}/json").json()

    # package name not found
    try:
        requirements = json1["info"]["requires_dist"]
    except KeyError:
        print("package name not found")
        return
    
    # The end reached
    if not requirements:
        print(packageName, "is a leaf")
        return

    # drop the version (aesthetics only)
    global colorIndex
    thisColorIndex = colorIndex
    colorIndex += 1
    for i in range(len(requirements)):
        requirements[i] = getPackageName(requirements[i]).lower()
    requirements = set(requirements)
    for i in requirements:
        if i not in allPackages:
            dot.node(i, i, color='black', fillcolor=colors[thisColorIndex % len(colors)], style='filled')
            dot.edge(packageName, i)
    for i in requirements:
        if i not in allPackages:
            getPackageRequirements(i)


getPackageRequirements(packageName)
print(len(allPackages))
with open(packageName+".txt", 'w') as fout:
    fout.write(dot.source)