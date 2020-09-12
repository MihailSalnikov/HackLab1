import numpy as np

class State():
    def __init__(self, money=0, start_time=0):
        self.money = money
        self.time = start_time

    
class Action():
    def __init__(self, message, state_change, child, prob=None):
        self.message = message
        self.state_change = state_change
        self.child = child
        self.prob = prob
    
    def apply_state_change(self, state):
        return self.state_change(state)

    def __repr__(self):
        return f'action: {self.message}'


class Node():
    def __init__(self, message, actions):
        self.message = message
        self.actions = actions

class RandomNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'random'
    
    def do_action(self, state):
        probs = [a.prob for a in self.actions]
        action_id = np.random.choice(range(len(self.actions)), p=probs)
        action = self.actions[action_id]
        new_state = action.apply_state_change(state)
        return new_state, action.child, action.message

class ActionNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'action'

    @property
    def action_messages(self):
        for i, action in enumerate(self.actions):
            yield (i, action.message)

    def do_action(self, state):
        for i, msg in self.action_messages:
            print(f'{i}: ', end='')
            if msg:
                print(msg)
        act_id = int(input('Выбери ответ '))
        action = self.actions[act_id]
        new_state = action.apply_state_change(state)
        return new_state, action.child, None

class World():
    def __init__(self, nodes):
        self.nodes = nodes
        self.current_node = self.nodes[0]
        self.current_state = State(1000, 0)

    def time_step(self):
        if self.current_node.message:
            print(self.current_node.message)

        self.current_state, new_node_id, action_message = self.current_node.do_action(self.current_state)
        if action_message:
            print(action_message)
        
        self.current_node = self.nodes[new_node_id]
    
    def __repr__(self, ):
        return f'current state: {self.current_state.money} ТФ Рублей. Сейчас {self.current_state.time} игровой день'



