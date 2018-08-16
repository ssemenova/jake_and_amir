# Really gross pls don't look

def cleanup(line):
    line = line.strip()
    repls = ('<br>', ''), ('<span class="highlight">', ''),('</span>', '')
    return reduce(lambda a, kv: a.replace(*kv), repls, line)


archive_file = open("archive.txt", "r")
corpus_file = open("corpus.txt", "w")

script = False
for line in archive_file:
    if script:
        if "THE END.<br>" in line or "</div>" in line:
            script = False
        else:
            corpus_file.write(cleanup(line) + "\n")
    elif "<div class=\"episode-script-inner\">" in line:
        script = True
