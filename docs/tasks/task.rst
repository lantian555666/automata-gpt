Task
====

``Task`` is a primary object used by ``TaskExecutor`` in the Automata
library. The ``Task`` object is responsible for storing the task id,
priority, max retries, and delivering task-oriented action to the
respective task function when the task is executed. In addition to
these, it also contains a method to generate a deterministic task id
which is based on the hash of the hashable keyword arguments.

Overview
--------

The ``Task`` plays a pivotal role in task execution by storing the
necessary details about the task. By default, it assigns unique
identifiers generated by the universally unique identifier (uuid)
module. However, you have the option to generate a deterministic id
based on the hash of the hashable keyword arguments.

Note that the task status will be noted by ``TaskExecutor`` as it
proceeds to execute different stages. This task status is retrievable
using the status property of the class. Furthermore, you can set the
status of the task using the status setter property.

Related Symbols
---------------

-  ``automata.tests.unit.test_task_database.task``
-  ``automata.tests.unit.test_task_environment.test_commit_task``
-  ``automata.tasks.tasks.AutomataTask``
-  ``automata.tests.unit.test_task_database.test_get_tasks_by_query``
-  ``automata.tasks.base.ITaskExecution.execute``
-  ``automata.tests.unit.test_task_database.test_update_task``
-  ``automata.tests.unit.test_task_database.test_database_lifecycle``
-  ``automata.tests.unit.test_task_database.test_insert_task``
-  ``automata.tasks.base.ITaskExecution``
-  ``automata.tests.conftest.registry``

Usage Example
-------------

.. code:: python

   from automata.tasks.base import Task

   task = Task(priority=1, max_retries=5)
   print(f"ID of the created task: {task.task_id}")

Limitations
-----------

The current design does not allow to retrieve the task id, priority and
max retries once the task object is initialized. If you need to retrieve
these properties, you will need to capture these values during task
initialization.

If a task status is set to ``RETRYING``, and if the maximum retries set
is exceeded, the task status will be marked ``FAILED``. In case, the
application logic requires further retries despite the retry limit, you
will need to create a new Task instance with the required parameters and
execute it as a fresh task.

Follow-up Questions
-------------------

-  Can we include mechanism that would enable us to retrieve the initial
   properties of Task object, such as task id, priority and max_retries
   once initialized?
-  Should we allow indefinite retries despite exceeding the maximum
   retry limit? If yes, what would be the best approach to implement
   this feature?
-  Should there be an option to reset the status of the task back to its
   original state in case of failure in execution?
