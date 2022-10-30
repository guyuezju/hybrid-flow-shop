How to read the best results obtained by our proposed methods.

EXAMPLE:

0 , 10 , 2 , 592 , ILS
       3 ,        0 ,        8 ,        4 ,        5 ,        1 ,        7 ,        6 ,        2 ,        9 , 
       0 ,        3 ,        8 ,        5 ,        4 ,        1 ,        7 ,        2 ,        6 ,        9 , 
	   
The first number is row number of the InstanceNameLarge.txt file. 
That row indicates the instance name for the instances folder

The second number gives the number of jobs
The third number gives the number of stages
The fouth number is Total Weighted Earliness-Tardiness Objective Function Value (the best known)
The next field is the name of the algorithm that obtained this best solution.

After this information we have one row per stage indicating the job order 
(the order in which jobs have been launched to the stage).
 Remind that jobs are assigned to machines using the FAM Rule.