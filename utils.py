#/usr/bin/env python3

import os
import json
import action_tree
import yaml
from game import node_parser

def wrap_action(action):
    return action

def load_nodes(filename):
    with open(filename, 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.FullLoader)
    raw_nodes = config['nodes']
    start_message, help_message = config['intro']['start'], config['intro']['help']
    nodes = [node_parser(n) for n in raw_nodes]
    return nodes, start_message, help_message

def load_worlds(filename, nodes):
    if os.path.exists(filename):
        data = json.load(open(filename))
        worlds = {k:action_tree.World(nodes).load(v) for k, v in data.items()}
        return worlds
    else:
        return dict()

def get_action_id(world, message):
    for i, action in enumerate(world.possible_actions()):
        if message == action.message:
            return i
    return -1

def dump_worlds(worlds):
    return {k:v.dump() for k, v in worlds.items()}
