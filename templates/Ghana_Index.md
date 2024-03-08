


# \VAR{kanda['title'].strip()} #

\BLOCK{ for prasna in kanda['Prasna']}
# \VAR{prasna['section'].strip()} #




\BLOCK{ for anuvakkam in prasna['Anuvakkam']}
[_Anuvakkam-\VAR{ anuvakkam['id']}_]
\BLOCK{ for panchasat in anuvakkam['Panchasat']}
\BLOCK{ if panchasat.get("GhanaPaatha") }
[Panchasat \VAR{ panchasat['id']}](Kanda-\VAR{ kanda['id']}/\VAR{ panchasat['header'].strip() | replace (" ","_")}.md),
\BLOCK{ else}
\VAR{ panchasat['header'].strip()}

\BLOCK{ endif}
\BLOCK{endfor}





\BLOCK{endfor}
\BLOCK{endfor}




