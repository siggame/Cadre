# Client <--> Server IO

This document describes the format and expected input/output for the Cadre game clients and server. It assumes you have some familiarity with [TCP sockets](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) and [JSON encoding](https://en.wikipedia.org/wiki/JSON).

## Forward

The game server and clients are [mostly] well documented. I urge you to follow how they work to trace their IO. In fact, clients have the `--printIO` flag you can read what is sent and received and make your client work with the same input/output.

This document acts as additional documentation to guide you how their operations work when they talk back and forth.

## The Format

All messages exchanged after the initial TCP handshake (where most TCP libraries give you control) are encoded using the following format:

```json
{
    "event": "some string",
    "data": "any valid JSON type, or the data key may be omitted",
    "sentTime": 123456789,
}
EOT_CHAR
```

When sending data it must **always** be a valid JSON object, stringified, and then followed the the End of Transmission character (`U+0004`). All messages are ended via the EOT character, which signifies when your transmission ends and the client/server on the other end should parse the JSON.

The encoded JSON must be an object with 3 properties at most:

* `event`: This key must be present, and the value **must** be another string. The client/server on the other end will use this event name to figure out how to deal with the sent `data`.
* `data`: This key is optional, depending on the event (as just an event name may be enough data for the receiver to work off of), though most events will require some data. The value can be any valid JSON, and object, an array, a number, a string, etc. Again this is wholly dependent on the `event`.
* `sentTime`: This should be the current [Unix time (epoch)](https://en.wikipedia.org/wiki/Unix_time) when the transmission was sent. This is used to calculate latency between the two connected applications.

## Client to Server and back

Because this guide is most useful to add new clients, we will from here on out we will order and assume you are making a new client language and need to know how a client will talk to the server. Basically the order will be after the TCP connection is made what events will be sent to the server and received back from it.

A _Client Event_ means a transmission _from_ a Client, _to_ the Server. Basically the client is asking the server for that event. A _Server Event_ Is the opposite. All events are asynchronous, but to coders using your client should appear synchronous.

_Note_: `sentTime` will be omitted from examples.

### Client Event "alias"

Asks the game server what the actual game name (id) is for some game alias is. The returned "named" event's `data` will be a string of the actual name. If the alias is unknown an "error" event will be sent and the client will be force disconnected from the server.

#### Example

```json
{
    "event": "alias",
    "data": "sP2017-ChEsS"
}
```

### Server Event: "named"

Sent back from a client event "alias" to name the sent alias. Sends back `data` that is a string of the actual name (id).

#### Example

Server --> Client:

```json
{
    "event": "named",
    "data": "Chess"
}
```

### Client Event: "play"

The Client tells the server it wants to play some game in some session. Once this occurs the server should soon after reply that it has been moved to some game lobby waiting for that game to starting playing.

#### `data` options

- `gameName` {string}: the name (id) of the game to play. Use the "alias" event to get the actual id before this.
- `requestedSession` {string}: an identifier for the game session you want to play in. If omitted it means you want to play in the first available session of that game. Send a string if you want to play in a private session, like "MyPrivateGameSession". _Note_: this is _requested_ the actual session you are put in may differ if the given string is "new", "*", or taken by an in progress game.
- `clientType` {string}: the programming language this client is. This should probably be hard coded and not able to be changed by the client.
- `playerName` {string}: The name the of player the client is working on behalf of.
- `playerIndex` {number} _(optional)_: The preferred player index this player wants to play as. By default if this is omitted the first player to connect is the first player in the game, however you can override that by sending a number, so if the second player to connect sends `0`, then they will be the first player in the game (0 is first, not 1, think arrays).
- `password` {string} _(optional)_: If the game server has authentication enabled, this is the password to be allowed to play on said server.
- `gameSettings` {string} _(optional)_: Settings for the game. This varies based on each game and there is no way for a client to know which game settings are valid. Instead send a [Query string](https://en.wikipedia.org/wiki/Query_string) formatted string of the settings.
- `spectating` {boolean} _(optional)_: If set to `true`, then this client is treated as a spectator and will not play, but will still be sent information about the game as it progresses. Any other value will be treated as false (such as omitting the key).

#### Example

```json
{
    "event": "play",
    "data": {
        "gameName": "Chess",
        "requestedSession": "BestSession",
        "clientType": "C++",
        "playerName": "John Smith",
        "playerIndex": 0,
        "password": "",
        "gameSettings": "startTime=300000&something=somethingElse"
    }
}
```

### Server Event "lobbied"

This should be sent after a client sends a "play" event, notifying them they are in a lobby waiting for the game to start. After this event clients should wait for a "start" even to be sent from the server when the game starts.

After this point the game client should have enough information to initialize classes for its AI and Game instances.

#### `data` options

- `gameName` _(string)_: The name of the game that is starting. Should be the same as the name you send via "play"
- `gameSession` _(string)_: The game session you actually ended up in. May differ from the sent `requestedSession`.
- `constants` _(object)_: a string key to string value dictionary. Clients **must** save this somewhere, as the constants sent back from this will be used from the server to encode future messages such as delta changed events.

#### Example

Server --> Client:

```json
{
    "event": "lobbied",
    "data": {
        "gameName": "Chess",
        "gameSession": "BestSession",
        "constants": {
            "DELTA_REMOVED":"&RM",
            "DELTA_LIST_LENGTH":"&LEN"
        }
    }
}
```

### Server Game Event "delta":

This event will occur _any time a change in state occurs on the game server_ (except players' timers ticking, as time is always changing). The delta's exact makeup cannot be predicted, as it depends wholly on the game being played's structure, and what changed. Delta merging is a crucial concept to understand to merge game states, that is outside the scope of this document.

The `data` property will always be an object that represents the game's current state, but that object will only contain changed keys/values. Clients should be able to delta merge that object on top of the current Game.

__Note__: This event will occur while game play is occurring, but it will also be sent _once_ before. Right before the "start" event is sent, this initial "delta" event can be seen as a change in state of the game from un-started to the initial game state.

### Server Event: "start"

This will eventually be sent from the server to the client when the game starts. This event is dependent on other client(s) connecting to start the game. When this is sent the client and game should shift to Game mode, where events are exchanged quickly to do gameplay. All prior events not marked Client/Server Game Event, are no longer valid and will never be seen again.

The sent data is optional. If it is sent it contains game information pertinent to only your client.

#### `data` options

- `playerID`: The player index of your player in the `Game.players` array. Synonymous with `PlayerIndex`.

#### Example

```json
{
    "event":"start",
    "data":{
        "playerID":"0"
    }
}
```

### Server Game Event "order":

Sent from the game server instructing them to fulfill some order. Probably "runTurn". You can think of this as the server telling the client to run a function and send back the result. While the order is happening clients may send certain "run" events depending on the game.

#### `data` options

- `name` {string}: The name of the order to execute (probably a function name in camelCase).
- `index` {number}: An identifier for the order. When the client finishes executing this order this index should be sent back too (just in-case of duplicate identical orders).
- `args` {array}: An array of arguments to be piped to the order's named function, in positional order.

#### Example

```json
{
    "event":"order",
    "data": {
        "name":"runTurn",
        "index":0,
        "args":[]
    }
}
```

### Client Game Event "finished"

Sent from a client to the server as the result of an "order" event. This is basically the return event from said order.

#### `data` options

- `orderIndex` {number}: the index of the order the client finished running
- `returned` {any}: The value returned from that order

#### Example

```json
{
    "event": "finished",
    "data": {
        "orderIndex": 0,
        "returned": true,
    }
}
```

### Client Game Event "run"

Sent from the client to the game server as a request to run some game logic server side. The server should eventually send back a "ran" event, but before that expect other events such as a "delta" for how this ran changed the game state.

### `data` options

- `caller` {GameObjectReference}: the game object's reference (object with just its ID) to the game object calling this run command
- `functionName` {string}: the name of the function to run on the caller
- `args` {object}: The arguments for the function being ran. This will be a key/value dictionary where each key is the string of the argument to the function by name, and the value is the value for that argument (type varies by function obviously)

#### Example

```json
{
    "event": "run",
    "data": {
        "caller": {"id": "20"},
        "functionName": "move",
        "args": {
            "file": "d",
            "promotionType": "",
            "rank": 1
        }
    }
}
```

### Server Game Event "ran"

The response to a client's run event. This occurs once it has been, well, ran. The `data` send from this is optional. If the requested 'run' would have a return value, that is sent as the `data` value for this command.

#### Example

```json
{
    "event": "ran",
    "data": {"id": "34"}
}
```

### Server Game Event "invalid"

An event that should not occur during normal operations. This is often sent if a client sends a "run" event with invalid properties, such as trying to run a function on a GameObject they do not own. These should result in printing a yellow message telling the coder why the run is invalid. The message will be in the `data` part of the event as a stand alone key `message`.

_Note_: a "ran" even will still be sent back after the "invalid" event. This is an _additional_ event.

### Example

```json
{
    "event":"invalid",
    "data": {
        "message":"Tried to Move Piece White Pawn #20 at c2 to d1."
    }
}
```

### Server Game Event: "over"

This occurs when the game is over. Once this event is sent no further events can be sent from either party. In addition the game server will disconnect automatically.

With the game being over, the last state received should have players set if they won or lost. That data is not directly sent in this event however.

#### `data` options

The entire `data` object is optional, but game servers may elect to send additional meta-data about the end of the game, such as gamelog information. Because the game server's hostname may vary from client to client, any strings with the term `__HOSTNAME__` in them should have that substring replaced by the hostname they used to connect to the game server. This is expected client side behavior.

- `gamelogURL` {string}: The url to the gamelog, in case it needs to be downloaded.
- `visualizerURL` {string}: The url to the visualizer which will download the gamelog and play it back.
- `message` {string}: A message to display to the coder running the client. It will probably tell them that the game is over and they can watch their gamelog via a link embed in the message.

#### Example

```json
{
    "event": "over",
    "data": {
        "gamelogURL": "http://__HOSTNAME__:3080/gamelog/2017.08.18.13.26.44.351-Chess-1",
        "visualizerURL": "http://vis.siggame.io/?log=http%3A%2F%2F__HOSTNAME__%3A3080%2Fgamelog%2F2017.08.18.13.26.44.351-Chess-1",
        "message": "---\nYour gamelog is viewable at:\nhttp://vis.siggame.io/?log=http%3A%2F%2F__HOSTNAME__%3A3080%2Fgamelog%2F2017.08.18.13.26.44.351-Chess-1\n---"
    }
}
```

### Server Event "fatal"

This event should never happen, but may do so during development. This means a fatal error was thrown on the server for some reason, and it could not recover. The game server disconnects after this message, but at least the game clients are given some reason why they were disconnected unexpectedly.

#### `data` options

The `data` will always be the JavaScript Error thrown. However it is expected Errors will have one property, but not for certain:

- `message` {string}: the error message about what fatal error occurred.

#### Example

```json
{
    "event": "fatal",
    "data": {
        "message": "An un-handled fatal error has occurred on the server."
    }
}
```

## Other notes

The game server and clients are [mostly] well documented. Again I urge you to follow how they work to trace their IO. In fact, clients have the `--printIO` flag you can read what is sent and received and make your client work with the same input/output.
