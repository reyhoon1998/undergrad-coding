
# Percolation
Percolation problems are often modeled by a lattice of cells, where each cell can be either on or off,
representing the presence or absence of a pore.
The goal is to find if there is a path of open cells from one side of the lattice to another.
There are various algorithms to solve percolation problems. Here I present two algorithms: coloring(time complexity of O(l^(2d))) and Hoshen-Kopelman(time complexity of O(l^2)).
## coloring algorithm
1. Initialize a lattice of size l by l, where l is the number of nodes per side. Set the value of each node to 0, which means the node is off.
2. Turn on all the nodes on the left border by setting their value to 1.
3. Turn on all the cells on the right border by setting their value to a very large integer, max_int.
4. Start the main loop. For each iteration, do the following:<br>
Select nodes one by one,set its value to a non-zero number that is not used before.
Check all the neighboring nodes of the selected node. There are three possibilities:<br>
4.1. If all the neighbors are off, go back to the main loop.<br>
4.2. If there is only one neighbor that is on, set the value of the selected node to the value of that neighbor, and go back to the main loop.<br>
4.3. If there are more than one neighbor that is on, find the smallest value among them, and set the value of the selected node and all the other nodes that have the same or larger value to that value. 
5. Check the value of any node on the right border. If there is any 1, then percolation occurred.

## Hoshen_Kopelman algorithm
The main difference between this algorithm and the coloring algorithm is that in each step, we check the labels of the neighboring nodes of the selected node,
and if there are different labels, we set the label of the selected node to the smallest one.
This way, we only need to change a number in a one-dimensional array, instead of updating the values of all the nodes in the grid.
This reduces the time and space complexity of the algorithm.
### Percolation Probability
Percolation probability is the probability that there exists a path of open nodes from one side of the lattice to another, denoted by Q.
This probability exhibits critical behavior,meaning that it changes abruptly from 0 to 1 at a certain value of p. 


In the last part of this assignment, I analyzed the percolation probability using the Hoshen-Kopelman algorithm, 
As you can see in the results, the transition from 0 to 1 becomes sharper as the size of the lattice increases, indicating that the system approaches the critical point more closely.
