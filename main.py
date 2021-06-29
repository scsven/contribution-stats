from git import Repo
from pathlib import Path
import subprocess
import logging
import re

mail_mapping = {
    ("yhmo@zeronedata.com", "yihua.mo@zilliz.com"),
    ("40255591+BossZou@users.noreply.github.com", "yinghao.zou@zilliz.com"),
    ("xy.wang@zilliz.com", "xiangyu.wang@zilliz.com"),
    ("56623710+del-zhenwu@users.noreply.github.com", "zhenxiang.li@zilliz.com"),
    ("xiaohaix@student.unimelb.edu.au", "xiaohai.xu@zilliz.com"),
    ("46514371+shengjh@users.noreply.github.com", "shengjun.li@zilliz.com"),
    ("zw@milvus.io", "zhenxiang.li@zilliz.com"),
    ("xupeng3112@163.com", "peng.xu@zilliz.com"),
    ("ophunter52@gmail.com", "chengming.li@zilliz.com"),
    ("zz736@nyu.edu", "zhiru.zhu@zilliz.com"),
    ("zw@zilliz.com", "zhenxiang.li@zilliz.com"),
    ("49774184+shengjun1985@users.noreply.github.com", "shengjun.li@zilliz.com"),
    ("scsven@qq.com", "xiangyu.wang@zilliz.com"),
    ("zzhu@fandm.edu", "zhiru.zhu@zilliz.com"),  # TODO
    ("39671710+cqy123456@users.noreply.github.com", "qianya.cheng@zilliz.com"),
    ("cshiyu22@gmail.com", "shiyu.chen@zilliz.com"),
    ("67679556+godchen0212@users.noreply.github.com", "qingxiang.chen@zilliz.com"),
    ("51370125+XuanYang-cn@users.noreply.github.com", "xuan.yang@zilliz.com"),
    ("zongyufen@foxmail.com", "yufen.zong@zilliz.com"),
    ("48198922+Yukikaze-CZR@users.noreply.github.com", "zirui.chen@zilliz.com"),
}

project = {
    "milvus_master": {
        "repo_url": "https://github.com/milvus-io/milvus.git",
        "branch_name": "master",
        "block_list": [
            "./internal/core/src/pb",
            "./internal/core/src/index/thirdparty",
            "./internal/core/src/index/unittest/sift.50NN.graph",
            "./internal/core/src/index/unittest/siftsmall_base.fvecs",
            "./internal/core/thirdparty",
        ],
        "allow_suffix": [".go", ".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".hxx", ".py",
                         ".yaml", ".yml", ],
    },

    "milvus_1_x": {
        "repo_url": "https://github.com/milvus-io/milvus.git",
        "branch_name": "1.x",
        "block_list": [
            "./core/src/grpc",
            "./core/src/index/thirdparty",
            "./core/src/index/unittest/sift.50NN.graph",
            "./core/src/index/unittest/siftsmall_base.fvecs",
            "./core/thirdparty",
            "./sdk/grpc-gen",
            "./sdk/thirdparty",
        ],
        "allow_suffix": [".go", ".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".hxx", ".py",
                         ".yaml", ".yml", ]
    }
}

project = project["milvus_master"]
# project = project["milvus_1_x"]

logging.basicConfig(level=logging.DEBUG)


def list_paths(root_tree, path=Path(".")):
    for blob in root_tree.blobs:
        yield f"{path}/{blob.name}"
    for tree in root_tree.trees:
        yield from list_paths(tree, f"{path}/{tree.name}")


logging.info(f"start")

repo = Repo.clone_from(project["repo_url"], './repo')
logging.info(f"clone finish")

repo.git.checkout(project["branch_name"])

commit = repo.commit(repo.head.object.hexsha)
paths = [path for path in list_paths(commit.tree, ".")]
logging.info(f"paths.len: {len(paths)}")

# pprint(repo.blame(repo.head.object.hexsha, path))

with open("i1.tmp", "w") as file:
    for path in paths:
        if path.startswith(tuple(project["block_list"])):
            continue

        if path.endswith(tuple(project["allow_suffix"])):
            file.write(f"{path}\n")

with open("i1.tmp", "r") as input_file:
    paths = input_file.readlines()
    with open("i2.tmp", "w") as output_file:
        paths_count = len(paths)
        percentage = 0.1

        for i, path in enumerate(paths):
            path = path[:-1]
            res = subprocess.check_output(f"cd ./repo; git blame --line-porcelain {path} | sed -n 's/^author-mail //p'",
                                          shell=True).decode("utf-8")
            output_file.write(res + "\n")
            if percentage <= i / paths_count:
                logging.info(f"process {int(percentage * 100)} %")
                percentage += 0.1

subprocess.check_output(r"sed -r '/^\s*$/d' i2.tmp > i3.tmp", shell=True)

subprocess.check_output("cp i3.tmp i4.tmp", shell=True)
for m in mail_mapping:
    subprocess.check_output(f"sed -i 's/{m[0]}/{m[1]}/g' i4.tmp", shell=True)

subprocess.check_output("cat i4.tmp | sort -f | uniq -ic | sort -nr > i5.tmp", shell=True).decode("utf-8")

with open("i5.tmp", "r") as input_file:
    pattern = re.compile(r"([0-9]+).*<(.*)>")
    founds = re.findall(pattern, input_file.read())
    total = 0
    for found in founds:
        total += int(found[0])

    with open("i6.tmp", "w") as output_file:
        for found in founds:
            lines_percent = format(int(found[0]) * 100 / total, ".1f")
            output_file.write(f"{int(found[0])} : {lines_percent}% : {found[1]}\n")

print(open("i6.tmp", "r").read())

