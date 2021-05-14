require("tidyverse")
require("RJSONIO")

loadLog <- function() {
	con <- file("/var/data/download/small_log.json", "r")
	jdata <- RJSONIO::fromJSON(con)
	close(con)

	ddata <- lapply(jdata, `[`, c("date", "ip"))
	ddata2 <- lapply(ddata, unlist)
	ddata3 <- do.call(rbind, ddata2)
	ddata4 <- as.data.frame(ddata3)
	ddata4$date <- as.Date(ddata4$date)
	# ddata4 %>% ggplot(aes(x = date)) + geom_histogram(binwidth = 7)

	return (ddata4)
}

