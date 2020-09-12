import numpy as np


class State():
    def __init__(self, money=0, start_time=0):
        self.money = money
        self.time = start_time

    def __repr__(self):
        return f'''
Состояние:
money: {self.money}
time: {self.time}
'''

    def dump(self):
        return {
            'money': self.money,
            'time': self.time
        }
    
    @staticmethod
    def load(dict_obj):
        return State(dict_obj['money'], dict_obj['time'])
    
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

    def do_action(self, state, action_id):
        new_action = self.actions[action_id]
        new_state = new_action.apply_state_change(state)
        return new_state, new_action.child, new_action.message


class World():
    def __init__(self, nodes):
        self.nodes = nodes
        self.current_node = self.nodes[0]
        self.current_state = State(1000, 0)
    
    @property
    def state(self):
        return self.current_state
    
    @property
    def node(self):
        return self.current_node
    
    def possible_actions(self):
        return self.current_node.actions
    
    def do_action(self, action_id=None):
        '''
            if current_node is action, require action_id
            return new_state, child_id, action_message
        '''
        if self.current_node.type == 'action':
            if isinstance(action_id, int):
                if 0 <= action_id < len(self.current_node.actions):
                    new_state, child_id, action_message = self.current_node.do_action(
                        self.current_state, action_id
                    )
                else:
                    raise Exception('invalid action_id')
            else:
                raise Exception('require action_id')
        
        else:
            new_state, child_id, action_message = self.current_node.do_action(self.current_state)
        
        self.current_node = self.nodes[child_id]
        self.current_state = new_state
        return new_state, action_message 
    
    def __repr__(self, ):
        return f'current state: {self.current_state.money} ТФ Рублей. Сейчас {self.current_state.time} игровой день'

    def dump(self):
        state = self.current_state.dump()
        current_node_index = self.nodes.index(self.current_node)
        return {
            'current_node_index': current_node_index,
            'current_state': state,
        }
    
    def load(self, dict_obj):
        state = State.load(dict_obj['current_state'])
        self.current_state = state
        self.current_node = self.nodes[dict_obj['current_node_index']]

