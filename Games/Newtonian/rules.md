# MMAI 21: [Pirates]

Newtonian is a game focused on making fusion.

## [Map][Map]
- Tile-based
- Fairly large, around 51 x 29
- Tiles can be open, have a wall, or a generator
- Tiles can also be normal, a conveyor, a generator, or a spawn tile.
- Areas will be filled with 2x2 to 3x3 rooms with one large room in the middle.
- machines to refine materials will be spawned throughout the map.
- raw materials spawn in the conveyor room.
- Refined materials can be put in the generator room for points.

## Win Conditions
Create fusion by having the product of heat and pressure equal or exceed 800. Otherwise:
1. Have the highest score, with score equalubg the product of heat and pressure.
2. A random player wins.

## [Tiles][Tile]
Tiles have the following properties:

| Name | Description |
|---|---|
| Type | Either 'normal', 'conveyor', 'generator', or 'spawn' |
| Owner | Who owns that tile, used for generators and spawn. Heals units of the same owner. |
| Unit | unit on the tile |
| Direction | Which direction the conveyor goes. 'north', 'sourth', 'east', 'west', or 'blank' as the default or for directionless conveyors |
| blueium, blueiumOre, redium, rediumOre | Stores the amount of that material on the tile |
| Unit | The unit on this tile, if any |
| IsWall | True if the tile is a wall, false if it isn't |
| Machine | The machine on the tile |
| Decoration | Used by the visualizer to indicate doors and other small decorations, but does not affect gameplay |

## [Units][Unit]
There are three types of units, inters, physicists, and managers. Managers stun inters. Interns stun physicists, and physicists stun managers.

Interns can carry 4 raw ore and can reset the progress on machines.

Physicists can carry one raw or refined material and can work machines.

Managers can carry 3 refined material and have bonus health.

Units have the following properties:

| Name | Description |
|---|---|
| Owner | The owner of this unit. Merchant ships and neutral ships have no owner. To check if a ship is a merchant ship, check if it has a target port. |
| Tile | The tile this unit is on. |
| Health | How much health this unit has |
| Job | The job of the unit |
| blueium, blueiumOre, redium, rediumOre | Stores the amount of that material on the unit |
| Moves | How many more times this unit can move this turn. |
| Acted | Whether this unit has performed an action this turn. Actions are attacking, resting, and boarding ships. However, units that have acted cannot move/split. |
| StunTime | The amount of turns a unit cannot do anything. |
| Stun Immune | Number of turns a unit cannot be stunned |

Each type of unit, their jobs, has the following properties:

| Name | HP | Damage | Moves | Carry Limit |
|---|---|---|---|---|
| Intern | 12 | 4 | 5 | 4 |
| Physicist | 12 | 4 | 5 | 1 |
| Manager | 16 | 4 | 5 | 3 |

Units are created on spawn tiles owned by the player. They may perform one action per turn. All units can do the following things:

| Name | Unit | Details |
|---|---|--|
| Move | Any | Costs 1 move. Move to an adjacent (not diagonal) tile. Cannot move into a wall, another unit, or on a tile with a machine. |
| Attack | Any | Attack a ajacent unit. Costs an action, and consumes any remaining moves. |
| Pickup | Grabs x amount of one type of material from the tile they are on or ajacent to. |
| Drop | Drops x amount of one type of material to the tile they are on or ajacent to. |
| Act | Stuns a unit they can stun, works a machine if they are a physicist, or resets progress if they are a intern. |

## [Machines][Machine]

Machines spawn throughout the map. They use raw material on their tile to refine into the normal material.

Machines have the folling properties:

| Name | Description |
|---|---|
| OreType | Is either Redium, or Blueium. Determines what the machine defined. |
| RefineInput | The amount of raw material that needs to be put in to work the machine. |
| RefineOutput | The amount of mertial put on the tile after working the machine. |
| RefineTime | The number of times the machine needs to be worked to refine ore. |
| Tile | The tile this machine is on. |
| Worked | The amount of times this machine has been worked. |

## Redium/Blueium
The refined variants of their ore forms. These may be put in generator rooms to award points to their owners. Redium awards heat, and Blueium awards pressure.

## Ore
Ore variants of redium and blueium spawn on the oposite sides of the map from the machines that refine them and when refined turn into their refined variants.

## Heat and Pressure
This determines the score of the game. Their product is your score.

[Newtonian]: https://github.com/siggame/Cerveau/blob/master/games/newtonian/
[Map]:  https://github.com/siggame/Cerveau/blob/master/games/newtonian/game.ts
[Tile]: https://github.com/siggame/Cerveau/blob/master/games/newtonian/tile.ts
[Unit]: https://github.com/siggame/Cerveau/blob/master/games/newtonian/unit.ts
[Machine]: https://github.com/siggame/Cerveau/blob/master/games/newtonian/machine.ts