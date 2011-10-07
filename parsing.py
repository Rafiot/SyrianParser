import redis

elts = ["date", "time", "time-taken", "c-ip", "cs-username", "cs-auth-group",
"x-exception-id", "sc-filter-result", "cs-categories", "cs(Referer)", "sc-status",
"s-action", "cs-method", "rs(Content-Type)", "cs-uri-scheme", "cs-host",
 "cs-uri-port", "cs-uri-path", "cs-uri-query", "cs-uri-extension",
"cs(User-Agent)", "s-ip", "sc-bytes", "cs-bytes", "x-virus-id"]

# OBSERVED == not forbidden

skip_filter_result = ["OBSERVED"]
skip_elements = ["date", "time", "time-taken", "c-ip", "cs-categories", "s-ip",\
        "sc-bytes", "cs-bytes"]

import re
p = re.compile(r'(\S+) (\S+) (\d+) (\S+) (\S+) (\S+) (\S+) (\S+) "(\S+)" (\S+)  (\d+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) "(.*)" (\S+) (\d+) (\d+) (\S+)').findall

def stats_elements(splitted_line, pipeline):
    i = -1
    for s in splitted_line:
        i += 1
        if elts[i] in skip_elements:
            continue
        pipeline.zincrby(elts[i], s)

def stats_full_url(splitted_line, pipeline):
    full_url = splitted_line[14] + "://" + splitted_line[15] + ":" + splitted_line[16] + splitted_line[17]
    pipeline.zincrby("full_url", full_url)

def stats_words(splitted_line, pipeline):
    words = re.findall(r"\w+", splitted_line[17])
    for w in words:
        if len(w) > 3 :
            pipeline.zincrby("words", w)

def parser(line, pipeline):
    splitted = p(line)
    i = 0
    if splitted is not None and len(splitted) != 0:
        if splitted[0][8] in skip_filter_result:
            return
        stats_elements(splitted[0], pipeline)
        stats_full_url(splitted[0], pipeline)
        stats_words(splitted[0], pipeline)

def import_from_file(filename):
    r = redis.Redis(db=10)
    pipeline = r.pipeline(False)
    i = 0
    for line in open(filename):
        if i >= 5000:
            pipeline.execute()
            i = 0
        line = line.strip()
        if len(line) > 0:
            parser(line, pipeline)
            i +=1
    pipeline.execute()


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        import_from_file(sys.argv[1])
    else:
        print "filename needed"
