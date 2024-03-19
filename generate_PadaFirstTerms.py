import json
from pathlib import Path
import re
import jinja2
from generatePDF import CreatePdf,escape_for_latex
import grapheme

pattern1=r"[\d*]"
pattern2=r"{\d*}"
pattern3=r"\(\d*\)"
pattern4=r"\""

padaIndex={}
padaTerms=[]
padaTOC={}
ts_string = Path("TS_withPada.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)
for kanda in parseTree['TS']['Kanda']:
    #print(kanda['id'])
    for prasna in kanda['Prasna']:
        #print(prasna['id'])
        for anuvakkam in prasna['Anuvakkam']:
            #print(anuvakkam['id'])
            for panchasat in anuvakkam['Panchasat']:
                header=panchasat['header'].strip().replace(" ","_")
                #print(panchasat['PadaPaata'],panchasat['header'])
                #tokens=panchasat['PadaPaata'].split("।")
                tokens=re.split("। |॥ ",panchasat['PadaPaata'])
                padaList=[]
                iticount=0
                for t in tokens:
                    pada=t.strip()
                    pada=pada.replace("['']","")
                    pada=pada.replace("(","")
                    pada=pada.replace(")","")
                    pada=pada.replace(" - ","-")
                    pada=pada.replace("\"","")
                    pada=pada.replace("“","")
                    pada=pada.replace("[","")
                    pada=pada.strip()
                    if len(pada)>0:
                        padaList.append(pada)
                firstTerms="   ।   ".join(padaList[0:4])
                firstTerms+="   ।   "
                if padaIndex.get(firstTerms) is None:
                    padaIndex[firstTerms]=[header]
                else:
                    padaIndex[firstTerms].append(header)
                    #print("Duplicate ",firstTerms," occurring in ",padaIndex[firstTerms],header)
                #print(header,firstTerms )
                padaTOC[header]=firstTerms
                #padaOccurence=panchasat['header'].replace("TS ","")
                # print(panchasat['Content']
padaTupleList=[]
sno=1
for header in padaTOC.keys():
    
    firstTerms= padaTOC[header]
    listHeaders=padaIndex[firstTerms]
    if len(listHeaders)>1:
        listString = ' '.join(listHeaders)
        listString = listString.replace(header,"")
        
    else:
        listString = "_"
    #print(header, " - " ,firstTerms,listString)
    padaTuple=(sno,escape_for_latex(header),escape_for_latex(firstTerms),escape_for_latex(listString))
    padaTupleList.append(padaTuple)
    sno+=1


padaTemplateFileName="templates/TS_Index_main.tex"
CreatePdf(padaTemplateFileName,"TS","Index",escape_for_latex(padaTupleList))

sno=1
padaTupleList=[]
for item in sorted(padaIndex.keys()):
    listString = ' '.join(padaIndex[item])

    padaTuple=(sno,escape_for_latex(item), escape_for_latex(listString))
    #print(padaTuple)
    padaTupleList.append(padaTuple)
    sno+=1
padaTemplateFileName="templates/TS_Index_Alphabetical_main.tex"
CreatePdf(padaTemplateFileName,"TS_Alphabetical","Index",padaTupleList) 

padaIndex={}
padaTerms=[]
padaTOC={}
ts_string = Path("TA.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)
for prapaataka in parseTree['TA']['Prapaataka']:
    for anuvakkam in prapaataka['Anuvakkam']:
        for panchasat in anuvakkam['Panchasat']:
            
            header=panchasat['header'].strip().replace(" ","_")
            tokens=re.split("। |॥ | ",panchasat['SamhitaPaata'])
            #print(tokens)
            padaList=[]
            iticount=0
            for t in tokens:
                pada=t.strip()
                
                pada=pada.replace("['']","")
                pada=pada.replace("(","")
                pada=pada.replace(")","")
                pada=pada.replace(" - ","-")
                pada=pada.replace("\u0951","")
                pada=pada.replace("\u0952","")
                pada=pada.replace("\u1CDA","")
                pada=pada.replace("”","")
                pada=pada.replace("\"","")
                pada=pada.replace("“","")
                pada=pada.replace("[","")
                pada=pada.strip()
                res2=re.search(pattern2,pada)
                if res2 is not None:
                    pada=pada.replace(res2.group(),"")
                    #print(pada,header,res2)
                if len(pada)>0:
                    padaList.append(pada)
            
            firstTerms=' '.join(padaList[0:4])
            if grapheme.endswith(firstTerms,"र्"):
                x=firstTerms
                firstTerms=firstTerms.replace("र्","\u0903")
                print(header,",old = ",x," ,replacement = ",firstTerms)
            if grapheme.endswith(firstTerms,"द्"):
                #firstTerms=firstTerms.replace("र्","\u0903")
                #print(header,firstTerms)
                pass
            if grapheme.endswith(firstTerms,"ꣳ"):
                x=firstTerms
                firstTerms=firstTerms.replace("ꣳ","\u0902")
                print(header,",old = ",x," ,replacement = ",firstTerms)
            if padaIndex.get(firstTerms) is None:
                padaIndex[firstTerms]=[header]
            else:
                padaIndex[firstTerms].append(header)
                #print("Duplicate ",firstTerms," occurring in ",padaIndex[firstTerms],header)
            #print(header,padaList[0:4] )
            padaTOC[header]=firstTerms
            #padaOccurence=panchasat['header'].replace("TS ","")
            # print(panchasat['Content']
sno=1    
padaTupleList=[]
for header in padaTOC.keys():
    
    firstTerms= padaTOC[header]
    listHeaders=padaIndex[firstTerms]
    if len(listHeaders)>1:
        listString = ' '.join(listHeaders)
        listString = listString.replace(header,"")
        
    else:
        listString = "_"
    #print(header, " - " ,firstTerms,listString)
    padaTuple=(sno,escape_for_latex(header),escape_for_latex(firstTerms),escape_for_latex(listString))
    padaTupleList.append(padaTuple)
    sno+=1

padaTemplateFileName="templates/TA_Index_main.tex"
CreatePdf(padaTemplateFileName,"TA","Index",padaTupleList)

sno=1
padaTupleList=[]
for item in sorted(padaIndex.keys()):
    if len(item):
        listString = ' '.join(padaIndex[item])

        padaTuple=(sno,escape_for_latex(item), escape_for_latex(listString))
        #print(padaTuple)
        padaTupleList.append(padaTuple)
        sno+=1
padaTemplateFileName="templates/TA_Index_Alphabetical_main.tex"
CreatePdf(padaTemplateFileName,"TA_Alphabetical","Index",padaTupleList)

padaIndex={}
padaTerms=[]
padaTOC={}
ts_string = Path("TB.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)

for prasna in parseTree['TB']['Prasna']:
    for prapaataka in prasna['Prapaataka']:
        for anuvakkam in prapaataka['Anuvakkam']:
            for panchasat in anuvakkam['Panchasat']:
                header="TB_"+panchasat['header'].strip().replace(" ","_")
                tokens=re.split("। |॥ | ",panchasat['SamhitaPaata'])
                padaList=[]
                iticount=0
                for t in tokens:
                    pada=t.strip()
                    pada=pada.replace("['']","")
                    pada=pada.replace("(","")
                    pada=pada.replace(")","")
                    pada=pada.replace(" - ","-")
                    pada=pada.replace("\u0951","")
                    pada=pada.replace("\u0952","")
                    pada=pada.replace("\u1CDA","")
                    pada=pada.replace("”","")
                    pada=pada.replace("\"","")
                    pada=pada.replace("“","")
                    pada=pada.replace("[","")
                    
                    pada=pada.strip()
                    res2=re.search(pattern2,pada)
                    if res2 is not None:
                        pada=pada.replace(res2.group(),"")
                        #print(pada,header,res2)
                    if len(pada)>0:
                        padaList.append(pada)
                firstTerms=' '.join(padaList[0:4])
                if grapheme.endswith(firstTerms,"र्"):
                    x=firstTerms
                    firstTerms=firstTerms.replace("र्","\u0903")
                    print(header,",old = ",x," ,replacement = ",firstTerms)
                if grapheme.endswith(firstTerms,"द्"):
                    #firstTerms=firstTerms.replace("र्","\u0903")
                    
                    #print(header,firstTerms)
                    pass
                if grapheme.endswith(firstTerms,"ꣳ"):
                    x=firstTerms
                    firstTerms=firstTerms.replace("ꣳ","\u0902")
                    print(header,",old = ",x," ,replacement = ",firstTerms)
                if padaIndex.get(firstTerms) is None:
                    padaIndex[firstTerms]=[header]
                else:
                    padaIndex[firstTerms].append(header)
                    #print("Duplicate ",firstTerms," occurring in ",padaIndex[firstTerms],header)
                #print(header,padaList[0:4] )
                padaTOC[header]=firstTerms
                #padaOccurence=panchasat['header'].replace("TS ","")
                # print(panchasat['Content']

print("")
sno=1
padaTupleList=[]
for header in padaTOC.keys():
    
    firstTerms= padaTOC[header]
    listHeaders=padaIndex[firstTerms]
    if len(listHeaders)>1:
        listString = ' '.join(listHeaders)
        listString = listString.replace(header,"")
        
    else:
        listString = "_"
    #print(header, " - " ,firstTerms,listString)
    padaTuple=(sno,escape_for_latex(header),escape_for_latex(firstTerms),escape_for_latex(listString))
    padaTupleList.append(padaTuple)
    sno+=1

padaTemplateFileName="templates/TB_Index_main.tex"
CreatePdf(padaTemplateFileName,"TB","Index",padaTupleList)

sno=1
padaTupleList=[]
for item in sorted(padaIndex.keys()):
    if len(item) > 0:
        listString = ' '.join(padaIndex[item])

        padaTuple=(sno,escape_for_latex(item), escape_for_latex(listString))
        #print(padaTuple)
        padaTupleList.append(padaTuple)
        sno+=1
padaTemplateFileName="templates/TB_Index_Alphabetical_main.tex"
CreatePdf(padaTemplateFileName,"TB_Alphabetical","Index",padaTupleList)