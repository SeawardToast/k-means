import pandas as pd
import numpy as np
import random 
import matplotlib.pyplot as plt
import os.path

class Utilities:
	# returns x many random selection from given data
	@staticmethod
	def get_centroids(petal, sepal, num):
		list = []
		for x in range(0, num):
			num = random.randrange(0, 150, 1)
			list.append([petal[num], sepal[num]])
		return list

	@staticmethod
	def run_kmean(centroids, petal_list, sepal_list, K):
		distance_centroid_pair_list = []
		distance_list = []
		data_point_list = []
		new_centroid = []
		cluster_pair_list = []
		#iterate over each x (petal/sepal value) for length of petal/sepal arr
		for x in range(0, len(petal_list)): 	
			#compute distance between the data point and each centroid in order to assign clusters
			data_point_list.append([petal_list[x], sepal_list[x]])
		print("data point list is ", data_point_list)

		#iterate over each value in the list of petal, sepal ratio values and perform calculation of ratio data point to centroid distance
		for x in range(0, len(data_point_list)):
			for i in range(0, len(centroids)): #iterate over each centroid
				#print("arr at i ", arr[i], " : Centroid at i ", centroids[i] )
				print("data_point at x ", data_point_list[x])
				print("centroid at i ", centroids[i])
				arr = np.array(data_point_list[x])
				print("np arr ", arr)
				dist = np.linalg.norm(arr - centroids[i])
				print("dist calculation is ", dist)				
				distance_centroid_pair_list.append([dist, centroids[i], data_point_list[x]])
				distance_list.append(dist)
		print("pair list ", distance_centroid_pair_list)

		#create clusters
		for i in range(0, len(petal_list)):
			centroid_distances = []
			closest_centroid = []
			temp_dist = 1000;
			for x in range(0, len(centroids)):				
				print("centroid ", centroids[x])
				print("datapoint ", data_point_list[i])
				cent = np.array(centroids[x])
				data = np.array(data_point_list[i])
				dist = np.linalg.norm(cent-data)
				print("dist ", dist)
				if dist < temp_dist:
					temp_dist = dist
					closest_centroid = centroids[x]

				centroid_distances.append(dist)
			print("distances ", centroid_distances)
			print("closest centroid ", closest_centroid)
			centroid_distances.sort()
			cluster_pair_list.append([data_point_list[i], closest_centroid])

		print("cluster pairs ", cluster_pair_list)

		clusters = []
		for i in range(0, K): #create list of clusters with K different lists inside to represent clusters
			clusters.append([])
		#next step, generate new clusters
		for x in range(0, len(cluster_pair_list)): #iterate over all pairs
			print("pair list ", cluster_pair_list[x][1])
			for y in range(0, len(centroids)): #iterate over all centroids
				if cluster_pair_list[x][1] == centroids[y]:
					print("belongs to centroid ", centroids[y])
					clusters[y].append([cluster_pair_list[x][0]])
				
		new_centroids = []
		
		plt.clf()

		#next step, re-calculate centroid of new clusters
		for i in range(0, K):
			x = 0
			y = 0
			length = 0
			for t in range(0, len(clusters[i])):
				length += 1
				x += (clusters[i][t][0][0]) #get the x value of each point in cluster
				y += (clusters[i][t][0][1]) #get the y value of each point in cluster

				if i == 0:
					plt.scatter(clusters[i][t][0][0],clusters[i][t][0][1],c='red')
				if i == 1:
					plt.scatter(clusters[i][t][0][0],clusters[i][t][0][1],c='blue')
				if i == 2:
					plt.scatter(clusters[i][t][0][0],clusters[i][t][0][1],c='green')
				if i == 3:
					plt.scatter(clusters[i][t][0][0],clusters[i][t][0][1],c='purple')
				print("cluster ", i, " contains ", x)
				print("x is ", x)
				print("y is ", y)
			print("length is ", length)
			new_centroids.append([x / length, y / length])
		print("length ", length)
		print("new cents ", new_centroids)

		

		for x in range(0, len(new_centroids)):
			plt.scatter(new_centroids[x][0], new_centroids[x][1], c='yellow')
		plt.show()
		util = Utilities()
		util.run_kmean(new_centroids, petal_ratio_list, sepal_ratio_list, 4)

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
print(petal_centroids)
print(sepal_centroids)

util.run_kmean(centroids, petal_ratio_list, sepal_ratio_list, K)

plt.scatter(petal_centroids, sepal_centroids, c='red')
plt.show()




