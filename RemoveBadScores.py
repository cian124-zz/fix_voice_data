import json
import os
import re

interesting_cols = [0]


def main():
    rootdir = "/Users/cmccormack/Daon/VoiceModelGeneration/RBS_English/"
    count_all = 0
    count_four = 0
    count_two = 0
    count_three = 0
    count_one = 0

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(subdir, file)) as f:
                    data = json.load(f)
                    if 'score' in data:
                        count_all += 1
                        if data['score'] == 4:
                            os.remove(os.path.join(subdir, file))
                            file = re.sub('.json$', '.wav', file)
                            os.remove(os.path.join(subdir, file))
                            count_four += 1
                        elif data['score'] == 3:
                            os.remove(os.path.join(subdir, file))
                            file = re.sub('.json$', '.wav', file)
                            os.remove(os.path.join(subdir, file))
                            count_three += 1
                        elif data['score'] == 2:
                            count_two += 1
                        elif data['score'] == 1:
                            count_one += 1
                    # pprint(data['score'])

    print("All: " + str(count_all))
    print("Four: " + str(count_four))
    print("Threes: " + str(count_three))
    print("Twos: " + str(count_two))
    print("Ones: " + str(count_one))


if __name__ == '__main__':
    main()
