from nltk import data, ChartParser
from nltk import pos_tag
from nltk.corpus import inaugural

data.clear_cache()
G = data.load("file:mygrammar.cfg")
RDP = ChartParser(G)

# extract_short_sents :: Int?, Int?, Corpus?-> [[(String, String)]]
def extract_short_sents(num=8, max_len=8, corpus=inaugural):
	li = []
	num = num if num < len(corpus.fileids()) else len(corpus.fileids())
	
	for i in range(num):
		for sent in corpus.sents(corpus.fileids()[i]):
			if len(sent) <= max_len:
				li.append(pos_tag(sent))
				if len(li)/3.0 == i:
					break
	
	return li

# parse :: String -> ParseTree
def parse(s):
    return RDP.parse(s.split())

if __name__ == "__main__":
	sents = [	"We will show purpose without arrogance",
				"Every child must be taught these principles",
				"Communications and commerce are global",
				"I believe America can be better",
				"It ought therefore to be cherished",
				"That false philosophy is communism",
				"I do not mistrust the future",
				"The entire remedy is with the people",
				"It must be earned",
				"They are serious and they are many",
				"So it has been",
				"This can be such a moment",
				"And what a century it has been",
				"God bless you and welcome back",
				"The path of progress is seldom smooth",
				"The Bill of Rights remains inviolate",
				"Yet those divisions do not define America",
				"We are one nation and one people",
				"Agriculture has languished and labor suffered",
				"We crave friendship and harbor no hate",
				"We did those first things first",
				"Universal suffrage should rest upon universal education",
				"These favorable anticipations have been realized",
				"We are following the course they blazed"
			]

	parses = map(parse, sents)
	
	for sent in sents:
		print "%s:\t\"%s\"" % ("parse fails" if not parses[sents.index(sent)] else "parses fine", sent)
	
#End of file
