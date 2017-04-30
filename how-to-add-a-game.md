# How To Add a Game

Cadre is a rich, but complex, game framework. Emphasis has been put around rapid development of games knowing that requirements will change on a whim. Because of that we use many different tools to automate as much development as possible, which includes code writing code for us.

This document will guide you through the basics of using Cadre to add a new game. We will refer to it as `GAME_NAME`, or `game_name` when the lowercase version is needed (e.g. `Chess` vs `chess`) throughout this document.

## Requirements

Before running anything make sure this Cadre repo is setup correctly. Just cloning it is not enough, as we use git submodules. To help we have a script, `init.sh` which will properly initialize the submodules and clone them to their most current version on their master branches.

```bash
./init.sh
```

After that you need the requirements for each submodule you wish to run. At the minimum you will need:

1. The codegen, Creer
2. At least 1 game client, a Joueur
3. the game server, Cerveau

Go into each submodule and read their respective README.md for instructions. But in general Python, pip, Node.js, and npm should be enough if you just want the JS/Python clients.

## Step 1: The Game Data File

Everything starts with the new game's data file. to go `/games/` and look at the previously created games. In general it will probably help to copy and paste the folder of the closest game to yours, then edit it to your needs. Many will have a `story.md` and `rules.md` file, but those are mostly for competitors. The only file you **need** to edit is `/games/GAME_NAME/creer.yaml`.

See the [readme in Creer][creer-readme] for more in-depth instructions on what types can be used in the data file. In general you need a primitive type and description for everything. Once you have edited it to your liking move on to step 2.

## Step 2: Running Creer

Creer is our codegen, which means it generates code in all the various Cadre projects based on the game structure you defined in Step 1. Pretty neat eh.

[Creer's readme][creer-readme] has more in depth instructions for what requirements it needs, so follow those.

Now to see if you data file is syntactically valid, do the following from within the Creer directory:

```bash
export GAME_NAME=`name of your game`
./run ${GAME_NAME} -i ../Cerveau --test
```

This will try to template the game files for the game server (Cerveau), but not write any files. Instead it just tests to make sure it can template the files correctly, which includes parsing your data file and making sure it is valid. If it is not, fix it however Creer complains at you.

Once your data file seems correct and the test passes, it's time to write the files! You can repeat this step any time you need to re-run Creer if you change your data structure

```bash
./run ${GAME_NAME} -i ../Cerveau ../Viseur -o ../ --merge
./run ${GAME_NAME} -i ../Joueur.* -o ../
```

`-i` are the input directories, and `-o` is the output. Note that it outputs based on input directory name, so `../Cerveau` will output to `../` + `Cerveau`. If you omit the `-o` flag Creer has an `output/` directory it dumps files in by default.

The reason we separate the running of Cerveau (game server) and Visuer (visualizer) is because of the `--merge` tag. This will take code that the developers put between the `<<-- Creer-Merge: TAG -->>` tags, and preserve them between runs of Creer, eliminating the need to manually copy and paste code between Creer runs.

The Joueur's (game clients) master branch should always be fresh code with no logic, as the point is they are empty shells for _competitors_ to fill, so we won't have anything to merge anyways.

## Step 3: Play your game

Now you game has been freshly templated by Creer. _Technically_ it can be played.

Make sure you have the requirements for Cerveau and your choice Joueur installed, and then open 3 separate terminals (or I guess 1 + number of players for your game, but most games are 2).

The first will run the game server:

```bash
cd Cerveau/
npm install
node main.js
```

If all goes well Cerveau should be waiting to play any games, and your new game should be detected. Sure it's an empty husk of a game with nothing to do, but we want to play it!

Now in each player's terminal run the following (we will use js for this example)

```bash
cd Joueur.js/
make
./run ${GAME_NAME}
```

All game clients have a Makefile, even if it does nothing. Then you tell it to run `GAME_NAME`, and it will ask the game server running on localhost on the default port to connect it to any game session.

If they both connect successfully (and if it is a turn based game), the game will just consist of doing nothing for 500 turns, then someone will win via coin flip!

It will probably also tell you your gamelog is available to view at `http://vis.siggame.io/` but that is a lie. The Viseur instance there has no concept of the new game you just made, so it can't render your game.

## Step 4: "Visualizing" Your Game

_Note_: You can skip this step if you want, it's just to help you get the Visualizer up and running for testing purposes, mostly for Vis developers.

Follow the steps in [Viseur's readme][visuer-readme] to install its dependencies and get it up and running. Then it too should be on localhost, so take the link from Step 3, and change it to:

```
http://localhost:8080/?log=WHATEVER_THE_LOG_SLUG_WAS
```

Then the visualizer should show you your game in it's pure black screen glory! At the very least you should be able to see player names.

## Step 5: Development starts!

At this point everything is "ready" and now humans need to step in and add some game logic. All Cadre projects follow the paradigm that game files are located in `/games/${GAME_NAME}/`.

### Clients

Joueurs (game clients) never require development aside from ShellAI logic. All game logic is server side, as they are glorified shared state programs.

### Server

The game server logic is largely filling in the functions you defined in the `creer.yaml` data file. Go into each class file and look for their `invalidateFunctionName` and `functionName` functions. Fill them in with logic, and look at older games for examples.

In general try as hard as possible to invalidate logic, like making sure the given input is valid, and if it is not return a string explaining why not. Then if all that is valid the `functionName` function will be executed, and you can assume the inputs are valid (as you validated them before).

### Visualization

Each game object can be rendered on screen in it's `render()` function. Fill that in with PIXI.js code. A much more in-depth document for this is in the works.

TODO: link to that document.

## Questions?

We've tried to add markdown documents all over the place with help, and document the code. Otherwise the original system engineer, Jacob Fischer (jacob.t.fischer@gmail), can probably help.

I sincerely hope the process is pain free. I've designed it to be as fast and easy as possible, but I am also a silly person at times.

[creer-readme]: https://github.com/siggame/Creer/blob/master/README.md
[visuer-readme]: https://github.com/siggame/Viseur/blob/master/README.md
