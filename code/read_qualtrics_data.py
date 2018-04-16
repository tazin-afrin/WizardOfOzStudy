from config import filesConfig
import csv, re


def save_draft(filename, essay):
    text_file = open(filename, "w")
    text_file.write(essay)
    text_file.close()


def read_draft1(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        fields = reader.fieldnames

        for row in data:
            if row['RecipientFirstName'] == name:
                print(row['RecipientFirstName'],row['RecipientLastName'],row['RecipientEmail'])
                # this is the answer for step 2 to check if participants read the provided material
                print(row['Q38'])

                save_draft(cond + outputfile, row['Q8'])

                print('\n\n')
                # essay = row['Q8'].split("\n")
                essay = re.split('\n{1,}',row['Q8'])

                for i in range(len(essay)):
                    id = 'FirstDraftParagraph'+str(i+1)+','
                    print(id+essay[i])
                    print('\n')


def read_draft2(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        fields = reader.fieldnames
        print(fields)

if __name__ == '__main__':

    draft = 2
    name = '-'
    cond = filesConfig.condB
    outputfile = 'draft1_2018argrewrite_2.txt'

    if draft == 1:
        read_draft1(filesConfig.draft1_file)
    else:
        read_draft2(filesConfig.draft2_file)