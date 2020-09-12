import yaml
import json
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


def get_new_action_id():
    chosed_id = input('choose id: ')
    try:
        chosed_id = int(chosed_id)
        return chosed_id
    except Exception as e:
        return  get_new_action_id()


if __name__ == '__main__':
    with open('action_tree.yaml', 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)

    print('start: ', config['intro']['start'])
    print('help:  ', config['intro']['help'])

    raw_nodes = config['nodes']
    nodes = [node_parser(n) for n in raw_nodes]

    world = World(nodes)

    while True:
        print('-'*50)
        print(world.state)

        if world.node.message and world.node.message != '':
            print(world.node.message)
        
        if world.node.type == 'random':
            new_state, action_message = world.do_action()
            if action_message and action_message != '':
                print(action_message)
        
        elif world.node.type == 'action':
            for idx, msg in world.node.action_messages:
                print(f'{idx:5}: {msg}')

            chosed_id = get_new_action_id()
            new_state, action_message = world.do_action(chosed_id)
        else:
            raise Exception(f'unexpected error. Not supported node type {world.node.type}')

            
        if world.state.money < 0:
            print("\n\nДенег больше нет!\nТы проиграл!")
            break

        # Dump world
        with open('world_dump.json', 'w') as f:
            f.write(json.dumps(world.dump()))
        
        # Load world
        with open('world_dump.json', 'r') as f:
            dict_obj = json.loads(f.read())
            world.load(dict_obj)



