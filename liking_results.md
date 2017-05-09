### Data
The data analyzed was IRC logs covering Feb 2014 to May 2017 (3.25 years).
I suppose the data best fits under close/stranger. My assumption is that I've grown closer to this other person in the last 3 years.

The data was formatted in html over multiple files. Each file represented a single day of conversation. Each had a header, a bunch of lines (see example below), and a footer.

Example line(s):
<font color="#16569E"><font size="2">(7:42:11 PM)</font> <b>Rob:</b></font> :(<br/>
<font color="#16569E"><font size="2">(7:42:15 PM)</font> <b>Rob:</b></font> im just picking a random value<br/>
<font color="#A82F2F"><font size="2">(7:42:16 PM)</font> <b>Patrick:</b></font> why<br/>
<font color="#16569E"><font size="2">(7:42:20 PM)</font> <b>Rob:</b></font> out of possiblePlaces<br/>
<font color="#A82F2F"><font size="2">(7:42:28 PM)</font> <b>Patrick:</b></font> whats ConsonantFeaturesContour<br/>
<font color="#16569E"><font size="2">(7:42:32 PM)</font> <b>Rob:</b></font> uh<br/>
<font color="#16569E"><font size="2">(7:42:34 PM)</font> <b>Rob:</b></font> a type<br/>
<font color="#16569E"><font size="2">(7:42:40 PM)</font> <b>Rob:</b></font> :O<br/>
<font color="#A82F2F"><font size="2">(7:42:50 PM)</font> <b>Patrick:</b></font> I dont get it<br/>
<font color="#16569E"><font size="2">(7:42:50 PM)</font> <b>Rob:</b></font> iuno why it expects that<br/>
<font color="#A82F2F"><font size="2">(7:42:57 PM)</font> <b>Patrick:</b></font> why isn&apos;t it<br/>
<font color="#A82F2F"><font size="2">(7:43:01 PM)</font> <b>Patrick:</b></font> RVar ConsonantFeaturesContour<br/>
<font color="#A82F2F"><font size="2">(7:43:02 PM)</font> <b>Patrick:</b></font> or something<br/>
<font color="#16569E"><font size="2">(7:43:09 PM)</font> <b>Rob:</b></font> uh<br/>
<font color="#16569E"><font size="2">(7:43:35 PM)</font> <b>Rob:</b></font> mebe<br/>
<font color="#A82F2F"><font size="2">(7:43:54 PM)</font> <b>Patrick:</b></font> also whats choice<br/>
<font color="#16569E"><font size="2">(7:44:02 PM)</font> <b>Rob:</b></font> picks random<br/>
<font color="#16569E"><font size="2">(7:44:04 PM)</font> <b>Rob:</b></font> thing<br/>
<font color="#16569E"><font size="2">(7:44:06 PM)</font> <b>Rob:</b></font> from list<br/>
<font color="#16569E"><font size="2">(7:44:20 PM)</font> <b>Rob:</b></font> hm<br/>
<font color="#16569E"><font size="2">(7:44:21 PM)</font> <b>Rob:</b></font> RvAr<br/>
<font color="#16569E"><font size="2">(7:44:26 PM)</font> <b>Rob:</b></font> fixed it<br/>
<font color="#16569E"><font size="2">(7:44:28 PM)</font> <b>Rob:</b></font> good work<br/>
<font color="#16569E"><font size="2">(7:44:29 PM)</font> <b>Rob:</b></font> :O<br/>
<font color="#A82F2F"><font size="2">(7:44:42 PM)</font> <b>Patrick:</b></font> lel<br/>


The data set contains 224,728 lines of messages.

### Pre-processing
Regular expressions were used to extract the speaker, the time, and the message. The date was extracted from the filename. Consecutive messages by the same speaker were concatenated (with a space in between) and the earliest time/date was used to represent that "turn". The 224,728 lines were concatenated down to 80,476 "turns".

The turns were tokenized and then sent to the feature extractor.

### Feature
I look at the average word vector for each turn in the conversation. The pre-trained word vector model used was trained with the Google News corpus.

The word vectors were each 300-dimensional.

### Similarity measure
I briefly considered using pearson correlation as the similarity measurement between consecutive turns before deciding on cosine similarity.

Cosine similarity represents approximately how well the conversation flows as well as some type of local conformity. For instance, if there is a digression in the conversation then that would show up as a small, possibly negative, value. Staying on topics would show up as a larger (and positive) value. And repeating the exact same message back shows up as +1.0.

There were some problems with the average word vector not being calculated because of short, out-of-vocab messages. I kept these as zero vectors and filtered them out of the results (they showed up as NaN when finding cosine similarity).

## Results
Originally I planned to take the average similarity for the first and latest year. Instead what I did was simple linear regression on all of the data to find a line of best fit.

1.24251082752e-10 * x + 0.405577802487

x is seconds from 1 Jan 2014

This is a positively sloped line. Predicted cosine similarity for Feb 2014 is 0.4059 and 0.4187 for May 2017. So the conclusion I draw from that is that we talk about more similar things today than they did 3 years ago. Conformity is shown to be a consequence of attraction (Byrne 1973), therefore we have grown closer in the past 3 years.

A plot of the cosine similarity between consecutive turns over time, as well as the line's equation can be seen in Figure 1.

### Future work
I'm pretty sure I have IRC logs that go back to 2012 on a hard drive at my parent's house. An analysis of that on top of the data analyzed here would be interesting. More data is always good.

The problem with out-of-vocab messages mentioned above could probably be lessened with a better tokenizer. Most of those out-of-vocab messages are probably urls. So what I could do is replace all urls with a <URL> tag, and then use a known URL that has a word embedding representation for those URL tags. I feel that would be better than just dropping them, like it does now.

## Works cited
Byrne, D., Griffitt W. 1973. Interpersonal Attraction.
