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
global_identifier["kandaInformation"]  = global_identifier["prasnaInformation"] = global_identifier["anuvakkamInformation"] = global_identifier["panchasatInformation"] =0

def initialInformation_parseAction(tokens):
    print("In initialInformatio Action",tokens)

def kramaHeader_parseAction(tokens):
    #print("In kramaHeader",tokens)
    for key in tokens.keys():
        #print(key, tokens[key])
        global_identifier[key] = int(tokens[key])


def kramam_parseAction(tokens):
    
    #print("In kramam Action",tokens)
    #for key in tokens.keys():
    #    print(key, tokens[key])
    #print("In samhitaGhana Action",tokens)
    kramaVakhyaToTransliterate=tokens['kramam']
    os1=transliterate(kramaVakhyaToTransliterate,sanscript.BARAHA, sanscript.DEVANAGARI)
    kandaInformation=global_identifier["kandaInformation"]
    prasnaInformation=global_identifier["prasnaInformation"]
    anuvakkamInformation=global_identifier["anuvakkamInformation"]
    panchasatInformation=global_identifier["panchasatInformation"]

    newnode={"Vakhyam": {"kramamVakhyam":os1}}
    
    node=parseTree['TS']['Kanda'][kandaInformation-1]['Prasna'][prasnaInformation-1]['Anuvakkam'][anuvakkamInformation-1]['Panchasat'][panchasatInformation-1]

    if node.get("KramamPaatha") is None:
        node["KramamPaatha"]=[]
    
    node["KramamPaatha"].append(newnode)

    #print("In samhitaGhana Action",kandaInformation,serialNumber,ghanaVakhyaNumber,os1,os2,link)
# Largely built following the example and comments in
# https://stackoverflow.com/questions/55909620/capturing-block-over-multiple-lines-using-pyparsing
# and
# https://stackoverflow.com/questions/15938540/how-can-i-do-a-non-greedy-backtracking-match-with-oneormore-etc-in-pyparsing
pp.enable_diag(pp.Diagnostics.enable_debug_on_named_expressions)

EOL = pp.LineEnd()
EmptyLine = pp.Suppress(pp.LineStart() + EOL)
EmptyLines=pp.OneOrMore(EmptyLine)


TaitriyaSamhitaAbbreviation = pp.CaselessLiteral("T.S.")
kandaInformation = pp.Word(pp.nums).setResultsName("kandaInformation")
prasnaInformation = pp.Word(pp.nums).setResultsName("prasnaInformation")
anuvakamInformation = pp.Word(pp.nums).setResultsName("anuvakkamInformation")
panchasatInformation = pp.Word(pp.nums).setResultsName("panchasatInformation")

padanumber1 = pp.Word(pp.nums).setResultsName("padanumber1")
padanumber2 = pp.Word(pp.nums).setResultsName("padanumber2")
panchasatInformation = pp.Word(pp.nums).setResultsName("panchasatInformation")



padaSeparator1 = pp.CaselessLiteral("|").setResultsName("separator1")
padaSeparator2 = pp.CaselessLiteral("||").setResultsName("separator2")
padaSeparator = padaSeparator1 | padaSeparator2

kramaHeader = TaitriyaSamhitaAbbreviation+kandaInformation.setResultsName("kandaInformation")+pp.CaselessLiteral(".") +\
                         prasnaInformation+pp.CaselessLiteral(".") +\
                         anuvakamInformation+pp.CaselessLiteral(".") +\
                         panchasatInformation+pp.CaselessLiteral("- kramam")+EOL

kramaHeader.setParseAction(kramaHeader_parseAction)
endPada = (panchasatInformation + \
          pp.CaselessLiteral("(")+\
          padanumber1+pp.CaselessLiteral("/") + padanumber2 + pp.CaselessLiteral(")") +\
          EOL +\
          pp.SkipTo(EOL)+EOL).setResultsName("endPada")

initialWords = pp.Word(pp.alphanums+"-\.()~")
initialInformation = pp.OneOrMore(initialWords,stopOn=TaitriyaSamhitaAbbreviation)

#initialInformation.setParseAction(initialInformation_parseAction)

kramam = pp.SkipTo(padaSeparator+panchasatInformation ).setResultsName("kramam")
kramam.setParseAction(kramam_parseAction)

kramamPara = kramaHeader + kramam + padaSeparator + endPada

endInformation = pp.CaselessLiteral("prasna korvai with starting padams")


parser = initialInformation + \
         pp.OneOrMore(kramamPara,stopOn=endInformation)+\
        endInformation
ts_string = Path("TS_withPadaGhanaJatai.json").read_text(encoding="utf-8")
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
json_file_name = "TS_withPadaGhanaJataiKrama.json"
#print(parseTree)
my_json = json.dumps(parseTree,indent=3,ensure_ascii=False, sort_keys=True)
my_json = my_json.replace("\uA8E3","\u1CDA")
with open(json_file_name, "w") as f:
    f.write(my_json)

