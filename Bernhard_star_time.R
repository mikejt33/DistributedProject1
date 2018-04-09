library(tidyverse)
library(mltools)

data <- read.csv("Barnard's_Star_comments.csv")
colnames(data) <- c("Design", "time", "name","ip", "comment","na")
time <- data$time
df <- data.frame(substr(time,12,16))
df <- df %>%
  mutate(id = row_number())
colnames(df) <- c("time","id")

df <- df %>%
  mutate(breaker = as.integer(substr(time,1,2)))


df$bins <- bin_data(df$breaker, bins=c(0, 4,9, 14, 20, 24), boundaryType = "[lorc")

#plot(df$bins, main = "Frequency")

#ggplot(df, aes(df$breaker, fill = bins)) + geom_histogram(binwidth = 4) 


#ggplot(df, aes(x=bins)) + geom_histogram(aes(y = ..count../sum(..count..)))



ggplot(data = df, aes(x = df$bins, fill = bins))+
  geom_bar() + 
  labs(x = "Time bins (Military Time)",
       title = "Distribution of users editing Barnard Star over 24 hr period in EST") + 
  ggsave("Barnard.star.png")
