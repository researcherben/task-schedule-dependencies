#!/usr/bin/env python3

# https://pypi.org/project/pygraphviz/
# https://pygraphviz.github.io/documentation/stable/
import pygraphviz
import random

"""
* Universal task ID. Randomly generated and uniquely assigned. 
* instance task id. Randomly generated and uniquely assigned. Enables duplication of task 
* referencesTask descriptionTask output parameters as a dictionary
* Task duration. A list of five values
* Task cost. A list of five values
* Task staffing
* Follow on task
* Is child of task ID task ID
* Cumulative cost
* Cumulative time

Task can be comprised of subtask. Then the duration and cost are functions of the subtasks
"""

def new_task_id(list_of_task_IDs: list):
    found_new = False
    while (not found_new):
        how_about_this_ID = random.randint(1000,9999)
        if how_about_this_ID not in list_of_task_IDs:
            found_new = True
            list_of_task_IDs.append(how_about_this_ID)
            return how_about_this_ID, list_of_task_IDs
    return None

class task:
    """
    """
    def __init__(self, 
                 persistent_ID, 
                 instance_ID,
                 description,
                 cost_duration_tuples_list,
                 output_parameters_dict,
                 follow_on_task_list_of_IDs):
        self.persistent_ID = persistent_ID
        self.instance_ID = instance_ID
        self.description = description
        self.cost_duration_tuples_list = cost_duration_tuples_list
        self.output_parameters_dict = output_parameters_dict
        self.follow_on_task_list_of_IDs = follow_on_task_list_of_IDs

    def print(self):
        print('persistent ID =', self.persistent_ID)
        print('instance ID   =', self.instance_ID)
        print('description =', self.description)
        print('cost_duration_tuples_list =', self.cost_duration_tuples_list)
        print('output_parameters_dict =', self.output_parameters_dict)
        print('follow_on_task_list_of_IDs =', self.follow_on_task_list_of_IDs)
        
def add_task(G, task):
    """
    """
    G.add_node("instance_"+str(task.instance_ID)+"_persistent_"+str(task.persistent_ID), 
           label="description: "+str(task.description)+"\l"+
                 "this task (cost,dur)="+str(task.cost_duration_tuples_list)+"\l"+
                 "cumulative (cost,dur)=TODO\l"+
                 "output param="+str(task.output_parameters_dict)+"\l",
           shape="rect");
    return G

        
if __name__ == "__main__":
    G = pygraphviz.AGraph(directed=True, compound=True)
    G.add_node("start_here", label="start here")
    
    list_of_task_IDs = []
    
    task_2_persistent_ID, list_of_task_IDs = new_task_id(list_of_task_IDs)
    task_2_instance_ID,   list_of_task_IDs = new_task_id(list_of_task_IDs)
    task2 = task(task_2_persistent_ID, 
                 task_2_instance_ID, 
                 "some task", # description
                 [(2,2), (3,4)], # cost and duration
                 {}, # outputs
                 []) # follow-on task IDs

#    task2.print()
    G = add_task(G, task2)
    
    G.add_edge("start_here", "instance_"+str(task2.instance_ID)+"_persistent_"+str(task2.persistent_ID))
    
    task_1_persistent_ID, list_of_task_IDs = new_task_id(list_of_task_IDs)
    task_1_instance_ID,   list_of_task_IDs = new_task_id(list_of_task_IDs)
    task1 = task(task_1_persistent_ID, 
                 task_1_instance_ID, 
                 "a task", # description
                 [(1,2), (3,4)], # cost and duration
                 {'a'}, # outputs
                 [task_2_instance_ID]) # follow-on task IDs
#    task1.print()

    G = add_task(G, task1)

    G.add_edge("instance_"+str(task1.instance_ID)+"_persistent_"+str(task1.persistent_ID),
               "instance_"+str(task2.instance_ID)+"_persistent_"+str(task2.persistent_ID))

    G.draw("automated_digraph.png", prog="dot")