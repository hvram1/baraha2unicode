# \VAR{prasna['section'].strip()} #

_\VAR{prasna['invocation'].strip()}_


\BLOCK{ for anuvakkam in prasna['Anuvakkam']}
\BLOCK{ for panchasat in anuvakkam['Panchasat']}


# \VAR{ panchasat['header'].strip()} #

\BLOCK{ if panchasat.get("SamhitaPaata") }
## Samhita Paata ##

\VAR{ panchasat['SamhitaPaata'].strip() }
\BLOCK{ endif }

\BLOCK{ if panchasat.get("PadaPaata") }
## Pada Paata ##

\VAR{ panchasat['PadaPaata'].strip() }  
\BLOCK{ endif }

\BLOCK{ if panchasat.get("KramamPaatha") }
## Krama Paata ##

\BLOCK{ for Vakhyam in panchasat.KramamPaatha}
***\VAR{Vakhyam['Vakhyam']['kramamVakhyam'].strip()}***
\BLOCK{endfor}
\BLOCK{ endif }

\BLOCK{ if panchasat.get("JataiPaatha") }
## Jatai Paata ##

\BLOCK{ for Vakhyam in panchasat.JataiPaatha}
***\VAR{Vakhyam['Vakhyam']['jataiVakhyam'].strip()}***
\BLOCK{endfor}
\BLOCK{ endif }

\BLOCK{ if panchasat.get("GhanaPaatha") }
## Ghana Paata ##

\BLOCK{ for Vakhyam in panchasat.GhanaPaatha}
***\VAR{Vakhyam['Vakhyam']['ghanaVakhyam'].strip()}***
\BLOCK{endfor}
\BLOCK{ endif }

\BLOCK{endfor}
\BLOCK{endfor}




