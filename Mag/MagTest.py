# Aim : Generating people, situations

Jobs = [ "%d"%x for x in range(30) ]

Capa = {}
for job in Jobs :
	Capa[job] = 15


i = 1
Pop = {}

for job in Jobs :
	Pop[ job ] = 2*i 
	i+=1


RandomList = {}
i = 0
for job in Jobs :
	for x in xrange( Pop[ job ] ) :
		RandomList[i] = job 
		i += 1

def getRandomJob() :
	import random
	i = random.randrange( 0, len( RandomList ) - 1 )
	return RandomList[i]


def getRandomChoices() :
	L = []
	S = set()
	i = 0
	for x in xrange( len( Jobs ) ):
		job = getRandomJob()
		while job in S :
			job = getRandomJob()
		S.add( job )
		L.append ( job )

	return L


	

People = [ "%d"%x for x in range(300) ] 

for joe in People :
	print joe

print "."

for job in Jobs :
	print "%s %d"%( job, Capa[job] )

print "."
for joe in People :
	print "%s "%joe + " ".join( getRandomChoices() )


	





