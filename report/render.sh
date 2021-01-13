#!/bin/sh

pandoc -f markdown --listings --template=./eisvogel.tex -V colorlinks -V urlcolor=NavyBlue --table-of-contents -o report.pdf report.md
