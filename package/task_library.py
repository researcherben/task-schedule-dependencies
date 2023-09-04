#!/usr/bin/env python3

import datetime

def validate_that_instance_ID_is_unique(instance_ID, all_tasks) -> None:
    """
    Args:
      instance_ID: integer
      all_tasks: a dictionary of {('task decription', integer task instance ID): <instance of Task class>}

    Returns:
      None

    Raises:
      failure message

    """
    for desc, task in all_tasks.items():
        if instance_ID==task.instance_ID:
            raise Exception("task ID",instance_ID,"is already in use by ",task.description)
    return

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


def cost_and_duration_sum(task, all_tasks):
    """
    Args:
      task: an instance of the Task class
      all_tasks: a dictionary of {('task decription', integer task instance ID): <instance of Task class>}

    Returns:
      all_tasks: a dictionary of {('task decription', integer task instance ID): <instance of Task class>}

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

def which_task_is_instance_ID(instance_ID, all_tasks):
    """
    Args:
      instance_ID: integer
      all_tasks: a dictionary of {('task decription', integer task instance ID): <instance of Task class>}

    Returns:
      None

    Raises:
      failure message

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
