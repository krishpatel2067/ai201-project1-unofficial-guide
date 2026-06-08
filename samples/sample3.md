# Sample 3

## Retrieval

### Semantic Search Only

```
Query: "Is it a good idea to skip Professor Naik's classes?"
Top 5 chunks by ascending cosine distance:

#1  distance=0.2763  source=kamlesh-naik.txt  type=review  id=kamlesh-naik-review-76
    Course: CS332
    Professor Naik is caring and straightforward. The class requires you to put in effort, which means not an easy A. However, he is very clear in terms of what will be asked in the exams. If you attend his classes and do the homework then things will be easier. Do not wait for the last moment to study for exams, he does tell you that.
    Tags: Skip class? You won't pass., Clear grading criteria, Caring

#2  distance=0.3787  source=kamlesh-naik.txt  type=review  id=kamlesh-naik-review-48
    Course: CS332
    Prof. Naik explains most concepts well, but sometimes he goes a bit too fast. He's a tough grader, which I'd say most people who have taken a course with him can agree with. I will say though that he is very transparent about what will appear on your exams, so when it's time to take them you shouldn't be shocked. Also, don't skip class, trust me
    Tags: Tough grader, Lecture heavy, Test heavy

#3  distance=0.3834  source=kamlesh-naik.txt  type=review  id=kamlesh-naik-review-72
    Course: CS630
    Prof. Naik's class has always been interesting. He has a fascinating personality and an excellent teaching style along with his ability to set goals. Prof. Naik is always elaborative, bold and confident during the delivery of lectures which makes the students understand the concepts well.
    Tags: Accessible outside class, Clear grading criteria, Amazing lectures

#4  distance=0.3902  source=abdul-rahman-itani.txt  type=review  id=abdul-rahman-itani-review-124
    Course: CS288
    Itani is the hardest professor I have had at this school. At time he comes off as narcissisti and full of himself, and this is his biggest drawback. If you look past this, you get one of the best professors the school has to offer that genuinely, honestly cares about you learning. And he will do his best to teach you what you need to know.
    Tags: Skip class? You won't pass., Graded by few things, Lecture heavy

#5  distance=0.4003  source=kamlesh-naik.txt  type=review  id=kamlesh-naik-review-22
    Course: CS332
    Prof. Naik is an amazing teacher. I recommend taking him over any other prof for 332. I was doing really well in his class and his class was the only one I looked forward to. I really have great respect for him but it deeply saddens me that because of negative comments in the past, he is much more strict & difficult with exams (final was a pain).
    Tags: Tough grader, Amazing lectures, Lecture heavy
```

## Generation

### Without Explicitly Disambiguating Tags from Review Body in System Prompt

```
Query: "Is it a good idea to skip Professor Naik's classes?"

Answer:
It's not a good idea to skip Professor Naik's classes, as multiple students have warned that skipping class will lead to poor performance, with one student stating "Skip class? You won't pass" and another advising "don't skip class, trust me" [kamlesh-naik.txt]

(Debug: retrieved candidates span 2 file(s): abdul-rahman-itani.txt, kamlesh-naik.txt; the answer must cite exactly one.)
```

### Explicitly Disambiguating Tags from Review Body in System Prompt

```
Query: "Is it a good idea to skip Professor Naik's classes?"

Answer:
It's not a good idea to skip Professor Naik's classes, as multiple students have advised against it, warning that skipping class will make it harder to pass. According to the students, attending classes and doing the homework makes things easier, and Professor Naik is transparent about what will be on the exams. [kamlesh-naik.txt]

(Debug: retrieved 5 chunks spanning 2 file(s): abdul-rahman-itani.txt, kamlesh-naik.txt.
 Answer drawn from kamlesh-naik.txt (4 chunk(s)).)
```
