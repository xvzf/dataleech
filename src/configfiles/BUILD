genrule(
  name = "dataleechconf",
  srcs = ["etc/dataleech/datasets"],
  outs = ["datasets"],
  cmd = "cat $< > $@"
)

genrule(
  name = "dataleechremoteconf",
  srcs = ["etc/dataleech/remoteoptions"],
  outs = ["remoteoptions"],
  cmd = "cat $< > $@"
)
# vim:set ts=8 sts=2 sw=2 et:
