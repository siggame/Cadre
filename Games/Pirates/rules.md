# MMAI 21: [Pirates]

Pirates is a math-heavy game where you must gain more infamy than your opponent. To gain infamy, you must either steal it from your opponent by killing their units, or kill merchant units. At the beginning, neither player will have any infamy. This means the primary source of infamy is merchant ships. Unlike many previous games, **killing your opponent is not the main objective**, and it may be difficult to win directly by doing so. Also, a lot of error messages from performing invalid actions will be thematic. Feel free to ask if they're unclear, but they should be pretty straightforward. We can change them if they're causing problems.

## [Map][Map]
- Tile-based
- Fairly large, around 40 x 28
- Two types of tiles: water and land
- Ocean with islands generated in it
  - Can generate several small islands or fewer larger islands
  - There should not be any "lakes". All water will be part of the main "ocean".
- Half of the map is generated, then that half is mirrored and flipped to generate the other half
- Players spawn on opposite sides
- Two merchant ports are spawned on opposite sides of the map

## Win Conditions
Destroy all of your opponent's units. If they're out of units and can't afford to build another ship, you win. Otherwise:
1. The player with the most infamy wins.
2. The player with the highest net worth wins.
3. A random player wins.

## [Tiles][Tile]
Tiles have the following properties:

| Name | Description |
|---|---|
| Type | Either 'land' or 'water' |
| Unit | The unit on this tile, if any |
| Port | The port on this tile, if any |
| Gold | Any gold buried on this tile. Every turn, the gold increases by 2.5% |
| Decoration | Used by the visualizer to indicate "deep sea" and "grassy" tiles, but does not affect gameplay |

## [Units][Unit]
There are two types of units: crew, and ships. **A single Unit object may contain any number of crew and optionally a ship.** Players cannot control units without crew. This means that players must have crew on their ships, otherwise the ship is considered neutral and unowned (even in ports).

Units cannot move or perform actions the turn they are spawned. If a unit is spawned on top of another unit, they are merged and cannot move or act for the rest of that turn.

Merchant ships will move from one merchant port to another. They carry 600 gold and 3 crew. They only move 1 tile per turn, and the ships have only half as much health as player ships. Each turn, if there is a player ship in range, they will deal damage to it. The player they attack alternates each turn, so they will never attack the same player two turns in a row.

Units have the following properties:

| Name | Description |
|---|---|
| Owner | The owner of this unit. Merchant ships and neutral ships have no owner. To check if a ship is a merchant ship, check if it has a target port. |
| Tile | The tile this unit is on. |
| Crew | The number of crew this unit has. This number will never be higher than the total health of all the crew. |
| Crew Health | The total health of all the crew in this unit. This number will never be less than the number of crew on this unit. If it would drop below the number of crew, then crew die. |
| Ship Health | If this unit has no ship, then this number is just 0. Otherwise, indicates how much health is left on this unit's ship. |
| Gold | How much gold this unit is carrying. There is no limit to how much gold a single unit can carry. |
| Moves | How many more times this unit can move this turn. |
| Acted | Whether this unit has performed an action this turn. Actions are attacking, resting, and boarding ships. However, units that have acted cannot move/split. |
| Path | Used by merchant ships to indicate the path they are following. This will only change if they run into an obstacle. |
| Target Port | Used by merchant ships to indicate which port they are going to. All merchant ships have a target port. |
| Stun Turns | Used by merchant ships to indicate how many more turns they will be stunned for. While stunned, they cannot move, but they will still attack. |

Each type of unit has the following properties:

| Name | HP | Damage | Moves | Range* | Cost | Description |
|---|---|---|---|---|---|---|
| Crew | 4 | 1 | 2 | 1 | 200 | Land only, can board neutral or friendly ships, can bury/dig gold. Can only attack crew. |
| Ship | 20 | 2 | 3 | 3 | 600 | Water only, crew dies when ship sinks, requires friendly crew to control the ship (otherwise it's neutral). Can only attack ships. |

**\* Range is circular**

A unit's max crew health is 4 times the number of crew it has. That means more crew on one unit will provide a higher buffer of damage before crew start to die.

Units are created at the friendly port. They can carry any amount of gold. They may perform one action per turn. All units can do the following things:

| Name | Unit | Details |
|---|---|--|
| Move | Any | Costs 1 move. Move to an adjacent (not diagonal) tile. If crew moving onto a ship, costs an action. |
| Attack | Any | Attack any unit in range. Must specify if attacking 'crew' or 'ship'. Costs an action, and consumes any remaining moves. If all the crew on a ship are killed, that ship's health is set to 1. |
| Bury | Crew | Bury any amount of gold on the unit's tile. Must be performed at least 10 tiles away from the home port, **using circular distance**. Formulas are provided below. |
| Dig | Crew | Dig up gold buried on this unit's tile. |
| Deposit | Any | Put gold into the player's gold pool. Must be used adjacent to (or on top of) its owner's port. If near a merchant port, invests money into the merchant port instead. (If in range of both somehow, then deposits into the player's gold pool) |
| Withdraw | Any | Take gold from the player's gold pool. Must be used adjacent to (or on top of) its owner's port. |
| Split | Any | Move some crew off of this unit. The crew that move consume a move. Crew health is split proportional to the number of crew being moved. Those crew may also take gold with them. Crew may be split onto other units, causing the other unit to merge with the crew. If crew splitting onto a ship, costs an action. |
| Rest | Any | Heals the unit. This also repairs ships. Must be used adjacent to (or on top of) its owner's port. Heals 25% of the ships health and max crew health, rounded up. |

## [Ports][Port]

Each player is given a port at the start of the game. Ports are used to spawn units. Each turn, players may spawn 600 gold worth of units. This means they can either spawn 1 ship or 3 crew. Merchant ports spawn ships every 24 turns. More specifically, they gain 100 gold each turn, and spawn a ship when they have 2400 gold.

Ports have the following properties:

| Name | Description |
|---|---|
| Owner | The owner of this port, or null for merchant ports. |
| Tile | The tile this port is on. |
| Gold | For players, how much more gold can be spent at this port this turn. For merchants, how much gold this port has accumulated. Merchant ports spawn a ship when they have 2400 gold. By default, the ship has half as much health as a player ship and 3 crew. |
| Investment | How much gold is invested into this port. See below. |

## Gold
Gold is obtained by destroying/capturing merchant ships or burying gold. Merchant ships spawn with 600 gold + 1.1 times their investment. After a merchant ship is spawned, the investment on that port is reset to 0. Buried gold increases in value by 2.5% each turn, but it must be buried at least 10 tiles (circular distance) away from the player's port. It can also be obtained by destroying/capturing enemy units that are carrying gold.

## Infamy
Although gold is an important resource, players need to earn infamy to win. To get infamy, players can destroy their opponent's units or merchant ships.
- If a player destroys a merchant unit, they gain 600 infamy for the ship plus 200 infamy for each crew on it. By default, that's 1200 infamy.
- If a player destroy an opponent's unit and the players have the same net worth, they gain 600 infamy for each ship plus 200 infamy for each crew. If their opponent has a higher net worth, the player gains twice that much. If their opponent has a lower net worth, the player gains half that much.
  - Net worth is calculated as 600 * ships + 200 * crew + their gold + the gold on their units. It's calculated before combat, so any units that die are also part of the calculation.

This means that the player who is worth less will gain more infamy per unit than the player who is worth more when attacking each other.

## Investment
Players may invest money into merchant ports. This increases the strength and value of the next ship that spawns. When a merchant ship spawns, it has 600 gold + 1.1 times the investment, and 3 crew + (1.1 times the investment / 200). They will always have half the ship health as a player's unit.

## Formulas
### Circular (Euclidean) Distance
This is used for calculating attack range and required distance from the player's port to bury gold.
```js
let distanceX = x1 - x2;
let distanceY = y1 - y2;
distance = Math.sqrt(distanceX * distanceX + distanceY * distanceY);
```
One trick is to skip the costly square root function and square the range instead:
```js
distanceX * distanceX + distanceY * distanceY <= range * range
```

### Interest for Buried Gold
Each turn, this is applied to every tile on the map:
```js
tile.gold = 1.025 * tile.gold;
```
This means that the gold increases by 1.050625 times every two turns. Additionally, the following formula can be used to calculate the gold after any given number of turns:
```js
tile.gold = Math.pow(1.025, numberOfTurns) * tile.gold;
```

### Merchant Ships
When a merchant ship is spawned, the following formulas are used:
```js
ship.shipHealth = 10;
ship.crew = 3 + (1.1 * investment) / 200;
ship.gold = 600 + 1.1 * investment;
```

[Pirates]: https://github.com/siggame/Cerveau/blob/master/games/pirates/
[Map]:  https://github.com/siggame/Cerveau/blob/master/games/pirates/game.js
[Tile]: https://github.com/siggame/Cerveau/blob/master/games/pirates/tile.js
[Unit]: https://github.com/siggame/Cerveau/blob/master/games/pirates/unit.js
[Port]: https://github.com/siggame/Cerveau/blob/master/games/pirates/port.js