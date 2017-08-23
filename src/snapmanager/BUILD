py_library(
  name = "zfs",
  srcs = ["zfs/__init__.py", "zfs/zfs.py"]
)

py_library(
  name = "snapmanager",
  srcs = ["snapmanager.py", "confreader.py"],
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

py_binary(
  name = "newcustomsnap",
  srcs = ["newcustomsnap.py"],
  deps = [":snapmanager"]
)


py_binary(
  name = "newweeklysnap",
  srcs = ["newweeklysnap.py"],
  deps = [":snapmanager"]
)

py_binary(
  name = "confreader",
  srcs = ["confreader.py"]
)

py_binary(
  name = "snapsync",
  srcs = ["snapsync.py"],
  deps = [":zfs"]
)

# vim:set ts=8 sts=2 sw=2 et:
