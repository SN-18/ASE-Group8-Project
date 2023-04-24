from data_loader import *
from settings import *
from globals import *


def isStatEqual(allY1, allY2):
    ret = ["=" for _ in range(len(allY1))]
    for i in range(len(ret)):
        if not (bootstrap(allY1[i].has.values(), allY2[i].has.values()) and cliffsDelta(list(allY1[i].has.values()), list(allY2[i].has.values()))):
            ret[i] = "!="
    return ret

#### STARTUP ####
d = cli(settings(help))

for key, val in d.items():
    the[key] = val

directoryPath = 'etc/data/'
files = ['auto93.csv', 'auto2.csv', 'SSN.csv', 'SSM.csv', 'china.csv', 'coc1000.csv', 'coc10000.csv', 'pom.csv', 'nasa93dem.csv', 'healthCloseIsses12mths0001-hard.csv', 'healthCloseIsses12mths0011-easy.csv']

for currFile in files:
    filePath = directoryPath + currFile
    data = DATA(filePath)

    allSway1Best = []
    allSway2Best = []
    allXpln1Best = []
    allXpln2Best = []
    length = 0
    sway1evals = 0
    sway2evals = 0

    for i in range(20):
        print('--> Running SWAY and XPLN iteration: ', i, 'for file: ', currFile)
        the['seed'] = random.randint(-sys.maxsize - 1, sys.maxsize)


        #### SWAY ####
        sway1best, sway1rest, sway1evals = data.sway1()
        allSway1Best = allSway1Best + list(sway1best.rows.values())
        sway2best, sway2rest, sway2evals = data.sway2()
        allSway2Best = allSway2Best + list(sway2best.rows.values())


        print("\nall ",data.stats('mid',data.cols.y, 2))
        print("    ",data.stats('div',data.cols.y, 2))
        print("\nsway1 best ", sway1best.stats('mid', sway1best.cols.y, 2))
        print("    ", sway1best.stats('div', sway1best.cols.y, 2))
        print("\nsway1 rest ", sway1rest.stats('mid', sway1rest.cols.y, 2))
        print("    ", sway1rest.stats('div', sway1rest.cols.y, 2))
        print("\nall ~= sway1best?", diffs(sway1best.cols.y, data.cols.y))
        print("best ~= sway1rest?", diffs(sway1best.cols.y, sway1rest.cols.y))


        #### XPLN ####
        rule, most = data.xpln(sway1best, sway1rest)
        rule2, most2 = data.xpln(sway2best, sway2rest)

        if (rule is None or rule2 is None):
            continue
        print("\n-----------\n explain1 =",showRule(rule))
        print("\n-----------\n explain2 =", showRule(rule2))
        # data1 = DATA(data.cols, selects(rule, data.rows))
        select = selects(rule, data.rows)
        data_select = [s for s in select if s != None]
        allXpln1Best = allXpln1Best + data_select
        xplnData = data.clone(data_select)

        select2 = selects(rule2, data.rows)
        data_select2 = [s for s in select2 if s != None]
        allXpln2Best = allXpln2Best + data_select2
        xpln2Data = data.clone(data_select2)

        print("all\t\t\t",data.stats('mid', data.cols.y, 2),data.stats('div', data.cols.y, 2))
        print("sway1 with ", sway1evals," evals", sway1best.stats('mid', sway1best.cols.y, 2), sway1best.stats('div', sway1best.cols.y, 2))
        print("xpln1 with ",sway1evals," evals",xplnData.stats('mid', xplnData.cols.y, 2), xplnData.stats('div', xplnData.cols.y, 2))
        print("sway2 with ", sway2evals, " evals", sway2best.stats('mid', sway2best.cols.y, 2),sway2best.stats('div', sway2best.cols.y, 2))
        print("xpln2", xpln2Data.stats('mid', xpln2Data.cols.y, 2), xpln2Data.stats('div', xpln2Data.cols.y, 2))
        top, _ = data.betters(len(sway1best.rows))
        length = len(sway1best.rows)
        # top = DATA(data.cols, top)
        selected_data = [s for s in top.values() if s != None]
        topData = data.clone(selected_data)
        print("sort with ",len(data.rows)," evals",topData.stats('mid',topData.cols.y,2),topData.stats('div',topData.cols.y,2))

    sway1best = data.clone(allSway1Best)
    sway2best = data.clone(allSway2Best)
    xpln1Data = data.clone(allXpln1Best)
    xpln2Data = data.clone(allXpln2Best)
    with open('etc/out/' + currFile + '-summary.txt', 'w') as file:
        print("--- TABLE ONE ---\n", file=file)
        print("all\t\t\t",data.stats('mid', data.cols.y, 2),data.stats('div', data.cols.y, 2), file=file)
        print("sway1 with ", sway1evals," evals", sway1best.stats('mid', sway1best.cols.y, 2), sway1best.stats('div', sway1best.cols.y, 2), file=file)
        print("xpln1 with ",sway1evals," evals",xplnData.stats('mid', xplnData.cols.y, 2), xplnData.stats('div', xplnData.cols.y, 2), file=file)
        print("sway2 with ", sway2evals, " evals", sway2best.stats('mid', sway2best.cols.y, 2),sway2best.stats('div', sway2best.cols.y, 2), file=file)
        print("xpln2 with ", sway2evals, " evals", xpln2Data.stats('mid', xpln2Data.cols.y, 2), xpln2Data.stats('div', xpln2Data.cols.y, 2), file=file)
        top, _ = data.betters(length)
        # top = DATA(data.cols, top)
        selected_data = [s for s in top.values() if s != None]
        topData = data.clone(selected_data)
        print("top",topData.stats('mid',topData.cols.y,2),topData.stats('div',topData.cols.y,2), file=file)

        print("\n\n\n--- TABLE TWO ---\n", file=file)
        print("\t\t\t\t", [s.txt for s in data.cols.y.values()], file=file)
        print("all to all\t\t", isStatEqual(data.cols.y, data.cols.y), file=file)
        print("all to sway1\t", isStatEqual(data.cols.y, sway1best.cols.y), file=file)
        print("all to sway2\t", isStatEqual(data.cols.y, sway2best.cols.y), file=file)
        print("sway1 to sway2\t", isStatEqual(sway1best.cols.y, sway2best.cols.y), file=file)
        print("sway1 to xpln1\t", isStatEqual(sway1best.cols.y, xplnData.cols.y), file=file)
        print("sway2 to xpln2\t", isStatEqual(sway2best.cols.y, xpln2Data.cols.y), file=file)
        print("sway1 to top\t", isStatEqual(sway1best.cols.y, topData.cols.y), file=file)
