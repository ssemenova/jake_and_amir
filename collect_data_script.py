# Really gross pls don't look
import re, sre_constants

archive_file = open("archive.txt", "r")
jake_text = open("jake.txt", "w")
amir_text = open("amir.txt", "w")
action_text = open("action.txt", "w")
modifiers = open("modifiers.txt", "w")

def get_text_from_line(line):
    line = line.strip()
    repls = (('<br>',''),('<span class="highlight">', ''),('</span>', ''),("INTRO", ''))
    return reduce(lambda a, kv: a.replace(*kv), repls, line)

def remove_actions_from_dialogue(line):
    # import pdb; pdb.set_trace()
    action = new_line = ""

    # import pdb; pdb.set_trace()
    try:
        split_bracket = re.split("(\[|\])", line)
        save_next_section = False
        for section in split_bracket:
            if "[" in section:
                save_next_section = True
                action += "["
            elif "]" in section:
                save_next_section = False
            elif save_next_section:
                action += section + "] \n"
            elif section:
                new_line += section
    except sre_constants.error:
        pass

    #Not worth the headache to resolve
    try:
        split_paren = re.split("(\(|\))", new_line)
        new_line = ""
        for section in split_paren:
            if "(" in section:
                save_next_section = True
            elif ")" in section:
                save_next_section = False
            elif save_next_section:
                modifiers.write("(" + section + ")\n")
            elif section:
                new_line += section
    except sre_constants.error:
        pass

    return new_line, action

def reset_for_next_video():
    return False, "", "", False


is_script, speaker_carryover, full_quote, force_newline = reset_for_next_video()
for line in archive_file:
    if is_script:
        if "THE END" in line or "</div>" in line or "END" in line:
            is_script, speaker_carryover, full_quote, force_newline = reset_for_next_video()
        elif line.strip() == "<br>" or force_newline:
            if speaker_carryover == "jake":
                full_quote, action = remove_actions_from_dialogue(full_quote)
                if full_quote:
                    jake_text.write(full_quote + "\n")
            elif speaker_carryover == "amir":
                full_quote, action = remove_actions_from_dialogue(full_quote)
                if full_quote:
                    amir_text.write(full_quote + "\n")
            elif speaker_carryover == "action":
                if not full_quote == "[End]" and not "[]" in full_quote:
                    action_text.write(full_quote.strip("[]") + "\n")
            speaker_carryover = ""
            full_quote = ""
            force_newline = False
        elif speaker_carryover:
            full_quote += get_text_from_line(line) + " "
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
                for section in split_line[1:]:
                    full_quote += section.lstrip() + " "
            elif "[" in cleaned_line:
                speaker_carryover = "action"
                full_quote += cleaned_line + " "
    elif "<div class=\"episode-script-inner\">" in line:
        is_script = True
