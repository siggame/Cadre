# Stumped

## The Map

The map is a 32x20 grid based board. Tiles can have water or land on them. A pond is present in the center of the map along some axis, and 2-8 rivers are procedurally generated flowing into the pond.

Trees are generated around the map, and are used to get branches. Food is available as groups of cattails which are present in the pond and rivers.

## Game Objects

_Note_: "Adjacent" means the cardinal directions (North, East, South, or West).

### Tiles

The basic map component.

* **Type**: will be "water" or "land".
* **Flow Direction**: Will be a cardinal direction, indicating the direction water is flowing on this Tile (meaning it is a river)
* **Beaver**: The Beaver that is on this Tile, if present
* **Spawner**: The Resource on this Tile, if present
* **Lodge Owner**: The owner of the beaver Lodge on this Tile, if anyone
* **Branches**: The number of branches dropped on this Tile, if any
* **Lodge**: A Lodge is completed when a requisite amount of branches are gathered on a tile, and can spawn beavers
* **Food**: The amount of food dropped on this Tile, if any

The player will be spawned with one branch and the first lodge will cost 1 branch to build. If a Tile has been turned into a lodge by a player, that player can spawn beavers there. A lodge will cost `ceiling(`**phi**`^n)`, where `n` is the current number of lodges controlled by a player and **phi** is the golden ratio (1.61803...). A lodge has health determined by the current number of branches on it. As soon as the branches on a lodge tile reaches 0, then the lodge is destroyed.

_Note_: The **phi** constant is made available during gameplay.

### Resource

A resource is basically something on the map that produces branches/food and can be harvested, e.g. a Tree or group of cattails.

* **Health**: How much of the "thing" there is. This increases once per turn if not harvested.
* **Tile**: The location of this Resource
* **Type**: The type of item you get from this Resource, either 'food' or 'branches'

If a Resource is harvested, it loses 1 health and produces `(2)*(spawner.health)*(skillScalar)` items, where `spawner.health` was the health of the resource prior to chopping it (with a maximum health of 5) and skillScalar will be either the beavers munching or chopping power depending on the spawner. When a resource it not damaged during a turn it grows by 1.

### Beavers

Beavers are the the main unit. These cute critters are the things you control to manipulate the map. If you have less than 10 beavers, beavers are free. Otherwise they cost servings of food. Food must first be dropped at a lodge and then the player can use the tile that the lodge is on to spawn a new beaver. Before the newly spawned beaver can do anything, they need to be offically recruited to your team. This means whenever a beaver is recruited, you won't be able to do anything with it until 1 turn has passed. The variable `beaver.recruited` will return a bool value telling you whether or not the calling beaver has been recruited.

Beavers have the following attributes:

* **Moves**: The number of moves remaining for this Beaver
* **Actions**: The number of actions remaining for this Beaver
* **Position**: The Tile this beaver is currently on
* **Health**: How much health this beaver has remaining
* **Distracted**: Number of turns the Beaver is distracted for (0 means not distracted)
* **Branches**: The number of Branches this Beaver is holding, if any
* **Food**: The amount of Food this Beaver is holding, if any
* **Job**: The Job this beaver was recruited to do

In addition, Beavers can do things. Such eager beavers!

* **Move**: Moves the Beaver to a nearby adjacent Tile. Costs 2 Moves, or 1 when moving down a river, or 3 when moving up a river.
* **Harvest**: Chews on a Tree or munches on Food, must be adjacent.
* **Attack**: Attacks another Beaver (must be adjacent) for damage to their health.
* **Build Lodge**: Requires an exponential cost of branches to use, and establishes a Lodge on this Tile.
* **Drop**: Drops the some branches/food this Beaver is holding onto the Beavers current tile or a ajacent one. Dropped food in water disappear instantly. Drops branches do not. Food dropped on land die off 1 per turn.
* **Pickup**: Picks up all the branches/food from the Tile the Beaver is on (must not be holding anything)

### Job

A Job is a container class that holds base information about a Beaver's job.

* **Title**: The job title, e.g. 'Builder', 'Hungry', etc
* **Health**: The starting health Beavers with this Job have
* **Moves**: The starting moves per turn Beavers with this Job have
* **Actions**: The starting actions per turn Beavers with this Job have
* **Damage**: How much damage Beavers with this Job do when they attack other Beavers
* **Chopping**: Scalar for how many additional branches Beavers with this can Job harvest
* **Munching**: Scalar for how much additional food Beavers with this can Job harvest
* **Distracts**: If this job's attacks distract the attacked Beaver
* **Carry**: The number of items a single beaver can hold.
* **Recruit**: Given a lodge, recruit a beaver with this job to the lodge owner's team

#### Specific Jobs

_(assume basic beaver stats if not stated)_

| Beaver Type | Cost | Damage | Health | Moves | Actions | Chopping | Munching | Distraction (duration) | Carry Capacity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Basic** | 3 | 1 | 3 | 3 | 1 | 1 | 1 | 0 | 3 |
| **Fighter** | 12 | 3 | 4 | 2 | 1 | 1 | 1 | 0 | 6 |
| **Bulky** | 12 | 2 | 10 | 2 | 1 | 1 | 1 | 0 | 2 |
| **Hungry** | 8 | 1 | 3 | 3 | 1 | 1 | 3 | 1 | 15 |
| **Swift** | 6 | 1 | 3 | 5 | 1 | 1 | 2 | 0 | 2 |
| **Hot Lady** | 15 | 1 | 3 | 3 | 1 | 1 | 1 | 3 | 1 |
| **Builder** | 6 | 1 | 3 | 3 | 1 | 3 | 1 | 0 | 15 |

## Other

#### Start
At the start of the game, you get 1 beaver that is holding 1 branch for use to build your first lodge.

#### Win Conditions

Primary: **Some player controls 10 lodges simultaneously**

Else, if 500 turns reached:

1. Player with most lodges completed
2. else, player with most scored branches in lodges
4. else, player with most extra food in lodges
5. else, flip a coin (they are the same AI)
