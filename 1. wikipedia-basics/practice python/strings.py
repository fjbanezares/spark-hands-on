print(" separator ".join(["hello", "world"]))
print(" ".join(["hello", "world"]))

wikiexample = "<page><title>Mimoxenolea</title><text>{{italic title}} {{Taxobox | regnum = [[Animal]]ia | phylum = [[Arthropod]]a | classis = [[Insect]]a | ordo = [[Beetle|Coleoptera]] | subordo = [[Polyphaga]] | familia = [[Cerambycidae]] | genus = '''''Mimoxenolea''''' }} '''''Mimoxenolea''''' is a genus of [[beetle]]s in the family [[Cerambycidae]], containing the following species:<ref>[http://www.biolib.cz/en/taxon/id11377/ Acanthocinini].  Retrieved on 8 September 2014.</ref>  * ''[[Mimoxenolea bicoloricornis]]'' <small>Breuning, 1960</small> * ''[[Mimoxenolea ornata]]'' <small>(Breuning, 1961)</small> * ''[[Mimoxenolea sikkimensis]]'' <small>(Breuning, 1961)</small>  ==References== {{reflist}}  [[Category:Acanthocinini]]  {{Acanthocinini-stub}}</text></page>"

subs = "</title><text>"
# https://www.programiz.com/python-programming/methods/string/index
index = wikiexample.index(subs)
print(index)
title = wikiexample[13: index]
print(title)
text  = wikiexample[index + len(subs): len(wikiexample)-14]
print(text)
string = "Geeksforgeeks"
print(len(string))
# private[wikipedia] def parse(line: String): WikipediaArticle =
# val subs = "</title><text>"
# val i = line.indexOf(subs)
# val title = line.substring(14, i)
# val text  = line.substring(i + subs.length, line.length-16)
# WikipediaArticle(title, text)