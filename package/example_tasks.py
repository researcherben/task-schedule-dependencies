#!/usr/bin/env python3

import copy # https://docs.python.org/3/library/copy.html

from task_library import Task
from task_library import cost_and_duration_sum

"""
tasks that get graphed by generate_graph.py 
"""

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

# last step is to insert cost/duration tuples
all_tasks = cost_and_duration_sum(all_tasks["start here",6168], all_tasks)

# EOF
