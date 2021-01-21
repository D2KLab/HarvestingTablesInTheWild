#!/bin/sh

pandoc -f markdown --listings --template=./eisvogel.tex -V colorlinks -V urlcolor=NavyBlue -o report.pdf report.md
