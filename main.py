from random import shuffle

# TODO: upgrade this class
class Genetic():
	def __init__(self, executable_list):
		self.executable_list = executable_list

	def generate_shuffle(self):
		program = self.executable_list.copy()
		shuffle(program)
		return program


class Searhing_Machine():
	def __init__(self, array, search_element):
		self.array = array
		self.search_element = search_element
		self.position = 0

	def execute(self, program):
		self.exceptions = list()
		self.warnings = list()

		self.program = program
		self.pointer = 0
		self.answer = None
		# special for eval
		safe_dict = {'self': self}

		while self.pointer < len(program):
			operator = program[self.pointer]
			# try to execute command
			no_error = eval("self" + "." + operator + "()", safe_dict)
			if not no_error:
				self.warning(-1)
			self.pointer += 1

		print(self.exceptions)
		print(self.warnings)

		if not self.exceptions:
			self.predict()
			return self.answer
		else:
			return None

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
			self.pointer += 1
			condition = self.program[self.pointer]
			self.pointer += 1
			operator = self.program[self.pointer]
		except:
			self.terminate(-2)
			return False

		i = 0
		while eval("self" + "." + condition + "()", safe_dict):
			# print(i)
			no_error = eval("self" + "." + operator + "()", safe_dict)
			if i > 100:
				self.terminate(-4)
				return False
			if no_error:
				i += 1
			else:
				self.terminate(-5)
				return False
		return True

	def predict(self):
		self.answer = self.position
		self.terminate(0)

	# exception catcher
	def terminate(self, exit_code):
		exception_list = ["OK", "Run-Time error", "Corrupted program", "List index out of range", "Everlasting loop", "Error in loop"]
		self.exceptions.append(exception_list[abs(exit_code)])

	# warning collector
	def warning(self, code):
		warning_list = ["OK", "Strange operation"]
		self.warnings.append(warning_list[abs(code)])

def test():
	arr = [1, 2, 3, 4, 5, 6, 7]
	a = 6
	arr1 = [7, 14, 15, 11, 22, 18, 10, 1, 2, 17, 12, 21, 7, 3, 22, 1, 21, 13, 5, 18, 18, 9, 11, 22, 5, 23, 16, 9, 18, 7, 15, 19, 1, 4, 5, 2, 6, 10, 8, 7]
	a1 = 5
	arr2 = [27, 21, 22, 8, 19, 16, 12, 17, 19, 8, 30, 18, 25, 25, 14, 14, 18, 24, 28, 26, 25, 11, 17, 21, 30, 10, 25, 15, 30, 14, 17, 20, 13, 7, 11, 10, 9, 10, 16, 21]
	a2 = 25
	machine = Searhing_Machine(arr, a)
	test_machine_1 = Searhing_Machine(arr1, a1)
	test_machine_2 = Searhing_Machine(arr2, a2)

	executable_list = ["right_shift", "left_shift", "compare_equal", "while_loop", "compare_not_equal"]
	special = ["predict"]

	generator = Genetic(executable_list)
	program = generator.generate_shuffle()
	ans = machine.execute(program)
	print(ans, program)

	# fine usage

	"""
	program = ["while_loop", "compare_not_equal", "right_shift", "predict"]
	ans = machine.execute(program)
	print(ans)
	"""

if __name__ == "__main__":
	test()