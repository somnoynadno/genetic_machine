from random import shuffle, randint

# our local program interpretator ^_^
class Searhing_Machine():
	def __init__(self, array, search_element):
		self.array = array
		self.search_element = search_element

	def execute(self, program):
		self.exceptions = list()
		self.warnings = list()

		self.position = 0

		self.program = program
		self.pointer = 0
		self.answer = None
		# special for eval
		safe_dict = {'self': self}

		while self.pointer < len(program):
			operator = program[self.pointer]
			# try to execute command
			no_error = eval("self" + "." + operator + "()", safe_dict)
			# catch each strange behavior
			if not no_error:
				self.warning(-1)
			self.pointer += 1

		if not self.exceptions:
			self.predict()
			return self.answer, self.exceptions, self.warnings
		else:
			return None, self.exceptions, self.warnings

	# executable methods below
	def right_shift(self):
		if self.position+1 < len(self.array):
			self.position += 1
			return True
		else:
			self.terminate(-3)
			return False

	def left_shift(self):
		if self.position-1 >= 0:
			self.position -= 1
			return True
		else:
			self.terminate(-3)
			return False

	def compare_equal(self):
		if self.array[self.position] == self.search_element:
			return True
		return False

	def compare_not_equal(self):
		if self.array[self.position] == self.search_element:
			return False
		return True

	def while_loop(self):
		safe_dict = {'self': self}
		try:
			# assure that cycle is executable
			self.pointer += 1
			condition = self.program[self.pointer]
			self.pointer += 1
			operator = self.program[self.pointer]
		except:
			self.terminate(-2)
			return False

		i = 0
		while eval("self" + "." + condition + "()", safe_dict):
			no_error = eval("self" + "." + operator + "()", safe_dict)
			# check for RT errors
			if i > 100:
				self.terminate(-4)
				return False
			if no_error:
				i += 1
			else:
				# catch strange behavior and exit loop
				self.warning(-2)
				return False
		return True

	def predict(self):
		self.answer = self.position
		# self.terminate(0)

	# exception catcher
	def terminate(self, exit_code):
		exception_list = [
		"OK", "Run-Time error",
		"Corrupted program", "List index out of range",
		"Everlasting loop", "Error in loop", "Array is empty"
		]
		self.exceptions.append(exception_list[abs(exit_code)])

	# warning collector
	def warning(self, code):
		warning_list = [
		"OK", "Strange behavior",
		"Strange behavior in loop",
		"Pointer out of range"
		]
		self.warnings.append(warning_list[abs(code)])

# testing part goes here
def test1(program):
	arr = [1]
	a = 1
	test = Searhing_Machine(arr, a)
	ans, e, w = test.execute(program)
	if ans == None:
		return False
	if arr[ans] == a:
		return True
	return False

def test2(program):
	arr = [5, 0, 0, 2, 4, 3]
	a = 3
	test = Searhing_Machine(arr, a)
	ans, e, w = test.execute(program)
	if ans == None:
		return False
	if arr[ans] == a:
		return True
	return False

def test3(program):
	arr = [4, 3, 2, 1]
	a = 2
	test = Searhing_Machine(arr, a)
	ans, e, w = test.execute(program)
	if ans == None:
		return False
	if arr[ans] == a:
		return True
	return False

def test4(program):
	arr = [0, 0, 5, 7, 0, 10, 11, 9]
	a = 10
	test = Searhing_Machine(arr, a)
	ans, e, w = test.execute(program)
	if ans == None:
		return False
	if arr[ans] == a:
		return True
	return False

# genetic algorithm to find program
# that do search for element in array
class Genetic():
	def __init__(self, executable_list):
		self.executable_list = executable_list
		self.answer = list()

	def run(self, epoch, training_set):
		WA_num = 8
		fatal_num = 20
		# we collect some fatal programs that may be good
		# and then try to fix them and put in better tier
		tier_WA = list()
		tier_fatal = list()

		a, arr = training_set

		# print(arr, a)
		machine = Searhing_Machine(arr, a)

		# fitness function
		w_average = 0

		# first colony
		while True:
			program = self.generate_random_program()
			ans, e, w = machine.execute(program)
			if ans != None:
				# if answer is right 
				# we try another tests
				if arr[ans] == a:
					if test1(program):
						if test2(program):
							if test3(program):
								if test4(program):
									self.answer.append(tuple(program.copy()))
				if len(tier_WA) < WA_num:
					w_average += len(w)
					tier_WA.append(program)
			else:
				if "Corrupted program" in w:
					program = self.fix(program)
				if len(tier_fatal) < fatal_num:
					tier_fatal.append(program)
			if len(tier_fatal) == fatal_num and len(tier_WA) == WA_num:
				break

		# taking mean
		w_average /= WA_num

		# main training
		for __ in range(epoch):
			# trying to mofify WA_tier members
			# and if their fitness better than average
			# put them back to WA_tier
			for i, program in enumerate(tier_WA):
				# we can't reduce short programs
				if len(program) > 3:
					program1 = self.reduce(program)
					ans, e, w = machine.execute(program1)
					if ans != None:
						if arr[ans] == a:
							if test1(program1):
								if test2(program1):
									self.answer.append(tuple(program1.copy()))
						if len(w) < w_average:
							tier_WA[i] = program1

				# but we can always add mutations
				program2 = self.mutation(program)
				ans, e, w = machine.execute(program2)
				if ans != None:
					if arr[ans] == a:
						if test1(program2):
							if test2(program2):
								self.answer.append(tuple(program2.copy()))
					if len(w) < w_average:
						tier_WA[i] = program2
				# and delete too short programs
				if len(program) == 3:
					tier_WA.pop(i)

			# trying to fix errors
			# else shuffle program and execute
			for i, program in enumerate(tier_fatal):
				program = self.mutation(program)
				ans, e, w = machine.execute(program)
				if ans == None:
					if ("Corrupted program") in w:
						program = self.fix(program)
						ans, e, w = machine.execute(program)
					if ("Everlasting loop") in w:
						program = mutation(program)
						ans, e, w = machine.execute(program)
					else:
						shuffle(program)
						ans, e, w = machine.execute(program)
				# delete program if it is completly shit
				if ans != None:
					tier_WA.append(program.copy())
					tier_fatal.pop(i)
			# create one new program in each epoch
			tier_fatal.append(self.generate_random_program())


	# fix corrupted crash
	def fix(self, program):
		program.append(self.executable_list[randint(0, len(self.executable_list)-1)])
		program.append(self.executable_list[randint(0, len(self.executable_list)-1)])
		return program

	def generate_random_program(self):
		l = randint(3, 12)
		program = [self.executable_list[randint(0, len(self.executable_list)-1)] for i in range(l)]
		return program

	# change random operator
	def mutation(self, arr):
		arr[randint(0, len(arr)-1)] = self.executable_list[randint(0, len(self.executable_list)-1)]
		return arr

	# delete random operator
	def reduce(self, arr):
		arr.pop(randint(0, len(arr)-1))
		return arr

	# swap two operators
	def random_swap(self, arr):
		i1, i2 = 0, 0
		while i1 == i2:
		    i1, i2 = randint(0, len(arr)-1), randint(0, len(arr)-1)
		arr[i1], arr[i2] = arr[i2], arr[i1]
		return arr

	# return set of working programs
	def predict(self):
		self.answer = set(self.answer)
		return self.answer


def main():
	# we can describe new operators in class
	# and then add them to this list
	executable_list = [
	"right_shift", "left_shift",
	"compare_equal", "while_loop",
	"compare_not_equal"
	]

	g = Genetic(executable_list)

	epoch = 200
	training_set = (21, [7, 14, 15, 11, 22, 18, 10, 1, 2, 17,
		12, 21, 7, 3, 22, 1, 21, 13, 5, 18, 18, 9,
		11, 22, 5, 23, 16, 9, 18, 7, 15, 19, 1, 4, 5])

	g.run(epoch, training_set)
	ans = g.predict()
	print(ans)

if __name__ == "__main__":
	main()
