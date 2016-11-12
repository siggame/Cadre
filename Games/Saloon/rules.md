# Saloon Game Rules

Saloon is a 2D, tiled based, turn based games. Two players control rival gangs in a Saloon and erupt in a drunken brawl trying to play pianos the most.

## Terminology

- Classes:
    - `Game` - The game class itself, all data within the game can be access via this class instance
    - `AI` - A program playing the game, each AI has access to the `Game` and the `Player` they control.
    - `Player` - A player in the game. Has units and each AI controls a player.
    - `Tile` - Makes up the map. Each `Tile` can have only 1 "thing" on it, no stacking.
    - `Cowboy` - The most basic unit. Walks around the map, playing pianos, shooting each other, etc. Capabilities are determined by its `job`.
    - `YoungGun` - A special unit that moves automatically around the map and can call in new `Cowboy`s.
    - `Furnishing` - Exists on tiles to obstruct movement. Some are "pianos" can can be played to increase game score.
- Terms:
    - Piano: A `Furnishing` whose `isPiano` is `true`
    - Balcony: A `Tile` whose `isBalcony` is `true`
    - Bartender: A `Cowboy` whose `job` is `"Bartender"`
    - Brawler: A `Cowboy` whose `job` is `"Brawler"`
    - Sharpshooter: A `Cowboy` whose `job` is `"Sharpshooter"`

*Note*: All the words in this document that look like `this` mean a variable or something for you writing code.

## Objective

1. Have the highest `score` once all pianos in the saloon are destroyed.
2. Failing that the `Player` with the most enemy `kills` wins.
3. Failing that we flip a coin.

Additionally, if we can calculate that the losing player cannot possibly score enough in the turns remaining to win, we will end the game early.

Once the `YoungGun`s walk around the map 3 times (`maxTurns` = 192), the game will be ended and we will apply the logic above as well.

## The Game Map

![Saloon Game Screenshot](http://i.imgur.com/C9PFlUp.png)

The game map is made up of 22x12 `Tile`s. `Tile`s can have only 1 "thing" on them. Valid "things" on tiles are:
- `Cowboy`
- `Furnishing`
- `YoungGun`
- `Bottle`

Additionally `Tile`s can be hazardous (`hasHazard = true`) to `Cowboy`s but this does not count as a "thing".

A `hasHazard` tile looks like:

![Hazard tile](http://i.imgur.com/9rDSe08.png)

Around the inner edges of the map are special `Tile`s whose `isBalcony` flag is set to `true`. This means they are a balcony around the map. `Cowboy`s cannot path onto balcony `Tile`s. Instead 1 `YoungGun` for each `Player` spawns at the start of the game in the top left and bottom right corners of the map. Each `YoungGun` then moves clockwise around the map at the end of its owner's turn.


### Map Generation

The map is randomly generated at the start of the game. The left side of the map is generated, then rotated 180 degrees to form the right side of the map. The initial map will always have pianos on it, and will probably have some useless `Furnishing`s placed as obstacles, and some `Tile`s will have their `hasHazard` flag set to true to damage units that path over them.

Maps are generated with the following variables to guide random generation:

- Map Width: 22 Tiles
- Map Height: 12 Tiles
- Number of non piano Furnishings: 0 to 10
- Number of Pianos: 4 to 8
- Number of hazard Tiles: 0 to 24

Because we diagonally mirror the map, the number of spawned things will always be divisible by 2.

## Young Guns

![YoungGun Sprite](http://i.imgur.com/curwPOB.png)

The `YoungGun` class acts as a mobile spawn point. They can `callIn(job)`, where job is a string of the `Cowboy` with said `job`.

Newly called in `Cowboy`s by the `YoungGun` are placed in the closest non-balcony tile. So, when at the top of the map it will the tile to the south of him, when on the right side it will spawn to the west etc. In the corners of the map the new `Cowboy` will spawn diagonally to the `YoungGun`.

In addition, if there is something on the `Tile` that the newly called in `Cowboy` will spawn on, it will be destroyed. This means the new `Cowboy` jumps down from the balcony, crushing any `Furnishing`, other `Cowboy`, or `Bottle` he lands on. If the new `Cowboy` lands on a `Bottle` they will get drunk.

You can only spawn one cowboy per turn as long as it doesn't exceed the 2 job limit.

## Cowboys

The `Cowboy` is your main unit type. They can `move(tile)`, where `tile` is the `Tile` you want to move to. It must be adjacent. `Cowboy`s cannot move diagonally. `Cowboy`s cannot move into a `Tile` that already has a `Cowboy`, `Furnishing`, or `isBalcony`. If they move onto a `Tile` that has a `Bottle` on it, then they automatically drink it and get drunk.

The goal is to have your `Cowboy`s `play(piano)`, where `piano` is a Piano. Every time they play an adjacent piano `Furnishing`, they increase their `owner`'s score by 1. When they do this their `turnsBusy` is set to 1, and their `focus` is set to 0. Additionally, the Piano being played is damaged by 1 and its `isPlaying` is set to `true`. Pianos can only be played once per turn.

`Cowboy`s start with 10 health, and can take damage from hazards, Sharpshooters, Brawlers, and called in Young Guns.

### Drunkenness

![A drunk Cowboy](http://i.imgur.com/3RCSkB2.png)

*A drunk Cowboy has a greenish sick hue*

When a `Cowboy` collides with a `Bottle`, he drinks it and `isDrunk` is set to `true`. They will then have their `turnsBusy` set to 5, and for your next 5 turns they will automatically move in their `drunkDirection`, which is set by the Bartender throwing the `Bottle`. You cannot control drunk units.

If a drunk `Cowboy` runs into another `Cowboy`, the other `Cowboy` will lose all focus (set to 0, because who can focus with a drunk person running into you).

If a drunk `Cowboy` runs into a `Furnishing` or Balcony, the `Cowboy` takes 1 damage to their `health`.

Each time a `Bottle` hits a `Cowboy`, that `Cowboy`'s `owner` has their `rowdiness` increased by 1. Once that variable reaches 8 (`Game.rowdinessToSiesta`) then all alive `Cowboy`s on that `owner`'s team take a collective nap, or siesta. The siesta takes 8 turns (`Game.siestaLength`) to pass. During this time all cowboys that are taking the nap have their `isDrunk` flag set to true, but they will have no `drunkDirection` (`""`), as they just sit in place and nap.

*Note* that if `YoungGun` calls in a new `Cowboy`, that new `Cowboy` is unaffected by the siesta, and can play normally.

### Jobs

`Cowboy`s also have a `job`. This tells you what actions the cowboy will perform when it `act()`s. The valid jobs are:

- `"Sharpshooter"`
- `"Brawler"`
- `"Bartender"`

You can only `callIn()` 2 of each `Cowboy` per `job`. This constant is exposed via the integer `Game.maxCowboysPerJob`.

#### Sharpshooters

![Sharpshooter Sprite](http://i.imgur.com/9SyDI29.png)

`Cowboy`s with the `job` of `"Sharpshooter"` have a revolver and can shoot other things. Every turn they choose not to `move()`, `act()`, or `play(piano)`, they will gain 1 `focus`. Every `focus` they have lets them shoot 1 more `Tile` away. They shoot in the cardinal directions in a straight line, and the bullet damages everything on the `Tile`(s) in that line that they hit (bullet penetration), including friendlies! Those hit by his shot are damaged for 4 health damage (`Game.sharpshooterDamage`). His `focus` is then set to 0.

If a Sharpshooter moves or acts, his `focus` is set to 0. If he plays a piano his `focus` is unchanged.

For his `act(tile)`, pass the adjacent `Tile` to him in the cardinal direction you want to shoot.

#### Brawler

![Brawler Sprite](http://i.imgur.com/IeyAK5B.png)

The `"Brawler"` cannot `act()` directly. Calling that function will result in an invalid message.

Instead, at the end of every turn, even while drunk, he punches everything around on adjacent `Tile`s, dealing 1 damage (`Game.brawlerDamage`) to `Cowboy`s and `Furnishings` on those `Tile`s, including friendlies! `Bottles` are not hit by Brawlers.

#### Bartender

![Bartender Sprite](http://i.imgur.com/R3txDDo.png)

A `"Bartender"` throws `Bottle`s. When a Bartender does their `act(tile, drunkDirection)` on a valid adjacent `Tile`, a new `Bottle` is spawned on that `Tile`. The `drunkDirection` string should be a cardinal direction (`"North"`, `"South"`, `"East"`, or `"West"`) and is chosen by the AI calling the act. `Bottle`s make any `Cowboy`s that get drunk off that bottle walk in that `drunkDirection`.

Once a Bartender throws a bottle his `turnsBusy` is set 5, as he needs 5 turns to fill up a new `Bottle`. This is stored in the `Game.bartenderCooldown` variable. He cannot act or play during this time.

*Note<sub>1</sub>*: The new `Bottle` created by this `Bartender` is added to the end of the `Game.bottles` list.

*Note<sub>2</sub>*: However, If the Bartender tries to act on an adjacent Tile with a "thing" on it, no new `Bottle` GameObject will be created, instead if it's a `Cowboy` it instantly becomes drunk.

## Bottles

![Bottle Sprite](http://i.imgur.com/3AY2puv.png)

Bottles are thrown by Bartenders. They have a `direction`, and automatically travel 1 `Tile` per turn in that direction until they collide with:
- Another `Bottle`
- A `Cowboy`
- A `Furnishing`
- A Balcony `Tile`.

Colliding with a `Furnishing`, Balcony, or another `Bottle` just destroys the `Bottle`(s). `Cowboy`s get drunk.

No `Furnishing`s or `Cowboy`s get damaged by a `Bottle` breaking. `Bottle`s exist to get `Cowboy`s drunk.

### End of Turn Collisions

Between `Player`s' turns are when `Bottle`s move. They **all** move at the same time, ignoring any potential collisions. Only once all bottles have moved to their new tiles do we check for collisions. This does mean that bottles can pass by each other.

## Furnishings

![Piano Sprite](http://i.imgur.com/KenrOwJ.png)

![Furnishing Sprite](http://i.imgur.com/uDSanIi.png)

`Furnishing`s exist on `Tile`s and never move after spawning. Each has a `health`, and can be damaged. If a `Furnishing`'s `isPiano` is `true`, it is a piano, and can be played.

Pianos start with 48 `health`. `Furnishing`s whose `isPiano` is `false` start with 16 `health`, and cannot be played.

*Note*: `Furnishing`s cannot get drunk. Because that's silly. Stop asking.

## Additional Technical Details

### Lists Resizing

During your turn if the health for a `Cowboy` or `Furnishing` reaches 0, its `isDead` or `isDestroyed` flag is set to `true`, and their `tile` is set to `null`. However, they will **not** be removed from the lists they are contained in (`Game.cowboys`, `Game.furnishings`, `Player.cowboys`) until the turn they died on ends. This is because if we resized the lists during your turn, and you were iterating over the lists, a lot of programming languages don't like things being resized during `for()` loops, and your code will blow up because of us. So, make sure to check that the `Cowboy` or `Furnishing` in each of those lists did not die before trying to interact with them.

### Variable Names

We assume `camelCase` for variables in this document, but some clients (Such as Python) use `underscore_case` for the actual variable names.
