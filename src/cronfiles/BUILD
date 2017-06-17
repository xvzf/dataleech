genrule(
	name = "cronconf",
	srcs = ["etc/dataleech.10min"],
	outs = ["dataleech"],
	cmd = "cat $< > $@"
)


genrule(
	name = "crondaily",
	srcs = ["etc/dataleech.daily"],
	outs = ["dataleech_daily"],
	cmd = "cat $< > $@"
)
