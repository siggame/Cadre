# MMAI 25: [Coreminer]

Coreminer is a resource gathering game about undermining your opponent.

## [Map][Map]
- Tile-based
- Fairly large, around 30 x 30
- Tiles can contain dirt and ore, anti-bomb shielding, ladders, supports, hoppers, any number of Miners and/or bombs, and a Player's base.
- There is more dirt and ore as you go deeper underground, which takes longer to mine.
- Bases are in the top left and right corners of the map.
- As tiles are mined directly underneath a Player's base, a hopper is extended downwards into empty tiles. This can be used to score resources without traveling back to the surface.
- Note that hopper tiles must not have filled tiles between them and the base, and once a hopper is extended, its tile cannot be filled again.
- There is a high concentration of ore in the bottom center of the map.
- Tiles are affected by gravity, and so must be supported by supports or other tiles.
- Supports prevent tiles from falling, but only the three tiles above it (in a horizontal line).
- In other words, supports support the tiles to their north, northeast, and northwest.
- Miners can collect dirt and ore to tunnel their way deeper, and use ladders to get back up.

## Scoring
Player Value is the score. This is increased when ore is deposited in your base.
Player Money is your money. This is increased when ore or dirt is deposited in your base.

## Win Conditions
The first player to reach the victory amount wins! Otherwise:
1. The player who has gathered and deposited the most ore wins.
2. The player with the most money wins.
3. A random player wins.

## [Players][Player]

Players have a single function: SpawnMiner. It takes no arguments, and spawns a Miner on their Base Tile.

## [Tiles][Tile]
Tiles have the following properties:

| Name | Description |
|---|---|
| owner | Who owns that tile, players "own" their base tile and hopper tiles.
| dirt | The amount of dirt occupying the tile. |
| ore | The amount of ore occupying the tile. |
| shielding | The amount of shielding on the tile. Prevents bomb explosions from destroying it that many times. |
| miners | A list of miners on this tile. |
| bombs | A list of bombs on this tile. |

Tile types (as found using .isBase, .isHopper, etc.) and what they involve:
| isBase | Can be walked on by Miners. Heals allied Miners and can intake dumped materials. |
| isHopper | Can be walked on by Miners. Prevents falling. Can also intake materials. Only appear under the base while there is an unblocked path upward. |
| isLadder | Can be walked on by Miners. Allows Miners to move up and down. |
| isSupport | Can be walked on by Miners. Helps prevent Tiles from falling. |
| isFalling | True if this Tile may fall next turn. |

## [Miners][Miner]
There are 4 types of Miners, one for each upgrade level. Newly spawned Miners are the lowest upgrade level.

Any number of Miners can occupy the same Tile.

Miners have the following properties:

| Name | Description |
|---|---|
| Owner | The owner/creator of this Miner. |
| Tile | The tile this Miner is on. |
| CurrentUpgrade | The Upgrade Miner this is using. |
| UpgradeLevel | The integer level this Miner's Upgrade is. |
| Health | How much health this Miner has. |
| Moves | How many more times this Miner can move this turn. |
| MiningPower | The remaining mining power this Miner has this turn. |
| BuildingMaterials | The number of building materials this Miner has. Used to create Supports and Ladders. |
| Bombs | The number of bombs being carried by this Miner. |
| Dirt | The amount of dirt being carried by this Miner. |
| Ore | The amount of ore being carried by this Miner. |

Miners may mine nearby tiles, collecting their resources.
They may dump dirt, ore, and bombs, which places them on a nearby tile. If that tile is a hopper or base, it is instead sold.

Miners have the following functions:

| Name | Arguments | Description |
|---|---|---|
| Dump | Tile, Material, Amount | The Miner drops a specified number of materials on the given Tile. Amounts <= 1 drops all available. Can drop "bomb", "ore", or "dirt". |
| Mine | Tile, Amount | The Miner mines a specified Tile. Amounts <= 1 mines as much as possible. Miners mine in this order: shielding, ladders, supports, ore, dirt. If you cannot mine all shielding, mining stops. |
| Move | Tile | The Miner attempts to move to the given Tile. Must be adjacent and empty of dirt and ore. Miners will fall if they move over a hole. |
| Build | Tile, Type | The Miner builds the structure type ("support", "ladder", "shield") on the given Tile using building materials. Shields must be on filled tiles, the others must be empty. |
| Upgrade | N/A | Upgrades the Miner to the next Upgrade. |
| Transfer | Miner, Resource, Amount | Transfers the resource ("dirt", "ore", "bomb", "buildingMaterials") to another adjacent Miner. |
| Buy | Resource, Amount | The Miner buys a resource ("dirt", "ore", "bomb", "buildingMaterials") from their base or an owned hopper Tile. |

##[Upgrades][Upgrade]

Upgrades define the maximum capabilities for any Miner, in terms of what upgrade module they are equipped with.
They have the following properties:

| Name | Description |
|---|---|
| Title | The title of this Upgrade module. |
| Health | The maximum amount of health this Upgrade has. |
| Moves | The number of moves this Upgrade level can make per turn. |
| MiningPower | The amount of mining power this Upgrade has per turn. |
| CargoCapacity | The amount of cargo capacity this Upgrade has. |

The Upgrades are as follows (though this may be subject to change):

| Title | Health | Moves | MiningPower | CargoCapacity |
|---|---|---|---|---|
| Standard Issue Exominer | 25 | 2 | 50 | 250 |
| Exominer MK2.0 | 50 | 3 | 100 | 500 |
| Exominer 3000 | 75 | 4 | 150 | 750 |
| Exominer 5000 Series X | 100 | 5 | 200 | 1000 |

Newly spawned Miners are considered Standard Issue Exominers.

## [Bombs][Bomb]

Bombs can be bought and dumped by Miners. They explode after the following turn.

Bombs have the following properties:

| Name | Description |
|---|---|
| Tile | The tile this Bomb is on. |
| Timer | The number of turns before this Bomb explodes. One means that it will explode after the current turn. |

Bombs destroy the tiles immediately adjacent to it, as well as the tile it is on. They deal explosion damage based on the game settings. However, if a tile that would be destroyed is shielded, the shield is instead damaged (decreased by one).

Bombs also send out a shockwave that damages any Miners in its path. The shockwave is sent out in the cardinal directions away from the Bomb until it hits a filled tile. Any Bombs affected by another Bomb are also immediately detonated.
