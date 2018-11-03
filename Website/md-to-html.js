const fse = require("fs-extra");
const path = require("path");
const { promisify } = require("util");

const { cleanIds, sectionize } = require("flat-html-helpers");
const htmlMinifier = require("html-minifier");
const marked = require("marked");
const sass = require("node-sass");
const sassRender = promisify(sass.render);

const INPUT_MD = process.argv[2] || "resume.md";
const OUTPUT_DIR = process.argv[3] || "./";

// we want to use async/await syntax, so invoke this function immediately
(async function main() {
    const md = await fse.readFile(INPUT_MD);

    // I don't want to introduce a whole transpiler like TypeScript for a single script, however I still want type safey
    // while editing in Visual Studio Code, so let's use JSDoc types for types TS can't completely infer.
    // Interestingly these are the only 2 spots TS can't. Otherwise it's smart enough literally everywhere else.
    // Good job TypeScript team!

    const html = sectionize(cleanIds(marked(md.toString()))); // |> would be ideal here
    const { css } = await sassRender({ file: path.join(__dirname, "style.scss") });

    // We don't care about the extra indentation space in this string literal,
    // as it will be minified out regardless.
    const fullFile = `
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Cadre: The AI Game Framework</title>
            <link rel="shortcut icon" type="image/x-icon" href="assets/favicon.ico" />
            <link rel="icon" type="image/x-icon" href="favicon.ico" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="theme-color" content="#D4AF37" />
            <style>${css}</style>
        </head>
        <body>
            <div id="main">${html}</div>
            <footer id="page-footer">
                <p>
                    &copy; ${(new Date()).getFullYear()} <a href="http://siggame.io/">SIG-Game</a>
                    &mdash;
                    Hosted on <a href="http://github.com/siggame/Cadre">GitHub</a>
                    &mdash;
                    Icons made by <a href="https://www.flaticon.com/authors/smashicons">Smashicons</a> from <a href="https://www.flaticon.com/">www.flaticon.com</a>
                </p>
            </footer>
        </body>
        </html>
    `;

    const minFile = htmlMinifier.minify(fullFile, {
        removeComments: true,
        minifyCSS: true,
        collapseWhitespace: true,
    })

    const stream = fse.createWriteStream(path.join(OUTPUT_DIR, "index.html"));
    await stream.write(minFile);
    stream.end();
})().catch((err) => {
    console.error("Error generating html for resume!");
    console.error(err);

    process.exit(1);
});
