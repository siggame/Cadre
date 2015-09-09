import os.path
import json
import numbers

game_infos = {}

def _get_json_file(path):
    if not os.path.isfile(path):
        raise Exception("No file found at '" + str(path) + "'.")

    with open(path) as json_file:
        return json.load(json_file)

def _get_gamelog(gamelog_or_pathto):
    if type(gamelog_or_pathto) == str:
        return _get_json_file(gamelog_or_pathto)
    else:
        return gamelog_or_pathto

def _get_game_info(game_name, games_dir):
    if not game_name in game_infos:
        game_infos[game_name] = _get_json_file(os.path.join(games_dir, game_name + ".data"))

    return game_infos[game_name]

def _merge(i, id, delta, counts):
    if not id in counts:
        counts[id] = {
            'first_delta': i,
            'sums': {},
            'obj': {}
        }

    count = counts[id]
    if delta == "&RM":
        count['last_delta'] = i
    else:
        for key, value in delta.items():
            if not key in count['sums']:
                count['sums'][key] = 0

            add = 0
            if isinstance(value, numbers.Number):
                add = value
            else: # default handler, count every time we get a delta for this change
                add = 1

            count['sums'][key] += add
            count['obj'][key] = value


def _get_kmeans(gamelog, games_dir):
    game_name = gamelog['gameName']
    game_info = _get_game_info(game_name, games_dir)
    counts = {}
    for i, delta in enumerate(gamelog['deltas']):
        game = delta['game']
        game['gameObjectName'] = "Game" # hackish way to handle Game kmeans as if they were game objects
        _merge(i, "Game", game, counts)
        if 'gameObjects' in game:
            for id, gameobject_delta in game['gameObjects'].items():
                _merge(i, id, gameobject_delta, counts)

    kmeans = []
    for kmean_info in game_info:
        obj_name = kmean_info['gameObjectName']
        obj_attr = kmean_info['attributeName']

        count_sum = 0
        count_objs = 0
        for id, count in counts.items():
            if count['obj']['gameObjectName'] == obj_name:
                count_sum += count['sums'][obj_attr]
                count_objs += 1

        if kmean_info['type'] == "sum":
            kmeans.append(count_sum)
        elif kmean_info['type'] == "average":
            average = 0
            if count_objs > 0: # no division by zero
                average = count_sum / count_objs
            kmeans.append(average)
        else:
            raise Exception("Unkown kmean type '" + str(kmean_info['type']) + "'")

    return kmeans

# This is the only "public" interface. See example.py for usage
def parse(gamelog_or_pathto, games_dir="./games/"):
    gamelog = _get_gamelog(gamelog_or_pathto)
    return _get_kmeans(gamelog, games_dir)
