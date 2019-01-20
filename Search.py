import os
import re
from tkinter import *
import io
from contextlib import redirect_stdout
import logging
import inspect
import time
from tkinter import messagebox
from time import gmtime, strftime
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


################## Functions#####################
########## TopleftFrame RadioButton Function###########
def GetRadioButton():

    selection = Radio_Var.get()
    #print(selection)
    return selection

def Getcheckbutton1():

    selection = Radio_Var1.get()
    #print(selection)
    return selection

def Getcheckbutton2():

    selection = Radio_Var2.get()
    #print(selection)
    return selection
########### TopMiddle1 ListBox Functions ##############
def change_dropdown(*args):
    # print(tkvar.get())
    return tkvar.get()

def labelchange_with_optionmenu(choices):
    option = choices
    if option == "Function Definition":
        text_var.set("Enter keyword(s) separated by a comma (1 to 3 words)")
    if option == "Object Names":
        text_var.set("Enter keyword(s) separated by a comma (1 to 3 words)")
    if option == "Search Anything":
        text_var.set("Enter any string")




########### TopRight Entry Box Functions ############

def fileLogger(loglevel=logging.INFO):
    loggerName = inspect.stack()[1][3]  # imp- Need to study INSPECT MODULE
    myfLogger = logging.getLogger(loggerName)
    myfLogger.setLevel(logging.INFO)

    fHandler = logging.FileHandler(filename='mylogger.log',mode='w')
    fHandler.setLevel(loglevel)

    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

    fHandler.setFormatter(formatter)

    myfLogger.addHandler(fHandler)

    return myfLogger

def readLogger():
    with open("mylogger.log",'r') as logfile:
        for logs in logfile.readline():
            OutPutField1.insert(0.0,logs)

def GetSearchWords():
    # print(Entry1.get())
    return Entry1.get()

def testsearch():
    selection=Radio_Var.get()
    # print(selection)
    # print(tkvar.get())
    # print(Entry1.get())
    Entry1.delete(0,END)

def keywordlenghtcheck(SearchKeywords):
    if SearchKeywords == "":
        return 0
    SearchKeywordsLower=SearchKeywords.lower()
    SearchKeywordsSplit=SearchKeywordsLower.split(",")
    SearchKeywordsSplit_length = len(SearchKeywordsSplit)
    return SearchKeywordsSplit_length


def WordInLine(line,SearchKeywords):
    LineLower=line.lower()
    LineSplit=LineLower.split(" ")
    SearchKeywordsLower=SearchKeywords.lower()
    SearchKeywordsSplit=SearchKeywordsLower.split(",")
    inc_button_value = Getcheckbutton1()
    t_button_value = Getcheckbutton2()

    if len(SearchKeywordsSplit) > 3:

        # messagebox.askokcancel("Warning!", "You cannot enter more than 3 words!!!")
        # Window.destroy()

        return "exceeded 3"
    elif len(SearchKeywordsSplit) <= 3 or len(SearchKeywordsSplit) >= 1:
        if len(SearchKeywordsSplit) == 3:
            for word in LineSplit:
                if SearchKeywordsSplit[0] in word and (SearchKeywordsSplit[1] in word and SearchKeywordsSplit[2] in word):
                    return word
        elif len(SearchKeywordsSplit) == 2:
            for word in LineSplit:
                if SearchKeywordsSplit[0] in word and SearchKeywordsSplit[1] in word:
                    return word
        elif len(SearchKeywordsSplit) == 1:
            for word in LineSplit:
                if SearchKeywordsSplit[0] in word:
                    return word
    elif len(SearchKeywordsSplit) or len(LineLower) == 0:
        return "Zero Input"

def WordInLine2(line,SearchKeywords):
    LineLower=line.lower()
    LineSplit=LineLower.split(" ")
    SearchKeywordsLower=SearchKeywords.lower()
    SearchKeywordsSplit=SearchKeywordsLower.split(",")
    inc_button_value = Getcheckbutton1()
    t_button_value = Getcheckbutton2()

    if len(SearchKeywordsSplit) > 3:

        # messagebox.askokcancel("Warning!", "You cannot enter more than 3 words!!!")
        # Window.destroy()

        return "exceeded 3"
    elif len(SearchKeywordsSplit) <= 3 or len(SearchKeywordsSplit) >= 1:
        if len(SearchKeywordsSplit) == 3:
            for word in LineSplit:
                if SearchKeywordsSplit[0] in word and (SearchKeywordsSplit[1] in word and SearchKeywordsSplit[2] in word):
                    if "(" in word:
                        word_split= word.split("(")
                        first_word=word_split[0]
                        if first_word in word:
                            return first_word
                    else:
                        return word
        elif len(SearchKeywordsSplit) == 2:
            for word in LineSplit:
                if SearchKeywordsSplit[0] in word and SearchKeywordsSplit[1] in word:
                    return word
        elif len(SearchKeywordsSplit) == 1:
            for word in LineSplit:
                if SearchKeywordsSplit[0] in word:
                    return word
    elif len(SearchKeywordsSplit) or len(LineLower) == 0:
        return "Zero Input"
def CommentCheck(line,x):
    commentcatch = '//'
    word = WordInLine(line, x)
    if word != "exceeded 3" and word != None:
        linelower = line.lower()
        if commentcatch in line:
            commentposition=line.find(commentcatch)
            wordposition=linelower.find(word)
            if wordposition < commentposition:
                return "CommentAfterWord"
            else:
                return "CommentBeforeWord"
        else:
            return "NoComments"

def object_catch (line,word):
    if CommentCheck(line,word) != "CommentBeforeWord":
        if CommentCheck(line,word) == "CommentAfterWord":
            line_split_comment=line.split("//")
            first_part=line_split_comment[1]
            first_part_split = first_part.split(" ")
            if len(first_part_split) <= 4:
                return "Object"
        if CommentCheck(line,word) == "NoComments":
            line_split = line.split(" ")
            if len(line_split) <= 4:
                return "Object"
    else:
        return "Not Object"

def FunctionDefCheck(line,SearchKeywords):
    commentcatch = CommentCheck(line,SearchKeywords)
    if commentcatch != "CommentBeforeWord" and commentcatch != None:
        if "[+]" in line or "[-]" in line:
            linesplitoncomment = line.split("//")
            functionpart=linesplitoncomment[0]
            if "(" in functionpart and ")" in functionpart:
                return functionpart



def returnfileType(searchoption):
    if searchoption== "Function Definition (.inc)":
        filetype = ".inc"
        return filetype

    if searchoption == 'Function Definition (.t)':
        filetype = ".t"
        return filetype

    if searchoption == 'Function Usage(.t)':
        filetype= ".t"
        return filetype

    if searchoption == 'Object Names(.inc)':
        filetype= ".inc"
        return filetype

    if searchoption == 'Object Names (.t)':
        filetype= ".t"
        return filetype

    if searchoption == 'Class Names(.inc)':
        filetype= ".inc"
        return filetype

################ Writing to google sheet ########################
def write2GoogleSheet(Keyword,SearchType,SearchesRetrieved,TimeTakenForSearch):

    # Row values to be updated in a list
    googleSheetList = []

    # Getting the computer name
    computerName = os.environ['COMPUTERNAME']

    # Getting the IP address of the machine
    userName = os.getlogin()

    # Getting system date and time
    cTime=strftime("%Y/%m/%d - %H:%M")

    # Getting Month and Year to update the correct google sheet and month sheet
    now = datetime.datetime.now()
    cYear = now.year   # class int
    cMonth = now.month  # class int

    monthName = datetime.date(1900, cMonth, 1).strftime('%B')  # String returns the name of month.

    # Getting the OS version
    import platform
    osName = platform.system() + platform.release()

    # Getting the machine IP
    import socket
    mIP = socket.gethostbyname(socket.gethostname())

    # Deatails to be updated to google sheet regarding every search.
    googleSheetList = ['{}'.format(userName),"{}".format(computerName),'{}'.format(mIP),'{}'.format(osName),'{}'.format(cTime),'{}'.format(Keyword),'{}'.format(SearchType),'{}'.format(SearchesRetrieved),'{}'.format(TimeTakenForSearch)]


    # Accessing Goole Yearly sheet, and then monthly sheet to update the search details.

    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('QuickSearchTry-9b12de4cf728.json', scope)
        client = gspread.authorize(creds)

        GS_Year = '{}'.format(cYear)

        #sheet = client.open('{}'.format(GS_Year)).sheet7
        sheet = client.open('2018_').sheet1

        index=2
        sheet.insert_row(googleSheetList,index)
    except:
        pass



# Main Backend Function for QAP Search and Domain Search
def QAPorDplan():

    wait.config(text='Searching..')
    wait.update_idletasks()


    OutPutField1.delete(0.0,'end')
    OutPutField2.delete(0.0,'end')
    total_time_taken_display.delete(0.0,"end")
    total_files_searched_display.delete(0.0,'end')
    last_search_kw_display.delete(0.0,'end')
    total_Search_results_display.delete(0.0,'end')


    # buffer = io.StringIO()
    # log = fileLogger()
    # Assigning Search options to variables
    # RadioButton
    SearchForQAPorDplan =1 #Radio_Var.get()#***Imp***# Add it back when the radio buttons are enabled
    if SearchForQAPorDplan != 1:
        if SearchForQAPorDplan !=2:
            SearchForQAPorDplan=1
    # DropDown
    SearchOption = tkvar.get()

    # Checkbutton values
    inc_button_value= Getcheckbutton1()
    t_buton_value=Getcheckbutton2()

    SearchKeyWord= GetSearchWords()
    # OutPutField1.insert(0.0,SearchKeyWord)

    if SearchForQAPorDplan == 1:
        start_time = time.time()
        rootDir = 'C:\QAP'
        File_Number = 0
        SearchNumber = 0
        File_Number_silkscripts=0
        File_Number_silkframe=0
        Total_FN=0
        for dirName, subdirList, fileList in os.walk(rootDir, topdown=True):
            ########## IF key word lenght is more than 3 -Start ##############
            if keywordlenghtcheck(SearchKeyWord) > 3:
                if inc_button_value == 3:
                    OutPutField1.insert(0.0, "Warning! More than 3 keywords are not allowed")
                    break
                if t_buton_value == 4:
                    OutPutField2.insert(0.0, "Warning! More than 3 keywords are not allowed")
                    break
            ########## IF key word length is 0 -Start ##############
            if keywordlenghtcheck(SearchKeyWord) == 0:
                if SearchOption == "Function Definition" or SearchOption == "Object Names":
                    if inc_button_value == 3 and t_buton_value ==0:
                        OutPutField1.insert(0.0, "Warning! Please enter a keyword")
                        break
                    if t_buton_value == 4 and inc_button_value == 0:
                        OutPutField2.insert(0.0, "Warning! Please enter a keyword")
                        break
                    if inc_button_value == 3 and t_buton_value == 4:
                        OutPutField1.insert(0.0, "Warning! Please enter a keyword")
                        OutPutField2.insert(0.0, "Warning! Please enter a keyword")
                        break
                if SearchOption == "Search Anything":
                    if inc_button_value == 3 and t_buton_value ==0:
                        OutPutField1.insert(0.0, "Warning! Please enter a String")
                        break
                    if t_buton_value == 4 and inc_button_value == 0:
                        OutPutField2.insert(0.0, "Warning! Please enter a String")
                        break
                    if inc_button_value == 3 and t_buton_value == 4:
                        OutPutField1.insert(0.0, "Warning! Please enter a String")
                        OutPutField2.insert(0.0, "Warning! Please enter a String")
                        break





            ########## IF key word lenght is more than 3 - End ##############

            if dirName == "C:\QAP\silkscripts" or dirName == "C:\QAP\silkframe":
                rootDir = dirName
                dirName_FN=dirName
                for dirName, subdirList, fileList in os.walk(rootDir, topdown=True):
                    for fname in fileList:
                         file_path = dirName + "\{}".format(fname)
                         file_path1=r"{}".format(file_path)
                         filetype=returnfileType(SearchOption)


                         ########### Code for Searching Functions (.inc only) ############
                         if SearchOption == "Function Definition" and inc_button_value ==3 and t_buton_value==0:
                             if fname.endswith(".inc"):
                                 try:
                                     with open(r"{}".format(file_path1), 'r', encoding='utf-8', errors='ignore')as file:
                                         File_Number = File_Number + 1
                                         i = 0
                                         for line in file.readlines():
                                             linel = line.lower()
                                             i = i + 1
                                             try:

                                                 FunctionName = WordInLine(line, SearchKeyWord)
                                                 commentCheck = CommentCheck(line, FunctionName)

                                                 if FunctionName is not None and commentCheck != "CommentBeforeWord" and FunctionName != "exceeded 3" :
                                                     if ('[+]' in line or "[-]" in line) and (
                                                             "(" in line and ')' in line) and (
                                                             "." not in line and " if" not in linel and "if " not in linel and ' else ' not in linel and " while " not in linel and " while" not in linel and ' for ' not in linel and ' for' not in linel and ' switch ' not in linel and " switch" not in linel and ' case ' not in linel and ' case'not in linel)  and " tag " not in linel and " multitag " not in linel and ' testcase ' not in linel and " appstate " not in linel and "=" not in linel:
                                                         # log.info("{} in line {} in file {}".format(line, i, file_path))
                                                         outputline = "\r {} in line {} in file {}\n\n".format(line, i,
                                                                                                               file_path)

                                                         linel_split = linel.split("(")
                                                         First_Half = linel_split[0]
                                                         Actual_Function = WordInLine2(First_Half, SearchKeyWord)

                                                         if Actual_Function is not None:
                                                             outputline = "\r {} in line {} in file {}\n\n".format(line,
                                                                                                                   i,
                                                                                                                   file_path)
                                                             outputline = outputline.lstrip()

                                                             outputline = outputline.lstrip()


                                                             OutPutField1.insert(0.0, outputline)
                                                             SearchNumber = SearchNumber + 1

                                             except:
                                                 pass

                                 except:
                                     # print("\t\tCould not open the file {}".format(file_path1))
                                     pass

                         ########### Code for Searching Objects in .inc files  ##############
                         if SearchOption == 'Object Names' and inc_button_value==3 and t_buton_value==0:
                             if fname.endswith(".inc"):
                                 try:
                                     with open(r"{}".format(file_path1), 'r', encoding='utf-8',
                                               errors='ignore')as file:
                                         File_Number = File_Number + 1
                                         i = 0
                                         for line in file.readlines():
                                             linel = line.lower()
                                             i = i + 1
                                             try:

                                                 ObjectName = WordInLine(line, SearchKeyWord)
                                                 commentCheck = CommentCheck(line, ObjectName)

                                                 if ObjectName is not None and ObjectName != "exceeded 3" and commentCheck != "CommentBeforeWord" and object_catch(line,SearchKeyWord) == "Object":
                                                     if ('[+]' in line or "[-]" in line) and (
                                                             "(" not in line and ')' not in line) and "." not in line  and (
                                                             "tag" not in linel) and " if" not in linel and " if " not in linel and ' else ' not in linel and " while " not in linel and ' for ' not in linel and ' case ' not in linel and ' switch ' not in linel and ' testcase' not in linel and ' appstate' not in linel and "with " not in linel:
                                                         # log.info("{} in line {} in file {}".format(line, i, file_path))
                                                         outputline = "\r {} in line {} in file {}\n\n".format(line,
                                                                                                               i,
                                                                                                               file_path)
                                                         outputline = outputline.lstrip()
                                                         OutPutField1.insert(0.0, outputline)
                                                         SearchNumber = SearchNumber + 1

                                             except:
                                                 pass

                                 except:
                                     # print("\t\tCould not open the file {}".format(file_path1))
                                     pass

                         ########### Code for Searching functions in .t fiels ##########
                         if SearchOption == "Function Definition" and inc_button_value ==0 and t_buton_value==4:
                             if fname.endswith(".t"):
                                 try:
                                     with open(r"{}".format(file_path1), 'r', encoding='utf-8', errors='ignore')as file:
                                         File_Number = File_Number + 1
                                         i = 0
                                         for line in file.readlines():
                                             linel = line.lower()
                                             i = i + 1
                                             try:

                                                 FunctionName = WordInLine(line, SearchKeyWord)
                                                 commentCheck = CommentCheck(line, FunctionName)

                                                 if FunctionName is not None and commentCheck != "CommentBeforeWord" and FunctionName != "exceeded 3" :
                                                     if ('[+]' in line or "[-]" in line) and (
                                                             "(" in line and ')' in line) and (
                                                             "." not in line and " if" not in linel and "if " not in linel and ' else ' not in linel and " while " not in linel and " while" not in linel and ' for ' not in linel and ' for' not in linel and ' switch ' not in linel and " switch" not in linel and ' case ' not in linel and ' case'not in linel)  and " tag " not in linel and " multitag " not in linel and ' testcase ' not in linel and " appstate " not in linel and "=" not in linel:
                                                         # log.info("{} in line {} in file {}".format(line, i, file_path))
                                                         outputline = "\r {} in line {} in file {}\n\n".format(line, i,
                                                                                                               file_path)
                                                         linel_split = linel.split("(")
                                                         First_Half = linel_split[0]
                                                         Actual_Function = WordInLine2(First_Half, SearchKeyWord)

                                                         if Actual_Function is not None:
                                                             outputline = "\r {} in line {} in file {}\n\n".format(line,
                                                                                                                   i,
                                                                                                                   file_path)
                                                             outputline = outputline.lstrip()

                                                             OutPutField2.insert(0.0, outputline)
                                                             SearchNumber = SearchNumber + 1

                                             except:
                                                 pass

                                 except:
                                     # print("\t\tCould not open the file {}".format(file_path1))
                                     pass

                         ########## Code for searching objects in . t files ############
                         if SearchOption == 'Object Names' and inc_button_value==0 and t_buton_value==4:
                             if fname.endswith(".t"):
                                 try:
                                     with open(r"{}".format(file_path1), 'r', encoding='utf-8',
                                               errors='ignore')as file:
                                         File_Number = File_Number + 1
                                         i = 0
                                         for line in file.readlines():
                                             linel = line.lower()
                                             i = i + 1
                                             try:

                                                 ObjectName = WordInLine(line, SearchKeyWord)
                                                 commentCheck = CommentCheck(line, ObjectName)

                                                 if ObjectName is not None and ObjectName != "exceeded 3" and commentCheck != "CommentBeforeWord"  and object_catch(line,SearchKeyWord) == "Object":
                                                     if ('[+]' in line or "[-]" in line) and (
                                                             "(" not in line and ')' not in line) and "." not in line  and (
                                                             "tag" not in linel) and " if" not in linel and " if " not in linel and ' else ' not in linel and " while " not in linel and ' for ' not in linel and ' case ' not in linel and ' switch ' not in linel and ' testcase' not in linel and ' appstate' not in linel and 'with ' not in linel:
                                                         # log.info("{} in line {} in file {}".format(line, i, file_path))
                                                         outputline = "\r {} in line {} in file {}\n\n".format(line,
                                                                                                               i,
                                                                                                               file_path)
                                                         outputline = outputline.lstrip()
                                                         OutPutField2.insert(0.0, outputline)
                                                         SearchNumber = SearchNumber + 1

                                             except:
                                                 pass

                                 except:
                                     # print("\t\tCould not open the file {}".format(file_path1))
                                     pass
                         ########### Object Search in .t and .inc files #############
                         if SearchOption == 'Object Names' and inc_button_value==3 and t_buton_value==4:
                             if fname.endswith(".t") or fname.endswith(".inc"):
                                 try:
                                     with open(r"{}".format(file_path1), 'r', encoding='utf-8',
                                               errors='ignore')as file:
                                         File_Number = File_Number + 1
                                         i = 0
                                         for line in file.readlines():
                                             linel = line.lower()
                                             i = i + 1
                                             try:

                                                 ObjectName = WordInLine(line, SearchKeyWord)
                                                 commentCheck = CommentCheck(line, ObjectName)

                                                 if ObjectName is not None and ObjectName != "exceeded 3" and commentCheck != "CommentBeforeWord"  and object_catch(line,SearchKeyWord) == "Object":
                                                     if ('[+]' in line or "[-]" in line) and (
                                                             "(" not in line and ')' not in line) and "." not in line  and (
                                                             "tag" not in linel) and " if" not in linel and " if " not in linel and ' else ' not in linel and " while " not in linel and ' for ' not in linel and ' case ' not in linel and ' switch ' not in linel and ' testcase' not in linel and ' appstate' not in linel and "with " not in linel:
                                                         # log.info("{} in line {} in file {}".format(line, i, file_path))
                                                         outputline = "\r {} in line {} in file {}\n\n".format(line,
                                                                                                               i,
                                                                                                               file_path)
                                                         outputline = outputline.lstrip()
                                                         if inc_button_value == 3:
                                                             if fname.endswith(".inc"):
                                                                 OutPutField1.insert(0.0, outputline)
                                                                 SearchNumber = SearchNumber + 1
                                                         if t_buton_value == 4:
                                                             if fname.endswith(".t"):
                                                                 OutPutField2.insert(0.0, outputline)
                                                                 SearchNumber = SearchNumber + 1


                                             except:
                                                 pass

                                 except:
                                     # print("\t\tCould not open the file {}".format(file_path1))
                                     pass

                         ########### Function Search in .t and .inc files ###########
                         if SearchOption == "Function Definition" and inc_button_value == 3 and t_buton_value==4:
                             if fname.endswith(".t") or fname.endswith(".inc"):
                                 try:
                                     with open(r"{}".format(file_path1), 'r', encoding='utf-8', errors='ignore')as file:
                                         File_Number = File_Number + 1
                                         i = 0
                                         for line in file.readlines():
                                             linel = line.lower()
                                             i = i + 1
                                             try:
                                                 FunctionName = WordInLine2(linel,SearchKeyWord)
                                                 commentCheck = CommentCheck(line, FunctionName)

                                                 if FunctionName is not None and commentCheck != "CommentBeforeWord" and FunctionName != "exceeded 3" :
                                                     if ('[+]' in linel or "[-]" in linel) and (
                                                             "(" in linel and ')' in linel) and (
                                                             "." not in linel and " if" not in linel and "if " not in linel and ' else ' not in linel and " while " not in linel and " while" not in linel and ' for ' not in linel and ' for' not in linel and ' switch ' not in linel and " switch" not in linel and ' case ' not in linel and ' case'not in linel)  and " tag " not in linel and " multitag " not in linel and ' testcase ' not in linel and " appstate " not in linel and "=" not in linel:
                                                         # log.info("{} in line {} in file {}".format(line, i, file_path))
                                                         #bracket_Catch = re.search(r'\((.*?)\)', linel).group(1)

                                                         linel_split = linel.split("(")
                                                         First_Half = linel_split[0]
                                                         Actual_Function = WordInLine2(First_Half,SearchKeyWord)

                                                         if Actual_Function is not None:

                                                            outputline = "\r {} in line {} in file {}\n\n".format(line, i,
                                                                                                               file_path)
                                                            outputline = outputline.lstrip()

                                                            if inc_button_value == 3:
                                                                if fname.endswith(".inc"):
                                                                    OutPutField1.insert(0.0, outputline)
                                                                    SearchNumber = SearchNumber + 1
                                                            if t_buton_value == 4:
                                                                if fname.endswith(".t"):
                                                                    OutPutField2.insert(0.0, outputline)
                                                                    SearchNumber = SearchNumber + 1



                                             except:
                                                 pass

                                 except:
                                     # print("\t\tCould not open the file {}".format(file_path1))
                                     pass

                         ############## Code for General Search (.t & inc ) ########
                         if SearchOption == "Search Anything":
                             if fname.endswith(".t") or fname.endswith(".inc"):
                                 try:
                                     with open(r"{}".format(file_path1), 'r', encoding='utf-8', errors='ignore')as file:
                                         File_Number = File_Number + 1
                                         i = 0
                                         for line in file.readlines():
                                             i = i + 1
                                             try:
                                                 #Anysearch = WordInLine(line,SearchKeyWord)
                                                 Anysearch = SearchKeyWord.lower()


                                                 if Anysearch in line.lower():


                                                     # log.info("{} in line {} in file {}".format(line, i, file_path))
                                                     outputline = "\r {} in line {} in file {}\n\n".format(Anysearch, i,
                                                                                                           file_path)
                                                     outputline = outputline.lstrip()
                                                     if inc_button_value == 3:
                                                         if fname.endswith(".inc"):
                                                             OutPutField1.insert(0.0, outputline)
                                                             SearchNumber = SearchNumber + 1
                                                     if t_buton_value == 4:
                                                         if fname.endswith(".t"):
                                                             OutPutField2.insert(0.0, outputline)
                                                             SearchNumber = SearchNumber + 1


                                             except:
                                                 pass

                                 except:
                                     # print("\t\tCould not open the file {}".format(file_path1))
                                     pass

                    if dirName_FN=="C:\QAP\silkscripts":
                        File_Number_silkscripts=File_Number
                    if dirName_FN=="C:\QAP\silkframe":
                        File_Number_silkframe=File_Number



                # print("\tTotal Files Opened under {} are {}".format(rootDir,File_Number),"##############"*5 )
            Total_FN=File_Number_silkscripts+File_Number_silkframe
        # print(Total_FN)
        total_files_searched_display.insert(0.0,Total_FN)
        Entry1.delete(0, END)
        end_time = time.time()
        total_time = end_time-start_time
        total_time2= round(int(total_time))
        total_time_taken_display.insert(0.0,total_time2)
        keyword_you_searched=SearchKeyWord
        last_search_kw_display.insert(0.0,keyword_you_searched)
        total_Search_results_display.insert(0.0, SearchNumber)
        # ########## Search display if no results are fetched #################
        if SearchNumber==0 and keywordlenghtcheck(SearchKeyWord) !=0:
            if inc_button_value ==3 and t_buton_value ==0:
                OutPutField1.insert(0.0,"No match found !!!")
            if inc_button_value==0 and t_buton_value==4:
                OutPutField2.insert(0.0,"No match found !!!")
            if inc_button_value ==3 and t_buton_value==4:
                OutPutField2.insert(0.0, "No match found !!!")
                OutPutField1.insert(0.0, "No match found !!!")

        write2GoogleSheet(SearchKeyWord, SearchOption, SearchNumber,total_time2)



        # print("Total Searches retrieved for keyword '{}' is {} and time taken for search is {} seconds".format(SearchKeyWord, SearchNumber,total_time2))

    if SearchForQAPorDplan == 2:
        # print("Somthing")
        pass
    # Writing Search details to google sheet everytime a search is completed.
    wait.config(text="Search Completed!!!")





##### -- MAIN Window--########
Window=Tk()
Window.title("QuickSearch")
Window.minsize(height=500,width=800)
Window.resizable(0,0)

##########--Frames---#########
######TopFrame-Start##########
TopFrame=Frame(Window,height=100,width=1100,relief=SUNKEN, borderwidth=1)
#TopFrame1
#TopleftFrame=Frame(TopFrame,height=100,width=75,relief=GROOVE, borderwidth=1)
#RadioButton_TopFrame1:
# Radio_Var=IntVar()
# QAP_RButton=Radiobutton(TopleftFrame,text="QAP",variable=Radio_Var,value=1,command=GetRadioButton,bd=2)#,state=DISABLED)
# QAP_RButton.pack(expand=True,fill=BOTH,side=TOP)
# D_PLAN_RButton=Radiobutton(TopleftFrame,text="D-PLAN",variable=Radio_Var,value=2,command=GetRadioButton,bd=2)#,state=DISABLED)
# D_PLAN_RButton.pack(expand=True,fill=BOTH,side=TOP)

#TopLeftFrame_Pack -END
# TopleftFrame.pack(expand=True,fill=BOTH,side=LEFT)
# TopleftFrame.pack_propagate(0)
#TopFrame2:
TopMiddleFrame1=Frame(TopFrame,height=100,width=200,relief=GROOVE, borderwidth=1)
#ListBox
tkvar = StringVar(TopMiddleFrame1)
# tupple with options
choices = ("Function Definition",'Object Names',"Search Anything") #,'Function Definition (.t)','Function Usage(.t)', 'Object Names(.inc)', 'Type-Record (.inc)', 'Class Names(.inc)','Function Definition (.inc)','Function Definition (.t)',}
tkvar.set('Function Definition')  # set the default option
popupMenu = OptionMenu(TopMiddleFrame1, tkvar, *choices,command=labelchange_with_optionmenu)
popupMenu.config(bg="White")
popupMenu["menu"].config(bg="White")
Label(TopMiddleFrame1, text="Choose Your Search Option").pack(expand=True,fill=BOTH,side=TOP)
popupMenu.pack(expand=True,fill=X,side=BOTTOM)
popupMenu.pack_propagate(0)
# on change dropdown value
# link function to change dropdown
tkvar.trace('w', change_dropdown)

TopMiddleFrame1.pack(expand=True,fill=BOTH,side=LEFT)
TopMiddleFrame1.pack_propagate(0)


#TopFrame3:
TopRightFrame=Frame(TopFrame,height=100,width=200,relief=GROOVE, borderwidth=1)
##TextField-to input keywords##
text_var = StringVar()
text_var.set("Enter keyword(s) separated by a comma (1 to 3 words)")

KeyLable=Label(TopRightFrame,textvariable= text_var,bd=1)
KeyLable.pack(expand=True,fill=BOTH,side=TOP)
# KeyLable2 = Label(TopRightFrame,text="Enter the string that you want to find the match for",bd=1)
# KeyLable2.pack(expand=True,fill=BOTH,side=TOP)
Entry_Var=StringVar()
Entry1=Entry(TopRightFrame,width=200,textvariable=Entry_Var,bd=1)
#Entry_var-Trace=Entry_Var.trace('w', GetSearchWords)
Entry1.pack(expand=True,fill=BOTH,side=TOP)




SearchButton=Button(TopRightFrame,text="Search",command=QAPorDplan,bg='Orange',bd=1)
SearchButton.pack(expand=True,fill=BOTH,side=TOP)

TopRightFrame.pack(expand=True,fill=BOTH,side=LEFT)
TopRightFrame.pack_propagate(0)

# TopFrame 4
TopdisplayFrame=Frame(TopFrame,height=100,width=400,relief=GROOVE,borderwidth=1)

# last keyword search
TopdisplayFrame1=Frame(TopdisplayFrame,height=23,width=200,relief=GROOVE,borderwidth=1)
last_search_kw_label = Label(TopdisplayFrame1,text="Your Last Search Keywords    ",bd=1).pack(expand=True,fill=BOTH,side=LEFT)#grid(row=1,column=1)
last_search_kw_display = Text(TopdisplayFrame1,height=10,width=100,relief=GROOVE,bd=1,fg="Black")#grid(row=1,column=2)
last_search_kw_display.pack(expand=True,fill=BOTH,side=RIGHT)
TopdisplayFrame1.pack(expand=True,fill=BOTH,side=TOP)
TopdisplayFrame1.pack_propagate(0)

# Total Files Searched
TopdisplayFrame2=Frame(TopdisplayFrame,height=23,width=200,relief=GROOVE,borderwidth=1)
total_Files_Searched_label = Label(TopdisplayFrame2,text="Total Files Searched                ",bd=1).pack(expand=True,fill=BOTH,side=LEFT)#grid(row=2,column=1)
total_files_searched_display=Text(TopdisplayFrame2,height=10,width=238,relief=GROOVE,bd=1,fg="Black")#grid(row=2,column=2)
total_files_searched_display.pack(expand=True,fill=BOTH,side=RIGHT)
TopdisplayFrame2.pack(expand=True,fill=BOTH,side=TOP)
TopdisplayFrame2.pack_propagate(0)

# Total Search Retrieved
TopdisplayFrame3=Frame(TopdisplayFrame,height=23,width=200,relief=GROOVE,borderwidth=1)
total_Search_results_label = Label(TopdisplayFrame3,text="Total Search Results                ",bd=1).pack(expand=True,fill=BOTH,side=LEFT)#grid(row=3,column=1)
total_Search_results_display=Text(TopdisplayFrame3,height=10,width=238,relief=GROOVE,bd=1)#grid(row=3,column=2)
total_Search_results_display.pack(expand=True,fill=BOTH,side=RIGHT)
TopdisplayFrame3.pack(expand=True,fill=BOTH,side=TOP)
TopdisplayFrame3.pack_propagate(0)
# Total Time Taken
TopdisplayFrame4=Frame(TopdisplayFrame,height=23,width=200,relief=GROOVE,borderwidth=1)
total_time_taken_label=Label(TopdisplayFrame4,text="Total Time Taken In Seconds",bd=1).pack(expand=True,fill=BOTH,side=LEFT)#grid(row=4,column=1)
total_time_taken_display = Text(TopdisplayFrame4,height=10,width=238,relief=GROOVE,bd=1)#grid(row=4,column=2)
total_time_taken_display.pack(expand=True,fill=BOTH,side=RIGHT)
TopdisplayFrame4.pack(expand=True,fill=BOTH,side=TOP)
TopdisplayFrame4.pack_propagate(0)

#TopdisplayFrame pack
TopdisplayFrame.pack(expand=True,fill=BOTH,side=RIGHT)
TopdisplayFrame.pack_propagate(0)
#TopFramePack
TopFrame.pack(expand=True,fill=BOTH,side=TOP)
TopFrame.pack_propagate(0)
######TopFrame-End##########

############# .t and .inc label frame ############
smallFrame = Frame(Window,height=17,width=675,relief=SUNKEN, borderwidth=0.5)

smallFrame_left = Frame(smallFrame,height = 17,relief= SUNKEN,borderwidth=0.25)
#.inc button
Radio_Var1=IntVar()
inc_button = Checkbutton(smallFrame_left,state=ACTIVE,variable=Radio_Var1,text=".inc results",onvalue=3,offvalue =0,command=Getcheckbutton1,bd=2)#,state=DISABLED)
inc_button.select()
inc_button.pack(expand=True,fill=BOTH,side=LEFT)
smallFrame_left.pack(expand=True,fill=BOTH,side=LEFT)

smallFrame_Right = Frame(smallFrame,height = 15,relief= SUNKEN,borderwidth=0.25)
Radio_Var2=IntVar()
t_button = Checkbutton(smallFrame_Right,state=ACTIVE,variable=Radio_Var2,text=".t results",onvalue=4,offvalue =0,command=Getcheckbutton2,bd=2)#,state=DISABLED)
t_button.pack(expand=True,fill=BOTH,side=RIGHT)
smallFrame_Right.pack(expand=True,fill=BOTH,side=RIGHT)

#packing small frame
smallFrame.pack(expand=True,fill=BOTH,side=TOP)
smallFrame.pack_propagate(0)
######BottomFrame-Start###########

ButtomFrame=Frame(Window,height=400,width=675,relief=SUNKEN, borderwidth=3)
OutPutField1=Text(ButtomFrame,relief=GROOVE,bd=3,fg="Black")
#OutPutField1.config(font=(Consolas,20))
# ScrollBar1=Scrollbar(ButtomFrame)
# ScrollBar1.pack(expand=True,fill=Y,side=RIGHT)
OutPutField1.pack(expand=True,fill=BOTH,side=LEFT)
OutPutField2=Text(ButtomFrame,relief=GROOVE,bd=3,fg="Black")
OutPutField2.pack(expand=True,fill=BOTH,side=LEFT)

ButtomFrame.pack(expand=True,fill=BOTH,side=BOTTOM)
######BottomFrame-End###########

######### Wait Frame ########
wait = Label(smallFrame_left,text="")
wait.pack(expand=True,fill=BOTH,side=RIGHT)

############ Hit enter to search ##########

def clickSearchButton(event):
    SearchButton.invoke()

Window.bind("<Return>",clickSearchButton)




#########--Mainloop--##########
Window.mainloop()



