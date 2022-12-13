

from pyspark.sql import SparkSession

from pyspark import RDD


# CSV -> RDD
# ((1, 6,   None, None, 140, Some(CSS)),  67)
# ((1, 42,  None, None, 155, Some(PHP)),  89)
# ((1, 72,  None, None, 16,  Some(Ruby)), 3)
# ((1, 126, None, None, 33,  Some(Java)), 30)
# ((1, 174, None, None, 38,  Some(C#)),   20)

# <postTypeId> Type 1 question, Type 2 answer
# <id>  post UUID
# <parentId> if an answer, id of the corresponding question; for a question, an empty string.
# <acceptedAnswer> UUID of the accepted answer post. This information is optional, so maybe be missing indicated by an empty string.
# <score> based on user votes
# <tag> if a question, programming language the post is about; for an answer, an empty string.

# Process:
# 1 generate RDD[Posting] for each CSV line
# 2 grouped: questions and answers grouped together, pairRDD with key the question and value the answers, then groupBy
# 3 scored: questions and scores, simple RDD:
# ((1, 6,   None, None, 140, Some(CSS)),  67)
# ((1, 42,  None, None, 155, Some(PHP)),  89)
# ((1, 72,  None, None, 16,  Some(Ruby)), 3)
# ((1, 126, None, None, 33,  Some(Java)), 30)
# ((1, 174, None, None, 38,  Some(C#)),   20)
# 4 vectors: pairs of (language, score) for each question

# The step 2 look obvious but it is expensive due to a lot of shuffling,
# maybe looks more trouble but in the end it is way more cheaper to just use a common question ID and partition by it
# Then we would be able to do the join without shuffling saving a ton of cost
# So instead of RDD[(Question, Iterable[Answer])] we will get RDD[(QID, Iterable[(Question, Answer))]
# To get there we generate RDD[id,Question] and RDD[parentId,Answer] and join (should be a left as the question is the main object)
# Now we would have RDD[(QID, (Question, Answer))] and with this
# From here we can produce RDD[(Question, HighScore)], just showing the highest score
# ((1, 6,   None, None, 140, Some(CSS)),  67)
# ((1, 42,  None, None, 155, Some(PHP)),  89)
# ((1, 72,  None, None, 16,  Some(Ruby)), 3)
# ((1, 126, None, None, 33,  Some(Java)), 30)
# ((1, 174, None, None, 38,  Some(C#)),   20)


class Posting:
    # Class WikipediaArticle, with this we will have an RDD of Wikipedia article objects instead of RDD of text
    # The object has as unique attribute the text in the line of the Wikipedia article
    def __init__(self, postingType, id, acceptedAnswer, parentId, score, tags):
        self.postingType = postingType
        self.id = id
        self.acceptedAnswer = acceptedAnswer
        self.parentId = parentId
        self.score = score
        self.tags = tags

    def __str__(self):
        return (self.postingType, self.id,self.acceptedAnswer,self.parentId,self.score,self.tags).__str__()

def postingFactory(line):
    arr = line.split(",")
    postingType = int(arr[0])
    id = int(arr[1])
    if arr[2].isnumeric():
        acceptedAnswer=int(arr[2])
    else:
        acceptedAnswer=0
    #acceptedAnswer = (0,int(arr[2]))[arr[2].isnumeric()]
    if arr[3].isnumeric():
        parentId=int(arr[3])
    else:
        parentId=0
    #parentId = (0,int(arr[3]))[arr[3].isnumeric()]
    score = int(arr[4])
    tags = ("", arr[5].strip())[len(arr) >= 6] # with strip() we remove the \n
    return Posting(postingType,id,acceptedAnswer,parentId,score,tags)

# Aliases
Question = Posting
Answer = Posting
QID = int
HighScore = int
LangIndex = int

# case class Posting(postingType: Int, id: Int, acceptedAnswer: Option[Int], parentId: Option[QID], score: Int, tags: Option[String]) extends Serializable


###
print("READING DATA")
text_file = open("stackoverflow.csv", "r")
lines = text_file.readlines()
print(type(lines)) # <class 'list'> we have a list of lines of text here
print(len(lines))  # 3000 articles from Wikipedia
print(lines[0])  # "<page><title> Title of it </title><text> bla bla bla </text></page>",
print(type(lines[0])) # str
text_file.close() # No longer need access to the  persisted data file
print("END READING DATA")
###

# Spark Session creation
spark = SparkSession.builder.master("local[2]").appName('ufv example Spark').getOrCreate()
stackOverflowArticles = spark.sparkContext.parallelize(lines)  # map(lambda line: Posting(line)).cache()

for row in stackOverflowArticles.take(5): print("An element on the RDD",row)

postingsRDD=stackOverflowArticles.map(lambda line: postingFactory(line)).cache()

for row in postingsRDD.take(5): print("An element on the RDD",row)

questionsRDD=postingsRDD.filter(lambda post:post.postingType==1).map(lambda question:(question.id, question))
for row in questionsRDD.take(5): print("An question on the RDD",row[1])

answersRDD=postingsRDD.filter(lambda post:post.postingType==2).map(lambda answer:(answer.parentId, answer))
for row in answersRDD.take(5): print("An answer on the RDD",row)

questionsAnswersRDD=questionsRDD.leftOuterJoin(answersRDD)
for row in questionsAnswersRDD.take(5): print("An answer on the RDD",row)




def answer_high_score(answers) -> int:
    high_score = 0
    i = 0
    while i < len(answers):
        score = answers[i].score
        if score > high_score:
            high_score = score
        i += 1
    return high_score


class KMeans:
    # Languages
    Langs=["JavaScript", "Java", "PHP", "Python", "C#", "C++", "Ruby", "CSS", "Objective-C", "Perl", "Scala", "Haskell", "MATLAB", "Clojure", "Groovy"]

    # K-means parameter: How "far apart" languages should be for the kmeans algorithm?  Must be greater than zero
    LangSpread = 50000

    # K-means parameter: Number of clusters
    KmeansKernels = 45

    # K-means parameter: Convergence criteria
    kmeansEta = 20.0

    # K-means parameter: Maximum iterations
    KmeansMaxIterations = 120

    # Parsing utilities:

    # Load postings from the given file
    # def rawPostings(lines: RDD[String]): RDD[Posting] =
    def rawPostings(lines: RDD[str]):
        def generatePostingFromLine(line):
            arr=line.split(",")
            return Posting(arr[0], arr[1], arr[2], arr[3], arr[4],arr[5])
        lines.map(lambda line: generatePostingFromLine(line))

    # Group the questions and answers together */
    # def groupedPostings(postings: RDD[Posting]): RDD[(QID, Iterable[(Question, Answer)])]
    def groupedPostings(postings: RDD[Posting]):
        return postings

    # Compute the maximum score for each posting */
  #  def scoredPostings(grouped: RDD[(QID, Iterable[(Question, Answer)])]): RDD[(Question, HighScore)] =

    def index_element_list(self, elem, ls):
        try:
            #search for the item
            index = ls.index(elem)
            #print('The index of', item,'in the list is:', index)
            return index
        except ValueError:
            print('item',elem,'not present')
            return -1
    # Compute the vectors for the kmeans
    #def vectorPostings(scored: RDD[(Question, HighScore)]): RDD[(LangIndex, HighScore)] =
    def vectorPostings(self, scored: RDD[(Question, HighScore)]) -> RDD[(LangIndex, HighScore)]:
        # Return optional index of first language that occurs in `tags`. */
        def firstLangInTag(tag, ls): return self.index_element_list(tag,ls)

        return firstLangInTag(scored,[1,2])











