# Competition against the time

The talk of the town at office all around the world these days is this: 

> Is AI in software development making you faster? By how much?

Some report 8x improvements, others say that our challenge is now testing daily the work of a 1000 engineers when we had 10 in the past. The expectations of more and faster (while maintaining quality) are everywhere. The reality in a lot of projects at large is still that while AI makes some parts faster, the things around that part make us deliver just the same as before, just with different tools. 

It feels like there is a competition on time. Faster, more (still maintaining quality). Winning at the wrong game is a loss for us all. The speed game without considerations of long-term sustainability of the codebase and the people who collaboratively tend it is the wrong game. 

We know this from metrics: anything we give as metric becomes a target. And a group I tried teaching testing taught me exactly that. 

## Capture-the-bugs I know of

While a test manager, I remember setting a metric for bugs, right at the start of the project. I told the other managers a number of bugs we would have to log, all relevant and unique, before we would be done with the project. The number felt ridiculous in size, even for me, and the point was not to make that number. It was to assess what would learning while testing look like so that we could track out progress towards that number, and correctness of that number. 

Learning how to test (explore) became essential. Not all bugs are equal. Some break the project schedule and make everyone sad. Some break what the users expect to gain from having the system built. But if you can't find them with a wide selection of perspectives, you can't make choices of what are relevant. You have to see it to classifify it. At least you have to see the class of it, to classify all the rest like that into the same rule of (in)action. 

Seeing bugs is essential. Teaching seeing bugs is hard. So we, myself and Ru Cindrea, we built [Capture the Bugs](https://exploratory-testing-academy.github.io/capture-the-bugs/) for self-directed learning with feedback. 

The first application we framed into it is a tiny one. It's essentially the "How would you test a text field" exercise with domain around it that forces you to be more specific about, well, how indeed would you test this text field. We listed bugs we know of, and have moved from a list of 38 bugs to 72 bugs as of today. So when you test it, you have a bar you are striving for. 

With this application, the infamous idea of getting lucky just being around at the right time won't suffice. Action is needed. 

![Clocks and time](<image14.png>)

## No, it was not supposed to be a competition!

Even when we know the number, or fake the number, it's not supposed to be a competition, but a point of reflection. If you invest 30 minutes, and do your best work, do you find the *important* ones, or are you going to be overwhelmed by the sheer amount of things you are observing? 

I did not set the space right to avoid sense of competion, when I had 21 people joining a training session I was facilitating, and testing for 30 minutes. There was competition against the time - find all in the time, using AI! There was competition against the exercise creator who held all the secrets and dangled them as opportunities for shortcuts in the Capture the Bugs application's hints section. And there was competition against the other people in the same training, from the same organization, my most important peers! 

What we learned is this: 

**Developers clearly can test**. They found, across all participants, all but four problems out of the 72. The group that found the most found 79% of the problems, writing 85 bugs reports, perhaps finding some that weren't on the list or not matched as per the automatic matching functionality of how people report and how we report within the application. 

**Competition brings out things**. 48% of people allowed the app to score their reports. That means more than half didn't. Out of the 52% that did not see their score, their collective score replayed from logs is 60%. Remember, the best pair got 79%. The groups who asked for scoring got 42% on average. The shared result of those who stopped before finish line outperforms the average of those who finished. 

I can only guess what the numbers tell me. I am guessing that some people did the work, but opted out from the scores. I know that some people opted out of the whole competition. 

With all of these, the only way to lose the *right game* is to not contribute to the overall by giving up before you even started. The game we played is one of learning. Learning requires effort. 

## Back to AI

When we feel pressured on the schedule, like with the time-boxed exercise and a number target with out colleagues watching, we are unlikely to do our best work as a group. We frame the game to individual results, when the group results matter. 

Watching the exercise unfold, I remind us all that we need to choose the framing of collaboration. I wrote down to start our next learning session from an insight of mine: 

> You clearly can test. If you don't take time for it, *that* is the problem you should solve.

Don't let AI and personal achievements make you lose the right game (your work purpose) just so that your personal score looks like you are winning. 

The team does better when we sum up everyone's contributions. In the exercise, the best pair (79%) and the whole team (94%) is relevant. 

Testing is too important to be left just for testers. But also too important to be left without them. Less bugs - higher experience of quality while use - makes finding the relevant ones significantly easier. Take the time you need. You can. 

