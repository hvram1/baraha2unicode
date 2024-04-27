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

def padaVakhya_parseAction(tokens):
    print("In padaVakhya Action",tokens)

def ghanaVakhya_parseAction(tokens):
    print("In ghanaVakhya Action",tokens)


def samhitaGhana_parseAction(tokens):
    
    padamString=tokens['padam']
    serialNumber=tokens['serialNumber']
    ghanaVakhyaNumber=tokens['ghanaVakhyaNumber']
    ghanaVakhya=tokens['ghanaVakhya']
    info=tokens['info']
    if "||" in padamString:
        separator="||"
    else:
        separator="|"
    padaVakhyaToTransliterate=""
    link=""
    padam = re.split('\| | \|\|',padamString)
    #print("In samhitaGhana Action",tokens)
    stringToCheck =  padam[len(padam)-1]
    patterns = "GS|JD|JM|GD"
    patternResult = re.search(patterns,stringToCheck)
    if len(stringToCheck) >0:
        if (patternResult):
            padaVakhyaToTransliterate = separator.join(padam[:-1])
            padaVakhyaToTransliterate+=separator
            link=padam[-1]
            
        else:
            padaVakhyaToTransliterate = separator.join(padam)
    else:
        padaVakhyaToTransliterate = separator.join(padam)
    #print(stringToTranliterate)
    os1=transliterate(padaVakhyaToTransliterate,sanscript.BARAHA, sanscript.DEVANAGARI)
    os2=transliterate(ghanaVakhya,sanscript.BARAHA, sanscript.DEVANAGARI)
    kandaInformation=int(tokens['info']['kandaInformation'])
    prasnaInformation=int(tokens['info']['prasnaInformation'])
    anuvakkamInformation=int(tokens['info']['anuvakkamInformation'])
    panchasatInformation=int(tokens['info']['panchasatInformation'])
    newnode={"Vakhyam": {"id":serialNumber,"ghanaVakhyaId":ghanaVakhyaNumber,"padaVakhyam":os1,"ghanaVakhyam":os2,"reference":link}}
    
    node=parseTree['TS']['Kanda'][kandaInformation-1]['Prasna'][prasnaInformation-1]['Anuvakkam'][anuvakkamInformation-1]['Panchasat'][panchasatInformation-1]

    if node.get("GhanaPaatha") is None:
        node["GhanaPaatha"]=[]
    
    node["GhanaPaatha"].append(newnode)

    #print("In samhitaGhana Action",kandaInformation,serialNumber,ghanaVakhyaNumber,os1,os2,link)
# Largely built following the example and comments in
# https://stackoverflow.com/questions/55909620/capturing-block-over-multiple-lines-using-pyparsing
# and
# https://stackoverflow.com/questions/15938540/how-can-i-do-a-non-greedy-backtracking-match-with-oneormore-etc-in-pyparsing
pp.enable_diag(pp.Diagnostics.enable_debug_on_named_expressions)

EOL = pp.LineEnd()
EmptyLine = pp.Suppress(pp.LineStart() + EOL)
EmptyLines=pp.OneOrMore(EmptyLine)


TaitriyaSamhitaAbbreviation = pp.CaselessLiteral("TS")
kandaInformation = pp.Word(pp.nums).setResultsName("kandaInformation")
prasnaInformation = pp.Word(pp.nums).setResultsName("prasnaInformation")
anuvakamInformation = pp.Word(pp.nums).setResultsName("anuvakkamInformation")
panchasatInformation = pp.Word(pp.nums).setResultsName("panchasatInformation")

serialNumber = pp.Word(pp.nums).setResultsName("serialNumber")
serialNumber_1 = pp.Word(pp.nums).setResultsName("serialNumber_1")
ghanaVakhyaNumber = pp.Word(pp.nums).setResultsName("ghanaVakhyaNumber")

DocfamilyName1 = pp.CaselessLiteral("Ghanam") 
DocfamilyName2 = pp.CaselessLiteral("Ghanam Baraha")
DocfamilyName = DocfamilyName2 | DocfamilyName1
versionInformation = pp.SkipTo(EOL)
versionInfoLine = TaitriyaSamhitaAbbreviation + kandaInformation +\
                  pp.CaselessLiteral(".") + prasnaInformation +\
                  DocfamilyName + pp.CaselessLiteral("-") + versionInformation +EOL
#versionInfoLine = "TS 1.1 Ghanam - Ver 1.0 dt 31st Jan 2023"
metaInformation = pp.SkipTo(EOL).setResultsName("metaInformation")
padaSeparator1 = pp.CaselessLiteral("|").setResultsName("separator1")
padaSeparator2 = pp.CaselessLiteral("||").setResultsName("separator2")
padaSeparator = padaSeparator1 | padaSeparator2
padam = (~padaSeparator + pp.OneOrMore(pp.Word(pp.printables,exclude_chars='| '),stopOn=padaSeparator)).setResultsName("padam",listAllMatches=True) + padaSeparator
padaVakhya_prefix_1=serialNumber+pp.CaselessLiteral(")").suppress() +\
              pp.Group(kandaInformation+pp.CaselessLiteral(".") +\
                         prasnaInformation+pp.CaselessLiteral(".") +\
                         anuvakamInformation+pp.CaselessLiteral(".") +\
                         panchasatInformation
                         ).setResultsName("info") +\
              pp.CaselessLiteral("(").suppress()+ghanaVakhyaNumber+pp.CaselessLiteral(")").suppress()+\
              pp.CaselessLiteral("-").suppress()

padaVakhya_prefix_2=pp.CaselessLiteral("(").suppress()+serialNumber+pp.CaselessLiteral(")").suppress() +\
            pp.CaselessLiteral("[P").suppress()+serialNumber_1+pp.CaselessLiteral("]").suppress() +\
              pp.Group(kandaInformation+pp.CaselessLiteral(".") +\
                         prasnaInformation+pp.CaselessLiteral(".") +\
                         anuvakamInformation+pp.CaselessLiteral(".") +\
                         panchasatInformation
                         ).setResultsName("info") +\
              pp.CaselessLiteral("(").suppress()+ghanaVakhyaNumber+pp.CaselessLiteral(")").suppress()+\
              pp.CaselessLiteral("-").suppress()

padaVakhya_prefix = padaVakhya_prefix_1 | padaVakhya_prefix_2

padaVakhya = padaVakhya_prefix + pp.SkipTo(EOL).setResultsName("padam") + EOL.suppress()

mangalaVakhya = pp.OneOrMore(pp.CaselessLiteral("=")).suppress()+pp.CaselessLiteral("subam").setResultsName("mangalam")+pp.OneOrMore(pp.CaselessLiteral("=").suppress())+EOL.suppress()
ghanaVakhya = pp.Combine((pp.SkipTo("|")+pp.OneOrMore(pp.CaselessLiteral("|")))).setResultsName("ghanaVakhya")+EOL.suppress()

samhitaGhana = pp.Optional(EmptyLines) +\
        padaVakhya +\
        ghanaVakhya
padaVakhya.setName("padaVakhya")
ghanaVakhya.setName("ghanaVakhya")
versionInfoLine.setName("VersionInfo")
mangalaVakhya.setName("mangalaVakhya")

padaVakhya.setParseAction(padaVakhya_parseAction)

ghanaVakhya.setParseAction(ghanaVakhya_parseAction)

samhitaGhana.setParseAction(samhitaGhana_parseAction)

parser = versionInfoLine + \
         pp.OneOrMore(samhitaGhana,stopOn=mangalaVakhya)+\
        mangalaVakhya
ts_string = Path("TS_withPada.json").read_text(encoding="utf-8")
parseTree = json.loads(ts_string)
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
json_file_name = "TS_withPadaGhana.json"
#print(parseTree)
my_json = json.dumps(parseTree,indent=3,ensure_ascii=False, sort_keys=True)
my_json = my_json.replace("\uA8E3","\u1CDA")
with open(json_file_name, "w") as f:
    f.write(my_json)

