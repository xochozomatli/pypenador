import os

if "test.img" not in os.listdir("tests/data"):
    os.chdir("tests/data")
    os.system("dd if=/dev/urandom of=test.img bs=1M count=384")
    os.system("dd if=./test.jpg bs=1M count=1 >> test.img")
    os.system("dd if=/dev/urandom bs=1M count=640 >> test.img")
    os.chdir("../..")
