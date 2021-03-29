# gh-action-post-to-wiki

This is a example repo for demonstrating how to publish MD files from a repo to a GH Wiki

[![GitHub Super-Linter](https://github.com/jmassardo/gh-action-post-to-wiki/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)


## Assumptions

This code makes the following assumptions

* The filename is the title of the article
* If it finds a matching title, it will update the content
* If the filename doesn't match an existing article, it will create a new one
* There is no current provision to delete articles that aren't in the GH repo

## What about....?

* List of tags in a single metadata item
* Linter should check for metadata tags and fail if they don't exist