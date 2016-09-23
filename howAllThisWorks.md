How AI Games Work in Cadre Work
===============================
**[Cadre]** is a game framework, primarily intended, to facilitate AI vs AI games.

[Cadre]: http://github.com/siggame/Cadre

AI vs. AI games differ from "normal" games in a variety of ways. **AIs** are just programs that "players" (programmers) write to "play" on their behalf.  These AIs are housed in game clients, and play games on a game server.

Games
---------
Cadre use a client ↔ server architecture to allow for multiplayer games. The game server is hosted somewhere, and game client(s) connect to it and play. Our game server is called **[Cerveau]**, and game clients are called **Joueurs**.

![Game server <--> client diagram](http://i.imgur.com/IaA8vJ7.png)

[Cerveau] is written in JavaScript and is powered by [Node.js].

[Cerveau]: http://github.com/siggame/Cerveau
[Node.js]: https://nodejs.org/en/

Joueurs are written in a number of programming languages, [C++], [C#], [Java], [JavaScript], [Lua], and [Python] currently. New ones can be added easily.

[C++]: http://github.com/siggame/Joueur.cpp
[C#]: http://github.com/siggame/Joueur.cs
[Java]: http://github.com/siggame/Joueur.java
[JavaScript]: http://github.com/siggame/Joueur.js
[Lua]: http://github.com/siggame/Joueur.lua
[Python]: http://github.com/siggame/Joueur.py

All game logic is server side. Clients do not need to know anything more than the game structure. Which speeds up game development considerably.

AIs
-----
AIs are contained *within* Joueurs (game clients). The Joueur wrapper for each programming language automates connecting to the game server, updating game information, and calling the functions in the `AI` class. A single AI represents a `Player` within each game. So the `AI`'s function should be the one calling the functions as part of the game's objects to manipulate the game state.

Visualizer
--------------
**Gamelogs** are a log of what happened in each game. These files are important because AI vs AI games normally are played very fast. Far faster than a human could interpret the actions. Instead, we use these files to "visualize" the games as they were played to better understand what happened, and help debug things. This is done with the **Visualizer**, **[Viseur]**.

[Viseur]: http://github.com/siggame/Viseur

![Viseur visualizer diagram](http://i.imgur.com/ryRqWsM.png)

[Viseur] is a web-based application programmed in JavaScript, with some [SCSS] and HTML for elements. Viseur parses gamelogs and turns them into pretty graphics.

[SCSS]: http://sass-lang.com/

Codegen
------------
Because we have so many different programs all communicating about the same game (6 clients, 1 server, 1 visualizer), coding *how* to talk about those games between all those for each game would be a lot of copy and paste work. That is perfect for automation! This is where our **Codegen** comes in, **[Creer]**.

[Creer]: http://github.com/siggame/Creer

Creer takes in a data file explaining what a game has in it. For example, in the game Chess, we have an AI that has a `runTurn()` function. During it's turn we expect it to read a `Game` Object to decide what move to make. And to make the actual move, if locates a `Piece` object and call's `piece.move(rank, file)` to actually move it. On all the clients they need to build these classes and function as their programming language syntax permits. On the server side developers just need to program how the `Game` is initialized (place `Pieces` on the board). And logic to check to make sure `Piece.move(rank, file)` is valid given the board state and given arguments. Then, the visualizer just needs to read the gamelogs and play them back. It should know *what* the gamelogs look like from Creer creating a skeleton template just needing rendering instructions.

Arena
--------
Remember, these are AIs are just programs, so we can actually automate game playing. Something you couldn't do with humans who can't play games 24/7. So, we play as many games as possible. This is done in the **Arena** which basically has everyone play each other on as many computers as you give it. This gives the coder a good idea of what is happening.

The Arena is being rewritten into a new part of [Cadre], called "Colisee"

AIs are retrieved from git repositories, normally provided by some API.

Web Server
----------------
[Cadre] has no official **Web Server**. However, if you wanted to create one, that would be rad.
