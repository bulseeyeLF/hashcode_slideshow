import sys

script_name = sys.argv[0]

args = (
    script_name,
    "input_file"
)

arg_len = len(args)

USAGE_STRING = "USAGE: python {0}".format(" ".join(["%s" for _ in range(arg_len)]))

if len(sys.argv) < arg_len:
    print USAGE_STRING % args
    sys.exit(-1)

input_path = sys.argv[1]


def get_score(node_a, node_b):
    set_a = set(node_a["tags"])
    set_b = set(node_b["tags"])
    return min(len(set_a.intersection(set_b)), len(set_a.difference(set_b)), len(set_b.difference(set_a)))


def find_min_max(tag_dict):
    current_minimum = sys.maxint
    current_maximum = 0
    for key in tag_dict:
        if tag_dict[key] < current_minimum:
            current_minimum = tag_dict[key]
        if tag_dict[key] > current_maximum:
            current_maximum = tag_dict[key]
    return current_minimum, current_maximum


def get_counters(input_list):
    per_tag_count = {}
    global_no_of_tags = 0
    unique_tags = 0
    for val in input_list:
        global_no_of_tags += val["no_of_tags"]
        for tag in val["tags"]:
            if tag not in per_tag_count:
                unique_tags += 1
                per_tag_count[tag] = 1
            else:
                per_tag_count[tag] += 1
    minimum, maximum = find_min_max(per_tag_count)
    return per_tag_count, global_no_of_tags, unique_tags, minimum, maximum


def create_input_object(vals, id):
    return {"orient": vals[0], "no_of_tags": int(vals[1]), "tags": [vals[x] for x in range(2, len(vals))], "id": id}


def merge_verticals(input_dicts):
    verticals = list()
    horizontals = list()
    avg_horizontal = 0
    for picture in input_dicts:
        if picture["orient"] == "H":
            horizontals.append(picture)
            avg_horizontal += len(picture["tags"])
        else:
            verticals.append(picture)
    avg_horizontal /= len(horizontals)
    # print "Avg ", avg_horizontal
    used = [False for i in range(0, len(verticals))]
    for i in range(0, len(verticals)):
        if used[i]:
            continue
        max_vert = i
        tag_set = set(verticals[i]["tags"])
        max_count = len(tag_set)
        for j in range(i+1, len(verticals)):
            if used[j]:
                continue
            tag_set2 = set(verticals[j])
            count = len(tag_set.union(tag_set2))
            if abs(avg_horizontal-count) > abs(avg_horizontal-max_count):
            # if count > max_count:
                max_vert = j
                max_count = count
            
        if max_vert != i:
            used[max_vert] = True
            max_vert_set = list(set(verticals[max_vert]["tags"]).union(tag_set))
            new_picture =  {"orient": "V", "no_of_tags": len(max_vert_set), "tags":max_vert_set, "id": verticals[i]["id"], "idvert": verticals[max_vert]["id"]}
            horizontals.append(new_picture)
            # print len(tag_set), len(verticals[max_vert]["tags"]), len(new_picture["tags"])
    
    return horizontals

def score_pictures(input_dicts, scores):
    max_count = 1
    min_count = 100
    for i in input_dicts:
        if len(i["tags"]) > max_count:
            max_count = len(i["tags"])
        if len(i["tags"]) < min_count:
            min_count = len(i["tags"])
        score = 0      
        for tag in i["tags"]:
            if scores[tag] > 1:
                score += scores[tag]
        i["score"] = score


def sort_fn(val0, val1):
    if val0["no_of_tags"] > val1["no_of_tags"]:
        return -1
    return 1


if __name__ == "__main__":
    input_list = []
    with open(input_path, "r") as inp, open("output_txt", "w") as out:
        lines = inp.readlines()
        lines = [x.strip() for x in lines]
        N = int(lines[0])
        for i in range(1, len(lines)):
            split_values = lines[i].split(" ")
            input_list.append(create_input_object(split_values, i))
        tag_counter, no_of_tags, no_of_unique_tags, _min, _max = get_counters(input_list)
        
        input_list = merge_verticals(input_list)
        # print input_list

        input_list.sort(cmp=sort_fn)
        score_pictures(input_list, tag_counter)

        print "No. of tags: {0}, no. of unique: {1}, max ocurrences: {2}, min ocurrences: {3}".format(
            no_of_tags, no_of_unique_tags, _max, _min
        )

