# A-Pathfinding with visualization
My second python project, A* pathfinding algorithm with GUI visualization.

On the setup screen please input coordinates in the form xx,yy for both starting and end point.
You can draw obstacles by leftclicking and draging mouse over the black squares.
Once you created your maze press spacebar to find the shortest path.

In the cube class in function get_h() (lines 40-43) you can choose between Manhattan and 
diagonal heristic by commenting/uncommeting to see different behavior of A* algorithm.

Tkinter is probably not very well suited for this application as it takes some time
to load the program initially, however then it runs smoothly on my pc.
