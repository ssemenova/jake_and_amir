# Really gross pls don't look

def get_text_from_line(line):
    line = line.strip()
    repls = ('<br>',''),('<span class="highlight">', ''),('</span>', ''),("INTRO", '')
    return reduce(lambda a, kv: a.replace(*kv), repls, line)

def reset_for_next_video():
    return False, "", "", False

archive_file = open("archive.txt", "r")
jake_text = open("jake.txt", "w")
amir_text = open("amir.txt", "w")
action_text = open("action.txt", "w")
# misc_text = open("misc.txt", "w")

is_script, speaker_carryover, full_quote, force_newline = reset_for_next_video()
for line in archive_file:
    if is_script:
        if "THE END" in line or "</div>" in line or "END" in line:
            is_script, speaker_carryover, full_quote, force_newline = reset_for_next_video()
        elif line.strip() == "<br>" or force_newline:
            if speaker_carryover == "jake":
                jake_text.write(full_quote + "\n")
            elif speaker_carryover == "amir":
                amir_text.write(full_quote + "\n")
            elif speaker_carryover == "action":
                if not full_quote == "[End]" and not "[]" in full_quote:
                    action_text.write(full_quote + "\n")
            speaker_carryover = ""
            full_quote = ""
            force_newline = False
        elif speaker_carryover:
            full_quote = full_quote + get_text_from_line(line) + " "
        else:
            if "<br>" in line:
                force_newline = True
            cleaned_line = get_text_from_line(line)
            if ":" in cleaned_line:
                split_line = cleaned_line.split(":")
                speaker = split_line[0]
                if "JAKE" in speaker or "Jake" in speaker:
                    speaker_carryover = "jake"
                elif "AMIR" in speaker or "Amir" in speaker:
                    speaker_carryover = "amir"
                full_quote = full_quote + split_line[1].lstrip() + " "
            elif "[" in cleaned_line:
                speaker_carryover = "action"
                full_quote = full_quote + cleaned_line + " "
    elif "<div class=\"episode-script-inner\">" in line:
        is_script = True
