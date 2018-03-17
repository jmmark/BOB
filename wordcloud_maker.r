# make a word cloud using GBV lyrics!

libraries <- c("tm", "SnowballC", "wordcloud", "RColorBrewer")

lapply(libraries, library, character.only = TRUE)

lyrics_file <- "all_gbv_lyrics.txt"

lyrics <- readLines(lyrics_file)

gbv_corpus <- Corpus(VectorSource(lyrics))

gbv_corpus <- tm_map(gbv_corpus, content_transformer(tolower))

gbv_corpus <- tm_map(gbv_corpus, removePunctuation)
gbv_corpus <- tm_map(gbv_corpus, stripWhitespace)
gbv_corpus <- tm_map(gbv_corpus, removeWords, stopwords("english"))

gbv_dtm <- TermDocumentMatrix(gbv_corpus)
intermediate <- as.matrix(gbv_dtm)
intermediate <- sort(rowSums(intermediate), decreasing = TRUE)

gbv_dtdf <- data.frame(word = names(intermediate), frequency = intermediate)

jpeg("gbv_cloud.jpg")
  wordcloud(gbv_dtdf$word, gbv_dtdf$frequency, max.words = 500, 
            random.order = FALSE, colors = brewer.pal(8, "Spectral"), 
            rot.per = 0.2)
dev.off()