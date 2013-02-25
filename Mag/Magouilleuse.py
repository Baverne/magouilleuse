import os,sys

class MagouilleuseException ( Exception ):
	pass


class Magouilleuse :
	def __init__( self, missing_wishes="equalize" ) :
		self.Slots = {}
		self.SlotIndexes = {}
		self.People = {}
		self.PeopleIndexes = {} 
		self.Wishes = {} 				# Where A:L means L is the ordered collection of jobs, by decreasing preference of guy A.
		self.Popularity = {} 		# Where A:i means : Job A has been seen i times as fisrt choice.
		self.Capacity = {}			# Where A:c means Job A has room for c guys.
		self.Inabilities = {} 	# Where A:L means : A can't do jobs in L.
		self.Equalities = {}		# Where A:L means guy A makes no differences inside job sequences in L.

		if missing_wishes != "complete" and missing_wishes != "equalize" :
			raise MagouilleuseException ( "Unknown missing wishes parameter value." )

		self.missing_wishes = missing_wishes 


# Input : Slot -> self.Capacity mapping.
# Provides the same mapping, and index -> slot,index mapping.
	def fill_Slots (self, iterable ) :
		if self.Slots :
			raise MagouilleuseException ( "Trying to fill slots dict twice...")

		i = 0
		j = 0
		for e in iterable :
			for x in xrange( iterable[e] ) :
				self.Slots[ i ] = e
				i += 1

			self.SlotIndexes[ e ] = j
			j += 1

			self.Capacity[ e ] = iterable[e]
		
			if not self.Popularity.has_key( e ) :
				self.Popularity[ e ] = 0
		
		

# Input : peoples list.
	def fill_People (self, iterable ) :
		if self.People :
			raise MagouilleuseException ( "Trying to fill people dict twice.")

		i = 0
		for e in iterable :
			self.People[ i ] = e
			self.PeopleIndexes [ e ] = i
			i += 1


	def fill_Equalities( self, mapping ) :
		for guy, L in mapping.items():
			if guy not in self.PeopleIndexes :
				raise MagouilleuseException( "Unknown guy in equality list" )
			for jobList in L :
				for job in jobList :
					if not job in self.SlotIndexes :
						raise MagouilleuseException( "Unknown slot in equality list" )
			self.Equalities[ guy ] = L


# Input : mapping : people -> wish list 
	def fill_Wishes (self, iterable ) :
		# Eliminating dummy wish mappings
		if self.Wishes:
			raise MagouilleuseException ( "Trying to fill wishes twice") 
		# Nothing in the collection
		if len( iterable ) == 0 :
			raise MagouilleuseException( "Empty wishes collection.")
		# Everyone must make a choice
		if len( iterable ) < len( self.PeopleIndexes ) :
			raise MagouilleuseException( "Incomplete wishes collection.")
		
		#
		for e in iterable :
			# Checking guy validity
			if not self.PeopleIndexes.has_key( e ) :
				raise MagouilleuseException( "Whish "+ str( (e, iterable[e]) ) +" not in People." )
			if not iterable[e] :
				raise MagouilleuseException( "Empty wish list for " + e + "." )
			# Checking the validity of each job.
			for slot in iterable[e] :
				if not self.SlotIndexes.has_key( slot ):
					raise MagouilleuseException( "Whish "+ str( (e, iterable[e]) ) +" has slot "+ str(slot) + " not in Slots."  )
			# Check if list complete :
			for job in self.SlotIndexes :
				if job not in iterable[e] :
					if VERBOSE :
						print >>sys.stderr, "Warning : "+e+" The bastard didnt choose " + job
					if self.missing_wishes == "complete" :
						if not isinstance( iterable[e], list ) :
							iterable[e] = [ x for x in iterable[e] ]
						iterable[e].append( job )

	

			self.Wishes[ e ] = iterable[e]
			g = iterable[e][0]
			if not self.Popularity.has_key( g ) :
				self.Popularity[ g ] = 0
			self.Popularity[ g ] += 1

	def fill_Inabilities( self, iterable ) :
		for people,slot in iterable :
			# Checking guy.
			if not people in self.PeopleIndexes :
				raise MagouilleuseException( "Unknown guy : " + people )
			# Checking job.
			if not slot in self.SlotIndexes :
				raise MagouilleuseException( "Unknown Slot : " + slot )
			
			if not people in self.Inabilities :
				self.Inabilities[people] = [slot]
			else :
				self.Inabilities[people].append( slot )
	


# Checks :

# Check if the bastard completed its choices list correctly :
# Check if the bastard used twice the same choice :
# Check for empty jobs...




# The cost, returns a list of cost values, in choice order.
	def popularity_cost(self, slot_collection ) :
		# Here lays the definition of the cost function.
		L = []
		i = 0

		for slot in slot_collection :
			L.append( ( ( i )**2 ))
			i += float(self.Capacity[slot]) / max( self.Popularity[slot], 1 )
		
		if len( slot_collection ) < len( self.SlotIndexes ) :
			if self.missing_wishes != "equalize" :
				raise MagouilleuseException( "Unrecoverable wish missing in wishes : "+ slot_collection )
			for x in xrange( len( self.SlotIndexes ) - len( slot_collection ) ) :
				L.append( L[-1] ) 

		return L

	def people_order (self, p1, p2 ) :
		return self.PeopleIndexes[p1] - self.PeopleIndexes[p2]


	def slots_order(self, s1, s2 ) :
		return self.SlotIndexes[s1] - self.SlotIndexes[s2]

	# Matrix description : A line will be one person.

	# A function which returns a line of the matrix given a People name and an ordered collection of slots :
	# It must reorder ans duplicate the usefulnesses, so that it matches the future matrix order.
	

	def getJoesLine(self, joe, joe_choices, cost=None ) :
		if cost is None :
			cost = self.popularity_cost
		mixed_list = []
		cost_list = cost( joe_choices )
		if len( joe_choices ) < len( self.SlotIndexes ) :
			joe_choices = [ x for x in joe_choices ]
			# Careful here, looping on SlotIndexes mapping returns actual names ( keys )
			for x in self.SlotIndexes :
				if x not in joe_choices :
					joe_choices.append( x )

				
		# creates a ( slot, cost ) list.
		for i,e in enumerate(joe_choices) :
			mixed_list.append( (e, cost_list[i]) ) 

		# Sort it according to slot order.
		mixed_list.sort( cmp = lambda e1,e2 : self.slots_order( e1[0], e2[0] ) )
		sorted_list = []

		# Takes inabilities into account :
		for slot, cost in mixed_list :
			if joe in self.Inabilities and  slot in self.Inabilities[joe] :
				sorted_list.append( (slot,sys.maxint) ) 

			else :
				sorted_list.append( (slot,cost) )

		# Duplicates the entries according to the capacity of the slots.
		duplicate_list = []
		for slot, cost in sorted_list :
			for j in xrange( self.Capacity[slot] ) :
				duplicate_list.append( cost )

		
		return duplicate_list

	
	def addNobody (self,x ):
		i = len( self.People )
		self.People[ i ] = "Nobody%d"%x
		self.PeopleIndexes[ "Nobody%d"%x ] = i


	def getEveryoneLines(self) :
		people_list = self.People.items()

		people_list.sort( cmp=lambda x,y : x[0] - y[0] )
	
		Matrix = []
		for people_id, people in people_list :
			if people.startswith("Nobody") :
				Matrix.append( [ 0 for x in xrange( len( self.Slots ) ) ] )
				continue
			Matrix.append( self.getJoesLine( people, self.Wishes[people] ) )
	
		if len(Matrix) > len ( Matrix[0] ) :
			raise MagouilleuseException("Too many candidates !!!" )

		if len(Matrix) < len ( Matrix[0] ) :
			for x in xrange ( len(Matrix[0] ) - len( Matrix ) ) :
				self.addNobody(x)
				Matrix.append( 
					[ 0 for x in xrange( len( self.Slots ) ) ]
					)

		return Matrix

	

	def decodPeopleSlot( self, args ) :
		R = []
		for arg in args :
			R.append ( ( self.People[ arg[0] ], self.Slots[arg[1]] ) )
		return R

	def equalizeChoicesIn ( self, m ):
		for guy,L in self.Equalities.items() :
			guyIndex = self.PeopleIndexes[guy]


			
			for equalChoices in L :
				
				miniCost = sys.maxint
				
				if not equalChoices :
					raise MagouilleuseException( "Empty equality list")
				
				# Fetch values & Get min
				for job in equalChoices :
					jobIndex = self.SlotIndexes[ job ]
					miniCost = min( m[ guyIndex ][ jobIndex ], miniCost )
				
				for job in equalChoices :
					jobIndex = self.SlotIndexes[ job ]
					m[ guyIndex ][ jobIndex ] = miniCost




	def solve (self, people, jobs, wishes, inabilities = [], equalities = {} ) :
	
		self.fill_People ( people )
		self.fill_Slots ( jobs )
		self.fill_Wishes ( wishes )
		self.fill_Equalities( equalities )
	
		if inabilities :
			self.fill_Inabilities( inabilities )
	
		Matrix = self.getEveryoneLines()
		self.equalizeChoicesIn( Matrix )

		import munkres

		solver = munkres.Munkres()
		solution = solver.compute( Matrix )

	
		return self.decodPeopleSlot( solution )
	

	def testGeneric(self,Test_people,Test_Jobs,Test_Wishes) :
		# Filling...
		if VERBOSE :
			print("Filling : ")
			print("self.People : ", Test_people)
		if VERBOSE :
			print("self.Slots : ", Test_Jobs)
		if VERBOSE :
			print("self.Wishes : ", Test_Wishes)


		
		print(self.solve( Test_people, Test_Jobs, Test_Wishes))
	
		Matrix =  self.getEveryoneLines()
		if VERBOSE :
			print("Matrix size : ", len( Matrix ), "X", len( Matrix[0] ))
			print(Matrix)	
		#Test :
		if VERBOSE :
			print("self.People : ",self.People, "\n self.Slots : ", self.Slots, "\n self.Wishes : ", self.Wishes)
			print("self.Popularity : ", self.Popularity)



##################Testing Verbosity:
VERBOSE = 0

	


	


def test2() :
	print("############ TEST  2 : Room for five ##############")
	mag = Magouilleuse()
	Test_people = [ "Lol", "Plop", "Moar" ]
	Test_Jobs   = { "Lol_Job" : 5, "Plop_Job" : 5  , "Moar_Job": 5 }
	Test_Wishes= { "Lol" : ( "Lol_Job", "Plop_Job", "Moar_Job" ),
								"Plop" : ( "Plop_Job","Moar_Job","Lol_Job"),
								"Moar" : ( "Moar_Job","Lol_Job","Plop_Job")}
	mag.testGeneric( Test_people, Test_Jobs, Test_Wishes )

def test3() :
	print("############ TEST  3 : empty bucket...  ##############")
	Test_people = [ "Lol", "Plop", "Moar" ]
	Test_Jobs   = { "Lol_Job" : 5, "Plop_Job" : 5  , "Moar_Job": 1  }
	Test_Wishes= { "Lol" : ( "Lol_Job", "Plop_Job", "Moar_Job" ),
								"Plop" : ( "Lol_Job","Moar_Job","Plop_Job"),
								"Moar" : ( "Moar_Job","Lol_Job","Plop_Job")}
	mag = Magouilleuse()
	mag.testGeneric( Test_people, Test_Jobs, Test_Wishes )

	
def test4() :
	print("############ TEST  4 : missing entry  ##############")
	Test_people = [ "Lol", "Plop", "Moar" ]
	Test_Jobs   = { "Lol_Job" : 5, "Plop_Job" : 5  , "Moar_Job": 1  }
	Test_Wishes= { "Lol" : ( "Lol_Job", "Plop_Job", "Moar_Job" ),
								"Plop" : ( "Lol_Job","Moar_Job"),
								"Moar" : ( "Moar_Job","Lol_Job","Plop_Job")}
	mag = Magouilleuse()
	mag.testGeneric( Test_people, Test_Jobs, Test_Wishes )


