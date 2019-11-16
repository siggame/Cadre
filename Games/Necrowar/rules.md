# MMAI 24: [Necrowar]

Necrowar is a tower defense-esq game about killing your opponent

## [Map][Map]
- Tile-based
- Fairly large, around 63 x 32
- Tiles can be grass, river, path, mine, island mine, unit spawn, worker spawn, or castle tiles
- There is a path traveling around the edges of the map, about 5 tiles away from the sides.
- There is a river splitting the map down the middle 3 tiles wide.
- There is a 2x2 gold mine on either players side
- There is a 3x3 island in middle of a 5x5 lake at the center of the map, on this island is a verticle 1x3 island gold mine.
- There is a castle in the bottom right and top left corners that act as each players main building.
- Workers must gather gold from gold mines and the island gold mines, and fish at the edge of the river for mana fish to get resources.

## Win Conditions
Destroy your opponent's castle on the other side of the map. Otherwise:
1. The castle with the higher amount of health wins.
2. A random player wins.

## [Tiles][Tile]
Tiles have the following properties:

| Name | Description |
|---|---|
| is... | The tile type, either 'Path', 'Grass', 'Tower', 'GoldMine', 'IslandGoldMine', 'River', 'Castle', 'WorkerSpawn', or 'UnitSpawn'. Explained further below. |
| owner | Who owns that tile, players "own" their respective sides and workers can't walk on or build on the other side. |
| unit | Unit on the tile, if any. |
| tower | Tower on the tile, if any. |
| corpses | The number of corpses on the tile, if any. |
| numZombies, numGhouls, numHounds | The amount of the 3 types of units that can stack on tiles with other units of the same type |

Tile types (as found using .isGrass, .isPath, etc.) and what they involve:

| Type | Description |
|---|---|
| isPath | Can be walked on by Units, not Workers |
| isGrass | Can be walked on by Workers, not Units, Workers can also build towers on grass |
| isTower | True if the tile has a tower on it, is true alongside isGrass |
| isGoldMine | Can be walked on by Workers, is true alongside isGrass |
| isIslandGoldMine | Can be walked on by Workers on either team, is true alongside isGrass, owned by nobody, gets flooded every 15 turns and kills all workers on them |
| isRiver | River tiles, can't be walked on by anyone, Workers must be adjacent to a river tile to be able to fish |
| isCastle | The castle tile, each player has one, must be destroyed in order to win |
| isWorkerSpawn | Each player has one, tile that the workers spawn on when created |
| isUnitSpawn | Each player has one, tile that combat units spawn on when created |

## [Units][Unit]
There are 7 types of units, workers, zombies, ghouls, hounds, abominations, wraiths and horsemen. Workers are the only unit that doesn't walk on paths and can only walk on grass or mines.

Ghouls can stack a few per tile, have medium health, have a medium speed, and can attack towers.

Hounds can stack a few per tile, have low health, have a fast speed, and can't attack towers that aren't the castle.

Abominations can't stack on tiles, have a lot of health, have a slow speed, and can attack towers.

Wraiths can't stack on tiles, have low health, have fast speed, and can't attack towers that aren't the castle.

Units have the following properties:

| Name | Description |
|---|---|
| Owner | The owner of this unit / Who made it. |
| Tile | The tile this unit is on. |
| Health | How much health this unit has. |
| Job | The type of the unit this is. |
| Moves | How many more times this unit can move this turn. |
| Acted | Whether this unit has performed an action this turn. Actions are either attacking if it's a combat unit, or building/mining/fishing if it's a worker unit. |

Each type of unit has the following properties:

| Title | Gold Cost | Mana Cost | Damage | Health | Moves | Range | Stackable | 
|---|---|---|---|---|---|---|---|
| Worker | 10 | 0 | 0 | 1 | 8 | 1 | 1 |
| Zombie | 0 | 2 | 1 | 5 | 3 | 1 | 10 |
| Ghoul | 20 | 5 | 5 | 15 | 3 | 1 | 2 |
| Abomination | 25 | 10 | 10 | 60 | 1 | 1 | 1 |
| Hound | 15 | 4 | 5 | 5 | 5 | 1 | 3 |
| Wraith | 40 | 20 | 10 | 10 | 6 | 1 | 1 |
| Horseman | 150 | 50 | 15 | 75 | 5 | 1 | 1 |

Combat units (all units that are not workers) are created on unit spawn tiles owned by the player. Worker units have their own spawn tile (worker spawn). They may perform one action per turn. All units can do the following things:

| Name | Unit | Details |
|---|---|---|
| Move | Any | Costs 1 move. Move to an adjacent (not diagonal) tile. Workers can move onto grass(on their side), mines (on their side) and the island mines. Units can only move on paths. |
| Mine | Worker | A worker on a mine or island mine tile starts mining, generating the amount of gold per turn for one unit. Counts as an act. |
| Fish | Worker | A worker on a tile adjacent to a river tile fishes for mana fish, generating the amount of mana per turn for one unit. Counts as an act. |
| Build | Worker | A worker on a grass tile builds a tower with the designated type/job. Counts as an act. |
| Attack | A unit attacks an adjacnt tower (or castle, which is technically also a tower) for the amount of damage they can do. Counts as an act. |

## [Towers][Tower]

Towers are the defensive structures that can be built by workers to defend their paths against enemy units going toward their castle on the path.

Each type of tower will has the folling properties:

| Title | Gold Cost | Mana Cost | Health | Range | Turns Between Attacks | All Units on a Tile | Damage | 
|---|---|---|---|---|---|---|---|
| Arrow | 50 | 0 | 30 | 3 | 1 | false | 5 |
| Ballista | 75 | 0 | 30 | 3 | 3 | false | 20 |
| Cleansing | 30 | 30 | 30 | 3 | 1 | false | 5 |
| Aoe | 40 | 15 | 30 | 3 | 1 | true | 3 |
| Castle | N/A | N/A | 100 | 3 | 1 | true | 3 |

## The River and the Island
The river splits the map down the middle, each player only being able to build and move workers on their respective sides. There is an island in the middle which has island gold mines that both players can access but can't cross to the other side. Every 15 turns, the workers in the island gold mines are killed as the island mines 'flood'.

## Gold and Mana
Gold is obtained in gold mines, and in higher amounts in the island gold mines, mana is obtained by fishing in the river for mana fish. Gold and Mana in differing amounts are spent in order to spawn units, workers, and build towers.

[Necrowar]: https://github.com/siggame/Cerveau/blob/master/games/necrowar/
[Map]:  https://github.com/siggame/Cerveau/blob/master/games/necrowar/game.ts
[Tile]: https://github.com/siggame/Cerveau/blob/master/games/necrowar/tile.ts
[Unit]: https://github.com/siggame/Cerveau/blob/master/games/necrowar/unit.ts
[Tower]: https://github.com/siggame/Cerveau/blob/master/games/necrowar/tower.ts