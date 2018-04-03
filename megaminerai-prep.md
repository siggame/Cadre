# MegaMinerAI Preperations

When preparing each client for competitors you will need to do a few things. You'll need to repeat these steps for every `Joueur.language/`, where `language` can be any of the programming languages

1. Delete the `_creer/` directory, and the `_dossier.data` file if it exists. They are just templates to generate code. Competitors do not need that, as we should have already generated the files for them.
2. Delete all other game directories in `games/` besides the game you are preparing this client for.
3. Update in `testRun` the line `./run GAME_NAME ...` replacing GAME_NAME with the game's name.
4. Update `README.md` replacing all GAME_NAMEs in there with the game name. Pay attention to casing, as `game_name` is probably the lowercased version of the game name (usually representing directory names).
5. Add "Shell AI" logic to `games/GAME_NAME/ai.language`, where `language` if the client's programing language extension. "Shell AI" logic should:
    * Call all possible game actions (except GameObject.log(), as that's a debugging function)
    * Be well commented and easy to understand
    * As simple as possible. If it's possible to play a game by just calling all the commands without looping over anything, don't loop.
6. Remove the Creer Tags from that `games/GAME_NAME/ai.language` file. Creer tags look like: `<<-- Creer-Merge: key -->>`.
    * The C++ client will also have an ai.h file to de-Creer as well.

Once you've done that commit all those changes to a new branch `GAME_NAME-ShellAI-Dev`. That is the branch were you can update the Shell AI logic, but not the branch competitors will use. We don't want compeititors having to deal with all our commits on the clients so they will use orphaned branches. Just create a new branch off `GAME_NAME-ShellAI-Dev` called `GAME_NAME-ShellAI`, and use the `--orphan` flag to "flatten" the commit history for them. If updates are made to the `GAME_NAME-ShellAI-Dev` branch, delete the orphaned `GAME_NAME-ShellAI` branch and re-create it. Ideally orhpaned branches always have just 1 commit.

Once that is done the `GAME_NAME-ShellAI` branches can be easily distributed to competitors via the web team.
