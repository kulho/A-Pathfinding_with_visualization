# A-Pathfinding with visualization
My second python project, A* pathfinding algorithm with GUI visualization.

On the setup screen, input the coordinates in the form x,y in range from 1 to 50 for both starting and end point.
You can draw obstacles by leftclicking and draging cursor over the black squares.
The algorithm can move diagonally so if the obstacle squares are touching only in the
corners it can pass through them. (Not a great explanation, but you'll understand
quickly what I mean if you play with it a bit ;)
Once you created your maze press spacebar to find the shortest path.

In the cube class in the function get_h() (lines 40-43) you can choose between Manhattan and 
diagonal heristic by commenting/uncommeting to see different behavior of A* algorithm.

Tkinter is probably not very well suited for this application as it takes some time
to load the program initially, however then it runs smoothly on my pc.
