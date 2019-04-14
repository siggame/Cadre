# MMAI 23: [StarDash]

stardash is a game focused on collecting the most mithicite.

## [Map][Map]
- coordinate based
- Fairly large, around 1800 x 3200
- There are bodies, ships, and projectiles
	- bodies can be the sun, planets, or asteroids.
- 4 types of materials spawn around the sun, genarium, rarium, legendary, mythicite.

## Win Conditions
Have the most mithicite to win!
1. Otherwise the most valuable player wins
2. otherwise coin flip.

## [Units][Unit]
Each player starts with 3 miners and nothing else.
There are five types of units, corvettes, missileboats, martyrs, miners, and transports. Martyrs block corvettes, corvettes can destroy missile ships, missile ships ignore martyrs.
a units radius is stored in the game settings.
There energy is their health pool.
All units cost ot purchase is stored in the job under unitCost (unitCost)

All units may dash at a rate of 50 per 1 energy spent. The rates can be found in the settings for a future proof reference.
 - dash ends a units turn. (AKA you cannot dash to a asteroid and immediatly start mining)
 - mining counts as dashing.

Corvette
 - fires projectiles that instantly damage in range. They currently have a range of 100. (job.range) does (job.damage) damage.
 - they may fire at projectiles, but it takes 2 shots to take them out. (uses shootdown)

missileboat
 - fires a missile that currently travels at a speed of 100 for 5 turns. Check it's fuel for it's life span and check the settings for it's speed.
     - missiles instantly kill their target if they collide with them.
 - They may fire at projectiles and instantly kill them, but only if they are in range of 1 missile movement. (use shootdown)
 - cannot fire if they have moved.

martyr
 - becomes the protector all of all untis within it's jobs range if it is the oldes martyr that is in range of that ship.
 - shields regenerate at a rate of the corvettes damage. (currently 20)
 - shield total is currently 100 (job.shield for max).
     - only martyrs use the shield value on units.

miner
 - can mine asteroids using the mine function (currently at a rate of 10 per turn, check the mining speed setting)
     - count it as warping to it's currentl location.
 - can only hold so much ore (currently 20, check the job.carrylimit)

transporter
 - reduced hp (currently 50 instead of 100, check job.energy)
 - increased cargo (currently 100, check job.carrylimit)
use unit.transfer to grab things from ships.

## [Body][Body]
There are three types of bodies: planets, asteroids, and the sun.
There is only one sun in the center of the map, you can't path through it in any way and anything that enters it dies. (position 2 of game.bodies)
There are two planets on either side of the map (bodies positions 0 and 1, ore check the player.homeBase)
Everyting else is asteroids that vanish if their amount hits 0.
they all store a material type property.

planets
- pull resourrces off of ships and add the value to the owning player.
- they recharge ships, pulling from their amount property.
     - check the settings for their recharge rate.

asteroids
 - Their amount is how much of their resource they have
     - should we had regeneration, check the settings. It is 0 for now.
     - you can check the map gerating settings in sets like min and max asteroid.
 - you can figure out where they will be x turns in the future by using nextx and nexty. Just tell it how many turns if they future you want to check.
 - If you are mining a asteroid, your opponent can't mine it
     - this is only true WHILE you are mining it.

[Stardash]: https://github.com/siggame/Cerveau/blob/master/games/stardash/
[Map]:  https://github.com/siggame/Cerveau/blob/master/games/stardash/game.ts
[Tile]: https://github.com/siggame/Cerveau/blob/master/games/stardash/tile.ts
[Unit]: https://github.com/siggame/Cerveau/blob/master/games/stardash/unit.ts
[Body]: https://github.com/siggame/Cerveau/blob/master/games/stardash/body.ts
[Projectle]: https://github.com/siggame/Cerveau/blob/master/games/stardash/projectile.ts