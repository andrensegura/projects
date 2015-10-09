from ctypes import cdll

lib = cdll.LoadLibrary("/home/andre/projects/rust/embed/target/release/libembed.so")

lib.process()

print("done!")
