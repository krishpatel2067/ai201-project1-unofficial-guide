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
