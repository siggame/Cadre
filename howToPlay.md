# How to Play Games

This is a more in-depth tutorial on getting Cadre up and running with Client VS Server games. It assumes you are know how to type things into a terminal, and how to install things on your computer.

First and foremost you'll need to clone Cadre and it's submodoules. the easiest way is with the recurisve flag with git:

```
git clone git@github.com:siggame/Cadre.git
cd Cadre
./init.sh
```

This clones the framework, and then checks out all the submodules to the latest version on their `master` branches.

Now we'll get a server up and running for clients to play games on. The server, called [Cerveau](https://github.com/siggame/Cerveau), runs on [Node.js](https://nodejs.org/en/). Make sure that is installed, then open a terminal in `Cadre/Cerveau/`.

So from inside the Cerveau director just run:

```
npm install
node main.js
```

You should get some statements telling you that the website is up and running at `locahost:3080`, and the game lobby is awaiting clients at `localhost:3000`, like so:

![Cerveau Terminal Running](http://i.imgur.com/XJqc2yv.png)

Verify it's up and running by going to [http://localhost:3080/](http://localhost:3080/), you should see something like this:

![Cerveau running in browser](http://i.imgur.com/SDP4cA4.png)

Good, now let's get two clients playing games. You can use clients in any of the languages. You'll obviously need the programming languages installed for each client you wish to use. For this example we'll use **Lua** and **Python**.

Open two more terminals, one in `Cadre/Joueur.lua` and the other in `Joueur.py`. Make sure the Cerveau terminal is still up and running (so you should have 3 terminals open).

In the Joueur.lua terminal run:

```
lua main.lua Checkers
```

The Lua client should connect to the default server and port (localhost:3000), like so:

![Lua in terminal](http://i.imgur.com/ih0ARFC.png)

And your Cerveau terminal should have recieved that connection:

![Cerveau got a connection](http://i.imgur.com/myfVhUU.png)

Now, Checkers is a two player game. Your Lua client needs someone to play against. Now we connect the Python client with a similar command to the lua client (all clients share virtually the same args). In your Joueur.py terminal:

```
python main.py Checkers
```

A whole bunch of things will happen, very, very quickly:

1. The Python Client connects to Cerveau and asks to play Checkers with anyone
2. Cerveau throws them in the Lobby with the waiting Lua client.
3. Cerveau then sees that lobby has two players (the number of Players Checkers requires), it then spins up a new thread running a Checkers game, and gives that thread the two clients to Handle.
4. The Checkers thread will then run Checkers game logic, taking turns asking the Lua client to run AI code, then the Python client to run AI code, then the Lua client... and so on until the game is over.
5. Checkers is now over, clients are notified to disconnect
6. Joueur.lua and Joueur.py each seperately recieve notification that the game is over, and run AI code cleanup, then exit with 0 (success).
7. The Checkers thread now sends back to the main thread Cerveau is running on a "gamelog", which is a log file describing what happened in the game. AIs play games far to fast for us humans to watch so we must use these logs.
8. The Checkers thread exits with 0 (success)
9. Back on the main Cerveau thead, it now finds that Checkers thread exited and sent a gamelog, it then saves that file (compressed) in `Cadre/Cerveau/output/gamelogs` as `GAMENAME-SESSION-EPOCH.json.gz`.

Yes it's complicated. We are dealing with networked communication between multi-threaded applications all written in different programming languages, and all running AI simulations. We've tried to keep everything simple and easy to understand, but this is a complex challenge we are tackling, so don't feel bad if this makes your head spin.

Games normally only take a few seconds to run on decent hardware. Checkers completes in about 300ms on my i7 4770k.

Here's the terminals after running:

Cerveau:

![Cerveau terminal](http://i.imgur.com/RI0NBQK.png)

Joueur.lua:

![Lua terminal](http://i.imgur.com/grZ75FO.png)

Joueur.py:

![Python terminal](http://i.imgur.com/14x8lO3.png)

You can close the Joueur.py and Joueur.lua terminals if you wish, they did their deed and ran their AIs against each other. Keep Cerveau running, as we are going to watch that Checkers game to make sure the AIs played.

Go back to the website, and refresh the page. You should see a new Game Archieve:

![Game ran in browser](http://i.imgur.com/YILRBTr.png)

Click "watch", and see the pretty visualizer.

![shit-vis](http://i.imgur.com/m4MP5W8.png)

Now we humans can "see" what the AIs did. Visualizers are basically glorified log viewers for AI vs AI games. Currently Cervuea has a "built-in" visualizer humbly names "shit-vis". Ideally in the future a new visualizer is made for the Cadre framework, or it is rolled into SIG-GAME's current ng-vis.

That's it. You've now run two networked AIs against each other. Congraduations, gold star, thumbs up!
