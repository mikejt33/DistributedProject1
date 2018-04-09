library(ggplot2)
library(tidyverse)

data <- read.csv("intelligent_design_subjects.csv", strip.white = TRUE)
colnames(data) <- "subject"
data$count <- rep(1,nrow(data))
d <- table(data)
df <- data.frame(d)

df <- df %>%
  select(subject,Freq) %>%
  filter(Freq > 1)

df.percent <- df %>%
  mutate(subject =subject,
         cumulatve = cumsum(Freq),
         midpoint = cumulatve - Freq /2,
         labels = paste0(round((Freq/sum(Freq))*100,1),"%"))

df.percent$subject.percent <- with(df.percent, paste0(subject, " ",labels))


ggplot(df, aes(x = "", y = Freq, fill = subject)) + geom_bar(width =1, stat ="identity")

ggplot(df.percent, aes(x = "", y = Freq, fill = subject.percent)) + 
  geom_bar(width =1, stat = "identity") + 
  coord_polar(theta = "y", start =0) +
  labs(x ="", y ="", title = "Breakdown of Edits made to Different Dubjects of Intelligent Design wiki \n", fill = "Subjects")+
  ggsave("ID.subject.pie.chart.png")

  


