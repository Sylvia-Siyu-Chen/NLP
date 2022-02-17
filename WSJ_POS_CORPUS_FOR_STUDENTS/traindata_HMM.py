import sys

POS = {}
STATE = {}

text_len = 0

probabilities_state = {}
probabilities_pos = {}

with open("WSJ_24.pos", "r") as f:
    for token in f.readlines():
        x = token.split("\t")
        if len(x) > 1:
            word = x[0]
            pos = x[1].strip('\n')
            if POS.get(pos) is None:
                POS[pos] = {word: 1}
            else:
                if POS[pos].get(word) is None:
                    POS[pos][word] = 1
                else:
                    POS[pos][word] = POS[pos][word] + 1

with open("WSJ_24.pos", "r") as f:
    tokens = f.readlines()
    STATE["Begin_Sent"] = {tokens[0].split("\t")[1].strip(): 1}
    for n in range(1, len(tokens)):
        if tokens[n] == "\n":
            current = "Begin_Sent"
        else:
            current = tokens[n].split("\t")[1].strip()
        try:
            if tokens[n + 1] != "\n":
                pos = tokens[n + 1].split("\t")[1].strip()
            else:
                pos = "End_Sent"
            if STATE.get(current) is None:
                STATE[current] = {pos: 1}
            else:
                if STATE.get(current).get(pos) is None:
                    STATE[current][pos] = 1
                else:
                    STATE[current][pos] = STATE[current][pos] + 1
        except IndexError:
            pass

# for key, value in STATE.items():
#     print(key, value)


for key, value in POS.items():
    probability = {}
    for k, v in value.items():
        probability[k] = round(v / sum(POS.get(key).values()), 4)
    probabilities_pos[key] = probability

# for key, value in probabilities_pos.items():
#     print(key, value)


for key, value in STATE.items():
    probability = {}
    for k, v in value.items():
        probability[k] = round(v / sum(STATE.get(key).values()), 4)
    probabilities_state[key] = probability

# for key, value in probabilities_state.items():
#     print(key, value)

# for key, value in POS.items():
#     print(key, value)

# with open("WSJ_24.pos", "r") as f:
#     text_len = len(f.readlines()) 

# columns = []
# for i in range(text_len):
#     columns.append(i)

row = list(POS.keys())

sample_sentence = "there you are"

sample_columns = []
for i in range(10):
    sample_columns.append(i)

compare = {}

word_list = sample_sentence.split(" ")
post_path = ["Begin_Sent"]

archive_list = []
archive_acc = 1
archive_post = []

def tag_rest(untag_list, acc_prob, previous_state, pos_path):
    if len(untag_list) == 0:
        compare[acc_prob] = pos_path
        # tag_rest(archive_list,archive_acc,previous_state,archive_post)
    else:
        current_word = untag_list.pop(0)
        pos_list = []
        for key, value in POS.items():
            if current_word in value.keys(): pos_list.append(key)
        if len(pos_list) == 0:
            pos_path.append("OOV")
            tag_rest(untag_list=untag_list, acc_prob=acc_prob * 1 / 100, previous_state="OOV", pos_path=pos_path)
        else:
            print(pos_list)
            for tag in pos_list:
                archive_post = pos_path
                archive_list = untag_list
                archive_acc = acc_prob
                pos_path.append(tag)
                state_prob = probabilities_pos[tag][current_word]
                transitory = probabilities_state[previous_state][tag]
                tag_rest(untag_list=untag_list, acc_prob=acc_prob * transitory * state_prob, previous_state=tag,
                         pos_path=pos_path)


tag_rest(word_list, 1, "Begin_Sent", post_path)
print(compare)
