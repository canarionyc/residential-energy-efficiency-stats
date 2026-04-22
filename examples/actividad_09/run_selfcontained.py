# class RuleNode:
#     def __init__(self, name, predicate, on_true, on_false):
#         self.name = name
#         self.predicate = predicate
#         self.on_true = on_true
#         self.on_false = on_false
#
#     def run(self, context, history=None):
#         if history is None:
#             history = []
#
#         result = self.predicate(context)
#         decision_path = "Passed" if result else "Failed"
#         history.append(f"{self.name}: {decision_path}")
#
#         next_step = self.on_true if result else self.on_false
#
#         if isinstance(next_step, RuleNode):
#             return next_step.run(context, history)
#
#         return {"result": next_step, "messages": history}


#%% --- CASCADING SUB-NODES ---



# Test Case 03: 23 meters (should trigger Local cascade)
case_03 = {
    "total_meters": 23,
    "room_height": 2.40,
    "frontal_clearance": 1.20
}

#%%
from pprint import pprint
output = root_node.run(case_03)
pprint(output)
print(f"Outcome: {output['result']}")
for msg in output['messages']:
    print(f" - {msg}")