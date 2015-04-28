# Cadre
A framework for creating networked AI and human games.

![{Cadre}](http://i.imgur.com/17wwI3f.png)

All inspiration taken from [MST's SIG-GAME framework](https://github.com/siggame), and most of the terminology is assuming some familiarity with it as this is a spiritual successor to it.

## Features

* Multi-Game Framework
  * One server instance can host multiple games at the same time, and the games can be completely different games.
  * All clients support this as well.
  * e.g. One server could host Chess, Checkers, Go, etc all at the same time and clients can choose which games to play.
* A mix of JavaScript (via Node.js) and Python 3.4 to go from game concept to running engine. With clients in a variety of languages
* Easy generation of new games using the [Creer](https://github.com/JacobFischer/Creer) codegen
* Games can be turn based or real time, with turn based code abstracted into an inheritable class.
  * More game prototypes can be added easily as new classes for re-use
* All logic is server side, with states updating for clients after anything changes.
* Web interface on the server
  * Gamelog viewer with visualizer for all games
  * Automatic general game documentation generation
* Networking via TCP Sockets
  * Communication via json strings with support for cycles within game references
  * Only deltas in states are send over the network, never entire states, to maximize bandwidth and speed.
* Automatic gamelog generation as a json structure of delta states
* Every game isntance is a seperate thread, so slower games don't block faster ones.
* Extra fields present for Arena and Data Mining purposes
* Clients can be adapted for human players, and if continued development a standalone visualizer could support this


## What's what?

The naming scheme is simple, *French*:

* Server = [Cerveau](https://github.com/JacobFischer/Cerveau)
* Codegen = [Creer](https://github.com/JacobFischer/Creer)
* Client (JavaScript) = [Joueur.js](https://github.com/JacobFischer/Joueur.js)
* Client (Lua) = [Joueur.lua](https://github.com/JacobFischer/Joueur.lua)
* Client (Python) = [Joueur.py](https://github.com/JacobFischer/Joueur.py)

Clients in C++, C#, and Java are easily possible. So long as the language support TCP Sockets it is simple to add to Cadre.


## Example

I've put up an example game server ([Cerveau](https://github.com/JacobFischer/Cerveau)) at:

http://home.jacobfischer.me:3000/

Please don't try to crash it. This is Proof of Concept level, not completely stable.


## Other notes

This is a polished proof-of-concept part of the Cadre framework. There are plently of bugs and issues present. The purpose at this time is not to be perfect, but to show that this framework is robust and meets all the needs of MST's ACM SIG-GAME.

