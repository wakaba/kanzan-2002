#!/bin/bash
echo "1..1"
basedir=$(cd `dirname $0`/.. && pwd)
($basedir/perl -c $basedir/kanzan.cgi && echo "ok 1") || echo "not ok 1"
