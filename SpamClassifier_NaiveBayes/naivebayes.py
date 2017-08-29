# this function opens a txt file and returns a dict of words and the # of emails in that text file

import math

def opener(filename):
    with open(filename, 'r') as f:
        one = f.read().replace('\n',' ').lower()
        two = one.split('</body>')
    emails = 0

    d = {}
    for email in range(0,len(two)-1):
        newlist = []
        emails += 1
        curr = two[email].split()
        #print (curr)


        for x in range(0, len(curr)):
            if curr[x] not in newlist:
                newlist.append(curr[x])
        #print(newlist)
        for y in range(0, len(newlist)):
            if (newlist[y] not in d):
                d[newlist[y]] = 1
            else:
                d[newlist[y]] += 1

    newdict = {}
    for x in d:
        if not x.startswith('<'):
            newdict[x] = d[x]
    return newdict, emails


def main ():
    correct_spam = 0
    correct_ham = 0
    filename1 = "train-spam.txt"#-small.txt"
    filename2 = "train-ham.txt"#-small.txt"
    filename3 = "test-spam.txt"#-small.txt"
    filename4 = "test-ham.txt"#-small.txt"
    spam, emails1 = opener(filename1)
    ham, emails2 = opener(filename2)

    for x in spam:
        if x not in ham:
            ham[x] = 0

    for x in ham:
        if x not in spam:
            spam[x] = 0

    #print("spam:", spam)
    #print("ham:", ham)
    #print("Number of emails in  ", emails1, " vs ", emails2)

    sums = emails1+emails2
    prior_spam = emails1/sums
    prior_ham = emails2/sums






    #print("\npriors: ", prior_spam, prior_ham)


    testspam , emails_spam = opener(filename3)
    testham, emails_ham = opener(filename4)

    #print("#of email's in testspam", emails_spam)
    #print("#of email's in testham", emails_ham)



    #print("testspam: ", testspam)
    #print("testhamn", testham)


    for i in range(0,emails_spam):

        vocab = {k: spam.get(k, 0) + ham.get(k, 0) for k in set(spam) | set(ham)}
        vocab_size = len(vocab)
        #print("vocab", vocab)
        sum_spam = 0
        occurance_spam = 0
        for x in vocab:
            if (x in testspam):
                #print("occurance of ", x , (spam[x]+1)/(emails1+2))
                sum_spam += math.log((spam[x] + 1) / (emails1 + 2))
                if (spam[x] != 0):
                    occurance_spam += 1
            else:
                #print("occurances of ", x, 1 - (spam[x] + 1) / (emails1 + 2))
                sum_spam +=  math.log(1 - (spam[x] + 1) / (emails1 + 2))
        output1 = sum_spam + math.log(prior_spam)


        sum_ham = 0

        for x in vocab:
            if (x in testham):
               # print("occurance of ", x , (ham[x]+1)/(emails2+2))
                sum_ham += math.log((ham[x] + 1) / (emails2 + 2))


            else:
                #print("occurances of ", x, 1 - (ham[x] + 1) / (emails2 + 2))
                sum_ham += math.log(1 - (ham[x] + 1) / (emails2 + 2))
        output2 = sum_ham + math.log(prior_ham)
        #print("new vocav", vocab)
        #format
        print("Test", i+1, occurance_spam, end='')
        print("/", end='')
        print(vocab_size, "features true ", end='')
        print('%.3f' % output1, "", end='')
        print('%.3f' % output2, end=' ')
        if (output1 > output2):
            print("spam right")
            correct_spam += 1
        else:
            print("spam wrong")

        #print(correct_spam, "/",emails_spam," classified correctly")


######################################################################
    print("testing ham emails!!!!")
    for i in range(0,emails_ham):
        #print("...")
        #print(vocab)
        #print(testham)
        occurance_ham = 0
        sum_spam = 0
        sum_ham = 0
        #print("e1",emails1)
        print(emails2)
        for x in vocab:
            if (x in testham):
                #print("occurance of ", x , (spam[x]+1)/(emails1+2))
                sum_spam += math.log((spam[x] + 1) / (emails1 + 2))
                if (spam[x] != 0):
                    occurance_ham += 1
            else:
                #print("occurances of ", x, 1 - (spam[x] + 1) / (emails1 + 2))
                sum_spam +=  math.log(1 - (spam[x] + 1) / (emails1 + 2))
        output3 = sum_spam + math.log(prior_spam)




        for x in vocab:
            if (x in testham):
                #print("occurance of ", x, (ham[x] + 1) / (emails2 + 2))
                sum_ham += math.log((ham[x] + 1) / (emails2 + 2))


            else:
                # print("occurances of ", x, 1 - (ham[x] + 1) / (emails2 + 2))
                sum_ham += math.log(1 - (ham[x] + 1) / (emails2 + 2))
        output4 = sum_ham + math.log(prior_ham)

        # format
        print("Test", i + 1, occurance_ham, end='')
        print("/", end='')
        print(vocab_size, "features true ", end='')
        print('%.3f' % output3, "", end='')
        print('%.3f' % output4, end=' ')
        if (output3 < output4):
            print("ham right")
            correct_ham += 1
        else:
            print("ham wrong")
        #print(correct_spam, "/", emails_spam, " classified correctly")
    print("Total: ", correct_spam + correct_ham, "/", emails_spam+emails_ham, "emails classified correctly")


main()