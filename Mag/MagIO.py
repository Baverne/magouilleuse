

# Input :

# One line per person// one word.
# Dot, or empty line, or nothing ( switch to two words lines ... )
# One line per Job, two words, second is capacity.
# End with single dot
# One line per wish suite : 
# Person Wish1 Wish2...
# End with dot
# Incapacities :
# Person Slot1 Slot2...²

from Magouilleuse import MagouilleuseException

class MagIO :
	def __init__( self, sin ) :
		self.sin = sin
		self.reading_people = True
		self.reading_slots = False
		self.reading_wishes = False
		self.reading_incapacities = False

		self.people = []
		self.wishes = {}
		self.slots = {}
		self.incapacities = []
		self.equalities = {}


	def switchToSlots( self ) :
			self.reading_people = False
			self.reading_slots = True
	
	def switchToWishes( self ):
			self.reading_slots = False
			self.reading_wishes = True
	
	def switchToIncapacities( self ) :
			self.reading_wishes = False
			self.reading_incapacities = True

	def readPeople( self, line ) :
	
		L = line.split()
		if ( len( L ) > 1 ) :
			self.readSlot( line )
			self.switchToSlots()
			return
	
		if not L :
			self.switchToSlots()
			return

		if L[0] == ".":
			self.switchToSlots()
			return
		self.people.append( L[0] )


	def readSlot( self, line ):
		L = line.split()
		
		if not L :
			self.switchToWishes()
			return

		if len(L) > 2 :
			self.switchToWishes()
			self.readWish( line )
			return

		if len(L) == 1 and L[0] == "." :
			self.switchToWishes()
			return
		try :
			i = int( L[1] )
		except ValueError as e :
			raise MagouilleuseException( e )

		self.slots[ L[0] ] = i


	def readWish( self, line ) :
		L = line.split()
		
		if not L :
			self.switchToIncapacities()
			return

		if len(L) == 1 and L[0] == "." :
			self.switchToIncapacities()
			return

		joe = L.pop(0)

		L_EqualitySplitted = []
		for x in L :
			if '=' in x :
				for jobname in x.split('=') :
					L_EqualitySplitted.append( jobname )
				if joe not in self.equalities : 
					self.equalities[ joe ] = []
				self.equalities[ joe ].append( x.split('=') )
			else :
				L_EqualitySplitted.append( x )
	
		self.wishes[ joe ] = L_EqualitySplitted
		

	def readIncapacities( self, line ) :
		L = line.split()

		if not L :
			return

		if len( L ) == 1 :
			return

		joe = L.pop(0)
		for job in L :
			self.incapacities.append( ( joe, job ) )


	def readLine ( self, line ) :
		print("readLine")
		if self.reading_people:
			self.readPeople( line )
		elif self.reading_slots:
			self.readSlot( line )
		elif self.reading_wishes:
			self.readWish( line )
		elif self.reading_incapacities:
			self.readIncapacities( line )

	def readLines ( self ) :
		oneSeen = False
		print("readLines")
		for line in self.sin :
			print(line)
			if not oneSeen and not line.split() :
				continue
			else :
				oneSeen = True

			self.readLine( line )
		print("readLines done")


	def getPeopleSlotsWishesIncapacitiesEqualities ( self ) :
		return self.people, self.slots, self.wishes, self.incapacities, self.equalities




		
	
	
