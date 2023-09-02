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

def new_task_id(all_tasks: dict):
    task_ID_list = []
    for desc, task in all_tasks.items():
        task_ID_list.append(task.instance_ID)
        
    found_new = False
    while (not found_new):
        how_about_this_ID = random.randint(1000,9999)
        if how_about_this_ID not in task_ID_list:
            found_new = True
            return how_about_this_ID
    return None

class Task:
    """
    """
    def __init__(self, 
                 #persistent_ID, 
                 instance_ID,
                 description,
                 cost_duration_tuples_list,
                 output_parameters_dict,
                 followed_by_task_instance_IDs):
        #self.persistent_ID = persistent_ID
        self.instance_ID = instance_ID
        self.description = description
        self.cost_duration_tuples_list = cost_duration_tuples_list
        self.output_parameters_dict = output_parameters_dict
        self.followed_by_task_instance_IDs = followed_by_task_instance_IDs

    def print(self):
        #print('persistent ID =', self.persistent_ID)
        print('instance ID   =', self.instance_ID)
        print('description =', self.description)
        print('cost_duration_tuples_list =', self.cost_duration_tuples_list)
        print('output_parameters_dict =', self.output_parameters_dict)
        print('followed_by_task_instance_IDs =', self.followed_by_task_instance_IDs)

def sum_cost_and_duration(task, all_tasks):
    """
    """
    
    return 
        
def add_task(G, task, all_tasks):
    """
    """
    #task.print()
    G.add_node("instance_"+str(task.instance_ID), 
           label="description: "+str(task.description)+"\l"+
                 "this task (cost,dur)="+str(task.cost_duration_tuples_list)+"\l"+
                 "cumulative (cost,dur)=TODO\l"+
                 "output param="+str(task.output_parameters_dict)+"\l",
           shape="rect");
    return G

def add_task_that_has_subtasks(G, task, list_of_subtasks, all_tasks):
    """
    """
    # TODO; trace costs using all_tasks
    
    B = G.add_subgraph(name="cluster_instance_"+str(task.instance_ID),
                       label="description: "+str(task.description)+"\l"+
                             "this task (cost,dur)="+str(task.cost_duration_tuples_list)+"\l"+
                             "cumulative (cost,dur)=TODO\l"+
                             "output param="+str(task.output_parameters_dict)+"\l")

    B.add_node("instance_"+str(task.instance_ID), style="invis");
    
    for subtask in list_of_subtasks:
        B = add_task(B, subtask, all_tasks)
    
    return G


def add_edges(G, task):
    """
    """
    for followed_by_instance_ID in task.followed_by_task_instance_IDs:
        G.add_edge("instance_"+str(task.instance_ID       ),
                   "instance_"+str(followed_by_instance_ID))
    return G


        
if __name__ == "__main__":
    G = pygraphviz.AGraph(directed=True, compound=True)
    #G.add_node("start_here", label="start here")
    
    all_tasks = {}
        
    task = Task(new_task_id(all_tasks), 
                 "a task", # description
                 [(1,2), (3,4)], # cost and duration
                 {'a'}, # outputs
                 []) # followed by task IDs
    all_tasks[task.description] = task
    
    #G.add_edge("start_here", "instance_"+str(task.instance_ID))

    task = Task(new_task_id(all_tasks), 
                 "some task", # description
                 [(2,2), (3,4)], # cost and duration
                 {}, # outputs
                 []) # followed by task IDs
    all_tasks[task.description] = task
    all_tasks["some task"].followed_by_task_instance_IDs.append(all_tasks["a task"].instance_ID)

    task = Task(new_task_id(all_tasks), 
                 "the task", # description
                 [(3,1), (3,4)], # cost and duration
                 {'a'}, # outputs
                 []) # followed by task IDs
    all_tasks[task.description] = task

#    task.followed_by_task_instance_IDs.append(task_parent.instance_ID)
    
    task = Task(new_task_id(all_tasks), 
                 "parent task", # description
                 [(4,3), (3,4)], # cost and duration
                 {'b'}, # outputs
                 []) # followed by task IDs
    all_tasks[task.description] = task

    task = Task(new_task_id(all_tasks), 
                 "la child task", # description
                 [(8,3), (3,4)], # cost and duration
                 {'c'}, # outputs
                 []) # followed by task IDs
    all_tasks[task.description] = task

    task = Task(new_task_id(all_tasks), 
                 "el child task", # description
                 [(7,7), (3,4)], # cost and duration
                 {'c'}, # outputs
                 []) # followed by task IDs    
    all_tasks[task.description] = task
    
    task = Task(new_task_id(all_tasks), 
                 "child task", # description
                 [(7,7), (3,4)], # cost and duration
                 {'c'}, # outputs
                 []) # followed by task IDs
    all_tasks[task.description] = task

    all_tasks["parent task"].followed_by_task_instance_IDs.append(all_tasks["el child task"].instance_ID)
    all_tasks["parent task"].followed_by_task_instance_IDs.append(all_tasks["child task"].instance_ID)

    
    G = add_task_that_has_subtasks(G, all_tasks["parent task"], 
                                   [all_tasks["el child task"], all_tasks["child task"]], 
                                   all_tasks)
    
    for desc, task in all_tasks.items():
        task.print()
    
    for desc, task in all_tasks.items():
        G = add_task(G, task, all_tasks)
        
        G = add_edges(G, task)
    

    G.draw("automated_digraph.png", prog="dot")