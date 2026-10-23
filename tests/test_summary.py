# Unit test for the new summary() feature
from app import summary
 
 
def test_summary_counts_tasks():
    assert summary([]) == "No tasks"  # an empty list
    assert summary(["Write tests"]) == "1 task"  # one task uses the singular word
    assert summary(["Write tests", "Build artifact"]) == "2 tasks"  # two tasks
