# Cadre
A framework for creating networked AI and human games.

![{Cadre}](http://i.imgur.com/17wwI3f.png)

All inspiration taken from [MST's SIG-GAME framework](https://github.com/siggame), and most of the terminology is assuming some familiarity with it as this is a spiritual successor to it.

## Features

* Multi-Game Framework
  * One server instance can host multiple games at the same time, and the games can be completely different games.
  * All clients support this as well.
  * e.g. One server can host Chess, Checkers, Go, etc all at the same time and clients can choose which games to play.
* A mix of JavaScript (via Node.js) and Python 3.4 to go from game concept to running engine. With clients in a variety of languages
  * To code a game server logic wise only a basic knowledge of programming concepts is required. CS 1570 (old 53) students should be capable of grasping the game logic, and contributing.
* Easy generation of new games using the [Creer](https://github.com/siggame/Creer) codegen.
* Automatic documentation creation to html docs. This is a new concept outside of the old SIG-GAME framework. Basically a codegen for documentation.
* Games can be turn based or real time, with turn based code abstracted into an inheritable class for re-use between games.
  * More game prototypes can be added easily as new classes for re-use, such as hidden information games.
* All logic is server side, with states updating for clients after anything changes.
* Web interface on the server
  * Gamelog viewer with visualizer for all games
  * Automatic cross-language game documentation generation
* Networking via TCP Sockets
  * Communication via json strings with support for cycles within game references
  * Only deltas in states are send over the network, never entire states, to maximize bandwidth and speed.
* Automatic gamelog generation as a json structure of delta states, complete with game state and data on what caused the delta.
* Every game instance is a seperate thread, so slower games don't block faster ones.
* Extra fields present for Arena and Data Mining purposes
* Clients can be adapted for human players, and if continued development a standalone visualizer could support this
* Hooks to and for the Arena

## What's what?

The naming scheme is simple, *French*:

* Game Server = [Cerveau](https://github.com/siggame/Cerveau) - runs the game
* Codegen = [Creer](https://github.com/siggame/Creer) - generates code for the game in all projects
* Game Client (C++) = [Joueur.cpp](https://github.com/siggame/Joueur.cpp) - plays the game in C++
* Game Client (C#) = [Joueur.cs](https://github.com/siggame/Joueur.cs)
* Game Client (Go) = [Joueur.go](https://github.com/siggame/Joueur.go)
* Game Client (Java) = [Joueur.java](https://github.com/siggame/Joueur.java)
* Game Client (JavaScript) = [Joueur.js](https://github.com/siggame/Joueur.js)
* Game Client (Lua) = [Joueur.lua](https://github.com/siggame/Joueur.lua)
* Game Client (Python) = [Joueur.py](https://github.com/siggame/Joueur.py)
* Game Client (TypeScript) = [Joueur.ts](https://github.com/siggame/Joueur.ts)
* Visualizer = [Visuer](https://github.com/siggame/Viseur) - renders the game

Clients in Ruby, PHP, D, and Go are easily possible. In fact, so long as the language support json and tcp communication it should be easy to add a client in that language to this framework.

## How to Play

For a detailed tutorial on how to play games using this framework see the `howToPlay.md` file alongside this README.

## Other Notes

All the submodules are intended to be kept at the most recent commit on the master branch. To easily checkout them all on master just use the init.sh script:

```
./init.sh
```
