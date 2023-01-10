from pyspark.sql import SparkSession

# WikipediaArticle class has inner method to say if a text is in the article or not
class WikipediaArticle:
    # Class WikipediaArticle, with this we will have an RDD of Wikipedia article objects instead of RDD of text
    # The object has as unique attribute the text in the line of the Wikipedia article
    def __init__(self, textInput):
        # The __init__ function is called when an object of this class is created.
        # It takes in a string as input, which represents the text of a Wikipedia article

        # Separate the title and text of the article by finding the index of the string "</title><text>"
        subs = "</title><text>"
        index = textInput.index(subs)  # index of separator tittle-text

        # The title of the article is everything from the 14th character (index 13) to the index of the separator string
        self.title = textInput[14: index]

        # The text of the article is everything from the index of the separator string to the end of the input string, minus the last 14 characters
        self.text = textInput[index + len(subs): len(textInput)-14]

    # The __str__ function is called when an object of this class is passed to the print function
    # It returns the text of the article as a string
    def __str__(self):
        return self.text

    # This function takes in a string as input and returns a boolean indicating if the string appears in the text of the Wikipedia article
    def string_appearence_in_text(self, cadena):
        # Split the text of the article into a list of individual words, stripping away any punctuation
        listita = map((lambda x: x.strip(' ,:;{}')), self.text.split())

        # Check if the input string appears in the list of words
        return cadena in listita


# We start by reading the data and storing the text in a variable called lines
print("READING DATA")

# Open the file in read mode
text_file = open("wikipedia-grading.dat", "r")

# Read all the lines of the file and store them in a list called lines
lines = text_file.readlines()

# Print the type of the object 'lines' to check that it is a list
print(type(lines))

# Print the length of the list 'lines' to check that it contains 3000 articles
print(len(lines))

# Print the first element of the list 'lines' to check its format
print(lines[0])

# Print the type of the first element of the list 'lines' to check that it is a string
print(type(lines[0]))

# Close the file, we no longer need access to the persisted data file
text_file.close()

# Print a message to show that the data reading process has ended
print("END READING DATA")



# Create Spark Session from builder
spark = SparkSession.builder.master("local[1]") \
    .appName('ufv example Spark') \
    .getOrCreate()

# Create RDD of WikipediaArticle objects using the lines of text as input
# The WikipediaArticle class is defined earlier in the code
rddWikipediaArticles = spark.sparkContext.parallelize(lines).map(lambda line: WikipediaArticle(line)).cache()

# cache() is used to store the RDD in memory, so that future actions on the RDD will be much faster


# The function numer_times_language_appear takes in two arguments:
# a string prog_lan representing a programming language and
# an RDD rdd representing a list of Wikipedia articles.
# The function returns the number of times the programming language prog_lan appears in the
# text of any of the Wikipedia articles in the RDD rdd.

# The function first filters the RDD rdd by calling the filter method and passing in a lambda function as an argument.
# The lambda function takes in an object article and returns a boolean value indicating whether
# the programming language prog_lan appears in the text of the Wikipedia article represented by article.
# This filtered RDD is then counted using the count method and the result is returned by
# the numer_times_language_appear function.
def numer_times_language_appear(prog_lan, rdd):
# To know how many times a language appears in a line of the RDD
    return rdd.filter(lambda article: article.string_appearence_in_text(prog_lan)).count()


# This function takes in two arguments: a list of languages called "langs" and an RDD called "rdd".
# It creates an empty dictionary called "map_of_appearances" which will be used to store the
# number of times each language appears in the RDD.
# It then iterates through each language in the "langs" list and calls the "numer_times_language_appear" function,
# passing in the current language and the RDD as arguments.
# This function returns the number of times the language appears in the RDD,
# which is stored in the "number_of_appearances" variable.
# The language and its number of appearances are then added to the "map_of_appearances" dictionary as a key-value pair.
# Once all languages have been processed, the "map_of_appearances" dictionary is returned.
def rank_langs(langs, rdd):
    map_of_appareances = {}
    for lang in langs:
        number_of_appareances = numer_times_language_appear(lang, rdd)
        map_of_appareances[lang] = number_of_appareances
    return map_of_appareances
