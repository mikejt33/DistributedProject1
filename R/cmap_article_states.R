library("data.table")
library("rjson")
library("countrycode")
library('dplyr')
library('plotly')
library('plyr')
library('tidyr')
library('stringr')

#read in file
edits <- data.table(read.csv("/Users/stephanierivera/Desktop/Distributed Project/DistributedProject1/actually_cleaned_random_data_of_interest.csv"))
colnames(edits) <- c("Article","Date","User1","User2","Category","Comment")

edits <- edits %>% filter(Article=="Barnard's_Star")

count(unique(edits$User1))

count(str_detect(User1, regex('ip:', ignore_case = TRUE)))

#filter for rows where user has an ip address
edits_ip <-edits %>%
  filter(str_detect(User1, regex('ip:', ignore_case = TRUE)))
##remove ip: from column for every row (data cleaning)
edits_ip$User2 <-gsub('ip:','',edits_ip$User2)

#filter again for if entry includes letter from alphabet (exclude this, more data cleaning)
is.letter <- function(x) grepl("[[:alpha:]]", x)

edits_ip <- edits_ip %>%
  filter(!is.letter(edits_ip$User2))


#filter for specific article 

#article <- "Alabama"

#edits_ip <- edits_ip %>% filter(Article ==article)


#this function is used to get the location of the ip address
#https://heuristically.wordpress.com/2013/05/20/geolocate-ip-addresses-in-r/

freegeoip <- function(ip, format = ifelse(length(ip)==1,'list','dataframe'))
{
  if (1 == length(ip))
  {
    # a single IP address
    require(rjson)
    url <- paste(c("http://freegeoip.net/json/", ip), collapse='')
    ret <- fromJSON(readLines(url, warn=FALSE))
    if (format == 'dataframe')
      ret <- data.frame(t(unlist(ret)))
    return(ret)
  } else {
    ret <- data.frame()
    for (i in 1:length(ip))
    {
      r <- freegeoip(ip[i], format="dataframe")
      ret <- rbind(ret, r)
    }
    return(ret)
  }
} 

#loop to change user2 column to a column with country names
for (i in 1:nrow(edits_ip))
{
  
  edits_ip$User2[i] <- toString(freegeoip(edits_ip$User2[i])[4])
  
}
edits_ip <- filter(edits_ip, User2=="United States")
edits_ip$User1 <-gsub('ip:','',edits_ip$User1)
edits_ip <- edits_ip %>%
  filter(!is.letter(edits_ip$User1))

freegeoip(edits_ip$User1[1])[5]

for (i in 1:nrow(edits_ip))
{
  
  edits_ip$User1[i] <- toString(freegeoip(edits_ip$User1[i])[5])
  
}

colnames(edits_ip) <- c("Article","Date","State","Country","Category","Comment")

#edits_ip$User2 <- NA

edits_ip <- edits_ip%>% group_by(State) %>% tally()

#get the log of the tally 
edits_ip$log <- log(edits_ip$n)

df <- edits_ip


l <- list(color = toRGB("white"), width = 2)
# specify some map projection/options
g <- list(
  scope = 'usa',
  projection = list(type = 'albers usa'),
  showlakes = TRUE,
  lakecolor = toRGB('white')
)

p <- plot_geo(df, locationmode = 'USA-states') %>%
  add_trace(
    z = ~log, text = ~State, locations = ~State,
    color = ~log, colors = 'Oranges'
  ) %>%
  colorbar(title = "Log number of Edits") %>%
  layout(
    title = 'Wikipedia Edits by State - Random',
    geo = g
  )
p



