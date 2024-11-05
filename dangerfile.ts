import { message, warn, fail, markdown } from "danger"

// Add a CHANGELOG entry for app changes
const hasChangelog = danger.git.modified_files.includes("changelog.md")
const isTrivial = (danger.github.pr.body + danger.github.pr.title).includes("#trivial")

if (!hasChangelog && !isTrivial) {
    warn("Please add a changelog entry for your changes.")
}

// Enforce smaller PRs
var bigPRThreshold = 600;
if (danger.github.pr.additions + danger.github.pr.deletions > bigPRThreshold) {
    warn(':exclamation: Big PR (' + ++errorCount + ')');
    markdown('> (' + errorCount + ') : Pull Request size seems relatively large. If Pull Request contains multiple changes, split each into separate PR will helps faster, easier review.');
} else {
    message("Thanks - We :heart: small PR!")
}

// Always ensure we assign someone, so that our Slackbot can do its work correctly
if (danger.github.pr.assignee === null) {
    fail("Please assign someone to merge this PR, and optionally include people who should review.")
}

// Check documentation change and ensure test
const docs = danger.git.fileMatch("**/*.md")
const main = danger.git.fileMatch("**/*.py")
// const tests = danger.git.fileMatch("src/test/java/**/*.java")

if (docs.edited) {
    message("Thanks - We :heart: our documentarians!")
}

if (main.modified) {
    fail("python file is not modified")
}
