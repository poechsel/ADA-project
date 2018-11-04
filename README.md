Understanding Virality
===

_How does information and influence propagate on social networks?_

## Abstract

When looking at trending topics, users, tweets or videos on YouTube and Twitter, it is not always clear what made them popular. With this project, we want to understand the mechanisms that govern virality and popularity on these platforms. As this is a wide subject, we narrowed down our search to a few questions:
- How do hashtags spread on Twitter? What happens between the time hashtags are first used and the time they reach Trending Topics?
- What are key ingredients that make a video or a tweet spread quickly?
- Can we find metrics which discriminate "regular" Twitter users from celebrities or corporate accounts?
- Are there patterns that govern subscriber growth on YouTube? Does it always start with a few viral videos, or can it be gained steadily?

By doing this, we hope to not only gain a better understanding of how social media works, but also how we could help important issues gain traction or fight against users who use those mechanisms unfairly.


## Research questions

- How to efficiently traverse large social graphs like that of Twitter?
- How to find a relevant measure of influence on a social graph?
- How to process the large number of tweets that use a given hashtag?
- How to intuitively visualize the spreading of a video or a tweet on the social graph?
- How to cluster social media users based on their patterns of activity?

## Datasets

We had several datasets in mind, each providing a part of the answers we're after:
- The _Twitter_ dataset from the official list, which contains 1% of the tweets from the year 2017 in plain text format. Even though it does not contain every tweet, it will allow us to obtain a general overview of the behavior behind spread of hashtags without using too much processing power.
- Data from the _Twitter Standard Search API_ (https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html), which we would use to export all the tweets with a given hashtag within a specific period of time. This would be like a scalper, allowing us to extract more insights about a precise phenomena.
- Data from _SocialBlade_ (https://socialblade.com), which would give us the evolution of the number of followers, subscribers and video views of Twitter and YouTube accounts over time. Although SocialBlade does not officially provide a complete dataset or an API to export their data, there are several unofficial scrapers available on GitHub, e.g. https://github.com/vinceh121/socialblade-api.

## A list of internal milestones up until project milestone 2
Add here a sketch of your planning for the next project milestone.

## Questions for TAa
Add here some questions you have for us, in general or project-specific.
