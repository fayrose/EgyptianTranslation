with open('./compiled_corpora/aligned.egy.csv', 'r') as file:
    lines = file.readlines()

dic = {}
failed_idxes = {}
idx_list = []
for i, item in enumerate(lines):
    item = item.strip('\n')
    if item in dic:
        if item in failed_idxes:
            failed_idxes[item].append(i)
        else:
            failed_idxes[item] = [dic[item], i]
        idx_list.append(i)
    else:
        dic[item] = i

ranges = []
for i in idx_list:
    if not len(ranges):
        ranges.append([i, i + 1])
    elif ranges[-1][1] == i:
        ranges[-1][1] += 1
    elif ranges[-1][1] == i + 1:
        ranges[-1][1] += 2
    else:
        ranges.append([i, i + 1])
    # if not len(ranges) or ranges[-1][1] != i or ranges[-1][1] != i + 1:
    #     ranges.append([i, i + 1])
    # elif ranges[-1][1] == i:
    #     ranges[-1][1] += 1
    # elif ranges[-1][1] == i + 1:
    #     ranges[-1][1] += 2

diffs = [item[1] - item[0] for item in ranges]
max_diff = max(diffs)
max_idx = diffs.index(max_diff)
print(len(failed_idxes))
print('done')