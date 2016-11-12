# Megaminer 16: ANARCHY #
## Gameplay Mechanics And Rules ##

### Win Conditions ###
Win conditions are evaluated sequentially.
 1. Burn down enemy HQ
 2. Do more damage to enemy HQ
 3. Have more buildings left at the end of the game
 4. Greater health sum across buildings
 5. Coin Flip

Winning condition 1 ends the game, if neither Headquarters are burned down at the end of the game the next conditions are evaluated in order.

### The Map ###
Buildings are randomly spread across the map, vertically mirrored across the center with both players' HQ on opposite sides.
The game has the following properties that are known to players:
 1. mapWidth = 40
 2. mapHeight = 20
 3. buildings = list of all buildings
 4. forecasts = list of every forecast that will occur in the game
 5. currentForecast = the current forecast
 6. maxTurns = 300
 7. baseBribesPerTurn = 10

### The Buildings ###
Buildings are your units for the game; all of your buildings can be bribed, unless they are burned down, and are subject to destruction by fire.

##### Headquarters: #####
 Your Headquarters; destroying your opponent's HQ wins you the game. All Warehouses on the map have a boolean value called isHeadquarters. If this is true the building is a Headquarters. If your Headquarters is destroyed you lose the game.
+ Health: 300
+ fireAdded- How much fire is added when ignite is used. Headquarters add 20 fire to a building
+ ignite(building): costs 1 bribe. Lights a building on fire and creates a fire of intensity equal to fireAdded. Exposure is increased by the Manhattan distance between its location and the target.
+ NOTE: The Headquarters cannot be directly ignited. Wind must be used to transfer fire to the Headquarters.

##### Warehouse: #####
+ Health: 100
+ fireAdded- How much fire is added when ignite is used. Warehouses add 3 fire to a building
+ Exposure: Base minimum of 0. Drains at a rate of 10 per turn.
+ ignite(building): Costs 1 bribe. Lights a building on fire and creates a fire of intensity equal to fireAdded. Exposure is increased by the Manhattan distance between its location and the target.


##### Fire Departments: #####
Can be bribed by you to remove fire from a building.
+ Health: 100
+ extinguish: Costs 1 bribe and will reduce the fire on a building by 2
+ NOTE: Fire Departments cannot use extinguish on the headquarters!
##### Police Departments: #####
Can be bribed to deal damage to warehouses based on their exposure.
+ Health: 100
+ raid: Costs 1 bribe to deal damage to an Abandoned Warehouse equal to its exposure

##### Weather station: #####
Can be bribed to change the next forecast, which affects your opponent.
+ Health: 100
+ rotate- Costs 1 bribe per quarter rotation. Changes the direction of the wind on the next turn.
+ intensify- Costs 1 bribe to increase the intesnsity by 1. The max Forecast intensity is 10.

### Mechanics ###
#### Bribes ####
Bribes are your means to get your buildings to perform actions. Each building can only be bribed once per turn.
When a building is burned down (health = 0) the controllingPlayer of the building gains 1 additional bribe on their next turn.

#### Fire ####
Fire spreads across all buildings, regardless of player control.\n
All buildings have a fire attribute, represented by an int from 0 to 20. An intensity of 0 means no fire. Fire damages buildings by an amount equal to their intensity at the end of each turn and depletes at a rate of 1 per turn. \n
Fire can also be applied to buildings that have already been burned down, burned buildings can have all the same properties as buildings that are still alive, except that they cannot be bribed.

#### Forecast ####
The forecast of every turn has 3 attributes:
+ direction: What direction the fire will blow: North, East, South, or West
+ intensity: the number of buildings a fire will blow across and the intensity of the fire applied. If there is a fire on the building a fire is blown across the intensity of the fire become the greater of the two.
+ controlling player: The player who can control this forecast.

In the beginning of the game a list of forecasts is pre-generated. Every forecast for the entire game can be seen. The forecasts prior to being changed by weather stations are mirrored for both players. Here is an example for a list of 8 turns following the pattern (your forecast : intensity, opponent's forecast : intensity).
+ (N:3 , N:3) (E:4, E:4) (W:8, W:8) (S:6, S:6)
Changing the direction of a forecast will affect the way the wind blows on your opponents coming turn. For example:

#### Exposure ####
When Warehouses set fire to buildings the build up exposure equal to Manhattan distance (deltaX + deltaY) from them to their target. Police departments can be bribed to do damage based upon the exposure. \n
Exposure depletes at a rate of 10 per turn.
