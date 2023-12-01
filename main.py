
import os
import subprocess
import platform
from PyPDF2 import PdfReader
from openai import OpenAI
import tkinter as tk
from tkinter import filedialog
import datefinder
from dateutil.relativedelta import relativedelta

client = OpenAI(api_key='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')

#############################################################################################
# Function for using LLM to parse an excerpt of the OA using a question
#############################################################################################
def askLLM(question, excerpt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages =[{"role": "system","content": "Your task is to parse the following of an office action issued by the US Patent Office and answer questions about it:"+excerpt},
                   {"role": "user", "content": question}],
        temperature=0.0
    )

    return completion.choices[0].message.content

#############################################################################################
# Function for extracting an excerpt of the OA that includes a keyword
#############################################################################################
def getExcerpt(reader, keyword, startPage):
   ##### probably should expand the pages that are included in the excerpt to include the pages before+after the hit####
    numPages = len(reader.pages)
    excerpt = ""
    for i in range(startPage, numPages):
        if (reader.pages[i].extract_text().find(keyword) > -1):
            excerpt += reader.pages[i].extract_text()
    return excerpt

#############################################################################################
# Function for getting a yes or no answer to a question using LLM
#############################################################################################
def yesNoParser(reader, keyword, question, startPage):
    excerpt = getExcerpt(reader, keyword, startPage)

    if excerpt == "":
        return False
    else:
        answer = askLLM(question, excerpt)

        if (answer.lower().find("yes") > -1):
            return True
        else:
            return False

#############################################################################################
# Function for asking LLM to find the pending claims
#############################################################################################
def getPendingClaims(reader):

    excerpt = getExcerpt(reader, "pending",1)

    answer = askLLM("What are the pending claims in the application? Answer in the following form: Claims *** are pending in this application.", excerpt)
    return answer

#############################################################################################
# Function for asking LLM to find claims rejected under 35 USC 102
#############################################################################################
def get102Claims(reader):
    excerpt = getExcerpt(reader, "102",3)
    answer = askLLM("What is the list of claims rejected under 35 USC 102? Answer in list form without any additional text and do not proceed the list with the word claims", excerpt)
    return answer

#############################################################################################
# Function for asking LLM to find references used in 35 USC 102 rejection
#############################################################################################
def get102Refs(reader):
    excerpt = getExcerpt(reader, "102",3)
    answer = askLLM("What is the name and reference number of the prior art reference cited in the 35 USC 102 rejection? Answer in the following form without any additional text: name (reference number)", excerpt)
    return answer

#############################################################################################
# Function for asking LLM to find claims rejected under 35 USC 103
#############################################################################################
def get103Refs(reader):
    excerpt = getExcerpt(reader, "103",3)
    answer = askLLM("What is the name and reference number of the prior art references cited in the 35 USC 103 rejection? Answer in the following form without any additional text: Independent claim 1 is rejected as being unpatentable over [prior art reference 1] in view of [prior art reference 2].", excerpt)
    return answer

#############################################################################################
# Function for asking LLM to determine whether OA is final
#############################################################################################
def isFinal(reader):
    excerpt = getExcerpt(reader, 'final', 3)
    answer = askLLM("Is the office action a final office action? Constrain your answer to either: yes or no", excerpt)

    if (answer.lower().find("yes") > -1):
        return True
    else:
        return False

#############################################################################################
# Function for asking LLM to find resposne deadline
#############################################################################################
def getResponseDeadline(reader):
    excerpt = getExcerpt(reader, 'NOTIFICATION', 0)
    answer = askLLM(
        "What is the notification date? Provide only the date and constrain your answer to the following format: Month Day, Year",excerpt)

    dates=list(datefinder.find_dates(answer))
    responseDeadline = dates[0]+relativedelta(months=3)
    return responseDeadline.strftime("%B %d, %Y")

#############################################################################################
# Function for asking LLM to find early response deadline
#############################################################################################
def getEarlyReplyDeadline(deadline, reader):
    excerpt = getExcerpt(reader, 'NOTIFICATION', 0)
    answer = askLLM(
        "What is the notification date? Provide only the date and constrain your answer to the following format: Month Day, Year",
        excerpt)

    dates = list(datefinder.find_dates(answer))
    responseDeadline = dates[0] + relativedelta(months=2)
    return responseDeadline.strftime("%B %d, %Y")


#############################################################################################
# Main function
#############################################################################################
if __name__ == '__main__':

    # get path to OA .pdf
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    # make reader object for OA
    reader = PdfReader(file_path)

    # determine whether OA is final
    finality = isFinal(reader)

    # get initial response deadline
    initialDeadline = getResponseDeadline(reader)

    # is there a double patenting rejection?
    dblPatRejection = yesNoParser(reader,"double patent","Is there a double patenting rejection in the excerpt?", 2)
    print("Double Patenting? ", dblPatRejection)

    # are there claim objections?
    clObjection = yesNoParser(reader,"objection","Is there an objection to any claims in the excerpt?", 2)
    print("Claim Objections? ", clObjection)

    # are there drawing objections?
    drawingObjection = yesNoParser(reader, "drawings", "Is there an objection to the drawings in the excerpt?",2)
    print("Drawing Objections? ", drawingObjection)

    # is there an objection to the specification?
    specObjection = yesNoParser(reader, "specification", "Is there an objection to the specification in the excerpt?", 2)
    print("Specification Objections? ", specObjection)

    # is there an abstract idea objection?
    abstRejection = yesNoParser(reader,"101","Is there a rejection of any claims under 35 USC 101 in the excerpt?", 2)
    print("101? ", abstRejection)

    # is there a 35 USC 112 rejection?
    oneTwelveRej = yesNoParser(reader, "112","Are there any 35 USC 112 issues in the excerpt?", 2)
    print("112? ", oneTwelveRej)

    # is there a 35 USC 102 rejection?
    antRejection = yesNoParser(reader, "102","Is there a rejection of claim 1 under 35 USC 102 in the excerpt?", 2)
    print("102? ", antRejection)

    # is there a 35 USC 103 rejection?
    obvRejection = yesNoParser(reader, "103","Is there a rejection of claim 1 under 35 USC 103 in the excerpt?",2)
    print("103? ", obvRejection)

    # are there any allowed claims?
    allowed = yesNoParser(reader,"allow", "Are any claims allowed or allowable in the excerpt?", 0)


##########################
# Construct Paragraph 1
##########################
print("Constructing Paragraph 1")

if(finality):
    oaType="Final"
else:
    oaType="Non-Final"

paragraphOneFinal = "Enclosed is a copy of a "+oaType+" Office Action which we recently received from the United States Patent and Trademark Office in connection with the above-identified patent application. We also enclose copies of the pending claims and the references cited by the Examiner."

##########################
# Construct Paragraph 2
##########################
print("Constructing Paragraph 2")
pendingClaims = getPendingClaims(reader)

paragraphTwoFinal=""
if(not(allowed)):
    if (antRejection and not obvRejection):
     antRefs = get102Refs(reader)
     paragraphTwoFinal = pendingClaims + " The Examiner has rejected the independent claims as being anticipated by "+antRefs+"."

    if (obvRejection and not antRejection):
     obvRefs = get103Refs(reader)
     paragraphTwoFinal = pendingClaims+" " + obvRefs

    if (obvRejection and antRejection):
        paragraphTwoFinal = "THE PRIOR ART REJECTION IS COMPLICATED--NEEDS ATTORNEY REVIEW"
else:
    paragraphTwoFinal = "THERE ARE ALLOWED CLAIMS--NEEDS ATTORNEY REVIEW"


##########################
# Construct Paragraph 3
##########################
print("Constructing Paragraph 3")
paragraphThreeFinal = ""

# jump through hoops to make this paragraph look nice.
if (dblPatRejection or clObjection or drawingObjection or specObjection or abstRejection or oneTwelveRej):
    count = 0
    paragraphThree = "The Examiner has also "
    if(drawingObjection):
        paragraphThree+= "objected to the drawings"
        count+=1

    if(specObjection):
        if (count>0):
            paragraphThree+=", "
        paragraphThree+= "objected to the specification"
        count += 1

    if(clObjection):
        if (count>0):
            paragraphThree+=", "
        paragraphThree+= "objected to certain claims"
        count += 1

    if(abstRejection):
        if (count>0):
            paragraphThree+=", "
        paragraphThree+= "rejected certain claims as being directed to non-statutory subject matter"
        count += 1

    if(oneTwelveRej):
        if (count>0):
            paragraphThree+=", "
        paragraphThree+= "raised issues under 35 USC 112"
        count += 1

    paragraphThree+= ". We believe we can address these issues without requiring input from you or the inventors."

    # more hoops to deal with the ", and" before the last part of the sentence.
    lastCommaIdx = paragraphThree.rfind(",")
    paragraphThreeFinal=""
    if(lastCommaIdx > -1):
        if (count == 2):
            paragraphThreeFinal = paragraphThree[:lastCommaIdx] + " and" + paragraphThree[lastCommaIdx+1:]
        else:
            paragraphThreeFinal = paragraphThree[:lastCommaIdx+1] + " and" + paragraphThree[lastCommaIdx+1:]
    else:
        paragraphThreeFinal=paragraphThree


################################
#Construct Paragraph 4
################################
print("Constructing Paragraph 4")
paragraphFourFinal="We have not reviewed the office action in any detail. Rather, we thought that you would prefer to review the office action first and then provide us with your comments. Of course, if you would like us to review the office action and provide you with a response strategy, we are happy to do so."

################################
#Construct Paragraph 5
################################
print("Constructing Paragraph 5")
paragraphFiveFinal = ""

# Deadline differs based on finality of office action
if(finality):
    earlyDeadline=getEarlyReplyDeadline(initialDeadline, reader)
    paragraphFiveFinal = "The initial deadline for responding to the office action is "+initialDeadline+" and is extendible up to three months. However, since the Examiner has made this action final, it is strongly recommended that a response be filed as soon as possible and by "+earlyDeadline+" to minimize the possibility of having to refile, appeal, or request continued examination of the application."
else:
    paragraphFiveFinal="The initial deadline for responding to the office action is "+initialDeadline+ ". Three, one-month extensions of that deadline may be obtained automatically upon payment of the required fee with the response. To avoid paying additional fees, kindly provide us with instructions as to how to proceed in a timely manner."

################################
# Write to .txt file
################################
with open('report.txt', 'w') as f:
    f.write(paragraphOneFinal)
    f.write('\n\n')
    f.write(paragraphTwoFinal)
    f.write('\n\n')
    if(paragraphThreeFinal != ""):
        f.write(paragraphThreeFinal)
        f.write('\n\n')
    f.write(paragraphFourFinal)
    f.write('\n\n')
    f.write(paragraphFiveFinal)
    f.write('\n\n')
    f.write("Sincerely,")

if platform.system() == 'Darwin':  # macOS
    subprocess.call(('open', 'report.txt'))
elif platform.system() == 'Windows':  # Windows
    os.startfile('report.txt')
else:  # linux variants
    subprocess.call(('xdg-open', 'report.txt'))






