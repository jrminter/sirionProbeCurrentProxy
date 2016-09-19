# plot-Cu-voltage-series

rm(list=ls())
library(ggplot2)
library(grid)
library(gridExtra)

gitDir <- Sys.getenv("GIT_HOME")
str.wd <- paste0(gitDir, '/sirionProbeCurrentProxy/R/')
setwd(str.wd)

fi <-'../dat/csv/Cu-10000-Traj.csv'

df <- read.csv(fi, header=TRUE, as.is=TRUE)
print(head(df))


si.int.lm = lm(Cu.Int.mu~e0.kV, df)
si.int.loess = loess(Cu.Int.mu~e0.kV, df)

e0.kV <- seq(from=5.0, to=30.0, by=0.5)
df2 <- data.frame(e0.kV=e0.kV)
df3 <- data.frame(e0.kV=e0.kV)

df2$Cu.Int.mu = round(predict(si.int.lm, newdata = df2), 2)
df3$Cu.Int.mu = round(predict(si.int.loess, span=0.75, newdata = df3), 2)



siInt <- ggplot(df, aes(x=e0.kV, y=Cu.Int.mu)) + 
  geom_errorbar(aes(ymin=Cu.Int.mu - 1.96*Cu.Int.unc,
                    ymax=Cu.Int.mu + 1.96*Cu.Int.unc), width=.1) +
  # geom_line(color='blue') +
  geom_point(color='black') + xlab("e0 [kV]") +
  ylab("Cu-L intensity [cts/nA-sec]") +
  # geom_line(color='red', size=1.25, aes(color="red"), data=df2) +
  # annotate("text", label = 'lm',
  #          x = 25, y = 110000.,
  #          size = 5, colour = "red") +
  geom_line(color='blue', size=1.25, aes(color="blue"), data=df3) +
  annotate("text", label = 'LOESS',
           x = 23, y = 15000.,
           size = 5, colour = "blue") +
  ggtitle("Monte Carlo model of Cu-L peak intensity") +
  theme(axis.text=element_text(size=12),
        axis.title=element_text(size=14))# or ,face="bold"))
 # +
#annotate("text", x = 0, y = 1750, label = "core") +
#annotate("text", x = 3.75, y = 1750, label = "shell")

print(siInt)


fi <- '../pdf/Cu-voltage-series-plt-10000.pdf'
ggsave(siInt, file=fi, width=9.0, height=6.0, units="in", dpi=300)

fi <- '../png/Cu-voltage-series-plt-10000.png'
ggsave(siInt, file=fi, width=9.0, height=6.0, units="in", dpi=300)

fi <- '../dat/csv/cu-loess-pred-10000.csv'
write.csv(df3, file=fi, row.names=FALSE)
