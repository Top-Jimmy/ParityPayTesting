# from component import Component
# pages w/ stepper
	# (1) send_to_bank
	# (2) send_to_atm
	# (3) send_to_cashout

class Stepper():
	def __init__(self, driver):
		self.driver = driver
		self.load()

	def load(self):
		self.steps = self.driver.find_elements_by_class_name('stepperButton')
		# Fail if not at least 3 steps
		fail = self.steps[2]
		self.step_names = self.read_step_names()
		self.current_step = self.get_current_step

	def read_step_names(self):
		step_names = []
		for i, step in enumerate(self.steps):
			step_names.append(step.find_element_by_tag_name('div').text)
		return step_names

	def get_current_step(self):
		selected_color = '(56, 217, 244'

		for i, step in enumerate(self.steps):
			svg = step.find_element_by_tag_name('svg')
			color = svg.value_of_css_property('color')
			if selected_color in color:
				return [i, self.step_names[i]]

	def click_step(self, step):
		# Step: int or string of step name
		self.driver.execute_script("window.scrollTo(0, 0)")
		if type(step) == int:
			index = step
		else:
			try:
				index = self.step_names.index(step)
			except ValueError:
				raise ValueError("Could not find step: " + str(step))
		self.steps[index].click()
		return [index, self.step_names[index]]


