from pyspark.sql import SparkSession





# We have articles of Wikipedia in a Dataset
# Our
# https://sparkbyexamples.com/pyspark/pyspark-what-is-sparksession/


# We start by reading the data and storing the text in a variable called lines
print("READING DATA")
text_file = open("wikipedia-grading.dat", "r")
lines = text_file.readlines()
print(type(lines)) # <class 'list'> we have a list of lines of text here
print(len(lines))  # 3000 articles from Wikipedia
print(lines[0])  # "<page><title> Title of it </title><text> bla bla bla </text></page>",
print(type(lines[0])) # str
text_file.close() # No longer need access to the  persisted data file
print("END READING DATA")
###


# Create Spark Session from builder
spark = SparkSession.builder.master("local[1]") \
    .appName('ufv example Spark') \
    .getOrCreate()
#############################################


class WikipediaArticle:
    # Class WikipediaArticle, with this we will have an RDD of Wikipedia article objects instead of RDD of text
    # The object has as unique attribute the text in the line of the Wikipedia article
    def __init__(self, textInput):
        subs = "</title><text>"
        index = textInput.index(subs)  # index of separator tittle-text
        self.title = textInput[14: index]  # tittle starts at index 13
        self.text = textInput[index + len(subs): len(textInput)-14]

    def __str__(self):
        return self.text


    def string_appearence_in_text(self, cadena):
        # Just we say if cadena appears in the text
        listita = map((lambda x: x.strip(' ,:;{}')), self.text.split())
        # print(cadena)
        # b = list(listita)
        # print(b)
        return cadena in listita
#####################

# CACHING
# The most important outcome here is, whenever you are going to use something several times, use cache()
# if not you will have to build the rdd every time you use it, huge inefficiency
rddWikipediaArticles = spark.sparkContext.parallelize(lines).map(lambda line: WikipediaArticle(line)).cache()
# This Map should be fast but once you have calculated, if we use this many times, why repeat ourselves?

# Some testing in the middle of the code to see what we are doing works fine
# Would be more pro to have another .py with tests keeping this cleaner

###########################
list5 = rddWikipediaArticles.take(5)

for elem in list5:
    print("Title... ",elem.title)
    print("Text... ",elem.text)
    # print(type(elem))  # <class '__main__.WikipediaArticle'>
    print(elem.string_appearence_in_text("Atherton"))

###################


def numer_times_language_appear(prog_lan, rdd):
    # To know how many times a language appears in a line of the RDD
    return rdd.filter(lambda article: article.string_appearence_in_text(prog_lan)).count()


def rank_langs(langs, rdd):
    map_of_appareances = {}
    for lang in langs:
        number_of_appareances = numer_times_language_appear(lang, rdd)
        map_of_appareances[lang] = number_of_appareances
    return map_of_appareances

# https://stackoverflow.com/questions/3783530/python-tuple-to-dict
# https://realpython.com/sort-python-dictionary/


def rank_langs_list_ordered(langs, rdd):
    fin_list = list(map(lambda x:(x,numer_times_language_appear(x,rdd)), langs))
    map_from_list = dict(fin_list)
    ordered_by_value_desc = dict(sorted(map_from_list.items(), key=lambda item: item[1], reverse=True))
    return ordered_by_value_desc


print(numer_times_language_appear("Java", rddWikipediaArticles))
list_of_languages = ["Java", "Scala", "Python"]
print(rank_langs_list_ordered(list_of_languages, rddWikipediaArticles))

# Compute an inverted index of the set of articles, mapping each language
# to the Wikipedia pages in which it occurs.

pepito = WikipediaArticle("<page><title> Title of it </title><text> Java  Java Scala bla bla bla </text></page>")
def findLanguages(langs, article):
    # devuelvo lista con los lenguajes que aparecen en el articulo
    # para ello filtro los que
    return list(filter(lambda language:article.string_appearence_in_text(language), langs))

print(findLanguages(list_of_languages,pepito))

print("flatMap nos devuelve...",rddWikipediaArticles.flatMap(lambda articulo:findLanguages(list_of_languages, articulo)).take(50), "el RDD de los lenguajes ")

def generate_maps(article,langs):
    # genero la lista de lenguajes de un articulo
    # luego para cada uno mapeo el lenguaje y el articulo
    return list(map(lambda lang:(lang, article),findLanguages(langs, article)))

print("generate maps devuelve...",generate_maps(pepito,list_of_languages), "mapeo del lenguage y el articulo")



def makeIndex(langs, rdd):  # RDD[(String, Iterable[WikipediaArticle])] =
    # primer paso veo los lenguajes que aparecen en el texto
    # para cada uno devuelvo el lenguaje y el articulo de la wikipedia
    # agrupo para que para cada lenguaje tengamos agrupados todos los articulos en los que aparece
   return rdd.flatMap(lambda article:generate_maps(article,langs)).groupByKey()


# Test del indice
# Mirad que la clave es por ejemplo Python y el valor una lista con todos los articulos en los que aparezca Python nombrado
# con un simple mapValues somos capaces de generar el ranking de forma immediate
print(makeIndex(list_of_languages,rddWikipediaArticles).mapValues(lambda x: len(x)).collect())





# toDo final

def generate_ones (article,langs):
    # muy similar a generate_maps pero en vez del articulo pongo un uno
    return list(map(lambda lang:(lang, 1),findLanguages(langs, article)))



def rank_languages_using_reduce_by_key(langs, rdd):
    return rdd.flatMap((lambda article:generate_ones(article,langs))).reduceByKey(lambda a,b:a+b).collect()

print("comprobar que funciona", rank_languages_using_reduce_by_key(list_of_languages,rddWikipediaArticles))
#wikiArticles = rdd1.map
#  val wikiRdd: RDD[WikipediaArticle] = sc.parallelize(wikiArticles).map(x=>x).persist()

# toDo, ver ahora quien es mas rapido descartando el indice invertido

# Import time module
def medir_tiempo(accion):
    import time
    # record start time
    start = time.time()
    print("START...", start)
    variable_retorno = accion
    print("variable_entorno...",variable_retorno)
    # record end time
    end = time.time()
    print("END...", end)

    # print the difference between start
    # and end time in milli. secs
    print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")

    return variable_retorno


# haciendo 3 filtros
print("con 3 filtros...",medir_tiempo(rank_langs_list_ordered(list_of_languages, rddWikipediaArticles)))


# con un ReduceByKey
print("con reduceByKey...",medir_tiempo(rank_languages_using_reduce_by_key(list_of_languages,rddWikipediaArticles)))

# con II
index = makeIndex(list_of_languages,rddWikipediaArticles).persist()
print(index.collect())
# que pasa si no pongo persist()
print("con II...",medir_tiempo(index.mapValues(lambda x: len(x)).collect()))



