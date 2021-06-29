import re

pattern = re.compile(r"([0-9]+) : .* : (.*)")

line_count = dict()
line_per = dict()
total = 0
with open("merged.log", "w") as merged_file:
    with open("1.x.log", "r") as file_1:
        with open("master.log", "r") as file_2:
            f1 = re.findall(pattern, file_1.read())
            print(f"f1.len: {len(f1)}")
            for f in f1:
                line_count[f[1]] = int(f[0])

            f2 = re.findall(pattern, file_2.read())
            print(f"f2.len: {len(f2)}")
            for f in f2:
                if f[1] in line_count.keys():
                    line_count[f[1]] += int(f[0])
                else:
                    line_count[f[1]] = int(f[0])

            for _, c in line_count.items():
                total += c

            line_count = {k: v for k, v in sorted(line_count.items(), key=lambda item: item[1], reverse=True)}

            for key, value in line_count.items():
                merged_file.write(f"{value} : {format(value * 100 / total, '.1f')}% : {key}\n")

