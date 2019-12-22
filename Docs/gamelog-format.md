# Gamelog Format

Gamelogs are a file that logs everything that happened in a game, for future playback. Expect them to to gzipped json files.

## Example

This example is a game called "Move". Two players each have 1 Unit, and the first player to move their Unit onto the same (x, y) as the other player's Unit wins!

This gamelog describes such a game where:

1. The game is initialized
2. Player 0's turn starts
3. Player 0 moves their Unit towards Player 1's Unit
4. Player 0 ends their turn
5. Player 1's turn begins
6. Player 1 moves their Unit towards Player 0's Unit, moving over it, and thus winning the game!

``` json
{
  "gameName": "Move",
  "gameSession": "2",
  "deltas": [
    {
      "type": "start",
      "game": {
        "players": {
          "0": {
            "id": "0"
          },
          "1": {
            "id": "1"
          },
          "&LEN": 2
        },
        "gameObjects": {
          "0": {
            "id": "0",
            "gameObjectName": "Player",
            "logs": {
              "&LEN": 0
            },
            "clientType": "Lua",
            "lost": false,
            "name": "Move Lua Player",
            "otherPlayer": {
              "id": "1"
            },
            "reasonLost": "",
            "reasonWon": "",
            "timeRemaining": 60000000000,
            "won": false
          },
          "1": {
            "id": "1",
            "gameObjectName": "Player",
            "logs": {
              "&LEN": 0
            },
            "clientType": "JavaScript",
            "lost": false,
            "name": "Move JavaScript Player",
            "otherPlayer": {
              "id": "0"
            },
            "reasonLost": "",
            "reasonWon": "",
            "timeRemaining": 60000000000,
            "won": false
          },
          "2": {
            "id": "2",
            "gameObjectName": "Unit",
            "logs": {
              "&LEN": 0
            },
            "hasMoved": false,
            "owner": {
              "id": "0"
            },
            "x": 8,
            "y": 8
          },
          "3": {
            "id": "3",
            "gameObjectName": "Unit",
            "logs": {
              "&LEN": 0
            },
            "hasMoved": false,
            "owner": {
              "id": "1"
            },
            "x": 9,
            "y": 10
          }
        },
        "session": "2",
        "name": "Move",
        "currentTurn": 0,
        "maxTurns": 100,
        "currentPlayer": {
          "id": "0"
        },
        "units": {
          "0": {
            "id": "2"
          },
          "1": {
            "id": "3"
          },
          "&LEN": 2
        }
      }
    },
    {
      "type": "ran",
      "data": {
        "player": {
          "id": "0"
        },
        "run": {
          "functionName": "move",
          "caller": {
            "id": "2"
          },
          "args": {
            "y": 9,
            "x": 9
          }
        },
        "returned": true
      },
      "game": {
        "gameObjects": {
          "0": {
            "timeRemaining": 59998045033
          },
          "2": {
            "x": 9,
            "y": 9,
            "hasMoved": true
          }
        }
      }
    },
    {
      "type": "finished",
      "data": {
        "player": {
          "id": "0"
        },
        "order": "runTurn",
        "returned": true
      },
      "game": {
        "gameObjects": {
          "0": {
            "timeRemaining": 59959439522
          },
          "1": {
            "timeRemaining": 60100000000
          },
          "2": {
            "hasMoved": false
          }
        },
        "currentTurn": 1,
        "currentPlayer": {
          "id": "1"
        }
      }
    },
    {
      "type": "ran",
      "data": {
        "player": {
          "id": "1"
        },
        "run": {
          "functionName": "move",
          "caller": {
            "id": "3"
          },
          "args": {
            "y": 9,
            "x": 9
          }
        },
        "returned": true
      },
      "game": {
        "gameObjects": {
          "0": {
            "lost": true,
            "reasonLost": "Got moved on."
          },
          "1": {
            "timeRemaining": 60099785443,
            "won": true,
            "reasonWon": "Moved to other unit."
          },
          "2": {
            "x": -1,
            "y": -1
          },
          "3": {
            "y": 9,
            "hasMoved": true
          }
        }
      }
    },
    {
      "type": "over",
      "game": {}
    }
  ],
  "constants": {
    "DELTA_REMOVED": "&RM",
    "DELTA_LIST_LENGTH": "&LEN"
  },
  "epoch": 1456434830562,
  "randomSeed": "1xftop9ya3piudi",
  "winners": [
    {
      "index": 1,
      "id": "1",
      "name": "Move Lua Player"
    }
  ],
  "losers": [
    {
      "index": 0,
      "id": "0",
      "name": "Move Lua Player"
    }
  ]
}
```

Yes, gamelogs are large. That's why we compress them.

## Structure

At the root of a gamelog you can expect the following:

| Field       | Type     | Description |
|-------------|----------|-------------|
| gameName    | string   | Name of the game |
| gameSession | string   | ID of the game session |
| deltas      | delta[]  | An array of deltas, more on deltas later, as they are the "meat" of a gamelog |
| constants   | Object   | string keys mapping to string values representing constants used for delta parsing |
| epoch       | int      | Unix epoch when the gamelog was created |
| randomSeed  | string   | The random seed used for any random events in the game |
| winners     | client[] | *depreciated* List of clients that won the game |
| losers      | client[] | *depreciated* List of clients that lost the game |

### `constants`

During delta parsing two constants are used, `DELTA_REMOVED`, and `DELTA_LIST_LENGTH`. Those keys should be present in this object, with their value being what to expect in the deltas.

Normally, `DELTA_REMOVED == "&RM"` and `DELTA_LIST_LENGTH == "&LEN"`, but don't assume as you have the actual values here.

### `winners` and `losers`

Clients will be contains in these lists, expect a client to have:

| Field | Type   | Description |
|-------|--------|-------------|
| index | int    | The index of the player in the game's players. should be >= 0 |
| id    | string | The id of the player as the player GameObject, if you need more information look in the deltas using this |
| name  | string | The name of the player/client |

**Note**: The winners/losers lists here are depreciated, and will be removed when the Arena does not need to parse gamelogs. You can discern winners/losers from the last state of the game.

### `deltas`

The `deltas` field is a list of delta objects. To get any state of the game you take the initial state, and apply deltas after it to it until you are at the state you want. Which makes sense as deltas are a change in state.

A Delta object looks like:

| Field  | Type   | Description |
|--------|--------|-------------|
| type   | string | What type of delta it is, or more accurately, *why* the delta occured.
| [data] | Object | Some data about *why* the data occured, different types have different datas for why they occured. Commonly this will contain some of the data sent over the network that caused the delta. |
| [game] | Object | How the game actually changed. This is the meat of a Delta. |

#### Parsing Deltas

If you look at each `deltas[i].game` and flatten them on each other, you will see the game, step by step. But how do you flatten/parse them? Well, the basic algorithm is:

``` js
function isObject(obj) {
    return typeof(obj) === "object" && obj !== null; // null is considered an object in js
};

function mergeDelta(state, delta) {
    var deltaLength = delta[gamelog.constants.DELTA_LIST_LENGTH];

    if(deltaLength !== undefined) { // then this part in the state is an array
        delete delta[gamelog.constants.DELTA_LIST_LENGTH]; // we don't want to copy this key/value over to the state, it was just to signify it is an array
        while(state.length > deltaLength) { // pop elements off the array until the array is short enough. an increase in array size will be added below as arrays resize when keys larger are set
            state.pop();
        }
    }

    for(var key in delta) {
        if(delta.hasOwnProperty(key)) {
            var d = delta[key];

            if(d === gamelog.constants.DELTA_REMOVED) {
                delete state[key];
            }
            else if(isObject(d) && isObject(state[key])) {
                mergeDelta(state[key], d);
            }
            else {
                if(isObject(d)) {
                    var newState = (d[gamelog.constants.DELTA_LIST_LENGTH] === undefined ? {} : []); // creates an object or array
                    state[key] = mergeDelta(newState, d);
                }
                else {
                    state[key] = d;
                }
            }
      }
  }

    return state;
};

var parsed = {};

for(var i = 0; i < gamelog.deltas.length; i++) {
    parsed = mergeDelta(parsed, gamelog.deltas[i].game);
}

// parsed is now the flattened game log, and in the above loop at each iteration i you have the state at that step
```

The basics here are to `mergeDelta(state, delta)`:

1. If the delta is a list, pop items off the back if the list shrank in size
2. now look at each key, value in the delta
3. if the delta value is DELTA_REMOVED, delte the key from the state
4. otherwise if the delta value is an object, and the state has an object at the same key, recursively mergeDelta into them.
5. otherwise just update the new value. If the new delta is an object make it a dictionary or list depeneding on what it is.

This is *almost* just recusively overwritting key/values in one object to another, with 3 exceptions:

1. An object containing the DELTA_LIST_LENGTH key is not an object, but an array. The length of the array is whatever the value for DELTA_LIST_LENGTH is. Keys in that object will be strings, but cast them to ints. This allows us to save space because if only one item at `i` in an array changed value a json array would require padded `nulls` in a json array, which would imply every item before `i` became `null`. This is more precises, without repeating data.
2. The special string DELTA_REMOVED represents a key deletion. This will occur most often on arrays when they shrink in size.
3. Cycles can and will be present, pointing to some GameObject in `game.gameObjects[id]`, so, if you see somewhere the value: `{ id: "1" }`, that means replace that value with the GameObject with id `"1"`, luckily the gameObjects dictionary is indexed by the id for you. The technical term for this is a shallow reference.

That's it, if you follow these rules you can parse deltas.

#### Delta Types

There are a variety of events that can occur that will cause a delta. If a `game` field is present on a delta, merge it. Otherwise we will describe what to expect in each type's data, as well as why the type occurs.

##### start

This should always be the first delta (`gamelog.deltas[0]`). This gets recorded right after the Game is initialized and begins.

`data`: There is no data for the `start` type.

##### ran

This occurs when a client requests some GameObject runs a function on the game server. Once that function is `ran`, the game will probably change.

`data`:
```
"player": { "id": "playerGameObjectID" },
"run": {
  "functionName": "someFunctionNameOnTheCaller",
  "caller": { "id": "someGameObjectsID" },
  "args": { "//": "key value pairs as arguments to the functionName. These are NOT sanatized from the client, so if they sent the string '1', and intended the int 1, the string version will be recorded here. This is great information for competitors to see if their AI is sending invalid data." }
},
"returned": "Whatever the function returned: booleans, strings, ints, GameObjects (as shallow references), etc."
```

##### finished

When an AI finishes an order, this is recorded. `AI::runTurn()` is an example of an order, where they return true or false if they want to end their turn. After they finish something game logic can happen.


`data`:
```
"player": { "id": "theAIsPlayerID" },
"order": "some string of the function on the AI that has finished (returned)",
"returned": "another return type, could be anything"
```

##### over

When the game is over this delta occurs. The game may change when it is over, but it is porbably more common that the delta before this contains the final change in game data.

`data`: There is no data for the `over` type.

##### disconnect

When a client disconnects, either unexpectedly, or via timeout, we record it here. The `game` on this delta should be set as when a client disconencts they lose the game.

`data`:
```
"player": { "id": "theAIsPlayerIDThatDisconnected" },
```

## Final Notes

Remember that the attributes and functions of the Game, GameObjects, and the AI are all defined in Creer data. Creer is Cadre's codegen, and if you need to parse gamelogs, you probably care about *what* the game objects are and should have. Feel free to plug into the Creer code generation via templates to ease parsing each game.
