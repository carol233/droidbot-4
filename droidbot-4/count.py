import os

def FirstDir(path):
    # return first_level dirs from a path
    list = []
    if (os.path.exists(path)):
        files = os.listdir(path)
        for file in files:
            m = os.path.join(path,file)
            # if (os.path.isdir(m)):
            h = os.path.split(m)
                # print(h[1])
            list.append(h[1])
        return(list)

workplace = 'G:/Ad/'
total = 0

for dir in FirstDir(workplace):
    if dir.startswith('out'):
        outdir = os.path.join(workplace+dir)
        count = len(FirstDir(outdir))
        total = total + count
print(total)
