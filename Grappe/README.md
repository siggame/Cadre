# Grappe
K-Means clustering for Cadre gamelogs. This script is intended for parsing out k-means data from gamelogs for the Arena to pick out "interesting" gamelogs.

![{Cadre}](http://i.imgur.com/17wwI3f.png)

All inspiration taken from [MST's SIG-GAME framework](https://github.com/siggame), and most of the terminology is assuming some familiarity with it as this is a spiritual successor to it.

## Usage

Like many Cadre scripts this is Python 3.

`
python example.py path/to/gamelog.joue
`

Alternatively you can import Grappe, just as any python module:

```python
import grappe

k_means = grappe.parse(gamelog)
```

Note: You can actually pass an already opened up gamelog, or just a string path to the gamelog to open.
