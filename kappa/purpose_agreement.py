import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import confusion_matrix
import itertools

Annotator1 = 'Gold'
Annotator2 = ''
boxPath = '/Users/tazinafrin/Box Sync/'


def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap='Reds'):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel(Annotator1)  # gold
    plt.xlabel(Annotator2)


def readExcelFiles(path):
    df = pd.DataFrame([])
    count = 0
    count_native = 0
    count_Experimental = 0
    id = 0
    print(path)
    for path, subdirs, files in os.walk(path):
        for name in files:
            # print(name)
            id += 1
            if name.endswith(".xlsx") and name.startswith("Anno"):
                file = os.path.join(path, name)
                print(file)
                count += 1
                dataOld = pd.read_excel(file, sheetname="Old Draft", encoding="utf-8")
                dataNew = pd.read_excel(file, sheetname="New Draft", encoding="utf-8")
                '''with open(file, 'r') as f:
                    xl = pd.ExcelFile(f,encoding='utf-8')
                    sheets = xl.sheet_names
                    dataOld = xl.parse(sheets[0])
                    dataNew = xl.parse(sheets[1])'''

                parts = file.split("/")
                print(parts)

                '''dataOld['language'] = parts[3].split("_")[0]
                dataOld['mode'] = parts[4]
                dataOld['revision'] = parts[5]'''
                dataOld['id'] = id  # parts[6].split("_")[2]
                dataOld['sheet'] = "Old"
                df = df.append(dataOld)

                '''dataNew['language'] = parts[3].split("_")[0]
                dataNew['mode'] = parts[4]
                dataNew['revision'] = parts[5]'''
                dataNew['id'] = id  # parts[6].split("_")[2]
                dataNew['sheet'] = "New"
                df = df.append(dataNew)

    print("\nTotal number of files: ", count)
    '''print "Experimental/Control users: ", count_Experimental, (count-count_Experimental)
    print "Native/ESL users:", count_native, (count-count_native)'''
    return df


def findAgreements(df_fan, df_huma):
    content = ['General Content Development', 'Warrant/Reasoning/Backing', 'Rebuttal/Reservation', 'Claims/Ideas',
               'Evidence']
    surface = ['Organization', 'Word-Usage/Clarity', 'Conventions/Grammar/Spelling', 'Precision']

    total = 0
    exact_match = 0
    high_level_match = 0
    all_fan = []
    all_huma = []
    all_highlevel_fan = []
    all_highlevel_huma = []
    for index, row_huma in df_huma.iterrows():
        if index == 46:
            continue
        if row_huma['Revision Purpose Level 0'] != '' and str(row_huma['Revision Purpose Level 0']).lower() != 'nan':
            annotation_huma = row_huma['Revision Purpose Level 0'].split(',')[0]
            total += 1
            # find the same row in fan's annotations
            row_fan = df_fan[(df_fan['id'] == row_huma['id']) & (df_fan['sheet'] == row_huma['sheet']) & (
            df_fan['Sentence Index'] == row_huma['Sentence Index'])]  # & (df_fan['revision'] == row_huma['revision'])
            # print('row_fan',row_fan)
            annotation_fan = row_fan['Revision Purpose Level 0'].values[0]

            all_huma.append(annotation_huma)
            all_fan.append(annotation_fan)

            if annotation_huma in content:
                all_highlevel_huma.append("content")
            else:
                all_highlevel_huma.append("surface")

            if annotation_fan in content:
                all_highlevel_fan.append("content")
            else:
                all_highlevel_fan.append("surface")

            if annotation_huma == annotation_fan:
                exact_match += 1

            if (annotation_huma in content and annotation_fan in content) or (
                    annotation_huma in surface and annotation_fan in surface):
                high_level_match += 1
            else:
                print('\n', row_fan['id'], '\n', row_huma['Aligned Index'], row_huma['Sentence Content'])
                print('Fan:', annotation_fan)
                print('Huma: ', annotation_huma)

    a_huma = np.array(all_huma)
    # print np.unique(a_huma)

    a_fan = np.array(all_fan)
    # print np.unique(a_fan)

    kappa = cohen_kappa_score(all_fan, all_huma)
    kappa_high_level = cohen_kappa_score(all_highlevel_fan, all_highlevel_huma)

    print("\nexact match: ", str(exact_match))
    print("high level match: ", high_level_match)
    print("total: ", total)
    print("exact (%): ", exact_match / (total * 1.0))
    print("high-level (%): ", high_level_match / (total * 1.0))
    print("Kappa exact : ", kappa)
    print("Kappa high-level: ", kappa_high_level)

    print("\n----------------\nPrint confusion matrix:")
    # Compute confusion matrix for all the detailed categories
    class_names = content + surface
    cnf_matrix = confusion_matrix(all_fan, all_huma, labels=class_names)
    np.set_printoptions(precision=2)
    # Plot non-normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names, title='Confusion matrix, without normalization')

    # confusion matrix only for the 2 high level categories
    class_names_highlevel = ['content', 'surface']
    cnf_matrix = confusion_matrix(all_highlevel_fan, all_highlevel_huma, labels=class_names_highlevel)
    np.set_printoptions(precision=2)
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names_highlevel, title='Confusion matrix, without normalization')

    plt.show()


def getStatistics():
    global Annotator1, Annotator2
    omid = False
    tazin = False
    meghan = False
    t_o = True
    t_m = False
    o_m = False
    dataPathGold = "../PracticeDante/HSchool1Gold/"
    if omid:
        dataPathUser = "../PracticeDante/Omid/"
        Annotator2 = 'Omid'
    elif meghan:
        dataPathUser = "../PracticeDante/Meghan/"
        Annotator2 = 'Meghan'
    elif tazin:
        dataPathUser = "../PracticeDante/Tazin/"
        Annotator2 = 'Tazin'
    elif t_o:
        dataPathGold = boxPath + "ArgRewrite NSF 2017/Datasets/ArgRewritePilot2018/Tazin/"
        dataPathUser = boxPath + "ArgRewrite NSF 2017/Datasets/ArgRewritePilot2018/Omid/"
        Annotator1 = 'Tazin'
        Annotator2 = 'Omid'
    elif t_m:
        dataPathGold = boxPath+"ArgRewrite NSF 2017/Datasets/ArgRewritePilot2018/Tazin/"
        dataPathUser = boxPath+"ArgRewrite NSF 2017/Datasets/ArgRewritePilot2018/Meghan/"
        Annotator1 = 'Tazin'
        Annotator2 = 'Meghan'
    elif o_m:
        dataPathGold = boxPath + "ArgRewrite NSF 2017/Datasets/ArgRewritePilot2018/Omid/"
        dataPathUser = boxPath + "ArgRewrite NSF 2017/Datasets/ArgRewritePilot2018/Meghan/"
        Annotator1 = 'Omid'
        Annotator2 = 'Meghan'

    # dataPathFan = "../../Annotations/ESL_annotated_Fan"
    # dataPathHuma = "../../Annotations/ESL_annotated_Huma"


    # 1. read all the excel files of Huma and Fan
    df_gold = readExcelFiles(dataPathGold)
    df_user = readExcelFiles(dataPathUser)

    # 2. find agreements between our annotations
    findAgreements(df_gold, df_user)


if __name__ == "__main__":
    getStatistics()
























