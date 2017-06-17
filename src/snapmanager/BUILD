py_library(
	name = "zfs",
	srcs = ["zfs/__init__.py", "zfs/zfs.py"]
)

py_library(
	name = "snapmanager",
	srcs = ["snapmanager.py"],
	deps = [":zfs"]
)

py_binary(
	name = "newshortsnap",
	srcs = ["newshortsnap.py"],
	deps = [":snapmanager"]
)

py_binary(
	name = "newdailysnap",
	srcs = ["newdailysnap.py"],
	deps = [":snapmanager"]
)
