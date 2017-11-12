# Catastrophe

Note: If this file does not match what's in game, please let a SIG-Game developer know. This file is provided for your convenience, however the in-game numbers will always take precedence.

## The Map

The map is a 26x18 grid based board. Tiles can contain structures on them. A unit can occupy the same space as some structures. Players will start on either side (left or right) of the map at a random height. A road will go through the center of the map, horizontally.

The player will be spawned on either side of the map with a shelter. Each player will have a friendly Cat Overlord in their shelter, and 3 friendly fresh humans. They can immediately change the fresh humans' jobs and send them out to gather resources.

Players alternate, taking turns. This means that both players taking a turn counts as two turns. One day is equivalent to one round or two turns (one turn per player).

Every 15 days (30 turns), one neutral fresh human will spawn on both sides of the road. Every turn, those units will move one space along the road. When they reach the other side of the map, they disappear. Additionally, food tiles will be randomly generated around the map with increasing density toward the center of the map. The harvest rate will depend on their location, with food tiles in the center having higher harvest rates. Neutral structures will be generated evenly around the map and can be deconstructed for materials to build new structures. There is a limited number of materials, but a constant supply of food and fresh humans.

#### Edge cases

* Fresh humans on the road will die after however many turns it would take them to cross the road normally. This means they will die if they're blocked.
* If a fresh human cannot spawn on the end of a road, it will spawn as far into the road as necessary. You cannot prevent fresh humans from spawning this way.
  * If there is nowhere for the fresh human to spawn on that row of the map, it will not spawn.

## Game Objects

_Note_: "Adjacent" means the cardinal directions (North, East, South, or West).

### Tiles

The basic map component.

* **Unit**: The Unit that is on this tile, or null if the tile doesn't have a Unit on it.
* **Structure**: The Structure that is on this tile, or null if the tile doesn't have a Structure on it.
* **HarvestRate**: The amount of food that can be harvested from this tile at once. This number decreases throughout the game.
* **TurnsToHarvest**: The number of turns before this tile can be harvested from. Every time a unit harvests a tile, the tile cannot be harvested for another 10 turns.
* **Materials**: The number of materials dropped on this tile.
* **Food**: The amount of food dropped on this tile.

Every 60 turns (30 days), the maximum amount of food that can be harvested from each food tile will be decreased by 10. Some tiles may not be able to generate food anymore later in the game, so players must make sure to stock up food for later in the game.

#### Pathing

The following tiles cannot be moved onto:

* Tiles with a structure on them, unless that structure is "shelter" or "road".
* Tiles with other units on them.

Units can only move 1 tile at a time, however they may have multiple moves per turn. This means you will need to move tile-by-tile. Units can only move north, south, east, and west. They cannot move diagonally. Every successful movement consumes a single move for that unit, regardless of the tile. You cannot move after some actions (more information below).

### Structure

A structure is a building that is on a tile. Each structure has its own function and effect range. Structure types are "shelter", "monument", "wall", "road", and "neutral". Only shelters and roads can be walked through.

* **Type**: The type of structure this is ("shelter", "monument", "wall", "road", "neutral").
* **Tile**: The tile that the structure is on.
* **Owner**: The owner of the structure, or null if the structure is "neutral".
* **Materials**: The number of materials in this structure. A structure is destroyed when this number reaches 0.
* **EffectRadius**: The range of this structure's effect. The range is a square with side length 2N + 1, where N is this value, centered on this structure. For example, if this value is 3, then the effect range is a 7x7 square centered on this structure (a square going out 3 in each direction, including the structure).

#### Specific Structures

| Type | Materials Needed | Effect Radius | Effect |
| --- | --- | --- | --- |
| **"wall"** | 75 | 0 (N/A) | These can be used to defend a structure by forcing the enemy to break through the wall or walk around it. |
| **"shelter"** | 50 | 1 (3x3) | Food can be dropped on a friendly shelter to add it to the player's food pool. Additionally, Gatherers can steal food from enemy shelters. |
| **"monument"** | 100 | 3 (7x7) | Friendly units in range of friendly monuments spend half as much energy per action. This does not apply to picking up resources. |
| **"neutral"** | 200 (cannot be created) | 0 (N/A) | A structure that is owned by nobody. These can be deconstructed for materials. |
| **"road"** | 0 (cannot be created) | 0 (N/A) | Roads cannot be destroyed or built on top of. Neutral fresh humans will walk across this every 15 days (30 turns). Roads are 2 wide to fit both of the neutral fresh humans. These cannot be attacked or deconstructed. |

### Unit

Units do all of the actions in the game. Aside from each player's Cat Overlord, all units can change to any job in the game (except "cat overlord") as long as they're adjacent or diagonal to the Cat Overlord and at max energy. Most actions they perform cost energy. They can regenerate energy by resting in range of a shelter. Additionally, all units have a food upkeep cost. At the beginning of your turn, if you can pay your total unit upkeep, the upkeep will be deducted from your player's food stash and your units will be fed. If you can't pay for your unit upkeep, you will not lose food, and your units will become starving and will regenerate 0.25 times as much energy that turn if they rest. New units can be obtained by converting neutral fresh humans to friendly ones and changing their job.

Units have the following attributes:

* **Owner**: The player who owns this unit, or null if it's a neutral fresh human.
* **Tile**: The tile this unit is on.
* **Job**: This unit's job.
* **Moves**: How many times this unit can still move this turn.
* **Energy**: The amount of energy this unit has. This is a floating point number between 0.0 and 100.0.
* **Squad**: The units in the same squad as this unit. If this unit enters combat, all units in this squad who have not acted yet will enter combat as well.
* **Acted**: Whether this unit has performed an action this turn. Units can only perform a single action per turn.
* **Food**: The amount of food this unit is carrying.
* **Materials**: The number of materials this unit is carrying.
* **Starving**: Whether this unit is starving.
* **TurnsToDie**: How many turns before this unit is removed from the game. This number only applies to neutral fresh humans. Otherwise, this number will be -1. For units on the road, this will be set to how many turns it will take them to cross the road.
* **MovementTarget**: The tile this unit is moving to. This value is only used by neutral fresh humans walking across the road, and will be on the end of the road. Otherwise, this value is null.

Additionally, units can do the following:

* **Move**: Moves this unit from the current tile to an adjacent tile. Units may be able to move multiple times per turn. Does not count as an action.
* **Harvest**: Harvests the food of an adjacent tile with food. Only gatherers may perform this action.
* **Attack**: Attacks an adjacent tile. Only soldiers may perform this action. All units in this unit's squad who may still perform an action will attack together (and will all consume an action). Costs 25 energy for each unit in the squad (half as much in range of a monument). Units cannot move after entering combat. Combat is explained in detail below.
* **Convert**: Converts an adjacent neutral fresh human to your side. Only missionaries can perform this action. Costs 75 energy.
* **Construct**: Creates a structure on an adjacent tile. Only builders can perform this action. The tile must contain enough materials on it for the structure to be created. Costs 75 energy.
* **Deconstruct**: Removes materials from an adjacent structure. Cannot deconstruct a friendly structure (you can attack it though). Only builders may perform this action. Removes as many materials as the builder can carry from the building. Costs 75 energy.
* **Drop**: Drops "materials" or "food" on an adjacent tile. Can be performed multiple times per turn. Does not count as an action. Dropping "food" onto a friendly shelter will add that food to your player's global food storage rather than to the tile.
* **Pickup**: Picks up "materials" or "food" on an adjacent tile. Can be performed multiple times per turn. Does not count as an action. Costs 1 energy per item picked up.
* **ChangeJob**: Changes this unit's job. It requires the Unit:
  * be at max energy (does not cost energy though, as in, it won't lose energy from changing jobs)
  * must be adjacent or diagonal to the Cat Overlord to change its job.
  * Additionally, the Unit cannot move after performing this action and will drop all of their "food" and "materials" when performing changing jobs (to safegaurd against Units carrying more than their carry limit).
* **Rest**: Regenerates energy for the unit equal to this unit's job's `regenRate` value. Must be in range of a shelter. It regenerates 2.0 times as much energy if the Cat Overlord is in that shelter. However, it regenerates 0.5 times as much energy if it is starving. Units cannot move after performing this action.
  * If the unit is starving and rests in a shelter that the Cat Overlord is in range of, they will regenerate energy equal to 0.5 times their `regenRate`.

#### Combat

When a unit attacks a tile, all units in that unit's squad enter combat. Every unit in that squad loses 25 energy. The total energy consumed by the units is put into something called the "attacker's pool". Finally, one of two things can happen:
* If the tile the unit is attacking has a structure on it, then materials are lost from the structure equal to how much energy is in the attacker's pool. If the structure runs out of materials, it's destroyed.
* If the tile the unit is attacking has a unit and no structure, then the energy in the attacker's pool is divided equally among the defending unit's squad, and all defending units lose that much energy.

For example:
* If a squad of 3 units attacks a wall, then 25 energy is deducted from each unit in that squad and added to the attacker's pool. The attacker's pool will contain a total of 75 energy in it. That much is dealt to the wall, so the wall loses 75 materials (the materials are lost for good).
  * Any units in that squad who ran out of energy are turned into neutral fresh humans and will die after 10 turns if they are not converted by a missionary.
* If a squad of 4 units attacks a squad of 2 units, then 25 energy is deducted from each unit in the attacking squad. The attacker's pool now has 100 energy in it. That energy is then divided evenly between the defending squad's units, and dealt to them. That means each defending unit will lose 50 energy.
  * Any units in the attacker's squad or defender's squad who ran out of energy are turned into neutral fresh humans and will die after 10 turns if they are not converted by a missionary.

Edge cases:
* Units in the attacking squad in range of a monument will only lose 12.5 energy, but still put 25 energy into the attacker's squad.
* Units in the defending squad in range of a monument will only lose half the energy they normally would.
* If an attacking unit doesn't have 25 energy, it will put as much as it can into the attacker's pool. For example, if it only has 10 energy, then it will only contribute 10 energy.
  * If that unit is near a monument, then it will lose 10 energy and contribute 20 energy.

#### Squads

A squad is any continuous chain of adjacent soldiers. This means that if 3 soldiers are next to each other, then all three of those soldiers are in a squad together. However, non-soldier units can also be in a squad. This is where we notice that squads are different for each unit. A non-soldier unit next to a soldier unit will be in a squad with them, as well as every other soldier unit next to them. Those soldiers will not be in a squad with the non-soldier unit, though.

For example:
* Three soldiers are next to each other and form a straight line. Each of those units are in a squad containing all three of those units. Each unit's `squad` value will be a list containing all three of those units.
* A gatherer is by itself collecting food. It will be in a squad by itself. Its `squad` value will be a list containing only itself.
* Three soldiers are next to each other and form a straight line. On one end of the line, there's a gatherer. Each soldier is in a squad containing all three of the soldiers. Their `squad` values will be a list containing all three soldiers. The gatherer is in a squad with itself and all three soldiers. Its `squad` value is a list containing all four of those units.
  * If the gatherer is attacked by an enemy squad, all four of those units will be in the defending squad because they are in the gatherer's squad. This means that the damage is dealt to all four units, not just the gatherer. This can be useful to protect the gatherer.
  * If a soldier near the gatherer is attacked by an enemy squad, only the three soldiers will be in the defending squad because the gatherer is not in that soldier's squad.
  * If one of the soldiers near the gatherer attacks an enemy squad, the gatherer will not enter combat because it is not in that soldier's squad.

### Job

A Job is a container class that holds base information about a Unit's job.

* **Title**: The job title ("cat overlord", "soldier", "gatherer", "builder", "missionary", "fresh human").
* **Moves**: The number of times a unit with this job can move per turn.
* **ActionCost**: The amount of energy it costs for this unit to perform an action.
* **RegenRate**: How much energy this unit regenerates while resting. This is doubled if resting in a shelter the Cat Overlord is in range of.
* **CarryLimit**: The total amount of combined materials/food this unit can carry at once.
* **Upkeep**: The amount of food this unit consumes at the start of your turn.

#### Specific Jobs

Here's the official stats used by the game server: https://github.com/siggame/Cerveau/blob/master/games/catastrophe/jobStats.json

| Type (title) | Moves | Action Cost | Regen Rate | Carry Limit | Upkeep | Details |
| --- | --- | --- | --- | --- | --- | --- |
| **"cat overlord"** | 2 | N/A | 10/turn | 10 | 0 | Units who rest near a shelter with the cat overlord in it regenerate twice as much energy. This unit cannot change jobs. Units cannot change to this job.
| **"soldier"** | 3 | 25 | 25/turn | 10 | 3/turn | Can attack other units or structures. |
| **"gatherer"** | 4 | 75 | 50/turn | 100 | 1/turn | Can harvest and steal food. |
| **"builder"** | 4 | 75 | 50/turn | 75 | 2/turn | Can construct and deconstruct. |
| **"missionary"** | 4 | 75 | 50/turn | 10 | 2/turn | Can convert neutral fresh humans to friendly fresh humans. |
| **"fresh human"** | 4 | N/A | 50/turn | 10 | 1/turn | Low upkeep, but can't really do anything. |

#### Stealing

Gatherers can steal food from an enemy shelter by harvesting from one. They will take as much as they can carry. Players should make sure their shelters are well defended. If necessary, they can destroy their own shelters with their soldiers by attacking them.

### Start

At the start of the game, you get a cat overlord inside of a friendly shelter, and 3 fresh humans. You only start with 100 food, so start harvesting as quickly as possible!

#### Win Conditions

Primary: **Destroy the enemy Cat Overlord**

Secondary: **Attack all the enemy humans. Once they have no more units, they lose!**

Else, if 360 days (720 turns, or 12 months) reached:

1. Player with the most units
2. else, player with the most food
2. else, player with the most structures
5. else, flip a coin (they are the same AI)

Additionally, if an AI locks up or takes an absurd amount of time to complete its turns, it will timeout and lose. The remaining time for each player is in `Player.timeRemaining`.
