#!/usr/bin/env python3

import random
# https://pypi.org/project/pygraphviz/
# https://pygraphviz.github.io/documentation/stable/
import pygraphviz

import example_tasks

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

To run this script use

    docker run -v `pwd`:/home/jovyan <jupyter> python3 generate_graph.py

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


def cumulative_probability_of_task_success(task, all_tasks):
    """
    Args:
      task: an instance of the Task class
      all_tasks: a dictionary of {('task decription', integer task instance ID): <instance of Task class>}

    Returns:
      all_tasks: a dictionary of {('task decription', integer task instance ID): <instance of Task class>}

    """
    print("[TRACE] cumulative_probability_of_task_success: ",task.description)
    return all_tasks



def add_task_to_graph(G, task, all_tasks):
    """
    Args:
      G: a pygraphviz AGraph -- https://pygraphviz.github.io/documentation/stable/reference/agraph.html
      task: an instance of the Task class
      all_tasks: a dictionary of {('task decription', integer task instance ID): <instance of Task class>}

    Returns:
      G: a pygraphviz AGraph -- https://pygraphviz.github.io/documentation/stable/reference/agraph.html

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
    Args:
      G: a pygraphviz AGraph -- https://pygraphviz.github.io/documentation/stable/reference/agraph.html
      task: an instance of the Task class
      list_of_subtasks: tuples
      all_tasks: a dictionary of {('task decription', integer task instance ID): <instance of Task class>}

    Returns:
      G: a pygraphviz AGraph -- https://pygraphviz.github.io/documentation/stable/reference/agraph.html

    >>> add_task_to_graph_that_has_subtasks()
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
    Args:
      G: a pygraphviz AGraph -- https://pygraphviz.github.io/documentation/stable/reference/agraph.html
      task: an instance of the Task class

    Returns:
      G: a pygraphviz AGraph -- https://pygraphviz.github.io/documentation/stable/reference/agraph.html

    >>> add_edges()
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
    Args:
      G: a pygraphviz AGraph -- https://pygraphviz.github.io/documentation/stable/reference/agraph.html
      all_tasks: a dictionary of {('task decription', integer task instance ID): <instance of Task class>}

    Returns:
      G: a pygraphviz AGraph -- https://pygraphviz.github.io/documentation/stable/reference/agraph.html

    >>> create_graph()
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

    G = create_graph(G, example_tasks.all_tasks)
    #print(G)
    G.draw("automated_digraph.png", prog="dot")


# EOF
