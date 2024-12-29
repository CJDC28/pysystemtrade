#! /usr/bin/env bash

cd ~/harbor-macro/harbor-macro-site/
git pull
git add -v public
git commit -m "Updating site"

git push origin

exit 0;
