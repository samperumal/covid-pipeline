require("tidyverse")
require("RJSONIO")

source("parse-log.R")

data <- as_tibble(read.csv("/var/data/analysis.csv")) %>%
  mutate(date = as.Date(date)) %>%
  # mutate(province = fct_relevel(data$province, "KwaZulu-Natal", "Western Cape", "Gauteng")) %>%
  # order(diff) %>%
  filter(diff > 0 & abs(diff) < 10000)

log_data <- loadLog()
log_data_daily <- log_data %>% group_by(date) %>% summarise(n = n())

data %>%
  ggplot(mapping = aes(x = date, y = diff, color = province)) +
  geom_line() +
  # geom_path(aes(y = total), linetype = "dashed") +
  # geom_point(aes(y = diff)) + geom_smooth(aes(y = diff))+
  facet_wrap(. ~ province, scale = "free") +
  # theme_ipsum(axis_title_just = "c") +
  theme(legend.position = "none") +
  scale_x_date(date_breaks = "4 months", date_labels = "%b '%y") +
  xlab("Date") + ylab("Daily new cases") +
  ggtitle("South African COVID-19 progression", subtitle = "New cases per day")

ggsave("/var/data/images/new-cases-summary.png", device = "png")

data %>% filter(province == "Western Cape") %>% 
  left_join(log_data_daily, copy = TRUE) %>%
  ggplot() +
  geom_line(mapping = aes(x = date, y = n, colour = "Total cases / 100")) +
  geom_line(mapping = aes(x = date, y = total / 100, colour = "Triaged cases")) +
  ggtitle("Western Cape Covid cases", subtitle = "Total vs Triaged") +
     scale_color_manual(name = "Model fit",
                        breaks = c("Total cases / 100", "Triaged cases"),
                        values = c("Cubic" = "blue", "Quadratic" = "red"))

ggsave("/var/data/images/triage-comparison.png", device = "png")