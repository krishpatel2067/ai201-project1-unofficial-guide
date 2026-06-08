# Sample 1

### Retrieval

### Semantic Search Only

```
Query: "Does professor Berenjian offer extra credit?"
Top 5 chunks by ascending cosine distance:

#1  distance=0.4592  source=samaneh-berenjian.txt  type=review  id=samaneh-berenjian-review-28
    Course: CS656
    Professor Berenjian is very respectful. She is caring and very supportive.
    Tags: Caring, Respected

#2  distance=0.4839  source=samaneh-berenjian.txt  type=review  id=samaneh-berenjian-review-62
    Course: CS656
    Professor Berenjian is a very good teacher who genuinely cares about her students' learning. Her ability to simplify complex concepts and make them understandable is great.
    Tags: Amazing lectures

#3  distance=0.4874  source=samaneh-berenjian.txt  type=review  id=samaneh-berenjian-review-8
    Course: CS356
    Everyone loves to say things like "this prof just read off the slides" which is terribly unproductive criticism. Berenjian is simply not good at teaching She struggles immensely to explain the concepts that she clearly understands. There should be a minimum communication skills requirement for anyone who wants to be a teacher or professor.
    Tags: Beware of pop quizzes

#4  distance=0.4963  source=samaneh-berenjian.txt  type=review  id=samaneh-berenjian-review-56
    Course: CS656
    Professor Berenjian is a great teacher! She really knows her stuff and explains things in a way that's easy to understand. She's always willing to help and genuinely cares about her students. Definitely recommend taking her class!
```

### Hybrid Search with BM25

```
Query: "Does professor Berenjian offer extra credit?"
```

```
Answer: "I can't find the answer to that question."
```

#### Hybrid On

```
Retrieved 5 chunks. Answer drawn from samaneh-berenjian.txt (5 chunk(s) after single-professor filtering).

#1 · distance 0.4592 · rrf 0.0312 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-28 ✅ used

Course: CS656
Professor Berenjian is very respectful. She is caring and very supportive.
Tags: Caring, Respected
#2 · distance 0.4839 · rrf 0.0303 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-62 ✅ used

Course: CS656
Professor Berenjian is a very good teacher who genuinely cares about her students' learning. Her ability to simplify complex concepts and make them understandable is great.
Tags: Amazing lectures
#3 · distance 0.4963 · rrf 0.0292 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-56 ✅ used

Course: CS656
Professor Berenjian is a great teacher! She really knows her stuff and explains things in a way that's easy to understand. She's always willing to help and genuinely cares about her students. Definitely recommend taking her class!
#4 · distance 0.5271 · rrf 0.0289 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-36 ✅ used

Course: CS656
Professor Berenjian is a fantastic teacher for the Networking course. She explains things clearly, keeps the class engaging and is great at managing the classroom.
Tags: Participation matters, Amazing lectures, Lecture heavy
#5 · distance 0.4874 · rrf 0.0286 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-8 ✅ used

Course: CS356
Everyone loves to say things like "this prof just read off the slides" which is terribly unproductive criticism. Berenjian is simply not good at teaching She struggles immensely to explain the concepts that she clearly understands. There should be a minimum communication skills requirement for anyone who wants to be a teacher or professor.
Tags: Beware of pop quizzes
```

#### Hybrid Off

```
Retrieved 5 chunks. Answer drawn from samaneh-berenjian.txt (4 chunk(s) after single-professor filtering).

#1 · distance 0.4592 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-28 ✅ used

Course: CS656
Professor Berenjian is very respectful. She is caring and very supportive.
Tags: Caring, Respected
#2 · distance 0.4839 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-62 ✅ used

Course: CS656
Professor Berenjian is a very good teacher who genuinely cares about her students' learning. Her ability to simplify complex concepts and make them understandable is great.
Tags: Amazing lectures
#3 · distance 0.4874 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-8 ✅ used

Course: CS356
Everyone loves to say things like "this prof just read off the slides" which is terribly unproductive criticism. Berenjian is simply not good at teaching She struggles immensely to explain the concepts that she clearly understands. There should be a minimum communication skills requirement for anyone who wants to be a teacher or professor.
Tags: Beware of pop quizzes
#4 · distance 0.4963 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-56 ✅ used

Course: CS656
Professor Berenjian is a great teacher! She really knows her stuff and explains things in a way that's easy to understand. She's always willing to help and genuinely cares about her students. Definitely recommend taking her class!
#5 · distance 0.5119 · source abdul-rahman-itani.txt · review · id abdul-rahman-itani-review-113

Course: CS288
This professor doesn't believe in partial credit, his job is to fail you (described by his TAs). On top of that, he is very degrading while talking in his lectures, completely demotivating you of ever getting a good grade in his difficult class. 100% would not recommend, do not listen to anyone giving him a 5 star rating. I repeat, STAY AWAY!!
Tags: Lots of homework, Lecture heavy, Tough grader
```

## Generation

### Without Forbidding Citation upon Refusal in System Prompt

```

Query: "Does Professor Berenjian offer extra credit?"

Answer:
I can't find the answer to that question. [samaneh-berenjian.txt]

(Debug: retrieved candidates span 2 file(s): abdul-rahman-itani.txt, samaneh-berenjian.txt; the answer must cite exactly one.)

```

### Forbidding Citation upon Refusal in System Prompt

```

Query: 'Does Professor Berenjian offer extra credit?'

Answer:
I can't find the answer to that question.

(Debug: retrieved 5 chunks spanning 2 file(s): abdul-rahman-itani.txt, samaneh-berenjian.txt.
Answer drawn from samaneh-berenjian.txt (4 chunk(s)).)

```

```

```
