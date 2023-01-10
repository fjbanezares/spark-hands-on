from pyspark.sql import SparkSession



# We have articles of Wikipedia in a Dataset
# We will create a ranking on what compute language is mentioned in more articles


# toDo read in Python a textfile and store the lines in a List
# We start by reading the data and storing the text in a variable called lines
# Use open("wikipedia-grading.dat", "r") function to read from the file
# use read_lines over the file object to iterate
# remember to close the file
###


# toDo create the SparkSession
# https://sparkbyexamples.com/pyspark/pyspark-what-is-sparksession/
# Create Spark Session from builder
# Use SparkSession object from Spark Python API (define a local number of executors)

#############################################

# toDO analyse how we pass from a line in Wikipedia text to a Wikipedia object
# Create WikipediaArticle Python Class
# I give you the code but please analyze and understand what we are doing and let me know
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
        # toDo what I am doing with this map, what is it affecting?
        listita = map((lambda x: x.strip(' ,:;{}')), self.text.split())
        # print(cadena)
        # b = list(listita)
        # print(b)
        return cadena in listita
#####################

# toDo I give you the code, please explain why we are caching the RDD?
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

# todo def numer_times_language_appear(prog_lan, rdd): ...
# give us the number of times the word prog_lan appears (in how many lines)
def numer_times_language_appear(prog_lan, rdd): ...


# toDo, using numer_times_language_appear we create following function; please explain what we are returning
def rank_langs(langs, rdd):
    map_of_appareances = {}
    for lang in langs:
        number_of_appareances = numer_times_language_appear(lang, rdd)
        map_of_appareances[lang] = number_of_appareances
    return map_of_appareances

# https://stackoverflow.com/questions/3783530/python-tuple-to-dict
# https://realpython.com/sort-python-dictionary/

# toDo finish this method similar to the rank_langs that returns the languages ordered in descending order
def rank_langs_list_ordered(langs, rdd):
    fin_list = list(map(lambda x:(x,numer_times_language_appear(x,rdd)), langs))
    map_from_list = dict(fin_list)
    ordered_by_value_desc = ...
    return ordered_by_value_desc


print(numer_times_language_appear("Java", rddWikipediaArticles))
list_of_languages = ["Java", "Scala", "Python"]
print(rank_langs_list_ordered(list_of_languages, rddWikipediaArticles))




# Esta es la parte dos donde vamos a crear un indice invertido y desde ahi resolver directamente el problema

# toDo Compute an inverted index of the set of articles, mapping each language to the Wikipedia pages in which it occurs.


pepito = WikipediaArticle("<page><title> Title of it </title><text> Java  Java Scala bla bla bla </text></page>")
def findLanguages(langs, article):
    # devuelvo lista con los lenguajes que aparecen en el articulo
    # para ello filtro los que
    return list(filter(lambda language:article.string_appearence_in_text(language), langs))

print(findLanguages(list_of_languages,pepito))

print(rddWikipediaArticles.flatMap(lambda articulo:findLanguages(list_of_languages, articulo)).take(500))


def generate_maps(article,langs):
    return list(map(lambda lang:(lang, article),findLanguages(langs, article)))

print(generate_maps(pepito,list_of_languages))


# toDo generate here the inverted index
def makeIndex(langs, rdd):  # RDD[(String, Iterable[WikipediaArticle])] =
    # primer paso veo los lenguajes que aparecen en el texto
    # para cada uno devuelvo el lenguaje y el articulo de la wikipedia
    # agrupo para que para cada lenguaje tengamos agrupados todos los articulos en los que aparece
    # usa flatMap que es una función que dada una entrada puede devolver varias salidas en el RDD de salida expandiendo
   return rdd.flatMap(lambda article:generate_maps(article,langs)).groupByKey()


# Test del indice
print(makeIndex(list_of_languages,rddWikipediaArticles).mapValues(lambda x: len(x)).collect())







# toDo final haciendo todo el trabajo en una sola funcion deduce (que combina groupBy ish y un aggregate ish)
# def rankLangsReduceByKey(langs: List[String], rdd: RDD[WikipediaArticle]): List[(String, Int)] = ???
def generate_maps(langs, article):
    return list(filter(lambda language:article.string_appearence_in_text(language), langs))


def rank_languages_using_reduce_by_key(langs, rdd):
    return rdd.flatMap((lambda article:generate_maps(article,langs))).reduceByKey()
rddWikipediaArticles.reduce()

#wikiArticles = rdd1.map
#  val wikiRdd: RDD[WikipediaArticle] = sc.parallelize(wikiArticles).map(x=>x).persist()

