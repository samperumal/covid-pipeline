require("tidyverse")

data <- as_tibble(read.csv("/var/data/analysis.csv")) %>% 
	mutate(date = as.Date(date), province = as.factor(province)) 

fit <- with(data, ksmooth(date, diff, kernel = "normal", bandwidth = 3))

p <- data %>%
	mutate(smooth_diff = fit$y, province = fct_relevel(data$province, "KwaZulu-Natal", "Western Cape", "Gauteng")) %>%
	# order(diff) %>%
	filter(diff > 0 & abs(diff) < 10000) %>%
	ggplot(mapping = aes(x = date, color = province)) +
	geom_line(aes(y = diff)) +
	# geom_point(aes(y = diff)) + geom_smooth(aes(y = diff))+
  facet_wrap(. ~ province) +
  theme(legend.position = "none") +
	scale_x_date(date_breaks = "4 months", date_labels = "%b '%y") + 
	xlab("Date") + ylab("Daily new cases") +
	ggtitle("South African COVID-19 progression", subtitle = "New cases per day")

p

ggsave("/var/data/images/new-cases-summary.png", plot = p)
