#
#     Convert CSV energy consmption files to a more suitable database format
#

library(RMySQL)
library(dplyr)
library(reshape2)
library(foreach)
library(doParallel)

#DB settings:
username <- ""
password <- ""
host <- ""
port <- 3306
dbname <- ""


#Files location:
path <- "~/data/"

#Geo -> Platform Tag mappings:
tags <- new.env(hash=T, parent=emptyenv())
tags[["Consumption"]] <- "all"
tags[["PRINTER"]] <- "printer"
tags[["WASHING_MACHINE"]] <- "washing-machine"
tags[["TV"]] <- "tv"
tags[["TV_2"]] <- "tv-2"
tags[["HEATER"]] <- "heating"
tags[["FRIDGE"]] <- "fridge"
tags[["GARDEN_EQPT"]] <- "garden-equipment"
tags[["PC"]] <- "computer"

# Parallel Processing:
cl <- makeCluster(8)
registerDoParallel(cl)


files <- paste(path,list.files(path = path, pattern = "*.csv"),sep = "")
foreach(f = files) %dopar% {
 require(RMySQL)
 require(dplyr)
 require(reshape2)

 user <- as.numeric(gsub(".*Data_([0-9]+).*$", "\\1", f))

 fun <- Vectorize(function(variable){ tags[[as.character(variable)]] })
 dat <- read.csv(f) %>% melt
 dat$variable <- as.vector(fun(dat$variable))

 con <-  dbConnect(dbDriver("MySQL"), username = username, password = password, host = host, port = port,  dbname = dbname)
 for( i in 1:nrow(dat)){
    vals <- paste("(", user, ",'", dat$DateTime[i], "','", dat$variable[i], "',", dat$value[i], ")", sep="", collapse=",")

    try({ #"Deal" with time changes...
      dbSendQuery(con, paste("INSERT INTO decarbonet_user_energyconsumption (userid, timestamp, concept, consumption) VALUES",vals))
    })
 }

 dbDisconnect(con)
}


library(ggplot2)
library(scales)
ggplot() + geom_line(data = dat[dat$variable != "all",], aes(as.POSIXct(DateTime, tz="EST"), log(value),color=variable))

#Average for the day and hours...
agg_dat <-  dat %>%
            mutate(day=weekdays(as.POSIXct(DateTime, tz="EST")),time=format(as.POSIXct(DateTime, tz="EST"), "%H"),dt=format(as.POSIXct(DateTime,tz="EST") , "%a %H:00"),dt2=format(as.POSIXct(DateTime,tz="EST") , "%w-%H"))  %>%
            group_by(dt2, dt, variable) %>%
            summarise(mean=mean(value),min=min(value),max=max(value))
#agg_dat$dt2 <- factor(agg_dat$dt2, order(unique(agg_dat$dt2)))

ggplot(data = agg_dat[agg_dat$variable != "all",], aes(x = dt2, y = mean, group = variable, color = variable)) + geom_line() +
#  scale_x_discrete(limits=order(unique(agg_dat$dt2))) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  theme_bw()




order(as.numeric(unique(format(as.POSIXct(dat$DateTime,tz="EST") , "%w%H"))))
#Weather forcast?


library(zoo)
library(reshape2)
library(ggplot2)
library(TTR)
library(forecast)
require(xts)

dat2 <- dcast(dat, DateTime ~ variable)
dat2$DateTime <- as.POSIXct(as.character(dat2$DateTime),tz="EST")
z <- zoo(dat2[,2:ncol(dat2)],dat2$DateTime,frequency = 96)
plot(z)

names(z)
v <- ts(z[,5], start=dat2$DateTime[1], frequency = 96)
plot(decompose(v))
acf(v,lag.max = 100)

dec <- decompose(v)
plot(dec$figure, t="l")
seasonplot(v,7*24*4,year.labels=TRUE)
lag.plot(v,lags=9)


#Average for the day...
agg_dat2 <-  dat %>%
  mutate(day=weekdays(as.POSIXct(DateTime, tz="EST")),time=format(as.POSIXct(DateTime, tz="EST"), "%H"),dt=format(as.POSIXct(DateTime,tz="EST") , "%a %H:00"),dt2=format(as.POSIXct(DateTime,tz="EST") , "%w-%H"))  %>%
  group_by(dt2, dt, variable) %>%
  summarise(mean=mean(value),min=min(value),max=max(value))

agg_dat2 <- dcast(agg_dat2, dt ~ variable)
plot(decompose(ts(agg_dat2[,2],start=dat2$DateTime[1],frequency = 30*24)))



time_index <- seq(from = min(dat2$DateTime),  to = max(dat2$DateTime), by = "15 min")
eventdata <- xts(dat2[,2], order.by = dat2$DateTime, frequency = "15 min")
plot(decompose(eventdata))

ts(dat2[,4], frequency="15 min")
