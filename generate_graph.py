#!/usr/bin/env python3

import datetime
import random
import copy # https://docs.python.org/3/library/copy.html
# https://pypi.org/project/pygraphviz/
# https://pygraphviz.github.io/documentation/stable/
import pygraphviz
"""
* Universal task ID = task description.
* unique instance task id. Enables duplication of task references
* Task output parameters as a dictionary
* Task duration. A list of N values
* Task cost. A list of N values
* Follow-on task
* Cumulative cost
* Cumulative time

Task can be comprised of subtasks. Then the duration and cost are functions of the subtasks

TODO: given a node, step through all time ticks for that branch and calculate staffing as a function of time.
Each branch has a separate staffing profile.

"""

# def new_task_id(all_tasks: dict):
#     task_ID_list = []
#     for desc, task in all_tasks.items():
#         task_ID_list.append(task.instance_ID)
#
#     found_new = False
#     while (not found_new):
#         how_about_this_ID = random.randint(1000,9999)
#         if how_about_this_ID not in task_ID_list:
#             found_new = True
#             return how_about_this_ID
#     return None

def validate_that_instance_ID_is_unique(instance_ID, all_tasks):
    """
    """
    for desc, task in all_tasks.items():
        if instance_ID==task.instance_ID:
            raise Exception("task ID",instance_ID,"is already in use by ",task.description)

class Task:
    """
    """
    def __init__(self,
                 instance_ID,
                 all_tasks,
                 condition,
                 description,
                 probability_of_task_success,
                 cost_duration_tuples_list,
                 staffing_list,
                 output_parameters_dict,
                 followed_by_task_instance_IDs):
        #self.persistent_ID = persistent_ID
        validate_that_instance_ID_is_unique(instance_ID, all_tasks)
        self.instance_ID = instance_ID
        self.condition = condition
        self.description = description
        self.probability_of_task_success = probability_of_task_success
        self.cumulative_probability_of_task_success = 0
        self.cost_duration_tuples_list = cost_duration_tuples_list
        self.staffing_list = []
        self.cumulative_cost_and_duration = []
        self.output_parameters_dict = output_parameters_dict
        self.followed_by_task_instance_IDs = followed_by_task_instance_IDs
        self.child_tasks = []

    def print(self):
        #print('persistent ID =', self.persistent_ID)
        print('instance ID   =', self.instance_ID)
        print('description =', self.description)
        print('probability_of_task_success =', self.probability_of_task_success)
        print('cost_duration_tuples_list =', self.cost_duration_tuples_list)
        print('staffing_list =',self.staffing_list)
        print('output_parameters_dict =', self.output_parameters_dict)
        print('followed_by_task_instance_IDs =', self.followed_by_task_instance_IDs)



def which_task_is_instance_ID(instance_ID, all_tasks):
    """
    """
    print("[TRACE] which_task_is_instance_ID: ",instance_ID)
    #print("looking for ",instance_ID)
    #print(type(instance_ID))
    #print("looking in ",all_tasks)
    for key_tuple, task in all_tasks.items():
        task_description = key_tuple[0]
        this_instance_ID = key_tuple[1]
        #print("does ",instance_ID,"match",this_instance_ID)
        #print(type(this_instance_ID))
        if this_instance_ID==instance_ID:
            return all_tasks[task_description,this_instance_ID]
    raise Exception("instance_ID ",instance_ID,"not found in all_tasks")
    return

def cumulative_probability_of_task_success(task, all_tasks):
    """
    """
    print("[TRACE] cumulative_probability_of_task_success: ",task.description)
    return all_tasks

def cost_and_duration_sum(task, all_tasks):
    """
    """
    print("[TRACE] cost_and_duration_sum: ",task.description)

    for follow_on_instance_ID in task.followed_by_task_instance_IDs:
        follow_on_task = which_task_is_instance_ID(follow_on_instance_ID, all_tasks)
        #all_tasks[follow_on_task.description,follow_on_task.instance_ID].cumulative_cost_and_duration = []
        for index, cost_dur_tuple in enumerate(task.cumulative_cost_and_duration):
            total_day_count= cost_dur_tuple[1]+follow_on_task.cost_duration_tuples_list[index][1]
            cumulative_date = datetime.datetime.today()+datetime.timedelta(days=total_day_count)
            all_tasks[follow_on_task.description,follow_on_task.instance_ID].cumulative_cost_and_duration.append(
                (cost_dur_tuple[0]+follow_on_task.cost_duration_tuples_list[index][0],
                 cost_dur_tuple[1]+follow_on_task.cost_duration_tuples_list[index][1],
                 datetime.datetime.strftime(cumulative_date, "%Y-%m-%d")) # https://strftime.org/
            )
        all_tasks[follow_on_task.description,follow_on_task.instance_ID].cumulative_probability_of_task_success = follow_on_task.probability_of_task_success*task.cumulative_probability_of_task_success

        # do this recursively
        all_tasks = cost_and_duration_sum(follow_on_task, all_tasks)

    for this_child_task in task.child_tasks:
        all_tasks = cost_and_duration_sum(all_tastsk[this_child_task], all_tasks)

    return all_tasks


def add_task_to_graph(G, task, all_tasks):
    """
    """
    print("[TRACE] add_task_to_graph: ",task.description)

    #task.print()
    G.add_node("instance_"+str(task.instance_ID),
           label="condition: "+str(task.condition)+"\l"+
                 "instance ID: "+str(task.instance_ID)+";  "
                 "description: "+str(task.description)+"\l"+
                 "p(success): "+str(task.probability_of_task_success)+";     "+
                 "cumulative p(success): "+str(round(task.cumulative_probability_of_task_success,5))+"\l"+
                 "cost and duration of this task="+str(task.cost_duration_tuples_list)+"\l"+
                 "sum(cost); sum(duration)= "+str(task.cumulative_cost_and_duration)+"\l"+
                 "staffing: "+str(task.staffing_list)+"\l"+
                 "output param="+str(task.output_parameters_dict)+"\l",
           shape="rect");
    return G

def add_task_to_graph_that_has_subtasks(G, task, list_of_subtasks, all_tasks):
    """
    """
    print("[TRACE] add_task_to_graph_that_has_subtasks: ",task.description)

    #all_tasks[(task.description,task.instance_ID)].child_tasks = list_of_subtasks

    B = G.add_subgraph(name="cluster_instance_"+str(task.instance_ID),
                       label="condition: "+str(task.condition)+"\l"+
                             "description: "+str(task.description)+"\l"+
                             "instance ID: "+str(task.instance_ID)+"\l"+
                             #"p(success): TODO\l"+ # depends on child tasks
                             #"cumulative p(success): "+str(cumulative_probability_of_task_success)+"\l"+
                             #"this task (cost,dur): TODO\l"+ # depends on child tasks
                             #"cumulative (cost,dur)= "+str(cumulative_cost_and_duration)+"\l"+
                             "output param="+str(task.output_parameters_dict)+"\l")

#    B.add_node("instance_"+str(task.instance_ID), style="invis");

    for subtask in list_of_subtasks:
        B = add_task_to_graph(B, all_tasks[subtask], all_tasks)

    return G


def add_edges(G, task):
    """
    """
    print("[TRACE] add_edges: ",task.description)
    for followed_by_instance_ID in task.followed_by_task_instance_IDs:
        G.add_edge("instance_"+str(task.instance_ID       ),
                   "instance_"+str(followed_by_instance_ID))
    return G

# def get_task_instance_ID(task_description, all_tasks):
#     """
#     """
#     print("[TRACE] get_task_instance_ID: ",task_description)
#     for task_tuple, this_task in all_tasks.items():
#         if this_task.description==task_description:
#             print("      ",this_task.instance_ID)
#             return this_task.instance_ID
#     print("ERROR: no task instance ID for ",task_description)
#     return

# def add_edge_from_task_to_task(task_description_source, task_description_sink, all_tasks):
#     """
#     """
#     source_instance_ID=get_task_instance_ID(task_description_source, all_tasks)
#     sink_instance_ID=get_task_instance_ID(task_description_sink, all_tasks)
#
#     return all_tasks

def create_graph(G, all_tasks):
    """
    """
    print("[TRACE] create_graph")
    for desc, task in all_tasks.items():
        # all_tasks = cumulative_probability_of_task_success(task, all_tasks)
        #
        # #print("last loop:",all_tasks)
        # cumulative, all_tasks = sum_cost_and_duration(task, all_tasks)
        #

        #task.print()

        #print("STATUS: now adding task to graph")
        if len(task.child_tasks)==0:
            G = add_task_to_graph(G, task, all_tasks)
        else:
            G = add_task_to_graph_that_has_subtasks(G, task,task.child_tasks,all_tasks)

        #print("STATUS: now adding edges to graph")
        G = add_edges(G, task)


    return G

if __name__ == "__main__":
    G = pygraphviz.AGraph(directed=True, compound=True)
    #G = pygraphviz.AGraph(directed=True, compound=True, rankdir="LR")
    #G.add_node("start_here", label="start here")

    all_tasks = {}

    # need to designate an entry point for calculating cumulative sums and products
    task = Task(6168,all_tasks,
                 "always", # condition
                 "start here", # description
                 1, # probability of success of this task
                 [(0,0), (0,0)], # cost and duration
                 [('a', 0.2)], # staffing: role and FTE
                 {}, # outputs
                 []) # followed by task IDs
    task.cumulative_cost_and_duration = [(0,0), (0,0)]
    task.cumulative_probability_of_task_success = 1
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(5842,all_tasks,
                 "if f<=4:", # condition
                 "a task", # description
                 0.91, # probability of success of this task
                 [(1,2), (3,4)], # cost and duration
                 [('a', 0.2)], # staffing: role and FTE
                 {'a'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

#    G.add_edge("start_here", "instance_"+str(task.instance_ID))

    task = Task(6643,all_tasks,
                 "always", # condition
                 "some task", # description
                 0.9, # probability of success of this task
                 [(2,2), (3,4)], # cost and duration
                 [('a', 0.2)], # staffing: role and FTE
                 {'f'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    all_tasks[("start here", 6168)].followed_by_task_instance_IDs.append(all_tasks[("some task",6643)].instance_ID)
    all_tasks[("some task", 6643)].followed_by_task_instance_IDs.append(all_tasks[("a task",5842)].instance_ID)

    task = Task(1234,all_tasks,
                 "always", # condition
                 "the task", # description
                 0.99, # probability of success of this task
                 [(3,1), (3,4)], # cost and duration
                 [('a', 0.2)], # staffing: role and FTE
                 {'a'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task_copy = copy.deepcopy(task)
    task_copy.instance_ID = 2345
    all_tasks[(task_copy.description, task_copy.instance_ID)] = task_copy

    task = Task(3456,all_tasks,
                 "always", # condition
                 "last task", # description
                 0.99, # probability of success of this task
                 [(1,1), (1,1)], # cost and duration
                 [('a', 0.2)], # staffing: role and FTE
                 {'k'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task_copy = copy.deepcopy(task)
    task_copy.instance_ID = 1456
    all_tasks[(task_copy.description, task_copy.instance_ID)] = task_copy

    task_copy = copy.deepcopy(task)
    task_copy.instance_ID = 2456
    all_tasks[(task_copy.description, task_copy.instance_ID)] = task_copy

    all_tasks[("the task", 2345)].followed_by_task_instance_IDs.append(all_tasks[("last task",3456)].instance_ID)
    all_tasks[("the task", 1234)].followed_by_task_instance_IDs.append(all_tasks[("last task",1456)].instance_ID)


    task = Task(4567,all_tasks,
                 "always", # condition
                 "my task", # description
                 0.99, # probability of success of this task
                 [(1,1), (1,1)], # cost and duration
                 [('a', 0.2)], # staffing: role and FTE
                 {'k'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    all_tasks[("a task", 5842)].followed_by_task_instance_IDs.append(all_tasks[("my task",4567)].instance_ID)
    all_tasks[("my task", 4567)].followed_by_task_instance_IDs.append(all_tasks[("last task",2456)].instance_ID)

    task = Task(5678,all_tasks,
                 "if f>4:", # condition
                 "parent task", # description
                 0.99, # probability of success of this task
                 [(4,3), (3,4)], # cost and duration
                 [('a', 0.2)], # staffing: role and FTE
                 {'b'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(6789,all_tasks,
                 "always", # condition
                 "la child task", # description
                 0.8, # probability of success of this task
                 [(8,3), (3,4)], # cost and duration
                 [('a', 0.2)], # staffing: role and FTE
                 {'c'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(7890,all_tasks,
                 "if c>=5", # condition
                 "el child task", # description
                 0.4, # probability of success of this task
                 [(1,1), (2,4)], # cost and duration
                 [('a', 0.2)], # staffing: role and FTE
                 {'b'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(1357,all_tasks,
                 "if c<5", # condition
                 "child task", # description
                 0.99, # probability of success of this task
                 [(7,7), (3,4)], # cost and duration
                 [('a', 0.2)], # staffing: role and FTE
                 {'b'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    all_tasks[("parent task",5678)].child_tasks = [
        ("la child task", 6789),
        ("el child task", 7890),
        ("child task", 1357)]

    all_tasks[("la child task", 6789)].followed_by_task_instance_IDs.append(all_tasks[("el child task", 7890)].instance_ID)
    all_tasks[("la child task", 6789)].followed_by_task_instance_IDs.append(all_tasks[("child task", 1357)].instance_ID)
    all_tasks[("some task", 6643)].followed_by_task_instance_IDs.append(all_tasks[("la child task", 6789)].instance_ID)

    all_tasks[("child task", 1357)].followed_by_task_instance_IDs.append(all_tasks[("the task", 1234)].instance_ID)
    all_tasks[("el child task", 7890)].followed_by_task_instance_IDs.append(all_tasks[("the task", 2345)].instance_ID)

    all_tasks = cost_and_duration_sum(all_tasks["start here",6168], all_tasks)

    #print("all_tasks",all_tasks)

    G = create_graph(G, all_tasks)
    #print(G)
    G.draw("automated_digraph.png", prog="dot")
