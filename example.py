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
        self.cumulative_cost_and_duration = []
        self.output_parameters_dict = output_parameters_dict
        self.followed_by_task_instance_IDs = followed_by_task_instance_IDs

    def print(self):
        #print('persistent ID =', self.persistent_ID)
        print('instance ID   =', self.instance_ID)
        print('description =', self.description)
        print('probability_of_task_success =', self.probability_of_task_success)
        print('cost_duration_tuples_list =', self.cost_duration_tuples_list)
        print('output_parameters_dict =', self.output_parameters_dict)
        print('followed_by_task_instance_IDs =', self.followed_by_task_instance_IDs)

def cumulative_probability_of_task_success(task, all_tasks):
    """
    """
    print("[TRACE] cumulative_probability_of_task_success: ",task.description)
    return all_tasks

def sum_cost_and_duration(task, all_tasks):
    """
    """
    print("[TRACE] sum_cost_and_duration: ",task.description)
    # what is the prior task?
    cumulative = []
    for candidate_prior_task_description, candidate_prior_task in all_tasks.items():
        for instance_ID in candidate_prior_task.followed_by_task_instance_IDs:
            if task.instance_ID == instance_ID:
                print("   sum_cost_and_duration: ", candidate_prior_task.description," is followed by",task.description)
                if len(candidate_prior_task.cumulative_cost_and_duration)==0:
                    print("   sum_cost_and_duration: cannot increment empty list")
                cumulative = []
                for index,old_cost_dur_tuple in enumerate(candidate_prior_task.cumulative_cost_and_duration):
                    cumulative.append((old_cost_dur_tuple[0]+task.cost_duration_tuples_list[index][0],
                                       old_cost_dur_tuple[1]+task.cost_duration_tuples_list[index][1]))
    return cumulative, all_tasks

def add_task(G, task, all_tasks):
    """
    """
    print("[TRACE] add_task: ",task.description)
    if task.description=="start here":
        all_tasks[(task.description, task.instance_ID)].cumulative_cost_and_duration = task.cost_duration_tuples_list

        cumulative_probability_of_task_success = task.probability_of_task_success
        cumulative_cost_and_duration = task.cost_duration_tuples_list
    else:
        #print(all_tasks)
        cumulative, all_tasks  = sum_cost_and_duration(task, all_tasks)
        cumulative_cost_and_duration = cumulative
        cumulative_probability_of_task_success = 1

    #task.print()
    G.add_node("instance_"+str(task.instance_ID),
           label="condition: "+str(task.condition)+"\l"+
                 "description: "+str(task.description)+"\l"+
                 "instance ID: "+str(task.instance_ID)+"\l"+
                 "p(success): "+str(task.probability_of_task_success)+"\l"+
                 "cumulative p(success): "+str(cumulative_probability_of_task_success)+"\l"+
                 "this task (cost,dur)="+str(task.cost_duration_tuples_list)+"\l"+
                 "cumulative (cost,dur)= "+str(cumulative_cost_and_duration)+"\l"+
                 "output param="+str(task.output_parameters_dict)+"\l",
           shape="rect");
    return G

def add_task_that_has_subtasks(G, task, list_of_subtasks, all_tasks):
    """
    """
    print("[TRACE] add_task_that_has_subtasks: ",task.description)
    # TODO; trace costs using all_tasks
    if task.description=="start here":
        cumulative_probability_of_task_success = task.probability_of_task_success
        cumulative_cost_and_duration = task.cost_duration_tuples_list
    else:
        cumulative, all_tasks  = sum_cost_and_duration(task, all_tasks)
        cumulative_cost_and_duration = cumulative
        cumulative_probability_of_task_success = 1

    B = G.add_subgraph(name="cluster_instance_"+str(task.instance_ID),
                       label="condition: "+str(task.condition)+"\l"+
                             "description: "+str(task.description)+"\l"+
                             "instance ID: "+str(task.instance_ID)+"\l"+
                             #"p(success): TODO\l"+ # depends on child tasks
                             #"cumulative p(success): "+str(cumulative_probability_of_task_success)+"\l"+
                             #"this task (cost,dur): TODO\l"+ # depends on child tasks
                             #"cumulative (cost,dur)= "+str(cumulative_cost_and_duration)+"\l"+
                             "output param="+str(task.output_parameters_dict)+"\l")

    B.add_node("instance_"+str(task.instance_ID), style="invis");

    for subtask in list_of_subtasks:
        B = add_task(B, subtask, all_tasks)

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

if __name__ == "__main__":
    G = pygraphviz.AGraph(directed=True, compound=True)
    #G.add_node("start_here", label="start here")

    all_tasks = {}

    # need to designate an entry point for calculating cumulative sums and products
    task = Task(6168,
                 all_tasks,
                 "always", # condition
                 "start here", # description
                 1, # probability of success of this task
                 [(0,0), (0,0)], # cost and duration
                 {}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(5842,
                all_tasks,
                 "if f<=4:", # condition
                 "a task", # description
                 0.99, # probability of success of this task
                 [(1,2), (3,4)], # cost and duration
                 {'a'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

#    G.add_edge("start_here", "instance_"+str(task.instance_ID))

    task = Task(6643,
                 all_tasks,
                 "always", # condition
                 "some task", # description
                 0.99, # probability of success of this task
                 [(2,2), (3,4)], # cost and duration
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
                 {'a'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(2345,all_tasks,
                 "always", # condition
                 "the task", # description
                 0.99, # probability of success of this task
                 [(3,1), (3,4)], # cost and duration
                 {'a'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(3456,all_tasks,
                 "always", # condition
                 "last task", # description
                 0.99, # probability of success of this task
                 [(1,1), (1,1)], # cost and duration
                 {'k'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(1456,all_tasks,
                 "always", # condition
                 "last task", # description
                 0.99, # probability of success of this task
                 [(1,1), (1,1)], # cost and duration
                 {'k'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(2456,all_tasks,
                 "always", # condition
                 "last task", # description
                 0.99, # probability of success of this task
                 [(1,1), (1,1)], # cost and duration
                 {'k'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    all_tasks[("the task", 2345)].followed_by_task_instance_IDs.append(all_tasks[("last task",3456)].instance_ID)
    all_tasks[("the task", 1234)].followed_by_task_instance_IDs.append(all_tasks[("last task",1456)].instance_ID)

    task = Task(4567,all_tasks,
                 "always", # condition
                 "my task", # description
                 0.99, # probability of success of this task
                 [(1,1), (1,1)], # cost and duration
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
                 {'b'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(6789,all_tasks,
                 "always", # condition
                 "la child task", # description
                 0.99, # probability of success of this task
                 [(8,3), (3,4)], # cost and duration
                 {'c'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(7890,all_tasks,
                 "if c>=5", # condition
                 "el child task", # description
                 0.99, # probability of success of this task
                 [(1,1), (2,4)], # cost and duration
                 {'b'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task

    task = Task(1357,all_tasks,
                 "if c<5", # condition
                 "child task", # description
                 0.99, # probability of success of this task
                 [(7,7), (3,4)], # cost and duration
                 {'b'}, # outputs
                 []) # followed by task IDs
    all_tasks[(task.description, task.instance_ID)] = task


    all_tasks[("la child task", 6789)].followed_by_task_instance_IDs.append(all_tasks[("el child task", 7890)].instance_ID)
    all_tasks[("la child task", 6789)].followed_by_task_instance_IDs.append(all_tasks[("child task", 1357)].instance_ID)
    all_tasks[("some task", 6643)].followed_by_task_instance_IDs.append(all_tasks[("parent task", 5678)].instance_ID)

    G = add_task_that_has_subtasks(G, all_tasks[("parent task", 5678)],
                                   [all_tasks[("el child task",7890)],
                                    all_tasks[("child task", 1357)],
                                    all_tasks[("la child task", 6789)]
                                   ],
                                   all_tasks)

    all_tasks[("child task", 1357)].followed_by_task_instance_IDs.append(all_tasks[("the task", 1234)].instance_ID)
    all_tasks[("el child task", 7890)].followed_by_task_instance_IDs.append(all_tasks[("the task", 2345)].instance_ID)

    for desc, task in all_tasks.items():
        # all_tasks = cumulative_probability_of_task_success(task, all_tasks)
        #
        # #print("last loop:",all_tasks)
        # cumulative, all_tasks = sum_cost_and_duration(task, all_tasks)
        #

        task.print()

        print("STATUS: now adding task to graph")
        G = add_task(G, task, all_tasks)

        print("STATUS: now adding edges to graph")
        G = add_edges(G, task)


    G.draw("automated_digraph.png", prog="dot")
