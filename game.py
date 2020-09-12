import yaml
from action_tree import *


def state_change_generator(money, time):
    def state_change(state):
        state.money += money
        state.time += time
        return state
    return state_change

def node_parser(raw_node):
    actions = []
    for raw_action in raw_node['actions']:
        if raw_node['type'] == 'action':
            prob = None
        else:
            prob = raw_action['prob']
        actions.append(
            Action(
                raw_action['message'],
                state_change_generator(
                    raw_action['state_change']['money'],
                    raw_action['state_change']['time']
                ),
                raw_action['child'],
                prob
            )
        )

    if raw_node['type'] == 'action':
        return ActionNode(raw_node['message'], actions)
    else:
         return RandomNode(raw_node['message'], actions)

if __name__ == '__main__':
    with open('action_tree.yaml', 'r') as f:
        raw_nodes = yaml.load(f.read())['nodes']

    nodes = [node_parser(n) for n in raw_nodes]

    world = World(nodes)
    while True:
        world.time_step()
        print('')