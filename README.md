Why
===

Datamining on The Syrian Censorship Logs: http://sec.tl/

Requirements
============

- redis: http://redis.io/
- redis-py: https://github.com/andymccurdy/redis-py
- some logs...

Usage
=====

0. Start the redis instance

    - If you used the git repository:

        $ src/redis-server redis.conf

    - If you installed a package:

        $ redis-server

1. Split the log(s):

    $ split -l 2000000 *.log splited/split-

2. Launch the processing (Note: it spawn one process by file!)

    $ ./launcher.sh

3. Get a coffee

Examples
========

If you never used redis, you should take a look at the website: http://redis.io/
And at the following commands: http://redis.io/commands#sorted_set

Most often forbidden hostnames
------------------------------

$ src/redis-cli -n 10 zrevrange "cs-host" 0 50 WITHSCORES

Most often forbidden URLs
-------------------------

$ src/redis-cli -n 10 zrevrange "full_url" 0 50 WITHSCORES

Most often forbidden Words
--------------------------

$ src/redis-cli -n 10 zrevrange "words" 0 50 WITHSCORES


