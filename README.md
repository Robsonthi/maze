# maze
 Solving maze with searching algorithms


## How to use?

 Main file: maze.py

 type_search: 'dfs', 'bfs', 'greedy' or 'a*'

 sort: 'default' or 'heap'

## Pathfinding Algorithms
Pathfinding algorithms or searching algorithms are algorithms from an initial state that can find a goal state.

This algorithm works with stack, queue and tree structure.

We can mention the most popular searching algorithm: Depth-first search (DFS), Breadth-first search (BFS), Greedy best-first search, Dijkstra's algorithm and A* search algorithm.

**Depth-first search (DFS)** always expands the deepest node in the frontier first, in other words, this algorithm uses a stack structure as memory. DFS isn’t cost-optimal, it returns the first solution it finds, even if it isn’t the cheapest. Recommended only finite tree/space.

Time complexity: $$O(b^m)$$

Memory complexity: $$O(bm)$$

Where $$m$$ is a limited depth, and $$b$$ is the number of ’siblings’.

**Breadth-first search (BFS)** the root node is expanded first, then all the successors of the root node are expanded next, then their successors, and so on, in other words, this algorithm uses a queue structure as memory. When all actions have the same cost, an appropriate strategy is this one. BFS is cost-optimal, and returns the first solution it finds, whereupon it’s the cheapest solution.

Time complexity: $$O(b^d)$$

Memory complexity: $$O(b^d)$$

DFS and BFS are used when the states don’t have an associate value, however, when the states have an associate value, and there is an associate priority, we can use searching algorithms with ordered queue.

**A\* (A-star) search algorithm** is the most common informed search algorithm, a best-first search that uses the evaluation function:

$$f(n)=g(n)+h(n)$$

where $$g(n)$$ is the path cost from the initial state to node $$n$$, and $$h(n)$$ is the estimated cost of the shortest path from $$n$$ to a goal state, so we have $$f(n)$$ = estimated cost of the best path that continues from $$n$$ to a goal. A* is complete and cost-optimal.

**Greedy best-first search algorithm** is a greedy algorithm, in other words, the priority nodes are the nodes closest to the goal. It also has an evaluation function, such as A*, it’s the same function, considered $$g(n)=0$$, therefore,

$$f(n)=h(n)$$

**Dijkstra's algorithm** also is similar, but it’s an opposite way, the priority node is with the past cost from the initial state to node $$n$$, this is $$h(n)=0$$,

$$f(n)=g(n)$$

When actions have different costs, it’s an appropriate strategy. Whether all actions have the same cost, the Dijkstra's algorithm will be a BFS.

The evaluation function, $$f(n)$$, will be an associated value to organize the nodes in an ordered queue.

Such as example, we have a maze. The associated value to the evaluation function is the distance (euclidean distance).

DFS: Path length: 183; Positions explored: 294

BFS: Path length: 113; Positions explored: 1335

Greedy: Path length: 125; Positions explored: 197

A*: Path length: 113; Positions explored: 849
