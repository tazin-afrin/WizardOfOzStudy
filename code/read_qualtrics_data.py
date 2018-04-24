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
            if row['RecipientEmail'] == email:# or row['Q9'] == name:
                print(row['RecipientFirstName'],row['RecipientLastName'],row['RecipientEmail'])
                # this is the answer for step 2 to check if participants read the provided material
                print(row['Q38'])

                # save_draft(cond + outputfile, row['Q8'])

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

        for row in data:
            if row['RecipientEmail'] == email:
                print(row['RecipientFirstName'],row['RecipientLastName'],row['RecipientEmail'])
                # this is the answer for step 2 to check if participants read the provided material
                essay = row['Q5']

                save_draft(cond + outputfile, essay)
                break


if __name__ == '__main__':

    draft = '1'
    print(draft)
    email = 'chl243@pitt.edu'
    # email = '@gmail.com'
    cond = filesConfig.essayRev12
    outputfile = 'draft2_2018argrewrite_#.txt'

    if draft == '1':
        read_draft1(filesConfig.draft1_file)
    elif draft == '2':
        read_draft2(filesConfig.draft2_file)