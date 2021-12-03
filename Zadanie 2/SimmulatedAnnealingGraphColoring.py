# simulated annealing implementation for graph coloring
import numpy as np
import random

# objective function

def objective(edges, vertices_colors):
	cost = 0
	for edge in edges:
		# print('Vrcholy', edge[0], edge[1])
		# print('Farby vrcholov', vertices_colors[edge[0]], vertices_colors[edge[1]])
		if vertices_colors[edge[0]] == vertices_colors[edge[1]]:
			cost += 1
			# print(">> shit, equal. COST:", cost)
	return cost

# simulated annealing algorithm
def simulated_annealing_for_graph_coloring(objective, edges, n_colors, n_iterations, temp):
	# Get vertices from edges
	vertices = np.arange(start=1, stop=np.amax(edges) + 1)
	print('🟢 Initialise assignement of vertices')
	best_vertices_colors = {key: np.random.randint(1, n_colors+1) for key in vertices}
	print('>> Initial state:\n', best_vertices_colors)
	# evaluate the initial point
	best_eval = objective(edges, best_vertices_colors)
	print('>> Initial cost:', best_eval)
	# current working solution
	curr_vertices_colors, curr_eval = best_vertices_colors.copy(), best_eval
	# run the algorithm
	for i in range(n_iterations):
		# take a step
		candidate_vertices_colors = curr_vertices_colors.copy()
		# candidate_vertices_colors[np.random.randint(1, len(candidate_vertices_colors))] = np.random.randint(1, n_colors+1)
		rand_i = np.random.randint(1, len(candidate_vertices_colors))
		rand_list = list(range(1, n_colors+1))
		candidate_vertices_colors[rand_i] = random.choice([ele for ele in rand_list if ele != curr_vertices_colors[rand_i]])
		# print('Changed solution:\n', candidate_vertices_colors)
		# evaluate candidate point
		candidate_eval = objective(edges, candidate_vertices_colors)
		# check for new best solution
		if candidate_eval < best_eval:
			print('🏁🏁', i, '🏁🏁\nCOST:', candidate_eval)
			# store new best point
			best_vertices_colors, best_eval = candidate_vertices_colors.copy(), candidate_eval
		# difference between candidate and current point evaluation
		diff = candidate_eval - curr_eval
		# calculate temperature for current epoch
		t = temp / float(i + 1)
		# calculate metropolis acceptance criterion
		metropolis = np.exp(-diff / t)
		# check if we should keep the new point
		if diff < 0 or np.random.rand() < metropolis:
			# store the new current point
			curr_vertices_colors, curr_eval = candidate_vertices_colors, candidate_eval
		# print('Curr VS Best solution:\n', curr_vertices_colors, '\n', best_vertices_colors)
		# print('Curr VS Best cost:\n', curr_eval, '\n', best_eval)
	return [best_vertices_colors, best_eval]


txt_in = 'Zadanie 1/coloring_examples/example1.txt'
txt_out = 'hop_z2.txt'
with open(txt_in, 'r') as infile:
	# Load input
	edges = np.loadtxt(infile).astype(int)
# seed the pseudorandom number generator
np.random.seed(4)
# define range for input
bounds = np.asarray([[-5.0, 5.0]])
# define the total iterations
n_iterations = 1000
# define the maximum step size
# step_size = 0.1
n_colors = 6
# initial temperature
temp = 10
# perform the simulated annealing search
best, score = simulated_annealing_for_graph_coloring(objective, edges, n_colors, n_iterations, temp)
with open(txt_out, 'w') as outfile:
	outcome = ''
	for key, value in best.items():
		outcome += "%s %s\n" % (key, value)
	outfile.write(outcome)
print('\n🎉 Done!')
# print('f(%s) = %f' % (best, score))
print('🏁 Cost:', score)
print('🏁 Best combination:\n', best, '\n')