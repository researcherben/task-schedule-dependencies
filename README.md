# Summary

These Python scripts implement a task dependency Gantt chart visualization in GraphViz.

Inspired by Microsoft Project (which features tasks, subtasks, task dependencies, and task duration), plus support for additional complexity like
* range of duration and cost per task
* branching of follow-on tasks
* probability of success per task
* staffing level and roles per task
* track cumulative duration, cumulative cost, and cumulative probability of success per branch

# Quick start

Assuming you have a Docker container that has GraphViz
```bash
cd package
docker run -v `pwd`:/home/jovyan <jupyter> python3 generate_graph.py
```

# Learning why complexity is challenging

## task duration and cost

A task in a Gantt chart has a duration. A task can be assigned a cost.
Can the task take less time if we spend more money?
Or is the case that a task compressed into less time costs less?
What is the shape of the Pareto frontier on a plot of cost versus duration? A task with a list of cost-duration tuples is one way to specify the Pareto frontier.

In the Python script the cost and duration are a list of tuples. Another interpretation of the list is to describe the uncertainty in cost-duration. Is the guess for cost a bell curve over time? Monotonically increasing or monotonically decreasing over time?

Regardless of interpretation, calculating the cumulative cost and cumulative duration impose constraints on the branching described below.


Each of the discrete tuples in the list is really an xor branching path. Extracting the staffing model for a branch is made difficult by having a range of durations per task.

## Task dependencies

Suppose I have task A followed by task B:
```
A --> B
```
The cumulative cost is additive, the cumulative duration is additive, and the cumulative probability of success is multiplicative.

Now suppose I have a task with two follow-on tasks:
```
  /--> B
 /
A
 \
  \--> C
```
There are a couple ways of interpreting the dependency diagram:
* xor branching: "(A followed by B) xor (A followed by C)". The calculation of cumulative variables (cost, schedule, probability of success) mean follow-on branches cannot merge downstream.
* conditional branching: "if x>5 then (A followed by B) else (A followed by C)." As with xor branching, follow-on branches cannot merge downstream.
* and branching: "A followed by (B and C)". You must do both B and C; follow-on tasks merge.
