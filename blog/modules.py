from material.frontend import Module

class main(Module):
	icon = 'mdi-image-compare'
	def get_urls(self):
		return 'blog/list.html'
