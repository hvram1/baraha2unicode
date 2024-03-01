import pyparsing as pp
import sys
from pathlib import Path
import re
from indic_transliteration import sanscript
from pathlib import Path
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
import json
from docx import Document
parseTree =  {"TB": {"Prasna":[]}}
sectionTitle_temp = ""
invocation_temp = ""
global_identifier = {}
global_identifier["Prapaataka"]  = global_identifier["Anuvakkam"] = global_identifier["Panchasat"] =0

def createPrasnaNodes(prasnaInfo):
    global global_identifier
    prasnaInfo = int(prasnaInfo)
    currentPrasnaLength = 0
    if parseTree["TB"].get("Prasna") == None:
        currentPrasnaLength = 0
    else: 
        currentPrasnaLength = len(parseTree["TB"]["Prasna"])
    #print("PrasnaInfo ",prasnaInfo, " currentPrasnaLength ",currentPrasnaLength)
    while (prasnaInfo - currentPrasnaLength) > 0:
        PanchasatNode={"id":0,"SamhitaPaata":"","header":""}
        AnuvakkamNode={"id":0,"Panchasat":[],"Korvai":""}
        AnuvakkamNode["Panchasat"].append(PanchasatNode)
        PrapaatakaNode={"id":0,"Anuvakkam":[]}
        PrapaatakaNode["Anuvakkam"].append(AnuvakkamNode)
        PrasnaNode={"id":0,"Prapaataka":[]}
        PrasnaNode["Prapaataka"].append(PrapaatakaNode)
        #print("Appending Prasna b4 ",parseTree)
        parseTree["TB"]["Prasna"].append(PrasnaNode)
        #print("Appending Prasna after ",parseTree)

        #parseTree["TA"]["Prapaataka"][currentPrapaatakaLength]["Anuvakkam"].append(AnuvakkamNode)
        #print("After appending Prapaataka",parseTree)
        currentPrasnaLength += 1

def createPrapaatakaNodes(prasnaInfo,prapaatakaInfo):
    global global_identifier
    prapaatakaInfo = int(prapaatakaInfo)
    prasnaInfo = int(prasnaInfo)
    currentPrapaatakaLength = 0
    if parseTree["TB"]["Prasna"][prasnaInfo-1].get("Prapaataka") == None:
        currentPrapaatakaLength = 0
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"]=[]
    else: 
        currentPrapaatakaLength = len(parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"])
    while (prapaatakaInfo - currentPrapaatakaLength) > 0:
        PanchasatNode={"id":0,"SamhitaPaata":"","header":""}
        AnuvakkamNode={"id":0,"Panchasat":[],"Korvai":""}
        AnuvakkamNode["Panchasat"].append(PanchasatNode)
        PrapaatakaNode={"id":0,"Anuvakkam":[]}
        PrapaatakaNode["Anuvakkam"].append(AnuvakkamNode)
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"].append(PrapaatakaNode)

        #parseTree["TA"]["Prapaataka"][currentPrapaatakaLength]["Anuvakkam"].append(AnuvakkamNode)
        #print("After appending Prapaataka",parseTree)
        currentPrapaatakaLength += 1

def createAnuvakkamNodes(prasnaInfo,prapaatakaInfo,anuvakkamInfo):
    global global_identifier
    prasnaInfo=int(prasnaInfo)
    prapaatakaInfo = int(prapaatakaInfo)
    anuvakkamInfo = int(anuvakkamInfo)
    currentAnuvakkamLength = 0
    if parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1].get("Anuvakkam") == None:
        currentAnuvakkamLength = 0
    else:
        currentAnuvakkamLength = len(parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"])
    while (anuvakkamInfo - currentAnuvakkamLength) > 0:
        PanchasatNode={"id":0,"SamhitaPaata":"","header":""}
        AnuvakkamNode={"id":0,"Panchasat":[],"Korvai":""}
        AnuvakkamNode["Panchasat"].append(PanchasatNode)
        
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"].append(AnuvakkamNode) 
        currentAnuvakkamLength += 1

def createPanchasatNodes(prasnaInfo,prapaatakaInfo,anuvakkamInfo,panchasatInfo):
    global global_identifier
    prasnaInfo=int(prasnaInfo)
    prapaatakaInfo = int(prapaatakaInfo)
    anuvakkamInfo = int(anuvakkamInfo)
    panchasatInfo = int(panchasatInfo)

    currentPanchasatLength = 0
    if parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1].get("Panchasat") == None:
        currentPanchasatLength = 0
    else:
        currentPanchasatLength = len(parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"])
    while (panchasatInfo - currentPanchasatLength) > 0:
        PanchasatNode={"id":0,"SamhitaPaata":"","header":""}
        
        
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"].append(PanchasatNode) 
        currentPanchasatLength += 1   

def createSpecialKorvaiNodes(prasnaInfo,prapaatakaInfo,anuvakkamInfo):
    prasnaInfo=int(prasnaInfo)
    prapaatakaInfo = int(prapaatakaInfo)
    anuvakkamInfo = int(anuvakkamInfo)
    SpecialKorvaiNode={"id":0,"SpecialKorvai":[]}
    if parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1].get("SpecialKorvai")==None:
        
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["SpecialKorvai"]=[]
    parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["SpecialKorvai"].append(SpecialKorvaiNode)
    
def anuvakkam_end_Action(tokens):
    print("In anuvakkam_end_Action ")
    
    anuvakkam_number_Pattern = r"\(A(\d+)\)"
    klist=[]
    for tok in tokens:
        result = re.search(anuvakkam_number_Pattern,tok,re.IGNORECASE)
        if result:
            x1=re.sub(anuvakkam_number_Pattern,"",tok,re.IGNORECASE)
            if len(x1) >0:
                klist.append(x1)
            pass
        elif tok=="\n":
            pass
        else:
            klist.append(tok)
    x=' '.join(klist)
    print(x)

    prasnaInfo= global_identifier["Prasna"] 
    prapaatakaInfo=global_identifier["Prapaataka"]
    anuvakkamInfo=global_identifier["Anuvakkam"]
    #createAnuvakkamNodes(prasnaInfo,prapaatakaInfo,anuvakkamInfo)
    outputString=transliterate(x.strip(),sanscript.BARAHA, sanscript.DEVANAGARI)
    #outputString=""
    parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Korvai"]=outputString
    #parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["id"]=anuvakkamInfo


    
              
def anuvakkam_header_Action(tokens):
    print("In anuvakkam_header ",tokens[0][0], tokens[0][4])
    components=tokens[0][0].strip().split(".")
    prasnaInfo= global_identifier["Prasna"] = int(components[0])
    prapaatakaInfo=global_identifier["Prapaataka"]=int(components[1])
            
    anuvakkamInfo=global_identifier["Anuvakkam"]=int(components[2])
    createAnuvakkamNodes(prasnaInfo,prapaatakaInfo,anuvakkamInfo)
    #print(tokens)
    outputString=""
    x=' '.join(tokens[0])
    outputString=transliterate(x.replace("\n","").strip(),sanscript.BARAHA, sanscript.DEVANAGARI)
    parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["header"]=outputString
    parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["id"]=anuvakkamInfo


 
    '''for key in tokens.keys():
            print("token ",key,tokens[key])'''

def specialKorvaiLines_Action(tokens):
    print("In specialKorvai ",tokens)
    prasnaInfo= global_identifier["Prasna"] 
    prapaatakaInfo=global_identifier["Prapaataka"]
    outputString=""        
    anuvakkamInfo=global_identifier["Anuvakkam"]
    panchasatInfo=global_identifier["Panchasat"]
    createSpecialKorvaiNodes(prasnaInfo,prapaatakaInfo,anuvakkamInfo)
    index=len(parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["SpecialKorvai"])-1
    x=tokens[len(tokens)-1]
    ''' The re.sub is not working . need to check why '''
    
    pattern1=r'for anuvakam 1'
    pattern2=r"regarding order of “Srushti"
    res = re.search(pattern1,x,re.IGNORECASE)
    #print("res is ",res)
    #print("x is ", x)
    x1=re.sub(pattern1,' ',x,re.IGNORECASE)
 
    x1=x.replace("fOr Anuvakam 1","")
    x2=x1.replace('rEgarding ordEr of “Srushti”',"")
    #print("x1 is ",x1)
    #x2=re.sub(pattern2,' ',x1,re.IGNORECASE)
    #print("x2 is ",x2)
    outputString=transliterate(x2.replace("\n","").strip(),sanscript.BARAHA, sanscript.DEVANAGARI)
    parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["SpecialKorvai"][index]["header"]=tokens[0]
    parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["SpecialKorvai"][index]["SpecialKorvai"]=outputString

def panchasatLinesAction(tokens):
    
    #print(tokens['panchasatLines'])
    #print(tokens['panchasat_header'][0][2])#,tokens['panchasat_id'])
    if tokens.get('panchasat_header') and tokens.get('panchasat_id') :
        header_array=tokens.get('panchasat_header')[0]
        header_length=len(header_array)
        id=tokens.get('panchasat_id')
        print("In panchasatLinesAction ",header_array[header_length-1].strip(),id)
        #print(tokens)
        components=header_array[header_length-1].strip().split(".")
        prasnaInfo= global_identifier["Prasna"] = int(components[0])
        prapaatakaInfo=global_identifier["Prapaataka"]=int(components[1])
            
        anuvakkamInfo=global_identifier["Anuvakkam"]=int(components[2])
        panchasatInfo=global_identifier["Panchasat"]=int(components[3])
        createPanchasatNodes(prasnaInfo,prapaatakaInfo,anuvakkamInfo,panchasatInfo)
        outputString=transliterate(tokens[1][0].replace("\n","").strip(),sanscript.BARAHA, sanscript.DEVANAGARI)
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["header"]=header_array[header_length-1].strip()
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["SamhitaPaata"]=outputString
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Anuvakkam"][anuvakkamInfo-1]["Panchasat"][panchasatInfo-1]["id"]=id    
        
    else:
        print("In panchasatLinesAction Nonecase")
        for key in tokens.keys():
            print("token ",key,tokens[key])

def coreAction(tokens):
    print("In CoreAction ")
    prasnaInfo= int(global_identifier["Prasna"])
    invocation_temp = global_identifier["invocation_temp"]
    parseTree["TB"]["Prasna"][prasnaInfo-1]["invocation"]=invocation_temp
    #print(tokens['panchasatLines*'])
    '''for key in tokens.keys():
        print("token ",key,tokens[key])'''

def sectiontitleLine_Action(tokens):
    strArray=tokens['sectiontitleLine_Section'][0].split(" ")
    print("In sectiontitleLine_Action ",tokens,strArray[0].strip())
    components=strArray[0].strip().split(".")
    prasnaInfo= global_identifier["Prasna"] = int(components[0])
    prapaatakaInfo=global_identifier["Prapaataka"]=int(components[1])
    createPrapaatakaNodes(prasnaInfo,prapaatakaInfo)
    '''for key in tokens.keys():
        print("token ",key,tokens[key])'''
    lines=""
    outputString=""
    for t in tokens:
        lines +=(str)(t)
    outputString=transliterate(lines.strip(),sanscript.BARAHA, sanscript.DEVANAGARI)
    #outputString=transliterate(lines,sanscript.BARAHA, sanscript.TAMIL)
    #print("##",outputString,"##")
    global_identifier["sectionTitle_temp"]=outputString
    parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["sectionTitle"]=outputString
    parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["sectionid"]=prapaatakaInfo

    return outputString

def titleLine_Action(tokens):
    #print("titleLine_Action ",tokens)
    strArray=tokens['titleLine_Section'].split(" ")
    print("In titleLine_Action ",strArray[0].strip())
    prasnaInfo= global_identifier["Prasna"] = int(strArray[0][0].strip())
    createPrasnaNodes(prasnaInfo)
    '''for key in tokens.keys():
            print("token ",key,tokens[key])'''
    lines=""
    outputString=""
    for t in tokens:
        lines +=(str)(t)
    outputString=transliterate(lines,sanscript.BARAHA, sanscript.DEVANAGARI)
    #outputString=transliterate(lines,sanscript.BARAHA, sanscript.TAMIL)

    global_identifier["title_temp"]=outputString
    parseTree["TB"]["Prasna"][prasnaInfo-1]["title"]=outputString
    parseTree["TB"]["Prasna"][prasnaInfo-1]["id"]=prasnaInfo
    #print("title Section")
    #MYGLOBAL.append("Title")
    strArray=tokens['titleLine_Section'].split(" ")
    return outputString

def invocationLine_Action(tokens):
    print("invocationLine_Action ",tokens)
    #prasnaInfo= int(global_identifier["Prasna"])
    lines=""
    outputString=""
    for t in tokens:
        lines +=(str)(t)
    outputString=transliterate(lines.strip(),sanscript.BARAHA, sanscript.DEVANAGARI)
    #outputString=transliterate(lines,sanscript.BARAHA, sanscript.TAMIL)

    global_identifier["invocation_temp"] = outputString
    #parseTree["TB"]["Prasna"][prasnaInfo-1]["invocation"]=outputString
    return outputString


    
def firstLastPadamLines_Action(tokens):
    print("In firstLastPadamsinesAction")
    prasnaInfo= int(global_identifier["Prasna"])
    prapaatakaInfo=int(global_identifier.get("Prapaataka"))
    prasnaInfo=int(prasnaInfo)
    prapaatakaInfo=int(prapaatakaInfo)
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    outputString=""
    tokenLength = len(tokens)
    if tokenLength >= 2 :
        header = tokens[0] + " " + tokens[1][0]
        lines=""
        for s in tokens[1][1:]:
            lines+=s
            
        x = transliterate(lines.strip(), sanscript.BARAHA, sanscript.DEVANAGARI)
        #x = transliterate(lines, sanscript.BARAHA, sanscript.TAMIL)

        outputString=header + "\n" + x
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["firstLastPadams_Sloka"] = x
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["firstLastPadams_header"] = header
    elif tokenLength <2 :
        print(" firstandLastPadams : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" firstandLastPadams : Check the parser. This is just a warning  ");
    return outputString

def prapaatakaKorvaiLines_Action(tokens):
    print("In prapaatakaKorvaiLinesAction")
    prasnaInfo=global_identifier.get("Prasna")
    prapaatakaInfo=global_identifier.get("Prapaataka")
    prapaatakaInfo=int(prapaatakaInfo)
    prasnaInfo=int(prasnaInfo)
    
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    outputString=""
    tokenLength = len(tokens)
    if tokenLength >= 2 :
        header = tokens[0] + " " + tokens[1][0]
        lines=""
        for s in tokens[1][1:]:
            lines+=s+"\n"
        #print(lines)
        x = transliterate(lines.strip(), sanscript.BARAHA, sanscript.DEVANAGARI)
        #x = transliterate(lines, sanscript.BARAHA, sanscript.TAMIL)

        outputString=header + "\n" + x
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["PrapaatakaKorvai_Sloka"] = x
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["PrapaatakaKorvai_header"] = header
    elif tokenLength <2 :
        print(" prapaatakaKorvaiLines : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" prapaatakaKorvaiLines : Check the parser. This is just a warning  ");
    return outputString

def korvaiLines_Action(tokens):
    print("In korvaiLinesAction")
    prasnaInfo=global_identifier.get("Prasna")
    prapaatakaInfo=global_identifier.get("Prapaataka")
    prapaatakaInfo=int(prapaatakaInfo)
    prasnaInfo=int(prasnaInfo)
    
    anuvakkamInfo=global_identifier.get("Anuvakkam")
    panchasatInfo=global_identifier.get("Panchasat")
    outputString=""
    tokenLength = len(tokens)
    if tokenLength >= 2 :
        header = tokens[0] + tokens[1][0]
        lines=""
        for s in tokens[1][1:]:
            lines+=s+"\n"
        x = transliterate(lines.strip(), sanscript.BARAHA, sanscript.DEVANAGARI)
        #x = transliterate(lines, sanscript.BARAHA, sanscript.TAMIL)

        outputString=header + "\n" + x
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Korvai_Sloka"] = x
        parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["Korvai_header"] = header
    elif tokenLength <2 :
        print(" korvaiLines : Check the token returned. Seems to be a problem")
        SystemExit(-1)
    if (tokenLength >2 ):
        print(" korvaiLines : Check the parser. This is just a warning  ");
    return outputString
    print("End of korvaiLinesAction")

def remainingLines_Action(tokens):
    print("In remainingLinesAction",tokens)
    xy= len(tokens)-1
    outputString=""
    #print("0: ", tokens[0])
    #print("1: ",tokens[1])
    #print("2: ",tokens[2])
    #lines=str(tokens[x]).split("\n")
    #y = lines[0].split("\n")
    englishPattern1=r"appearing"
    englishPattern2=r"appendix"
    if (xy >0 and len(tokens[0]) >0):
        x = transliterate(tokens[0], sanscript.BARAHA, sanscript.DEVANAGARI)
        outputString+=x
    for line in tokens[xy]:
        print(line)
        englishResult1 = re.search(englishPattern1,line,re.IGNORECASE)
        englishResult2 = re.search(englishPattern2,line,re.IGNORECASE)
        if englishResult1 or englishResult2:
            outputString+=line
            #print("no transliteration",line)
        else:
            if len(line) >1:
                x = transliterate(line, sanscript.BARAHA, sanscript.DEVANAGARI)
                outputString+=x

                #print(x)
            else :
                outputString+=line
                #print(line)
    print(outputString)
    prapaatakaInfo=int(global_identifier.get("Prapaataka"))
    prapaatakaInfo=int(prapaatakaInfo)
    prasnaInfo=global_identifier.get("Prasna")
    prasnaInfp=int(prasnaInfo)

    parseTree["TB"]["Prasna"][prasnaInfo-1]["Prapaataka"][prapaatakaInfo-1]["ending"]=outputString
    return outputString
    #print("End of remainingLinesAction")


#parseTree = json.loads(ts_string)





  
# Largely built following the example and comments in
# https://stackoverflow.com/questions/55909620/capturing-block-over-multiple-lines-using-pyparsing
# and
# https://stackoverflow.com/questions/15938540/how-can-i-do-a-non-greedy-backtracking-match-with-oneormore-etc-in-pyparsing
pp.enable_diag(pp.Diagnostics.enable_debug_on_named_expressions)

EOL = pp.LineEnd()
EmptyLine = pp.Suppress(pp.LineStart() + EOL)
EmptyLines=pp.OneOrMore(EmptyLine)
prasna_Separator_1 = pp.Keyword("==========================================").suppress()
prasna_Separator_2 = pp.Keyword("------------------------------------------").suppress()

prasna_Separator = prasna_Separator_1 | prasna_Separator_2 
englishLine_StopSeparator = pp.LineStart() + "OM"

englishLines = pp.Optional(EOL) + pp.Group(
    pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=englishLine_StopSeparator)
)
englishPreface = pp.Combine(pp.CaselessKeyword("Notes") + englishLines).setResultsName(
    "englishPreface_Section"
)
sectiontitleLine = pp.Combine(
    pp.Word(pp.nums) + pp.Literal(".") + pp.Word(pp.nums) + (pp.SkipTo(EOL)) + EOL
).setResultsName("sectiontitleLine_Section*")

sectiontitleLine.setParseAction(sectiontitleLine_Action)

titleLine = pp.Combine(
    ~sectiontitleLine + pp.Word(pp.nums) + (pp.SkipTo(EOL)) + pp.Suppress(EOL)
).setResultsName("titleLine_Section")
titleLine.setParseAction(titleLine_Action)

invocationLine_StopSeparator = pp.LineStart() + ( titleLine | sectiontitleLine )

invocationLines = pp.Optional(EOL) + pp.Group(
    pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=invocationLine_StopSeparator)
)
invocation = pp.Combine(pp.Keyword("OM") + invocationLines).setResultsName(
    "invocation_Section*"
)
invocation.setParseAction(invocationLine_Action)
prasnaKorvai_Starting = pp.CaselessLiteral("PrapAtaka Korvai with starting")
korvai_Starting = pp.CaselessLiteral("korvai with starting ")
firstLastPadam_Starting = pp.CaselessLiteral("first and last ")
prapaatakaKorvai_Starting = pp.CaselessLiteral("PrapAtaka Korvai with starting ") | pp.CaselessLiteral("Prapaataka korvai with starting ")
samhitaKorvai_Starting = pp.CaselessKeyword("samhita korvai with starting ")
specialKorvai_Starting = pp.CaselessKeyword("special korvai")

prasnaEnding_Starting_1 = pp.CaselessKeyword("|| hari#H OM ||")
prasnaEnding_Starting_2 = pp.CaselessKeyword("|| hariH# OM ||")
prasnaEnding_Starting_3 = pp.CaselessKeyword("|| hari# OM ||")

prasnaEnding_Starting = prasnaEnding_Starting_1 | prasnaEnding_Starting_2 | prasnaEnding_Starting_3


anuvakkam_header = pp.Group(
    pp.Combine(pp.Word(pp.nums) + pp.Literal(".") + pp.Word(pp.nums) + pp.Literal(".") + pp.Word(pp.nums))
    +pp.Optional(pp.White()) + pp.CaselessLiteral("anuvAkaM")+pp.Optional(pp.White())+ pp.Word(pp.nums) +(pp.SkipTo(EOL)) + EOL )
#"1.1.4	anuvAkaM 4 - saMBArasaM~MyuktAyatanEShu agnyAdhAnam "
anuvakkam_header.setResultsName("anuvakkam_header", listAllMatches=True)
anuvakkam_header.setParseAction(anuvakkam_header_Action)
panchasat_header_1 = pp.Group(
    pp.LineStart()+pp.CaselessLiteral("TB") +pp.ZeroOrMore(pp.White()) + pp.Combine(pp.Word(pp.nums) + pp.Literal(".") + pp.Word(pp.nums) + pp.Literal(".") + pp.Word(pp.nums)+ pp.Literal(".") + pp.Word(pp.nums)+(pp.SkipTo(EOL)) + EOL)
).setResultsName("panchasat_header", listAllMatches=True)
panchasat_header_2 = pp.Group(
    pp.LineStart()+pp.CaselessLiteral("T.B.") +pp.ZeroOrMore(pp.White()) + pp.Combine(pp.Word(pp.nums) + pp.Literal(".") + pp.Word(pp.nums) + pp.Literal(".") + pp.Word(pp.nums)+ pp.Literal(".") + pp.Word(pp.nums)+(pp.SkipTo(EOL)) + EOL)
).setResultsName("panchasat_header", listAllMatches=True)

panchasat_header =   panchasat_header_2 | panchasat_header_1
panchasat_header.setResultsName("panchasat_header", listAllMatches=True)
# TB 1.1.4.1
panchasat_numbering = pp.CaselessLiteral("|")+ \
                      pp.OneOrMore(pp.White()) + \
                      pp.Word(pp.nums).setResultsName("panchasat_id") + pp.OneOrMore(pp.White()) + \
                      pp.CaselessLiteral("(")+pp.Word(pp.nums).setResultsName("panchast_count")+pp.CaselessLiteral(")")
panchasat_numbering.setResultsName("panchasat_numbering", listAllMatches=True)
#panchasat_ending = pp.LineStart()+pp.SkipTo(pp.CaselessLiteral(")")+EOL)
panchasat_ending = pp.Group(pp.LineStart()+pp.SkipTo(panchasat_numbering+EOL))
panchasat_ending.setResultsName("panchasat_ending", listAllMatches=True)


#panchasat_ending = pp.Group(
#    pp.LineStart() + pp.OneOrMore(pp.Word(pp.printables),stopOn=pp.nums) +pp.Word(pp.nums) + pp.Optional(pp.White()) +pp.CaselessLiteral("(")+pp.Word(pp.nums)+pp.CaselessLiteral(")")+pp.SkipTo(pp.LineEnd())+EOL)

anuvakkam_numbering = pp.CaselessLiteral("(A") #+pp.Word(pp.nums)+pp.CaselessLiteral(")").setResultsName("anuvakkam_numbering")
anuvakkam_ending = pp.LineStart() +  pp.SkipTo(anuvakkam_numbering) + pp.SkipTo(pp.LineEnd() ) +EOL + EmptyLines
anuvakkam_ending.setResultsName("anuvakkam_ending",listAllMatches=True)
anuvakkam_ending.setParseAction(anuvakkam_end_Action)
#panchasatLines =  panchasat_header + pp.Combine(panchasat_ending + pp.CaselessLiteral(")"))+ ~anuvakkam_ending +EOL
panchasatLines =  panchasat_header + panchasat_ending + panchasat_numbering + pp.Optional(EmptyLines)+ ~anuvakkam_ending +EOL

panchasatLines.setResultsName("panchasatLines", listAllMatches=True)
panchasatLines.setParseAction(panchasatLinesAction)


korvaiLines = (
    korvai_Starting
    + pp.Optional(EOL)
    + pp.Group(
        pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=firstLastPadam_Starting)
    )
)
korvaiLines.setParseAction(korvaiLines_Action)
prapaatakaKorvaiLines = (
    prapaatakaKorvai_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine))
)
prapaatakaKorvaiLines.setParseAction(prapaatakaKorvaiLines_Action)
specialKorvaiLines = (
    specialKorvai_Starting
    + pp.Optional(EOL)
    + pp.Combine(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine|anuvakkam_header))
)
specialKorvaiLines.setParseAction(specialKorvaiLines_Action)

firstLastPadamLines = (
    firstLastPadam_Starting
    + pp.Optional(EOL)
    + pp.Group(pp.OneOrMore(pp.SkipTo(pp.LineEnd()) + EOL, stopOn=EmptyLine))
)
firstLastPadamLines.setParseAction(firstLastPadamLines_Action)




remainingLines = (
    
    prasnaEnding_Starting
    + pp.Optional(EOL)
    + pp.Group(
        pp.OneOrMore(
            ~invocation + pp.SkipTo(pp.LineEnd()) + EOL, stopOn=prasna_Separator
        )
    ).setResultsName("RemainingLines")
)

remainingLines.setParseAction(remainingLines_Action)
#remainingLines = remainingLines_WithoutAppendix  # This seems like a hack but this is the best I can do now
# Otherwise a greedy match happens
corePrasna_1 = (
    invocation + titleLine + sectiontitleLine + \
        pp.OneOrMore(anuvakkam_header + \
                     pp.OneOrMore(panchasatLines) +\
                     anuvakkam_ending +\
                     pp.ZeroOrMore(specialKorvaiLines)
                    ) +\
        prapaatakaKorvaiLines +\
        korvaiLines +\
        firstLastPadamLines +\
        remainingLines +\
        pp.Optional((prasna_Separator + pp.SkipTo(EOL))).suppress()
)
corePrasna_2 = (
    invocation  + sectiontitleLine + \
        pp.OneOrMore(anuvakkam_header + \
                     pp.OneOrMore(panchasatLines) +\
                     anuvakkam_ending +\
                     pp.ZeroOrMore(specialKorvaiLines)
                    ) +\
        prapaatakaKorvaiLines +\
        korvaiLines +\
        firstLastPadamLines +\
        remainingLines +\
        pp.Optional((prasna_Separator + pp.SkipTo(EOL))).suppress()
)

corePrasna = corePrasna_1 | corePrasna_2
corePrasna.setParseAction(coreAction)




'''anuvakkam_header.setName("anuvakkamHeader")
panchasat_header.setName("panchasatheader")

panchasat_header_2.setName("ph2")
panchasat_header_1.setName("ph1")
panchasat_ending.setName("panchasatending")
anuvakkam_ending.setName("anuvakkamending")
panchasatLines.setName("panchasatLines")
prasnaLines.setName("prasnaLine")
corePrasna.setName("core")
corePrasna_1.setName("P1")
corePrasna_2.setName("P2")
prasna_Section.setName("PS")
specialKorvaiLines.setName("SK")
korvaiLines.setName("Korvai")
sectiontitleLine.setName("sectiontitleLine")
titleLine.setName("titleLine")
invocation.setName("invocation")
prasnaKorvaiLines.setName("PSK")
firstLastPadamLines.setName("firstLast")
prapaatakaKorvaiLines.setName("PrapaatakaKorvai")
remainingLines.setName("rem")'''

parser = englishPreface + \
        pp.OneOrMore(corePrasna)

if args_count := len(sys.argv) < 2:
    print("Provide a file name ")
    raise SystemExit(2)
for file_name in sys.argv[1:]:
    #file_name = sys.argv[1]
    text=""
    document = Document(file_name)

    all_paras = document.paragraphs
    for para in all_paras:
        text += para.text + "\n"
    #text = Path(file_name).read_text(encoding="utf-8")
    text_file_name = file_name.replace(".docx", ".txt")
    with open(text_file_name, "w") as f:
        f.write(text)

    results = parser.parseString(text)
json_file_name = "TB.json"
#print(parseTree)
my_json = json.dumps(parseTree,indent=3,ensure_ascii=False, sort_keys=True)
my_json = my_json.replace("\uA8E3","\u1CDA")
with open(json_file_name, "w") as f:
    f.write(my_json)

