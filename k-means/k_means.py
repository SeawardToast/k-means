import pandas as pd
import numpy as np
import random 
import matplotlib.pyplot as plt
import os.path

class Utilities:

	flag = True

	def __init__(self):
		
		self.previous_centroids = []
		

	def is_first_time(self):
		return self.flag

	def first_time(self):
		self.flag = False

	def set_previous_centroids(self, centroids):
		self.previous_centroids.clear()
		self.previous_centroids = centroids
		print("self previous ", self.previous_centroids)
		print("get previous ", self.get_previous_centroids())
	
	def get_previous_centroids(self):
		print("gettin ", self.previous_centroids)
		return self.previous_centroids

	# compute the difference between sets of centroids and determine if we should continue algorithm 
	def check_centroids(self, centroids, previous_centroids):
		print("checking")
		previous_cents = previous_centroids
		print("previous check ", previous_cents)
		print("previous check ", self.previous_centroids)
		print("length ", len(previous_cents))

		values = []
		
		
		for i in range(0, len(centroids)):
			arr = np.array(centroids[i])
			arr2 = np.array(previous_cents[i])		
			num = np.linalg.norm(arr - arr2)		
			values.append(num)
		sum = 0
		print("sum")
		for i in range(0, len(values)):
			sum += values[i]
		print("sum ", sum)
		if sum < .05:
			print("STOP")
			return False
		else:
			return True

	# returns x many random selection from given data
	@staticmethod
	def get_centroids(petal, sepal, num):
		list = []
		for x in range(0, num):
			num = random.randrange(0, 150, 1)
			list.append([petal[num], sepal[num]])
		return list

	@staticmethod
	def run_kmean(centroids, petal_list, sepal_list, K, iterations):
		print("start")
		previous_centroids = centroids
		distance_centroid_pair_list = []
		distance_list = []
		data_point_list = []
		new_centroid = []
		cluster_pair_list = []
		#iterate over each x (petal/sepal value) for length of petal/sepal arr
		for x in range(0, len(petal_list)): 	
			#compute distance between the data point and each centroid in order to assign clusters
			data_point_list.append([petal_list[x], sepal_list[x]])
		#print("data point list is ", data_point_list)

		#iterate over each value in the list of petal, sepal ratio values and perform calculation of ratio data point to centroid distance
		for x in range(0, len(data_point_list)):
			for i in range(0, len(centroids)): #iterate over each centroid

				data_point_arr = np.array(data_point_list[x]) # create numpy array in order to use numpy to perform distance calculation
				cent_arr = np.array(centroids[i]) # same as above fr centroid

				dist = np.linalg.norm(data_point_arr - cent_arr) # calculate the distance between the data point and the centroid
			
				distance_centroid_pair_list.append([dist, centroids[i], data_point_list[x]]) # add the [distance, centroid, data point] to a list
				distance_list.append(dist)


		#create clusters
		for i in range(0, len(petal_list)): #iterate over each data point using petal_list as length
			centroid_distances = []
			closest_centroid = []
			temp_dist = 1000;
			for x in range(0, len(centroids)):	 # iterate over each centroid, want to find the closest centroid to data point
			
				cent = np.array(centroids[x]) #create numpy array of centroid
				data = np.array(data_point_list[i]) # create numpy array of data point
				dist = np.linalg.norm(cent-data) #perform calculation to find distance between centroid and data point
				
				if dist < temp_dist: # if this centroid is closer than the last centroid measured for this data point
					# set the current centroid as the closest and set the temp_dist to the new distance
					temp_dist = dist
					closest_centroid = centroids[x]
				# append the distance to a list of centroid distances
				centroid_distances.append(dist)
		
			centroid_distances.sort()
			# add each data point along with it's closest centroid to list
			cluster_pair_list.append([data_point_list[i], closest_centroid])

	

		clusters = []
		for i in range(0, K): #create list of clusters with K different lists inside to represent clusters
			clusters.append([])
		#next step, generate new clusters
		for x in range(0, len(cluster_pair_list)): #iterate over each pair of (data_point, closest_centroid)
			
			for y in range(0, len(centroids)): #iterate over all centroids
				if cluster_pair_list[x][1] == centroids[y]: #if data point's closest centroid is the current centroid
					# assign this data point to the current centroids cluster
					# this is an essential step, keeps track of which cluster a data point belongs to
					clusters[y].append([cluster_pair_list[x][0]])
				
		new_centroids = []
		
		plt.clf()

		#next step, re-calculate centroid of new clusters
		for i in range(0, K): #iterate over clusters
			# initialize some values for each centroid
			
			x = 0
			y = 0
			length = 0
			
			for t in range(0, len(clusters[i])): # iterate over each data point in current cluster
				length += 1 #add one to our length value to be used for average calculation

				#add the x and y values of current data point to the sum of the data points x and y for the current cluster
				x += (clusters[i][t][0][0]) #add the x value of data point in cluster
				y += (clusters[i][t][0][1]) #add the y value of data point in cluster

				if i == 0:
					plt.scatter(clusters[i][t][0][0],clusters[i][t][0][1],c='red')
				if i == 1:
					plt.scatter(clusters[i][t][0][0],clusters[i][t][0][1],c='blue')
				if i == 2:
					plt.scatter(clusters[i][t][0][0],clusters[i][t][0][1],c='green')
				if i == 3:
					plt.scatter(clusters[i][t][0][0],clusters[i][t][0][1],c='purple')
			

			# assign new centroid of this cluster to the midpoint of off data points in this cluster
			# to do this, we find the average of the data points x and y values and create a new centroid x,y

			new_centroids.append([x / length, y / length])


		

		for x in range(0, len(new_centroids)):
			plt.scatter(new_centroids[x][0], new_centroids[x][1], c='yellow')
		util = Utilities()
		
		if iterations == 99:
			plt.show()
		print("iters ", iterations)
		print("one ", util.check_centroids(new_centroids, previous_centroids))
		print("two ", iterations != 0)
		if util.check_centroids(new_centroids, previous_centroids) and iterations != 0:
			util.first_time()
			util.set_previous_centroids(new_centroids)
			util.run_kmean(new_centroids, petal_list, sepal_list, K, iterations-1)
		else:
			print("stopping")
			plt.show()
		
# create data frame from the database using pandas and fetch data using head
my_path = r'Iris.csv'
data = pd.read_csv(my_path)

#seperate data we want to examine, in this case only the lengths and widths of both the sepals and petals
petal_width_list = data.PetalWidthCm.tolist()
petal_length_list = data.PetalLengthCm.tolist()
sepal_width_list = data.SepalWidthCm.tolist()
sepal_length_list = data.SepalLengthCm.tolist()

#lists
petal_ratio_list = []
sepal_ratio_list = []

#create ratios for length/width for each petal and sepal
for x in range(0, len(petal_length_list)):
	#print(x)
	petal_ratio_list.append( petal_length_list[x] / petal_width_list[x] )
	sepal_ratio_list.append( sepal_length_list[x] / sepal_width_list[x] )

#plot ratios on x and y axis
plt.scatter(petal_ratio_list, sepal_ratio_list)
plt.xlabel("Petal Ratio")
plt.ylabel("Sepal Ratio")


#number of clusters
K = 4

#assigning centroids

util = Utilities()

centroids = util.get_centroids(petal_ratio_list, sepal_ratio_list, K)


petal_centroids = []
sepal_centroids = []

for x in range(0, len(centroids)):
	petal_centroids.append(centroids[x][0])
	sepal_centroids.append(centroids[x][1])
	

print(centroids)
#util.run_kmean(centroids, petal_ratio_list, sepal_ratio_list, K)
for i in range(0, len(centroids)):
	plt.scatter(centroids[i][0], centroids[i][1], c='yellow')
util.run_kmean(centroids, petal_ratio_list, sepal_ratio_list, K, 100)








