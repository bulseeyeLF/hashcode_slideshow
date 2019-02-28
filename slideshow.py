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
    print "Min tags {0}, max tags {1}".format(min_count, max_count)

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

        score_pictures(input_list, tag_counter)

        print(input_list)
        print "No. of tags: {0}, no. of unique: {1}, max ocurrences: {2}, min ocurrences: {3}".format(
            no_of_tags, no_of_unique_tags, _max, _min
        )