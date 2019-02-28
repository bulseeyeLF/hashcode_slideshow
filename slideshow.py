import sys
import copy

script_name = sys.argv[0]

args = (
    script_name,
    "input_file",
    "output_file"
)

arg_len = len(args)

USAGE_STRING = "USAGE: python {0}".format(" ".join(["%s" for _ in range(arg_len)]))

if len(sys.argv) < arg_len:
    print USAGE_STRING % args
    sys.exit(-1)

input_path = sys.argv[1]
output_path = sys.argv[2]


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


def get_max_for_element(element, input_ls, mark_array):
    _maximum = -1
    index = None
    for i in range(len(input_list)):
        if mark_array[i]:
            continue
        a = get_score(input_ls[i], input_list[element])
        if a > _maximum:
            _maximum = a
            index = i
    return index, _maximum


def get_first_link(input_list, marked_array):
    _max = -1
    best_index = None
    cur_x = None
    for x in range(len(input_list)):
        new_index, new_max = get_max_for_element(x, input_list, marked_array)
        if new_max > _max:
            _max = new_max
            best_index = new_index
            cur_x = x
    return cur_x, best_index


default_struct = {
    "left": {},
    "right": {},
    "index": None
}

if __name__ == "__main__":
    input_list = []

    with open(input_path, "r") as inp, open(output_path, "w") as out:
        lines = inp.readlines()
        lines = [x.strip() for x in lines]
        N = int(lines[0])
        for i in range(1, len(lines)):
            split_values = lines[i].split(" ")
            input_list.append(create_input_object(split_values, i - 1))
        tag_counter, no_of_tags, no_of_unique_tags, _min, _max = get_counters(input_list)
        
        input_list = merge_verticals(input_list)
        # print input_list

        # input_list.sort(cmp=sort_fn)
        mark = [False for x in range(len(input_list))]

        first, second = get_first_link(input_list, mark)
        first_elem = copy.deepcopy(default_struct)
        first_elem["index"] = first

        left = first_elem
        second_elem = copy.deepcopy(default_struct)
        second_elem["index"] = second
        right = second_elem
        left["right"] = right
        right["left"] = left
        mark[first] = mark[second] = True

        for i in range(len(input_list) - 2):
            new_index_1, potential_max_left = get_max_for_element(left["index"], input_list, mark)
            new_index_2, potential_max_right = get_max_for_element(right["index"], input_list, mark)
            if potential_max_left > potential_max_right:
                new_elem = copy.deepcopy(default_struct)
                new_elem["index"] = new_index_1
                new_elem["right"] = left
                left["left"] = new_elem
                left = new_elem
                mark[new_index_1] = True
            else:
                new_elem = copy.deepcopy(default_struct)
                new_elem["index"] = new_index_2
                new_elem["left"] = right
                right["right"] = new_elem
                right = new_elem
                mark[new_index_2] = True


        out.write(str(len(input_list)) + "\n")

        while len(left) != 0:
            current = left["index"]
            if input_list[current]["orient"] == "H":
                out.write(str(input_list[current]["id"]) + "\n")
            else:
                out.write("{0} {1}\n".format(input_list[current]["id"], input_list[current]["idvert"]))
            left = left["right"]

