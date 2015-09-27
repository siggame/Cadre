# Error Codes

All clients (Joueurs) in the Cadre framework are expected to return error code depending on how they exit. These exit codes can help for debugging and for the arena to detect why AIs error.

```json
NONE: 0,
INVALID_ARGS: 20,
COULD_NOT_CONNECT: 21,
DISCONNECTED_UNEXPECTEDLY: 22,
CANNOT_READ_SOCKET: 23,
DELTA_MERGE_FAILURE: 24,
REFLECTION_FAILED: 25,
UNKNOWN_EVENT_FROM_SERVER: 26,
SERVER_TIMEOUT: 27,
FATAL_EVENT: 28,
GAME_NOT_FOUND: 29,
MALFORMED_JSON: 30,
UNAUTHENTICATED: 31,
AI_ERRORED: 42
```

The names describe exactly what happened. In addition, clients should try to print to the *error* output stream information about why it returned what it did.

## NONE: 0

A return code of 0, as expected, is *not* an error. This should happen when a client plays a game, and the game ends without any errors.

## 20-40

Errors in this range are client side errors relating to the client code failing, and *probably* not the competitor's fault.

## AI_ERRORED: 42

This should be what happens when a competitor's AI code breaks, because their code threw an uncaught exception.
