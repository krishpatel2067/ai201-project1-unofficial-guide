# Semantic-Only vs Hybrid Search Comparison

Control:

- Conversational memory: **Disabled**
- Chunking strategy: **Structured**
- Filters applied: **None**

Note: the `rrf` is mentioned in hybrid retrieval ouput.

## 1

### Query

```
Does Professor Berenjian use the Kurose textbook?
```

### Semantic-Only Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from samaneh-berenjian.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.3979 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-6 ✅ used


Course: CS656
I took CS656 with Professor Berenjian. The class was well-structured and she really knows the material. However, the course relies heavily on the Kurose and Ross textbook, and sometimes it feels like the lectures just follow the book too closely. Still, I think the class is worth taking, especially if you stay on top of the readings.
Tags: Amazing lectures, Respected
#2 · distance 0.4674 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-56 ✅ used


Course: CS656
Professor Berenjian is a great teacher! She really knows her stuff and explains things in a way that's easy to understand. She's always willing to help and genuinely cares about her students. Definitely recommend taking her class!
#3 · distance 0.4796 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-62 ✅ used


Course: CS656
Professor Berenjian is a very good teacher who genuinely cares about her students' learning. Her ability to simplify complex concepts and make them understandable is great.
Tags: Amazing lectures
#4 · distance 0.5087 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-9 ✅ used


Course: CS656
Professor uses only Jim Kurose videos/slides, no original content. Emotionally invested but gives no exam guidance beyond 'study interactive questions.' No tutor available, must ask her/TA directly. Has an attitude. Won't take again, will voice concerns to school.
Tags: Tough grader, Group projects, Lots of homework
#5 · distance 0.5219 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-28 ✅ used


Course: CS656
Professor Berenjian is very respectful. She is caring and very supportive.
Tags: Caring, Respected
#6 · distance 0.5253 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-8 📄 same file


Course: CS356
Everyone loves to say things like "this prof just read off the slides" which is terribly unproductive criticism. Berenjian is simply not good at teaching She struggles immensely to explain the concepts that she clearly understands. There should be a minimum communication skills requirement for anyone who wants to be a teacher or professor.
Tags: Beware of pop quizzes
#7 · distance 0.5395 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-35 📄 same file


Course: CS356
Professor Berenjian is an excellent teacher who explains concepts clearly and keeps the class engaging. She's very organized and always makes sure students are on track. Even though the course was challenging, I learned a lot and appreciated her support throughout. Highly recommend her for CS356!
Tags: Amazing lectures, Respected, Lecture heavy
#8 · distance 0.5553 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-36 📄 same file


Course: CS656
Professor Berenjian is a fantastic teacher for the Networking course. She explains things clearly, keeps the class engaging and is great at managing the classroom.
Tags: Participation matters, Amazing lectures, Lecture heavy
#9 · distance 0.5743 · source kamlesh-naik.txt · review · id kamlesh-naik-review-60


Course: CS332
Professor Kamli is truly a standup comedian. I felt like his classes were more of crowd work than a lecture. He knows very less about the subject. Assignments are quite easy but the final exam is totally different. He keeps on stalking "people" and invites "people" to visit his office.
Tags: Lecture heavy
#10 · distance 0.5882 · source marvin-nakayama.txt · review · id marvin-nakayama-review-24


Course: CS341
Professor Nakayama is so far my best professor in NJIT. He really goes out of his way to make things as clear as possible. His videos are amazing. He really articulates very well and finds a way to explain abstract things. If I could take him again I wouldn't hesitate. I wish all my profs are like him
```

</details>

### Semantic-Only Generation

```
Professor Berenjian's course CS656 relies heavily on the Kurose and Ross textbook, and in some cases, she uses only Jim Kurose videos/slides. [samaneh-berenjian.txt]
```

### Hybrid Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from samaneh-berenjian.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.3979 · rrf 0.0333 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-6 ✅ used


Course: CS656
I took CS656 with Professor Berenjian. The class was well-structured and she really knows the material. However, the course relies heavily on the Kurose and Ross textbook, and sometimes it feels like the lectures just follow the book too closely. Still, I think the class is worth taking, especially if you stay on top of the readings.
Tags: Amazing lectures, Respected
#2 · distance 0.5553 · rrf 0.0311 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-36 ✅ used


Course: CS656
Professor Berenjian is a fantastic teacher for the Networking course. She explains things clearly, keeps the class engaging and is great at managing the classroom.
Tags: Participation matters, Amazing lectures, Lecture heavy
#3 · distance 0.5219 · rrf 0.0306 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-28 ✅ used


Course: CS656
Professor Berenjian is very respectful. She is caring and very supportive.
Tags: Caring, Respected
#4 · distance 0.5395 · rrf 0.0294 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-35 ✅ used


Course: CS356
Professor Berenjian is an excellent teacher who explains concepts clearly and keeps the class engaging. She's very organized and always makes sure students are on track. Even though the course was challenging, I learned a lot and appreciated her support throughout. Highly recommend her for CS356!
Tags: Amazing lectures, Respected, Lecture heavy
#5 · distance 0.5253 · rrf 0.0293 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-8 ✅ used


Course: CS356
Everyone loves to say things like "this prof just read off the slides" which is terribly unproductive criticism. Berenjian is simply not good at teaching She struggles immensely to explain the concepts that she clearly understands. There should be a minimum communication skills requirement for anyone who wants to be a teacher or professor.
Tags: Beware of pop quizzes
#6 · distance 0.6247 · rrf 0.0292 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-88 📄 same file


Course: CS656
Everything was from UMass and Kurose's Networking textbook. This professor never gave any clear guidance and was hard to get in contact with. When people in the class complained she said it was a "self-guided course". Spent 4000$+ to use free lectures and text from UMass.What a joke. I would love to be a NJIT professor and get paid to do nothing.
#7 · distance 0.4796 · rrf 0.0291 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-62 📄 same file


Course: CS656
Professor Berenjian is a very good teacher who genuinely cares about her students' learning. Her ability to simplify complex concepts and make them understandable is great.
Tags: Amazing lectures
#8 · distance 0.5893 · rrf 0.0288 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-7 📄 same file


Course: CS356
Guaranteed a quiz the class after you finish a chapter from the book/slides. As for difficulty: they're piss easy, literally look up the online end-of-chapter problems on the Kurose website and they're LITERALLY the same with the random generated options. Midterm and final are the same thing: 2 questions max from slides. Focus on group work 200%.
Tags: Group projects, Graded by few things
#9 · distance 0.6218 · rrf 0.0287 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-20 📄 same file


Course: CS696
I'm currently taking the CS696 online class with Professor Berenjian. I enjoy the course content—it's both engaging and informative. She's also thoughtful and supportive. I do feel the number of office hours is a bit limited though.
Tags: Group projects, Caring, Lecture heavy
#10 · distance 0.4674 · rrf 0.0267 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-56 📄 same file


Course: CS656
Professor Berenjian is a great teacher! She really knows her stuff and explains things in a way that's easy to understand. She's always willing to help and genuinely cares about her students. Definitely recommend taking her class!
```

</details>

### Hybrid Generation

```
Professor Berenjian uses the Kurose textbook in her CS656 course, as the course relies heavily on the Kurose and Ross textbook. [samaneh-berenjian.txt]
```

### Conclusion

**Hybrid** worked slightly better. The results were similar in generation, but during retireval, hybrid surfaced more `samaneh-berenjian.txt` reviews than semantic-only. For both, most if not all of the chunks are from `samaneh-berenjian.txt`, matching the query's intended professor. Furthermore, both surface chunks that mention Kurose's textbook.

## 2

### Query

```
What do students think about Professor Arafeh's use of Vocareum?
```

### Semantic-Only Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from bassel-arafeh.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.4510 · source bassel-arafeh.txt · review · id bassel-arafeh-review-45 ✅ used


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A+ in this course easily.
#2 · distance 0.4688 · source bassel-arafeh.txt · review · id bassel-arafeh-review-115 ✅ used


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A in this course easily.
Tags: Respected, Inspirational, Amazing lectures
#3 · distance 0.4764 · source bassel-arafeh.txt · review · id bassel-arafeh-review-74 ✅ used


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A in this course easily.
Tags: Amazing lectures, Respected
#4 · distance 0.5043 · source bassel-arafeh.txt · review · id bassel-arafeh-review-72 ✅ used


Course: CS280
Professor Bassel Arafeh is an amazing educator and communicator. He has a true passion for teaching and a talent for explaining complex concepts in a way that is easy to understand. His dedication to his students is remarkable, and he always goes above and beyond to ensure that they have the knowledge and skills they need to succeed.
Tags: Amazing lectures, Inspirational, Caring
#5 · distance 0.5170 · source bassel-arafeh.txt · review · id bassel-arafeh-review-8 ✅ used


Course: CS280
When I first looked at a snippet of code I thought "Oh it's just a piece of code" but when I stepped into my first lecture with Professor Arafeh, I gained severe Enlightenment. Every word of his speech eminates some sort of "aura" as they say nowadays. Arafeh has truly made me a better coder and has shown what it's like to be an exceptional teacher
Tags: Amazing lectures, Inspirational, Hilarious
#6 · distance 0.5388 · source bassel-arafeh.txt · review · id bassel-arafeh-review-85 📄 same file


Course: CS280
Arafeh is undoubtedly the best professor at NJIT. His lectures are some of the finest in the nation. He guides us all to perfection. Arafeh is very accessable and knowledgeable and personal. I am now a math major thanks to his wonderful insight. Please, if you have the chance, take Arafeh's class. It will change your perspective of life.
Tags: Amazing lectures, Inspirational, Respected
#7 · distance 0.5489 · source kamlesh-naik.txt · review · id kamlesh-naik-review-47


Course: CS683
The professor is always accessible and has really improved the subject. The subject in itself does not feel much helpful from an industry point of view. However, Kudos to the professor for making the class more interactive. He is really passionate for his subjects and students. Will take the professor again not the subject.
Tags: Tough grader, Participation matters, Accessible outside class
#8 · distance 0.5498 · source james-calvin.txt · review · id james-calvin-review-18


Course: CIS114
If you learn from examples and in-depth explanations, don't take this professor. There is a not many resources that he provides you, which includes a 200+ page powerpoint that vaguely relates to the textbook. Unlike other courses, you will not get credit for homework unless if it is 100% correct according to the autograding system on Vocareum.
#9 · distance 0.5793 · source bassel-arafeh.txt · review · id bassel-arafeh-review-5 📄 same file


Course: CS280
great sense of humor, vocareum is in my nightmares now
#10 · distance 0.5971 · source bassel-arafeh.txt · review · id bassel-arafeh-review-7 📄 same file


Course: CS280
His lectures are very monotonous and wordy. I sat in the front and tried to take notes and pay attention, but it's not a very good use of your time. Students usually just seem to struggle to study everything on their own. If there is ever another professor for cs280, take them instead. The autograded assignments in Vocareum are also annoying.
```

</details>

### Semantic-Only Generation

```
I can't find the answer to that question.
```

### Hybrid Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from bassel-arafeh.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.5170 · rrf 0.0320 · source bassel-arafeh.txt · review · id bassel-arafeh-review-8 ✅ used


Course: CS280
When I first looked at a snippet of code I thought "Oh it's just a piece of code" but when I stepped into my first lecture with Professor Arafeh, I gained severe Enlightenment. Every word of his speech eminates some sort of "aura" as they say nowadays. Arafeh has truly made me a better coder and has shown what it's like to be an exceptional teacher
Tags: Amazing lectures, Inspirational, Hilarious
#2 · distance 0.4510 · rrf 0.0318 · source bassel-arafeh.txt · review · id bassel-arafeh-review-45 ✅ used


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A+ in this course easily.
#3 · distance 0.5388 · rrf 0.0315 · source bassel-arafeh.txt · review · id bassel-arafeh-review-85 ✅ used


Course: CS280
Arafeh is undoubtedly the best professor at NJIT. His lectures are some of the finest in the nation. He guides us all to perfection. Arafeh is very accessable and knowledgeable and personal. I am now a math major thanks to his wonderful insight. Please, if you have the chance, take Arafeh's class. It will change your perspective of life.
Tags: Amazing lectures, Inspirational, Respected
#4 · distance 0.5971 · rrf 0.0312 · source bassel-arafeh.txt · review · id bassel-arafeh-review-7 ✅ used


Course: CS280
His lectures are very monotonous and wordy. I sat in the front and tried to take notes and pay attention, but it's not a very good use of your time. Students usually just seem to struggle to study everything on their own. If there is ever another professor for cs280, take them instead. The autograded assignments in Vocareum are also annoying.
#5 · distance 0.4688 · rrf 0.0305 · source bassel-arafeh.txt · review · id bassel-arafeh-review-115 ✅ used


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A in this course easily.
Tags: Respected, Inspirational, Amazing lectures
#6 · distance 0.4764 · rrf 0.0304 · source bassel-arafeh.txt · review · id bassel-arafeh-review-74 📄 same file


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A in this course easily.
Tags: Amazing lectures, Respected
#7 · distance 0.6065 · rrf 0.0300 · source bassel-arafeh.txt · overall · id bassel-arafeh-overall 📄 same file


Overall quality rating: 1.8 out of 5, based on 119 ratings.
21% of students would take Bassel Arafeh again.
Average level of difficulty: 3.8 out of 5.
Rating distribution: 15 students rated Awesome (5 stars), 3 Great (4 stars), 7 Good (3 stars), 13 OK (2 stars), 81 Awful (1 star).
#8 · distance 0.5793 · rrf 0.0294 · source bassel-arafeh.txt · review · id bassel-arafeh-review-5 📄 same file


Course: CS280
great sense of humor, vocareum is in my nightmares now
#9 · distance 0.6093 · rrf 0.0269 · source bassel-arafeh.txt · review · id bassel-arafeh-review-77 📄 same file


Course: CS280
I'm not really sure what he does as a professor - he doesn't teach well so a total of 4 people attend his class, he doesn't grade because vocareum does that for you. Overall, be ready to self study for this course - work in groups on the PAs and just memorize the powerpoints for the exams. And no point to going to any of his classes.
#10 · distance 0.6343 · rrf 0.0262 · source abdul-rahman-itani.txt · review · id abdul-rahman-itani-review-42


Course: CS288
Itani is simply an excellent professor; he's cracked, he knows what he's talking about, and is passionate about teaching. His course material is challenging, but that is because he has high standards for his students. Students should not submit substandard work, and then expect an easy A. He will give you the grade you earned. (part 1/n)
Tags: Participation matters, Amazing lectures, Respected
```

</details>

### Hybrid Generation

```
Students have mixed opinions about Professor Arafeh's class, but only one review mentions Vocareum, stating that the autograded assignments in Vocareum are "annoying". [bassel-arafeh.txt]
```

### Conclusion

**Hybrid** definitely won. It clearly led to a useable answer whereas semantic-only led to no answer. It's easy to see why: semantic-only did retrieve chunks with student opinions on Vocareum, but they didn't make the cap-5 cutoff; on the other hand, hybrid bumped up one of those chunks so that it made the cutoff and got passed to the LLM.

## 3

### Query

```
Does Professor Nakayama make you memorize proofs?
```

### Semantic-Only Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from marvin-nakayama.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.4217 · source marvin-nakayama.txt · review · id marvin-nakayama-review-24 ✅ used


Course: CS341
Professor Nakayama is so far my best professor in NJIT. He really goes out of his way to make things as clear as possible. His videos are amazing. He really articulates very well and finds a way to explain abstract things. If I could take him again I wouldn't hesitate. I wish all my profs are like him
#2 · distance 0.4400 · source marvin-nakayama.txt · review · id marvin-nakayama-review-39 ✅ used


Course: CIS341
material can get confusing, but nakayama is a good (though boring) teacher... very helpful, and very fair... there was a major screw up with a test i took and he handled it very well
#3 · distance 0.4542 · source marvin-nakayama.txt · review · id marvin-nakayama-review-2 ✅ used


Course: CS341
Professor Nakayama is a good professor and he does a good job explaining topics. The material before the midterm is easy but after that it gets a lot harder. He posts his lecture videos, previous exams, and homework all on his website. It's a lot of material and if you want to do well don't slack off and stay updated with the lectures and videos.
Tags: Lecture heavy, Test heavy, Online savvy
#4 · distance 0.5147 · source marvin-nakayama.txt · review · id marvin-nakayama-review-20 ✅ used


Course: CS341
Nakayama is the best professor at NJIT. He explains each topic with a ton of detail and makes it easier to understand. The class material is somewhat difficult especially towards the end but If you watch the videos and review the old exams its not too bad. For the final, focus on the review sheet and go over the old projects.
#5 · distance 0.5517 · source marvin-nakayama.txt · review · id marvin-nakayama-review-9 ✅ used


Course: CS341
I would not recommend taking this professor. Expects you to spend hours a week outside of his already crammed lectures to watch his long videos to be able to do remotely decent. Unless you can memorize all of his slides exactly word for word, youll lose half if not all points on his exam questions as he expects you to regurgitate abstract proofs.
Tags: Test heavy, Lecture heavy, Tough grader
#6 · distance 0.5562 · source marvin-nakayama.txt · review · id marvin-nakayama-review-35 📄 same file


Course: CS341
Professor Nakayama is a great teacher, one of the best in the CS department. CS 341 is by no means an easy class but if you keep up with the material, do the projects (2 total), and do well on the exams (study his old exams!), you should expect to do really well. Class requires a LOT of memorization of long proofs. Overall fun class and great prof.
#7 · distance 0.5566 · source marvin-nakayama.txt · review · id marvin-nakayama-review-19 📄 same file


Course: CS341
The material for this class is difficult but Nakayama makes it easy because he explains it so well. Gives 3 projects and 2 exams for online and vice versa for in person. The projects aren't hard and can be done in 5 hours. For exams, study homeworks and past exams, then the practice final for the final. No excuse to get under a B. Best prof at NJIT
#8 · distance 0.5758 · source kamlesh-naik.txt · review · id kamlesh-naik-review-78


Course: CS332
Professor Naik is great! Seriously, if you show up, pay attention, and take notes, it's literally a free A. He explains exactly what you need to know for homework, quizzes, and exams.
#9 · distance 0.5906 · source kamlesh-naik.txt · review · id kamlesh-naik-review-23


Course: CS332
Naik is amazing at explaining concepts and I loved having him as a teacher. Problem is the midterm and final which basically make up 70% of your final grade have problems that are much much harder than anything done in class or on quizzes. But that given he does make it basically impossible to fail the class if you do the work and try you'll pass.
Tags: Tough grader, Amazing lectures, Test heavy
#10 · distance 0.5916 · source kamlesh-naik.txt · review · id kamlesh-naik-review-36


Course: CS332
Professor Naik is by far one of the best professors I've come across.Cares a lot for your success. You will lose points in your answer from the point where a mistake has been made solving the question. So be sure to double check your answers! Note: THE MATERIAL IS NOT HARD! Pay attention in his class and you will be amazed at how much you learn!
Tags: Tough grader, Participation matters, Amazing lectures
```

</details>

### Semantic-Only Generation

```
According to one review, Professor Nakayama expects students to memorize his slides, including abstract proofs, in order to do well on exams, while other reviews do not mention this requirement. It seems that there is a disagreement among students about the level of memorization required in his class. [marvin-nakayama.txt]
```

### Hybrid Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from marvin-nakayama.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.5517 · rrf 0.0315 · source marvin-nakayama.txt · review · id marvin-nakayama-review-9 ✅ used


Course: CS341
I would not recommend taking this professor. Expects you to spend hours a week outside of his already crammed lectures to watch his long videos to be able to do remotely decent. Unless you can memorize all of his slides exactly word for word, youll lose half if not all points on his exam questions as he expects you to regurgitate abstract proofs.
Tags: Test heavy, Lecture heavy, Tough grader
#2 · distance 0.5562 · rrf 0.0310 · source marvin-nakayama.txt · review · id marvin-nakayama-review-35 ✅ used


Course: CS341
Professor Nakayama is a great teacher, one of the best in the CS department. CS 341 is by no means an easy class but if you keep up with the material, do the projects (2 total), and do well on the exams (study his old exams!), you should expect to do really well. Class requires a LOT of memorization of long proofs. Overall fun class and great prof.
#3 · distance 0.4542 · rrf 0.0308 · source marvin-nakayama.txt · review · id marvin-nakayama-review-2 ✅ used


Course: CS341
Professor Nakayama is a good professor and he does a good job explaining topics. The material before the midterm is easy but after that it gets a lot harder. He posts his lecture videos, previous exams, and homework all on his website. It's a lot of material and if you want to do well don't slack off and stay updated with the lectures and videos.
Tags: Lecture heavy, Test heavy, Online savvy
#4 · distance 0.4217 · rrf 0.0306 · source marvin-nakayama.txt · review · id marvin-nakayama-review-24 ✅ used


Course: CS341
Professor Nakayama is so far my best professor in NJIT. He really goes out of his way to make things as clear as possible. His videos are amazing. He really articulates very well and finds a way to explain abstract things. If I could take him again I wouldn't hesitate. I wish all my profs are like him
#5 · distance 0.6103 · rrf 0.0298 · source marvin-nakayama.txt · review · id marvin-nakayama-review-27 ✅ used


Course: CS341
Reads off slides and expects you to memorize pages of proofs. Programming assignments are a joke. A bit strict and somewhat of a harsh grader. Supposedly doesn't curve. For exams, look over past semester exams and memorize proofs. If you're good at memorizing stuff, the class won't be difficult. Else, then start memorizing weeks in advance. 7/10
#6 · distance 0.5906 · rrf 0.0284 · source kamlesh-naik.txt · review · id kamlesh-naik-review-23


Course: CS332
Naik is amazing at explaining concepts and I loved having him as a teacher. Problem is the midterm and final which basically make up 70% of your final grade have problems that are much much harder than anything done in class or on quizzes. But that given he does make it basically impossible to fail the class if you do the work and try you'll pass.
Tags: Tough grader, Amazing lectures, Test heavy
#7 · distance 0.5147 · rrf 0.0279 · source marvin-nakayama.txt · review · id marvin-nakayama-review-20 📄 same file


Course: CS341
Nakayama is the best professor at NJIT. He explains each topic with a ton of detail and makes it easier to understand. The class material is somewhat difficult especially towards the end but If you watch the videos and review the old exams its not too bad. For the final, focus on the review sheet and go over the old projects.
#8 · distance 0.5937 · rrf 0.0276 · source marvin-nakayama.txt · review · id marvin-nakayama-review-10 📄 same file


Course: CS341
Pros: He gives you past exams, notes and lectures to study. His exams follow his past ones in format so you know what you're gonna get. Will curve. Cons: Probably the most annoyingly strict grader. The proofs are ridiculously long and abstract; And you must follow them word for word or you will get points off. It is just rote memorization.
Tags: Lecture heavy, Tough grader
#9 · distance 0.6055 · rrf 0.0276 · source marvin-nakayama.txt · review · id marvin-nakayama-review-12 📄 same file


Course: CS341
I took CS341 in 2002 and I still use today what I learned in that course. Professor Nakayama was one of the few that I still remember to this day. Take his course if you can and pay attention. You'll be glad you did.
Tags: Gives good feedback, Participation matters, Accessible outside class
#10 · distance 0.4400 · rrf 0.0271 · source marvin-nakayama.txt · review · id marvin-nakayama-review-39 📄 same file


Course: CIS341
material can get confusing, but nakayama is a good (though boring) teacher... very helpful, and very fair... there was a major screw up with a test i took and he handled it very well
```

</details>

### Hybrid Generation

```
Professor Nakayama's class requires a significant amount of memorization of long proofs, with some students noting that he expects you to regurgitate abstract proofs word for word on exams. However, opinions on the class and professor vary, with some students finding him to be a great teacher and others struggling with the material. According to the reviews, memorization of proofs is a key component of success in the class [marvin-nakayama.txt].
```

### Conclusion

**Hybrid** won by a bit. It retrieved one more chunk that mentioned proofs than semantic-only did, causing the LLM to generate a more certain answer about students finding proof memorization a key component of the class. The retrieved chunks are partially relevant because most if not a vast majorty of them are from the intended `marvin-nakayama.txt` doc, and at least one of the docs mentions memorization and/or proofs.

## 4

### Query

```
Which professors offer extra credit?
```

### Semantic-Only Retrieval

```
Retrieved 10 chunks. Answer drawn from abdul-rahman-itani.txt (3 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.5212 · source abdul-rahman-itani.txt · review · id abdul-rahman-itani-review-113 ✅ used


Course: CS288
This professor doesn't believe in partial credit, his job is to fail you (described by his TAs). On top of that, he is very degrading while talking in his lectures, completely demotivating you of ever getting a good grade in his difficult class. 100% would not recommend, do not listen to anyone giving him a 5 star rating. I repeat, STAY AWAY!!
Tags: Lots of homework, Lecture heavy, Tough grader
#2 · distance 0.5353 · source abdul-rahman-itani.txt · review · id abdul-rahman-itani-review-16 ✅ used


Course: CS350
Dr. Itani is one of the best professors at this university. He knows the topics deeply, cares about his students, and wants them to pass and learn. Enough said.
Tags: Get ready to read, Caring, Respected
#3 · distance 0.5405 · source kamlesh-naik.txt · review · id kamlesh-naik-review-73


Course: CS630
He's one of the best Professors I've ever met in my entire life. Prof. Kamlesh is extremely dedicated to his work and keeps his class interesting. His immense knowledge, active communication and easily approachable personality makes learning fun. He's very handsome and friendly. Also, I'd definitely take his class once again.
Tags: Accessible outside class, Amazing lectures, Caring
#4 · distance 0.5418 · source kamlesh-naik.txt · review · id kamlesh-naik-review-50


Course: CS332
He's one of the best professors ever had in my life, his teaching skills are so exceptional, better teaching skills than the CS head of the department.
Tags: Tough grader, Amazing lectures, Caring
#5 · distance 0.5574 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-30


Course: CS356
Great Professor! She has deep knowledge about the course!
Tags: Tough grader, Extra credit, Clear grading criteria
#6 · distance 0.5589 · source bassel-arafeh.txt · review · id bassel-arafeh-review-50


Course: CS280
legit the greatest professor in all of NJIT, possibly even the whole United States. Actually probably the whole world. perhaps even the entire galaxy. Mans is the Thanos of the professional teaching world
Tags: Hilarious, Respected, Online savvy
#7 · distance 0.5590 · source abdul-rahman-itani.txt · review · id abdul-rahman-itani-review-62 ✅ used


Course: CS288
If you want the most out of the money you're paying for these courses, take Itani. Not only will you learn a lot more in his classes compared to other professors, but you will develop skills and projects that can be presented to employers.
Tags: Get ready to read, Amazing lectures, Lots of homework
#8 · distance 0.5608 · source bassel-arafeh.txt · review · id bassel-arafeh-review-64


Course: CS280
good professor
Tags: Amazing lectures, Hilarious, Online savvy
#9 · distance 0.5628 · source kamlesh-naik.txt · review · id kamlesh-naik-review-18


Course: CS332
Overall one of my favorite professors at NJIT. He does a great job at teaching the material, the only downside is that he doesn't post any of the material on canvas which makes it difficult to catch up if you miss a lecture.
Tags: Tough grader, Amazing lectures, Hilarious
#10 · distance 0.5634 · source kamlesh-naik.txt · review · id kamlesh-naik-review-15


Course: CS332
By far the best professor at NJIT. He is very funny, caring and is always willing to help his students. He is a loving man and makes all concepts super easy to understand. If you have the option to take his class, take him you will be glad you did.
Tags: Hilarious, Lecture heavy, Graded by few things
```

### Semantic-Only Generation

```
I can't find the answer to that question.
```

### Hybrid Retrieval

```
Retrieved 10 chunks. Answer drawn from samaneh-berenjian.txt (2 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.5574 · rrf 0.0320 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-30 ✅ used

Course: CS356
Great Professor! She has deep knowledge about the course!
Tags: Tough grader, Extra credit, Clear grading criteria
#2 · distance 0.5628 · rrf 0.0286 · source kamlesh-naik.txt · review · id kamlesh-naik-review-18

Course: CS332
Overall one of my favorite professors at NJIT. He does a great job at teaching the material, the only downside is that he doesn't post any of the material on canvas which makes it difficult to catch up if you miss a lecture.
Tags: Tough grader, Amazing lectures, Hilarious
#3 · distance 0.5212 · rrf 0.0278 · source abdul-rahman-itani.txt · review · id abdul-rahman-itani-review-113

Course: CS288
This professor doesn't believe in partial credit, his job is to fail you (described by his TAs). On top of that, he is very degrading while talking in his lectures, completely demotivating you of ever getting a good grade in his difficult class. 100% would not recommend, do not listen to anyone giving him a 5 star rating. I repeat, STAY AWAY!!
Tags: Lots of homework, Lecture heavy, Tough grader
#4 · distance 0.5353 · rrf 0.0270 · source abdul-rahman-itani.txt · review · id abdul-rahman-itani-review-16

Course: CS350
Dr. Itani is one of the best professors at this university. He knows the topics deeply, cares about his students, and wants them to pass and learn. Enough said.
Tags: Get ready to read, Caring, Respected
#5 · distance 0.5418 · rrf 0.0269 · source kamlesh-naik.txt · review · id kamlesh-naik-review-50

Course: CS332
He's one of the best professors ever had in my life, his teaching skills are so exceptional, better teaching skills than the CS head of the department.
Tags: Tough grader, Amazing lectures, Caring
#6 · distance 0.5743 · rrf 0.0268 · source kamlesh-naik.txt · review · id kamlesh-naik-review-62

Course: CS332
The class is very lecture heavy, but he does provide his own lecture notes after each chapter. While attendance wasn't mandatory, the quiz/exam content was only covered in class and not present on the textbooks recommended by the professor. He doesn't give much partial credit, so for multipart questions, it's almost always all or no credit.
Tags: Tough grader, Respected, Lecture heavy
#7 · distance 0.6039 · rrf 0.0257 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-37 ✅ used

Course: CS656
I think she is perfect she is knowledgeable about the course, she cares about students a lot and if she present another course that I can take, i will take it with her. Definitely take it.
Tags: Extra credit, Amazing lectures, Clear grading criteria
#8 · distance 0.5641 · rrf 0.0255 · source kamlesh-naik.txt · review · id kamlesh-naik-review-43

Course: CS332
My best professor so far. He made every class enjoyable and interesting. Attendance isn't required but if you attend, everything he teaches will be on the midterm/final. Quizzes are easy and made clear before taking it. He is tough on grading and seldom gives partial credit. No late work accepted, but he's always dripped out.
Tags: Tough grader, Amazing lectures, Clear grading criteria
#9 · distance 0.5937 · rrf 0.0252 · source abdul-rahman-itani.txt · review · id abdul-rahman-itani-review-89

Course: CS100
Dr. Itani has a reputation that made me concerned about taking the course with him. However, he is one of the best professors I've had for CS. While grading is tougher, it helps reinforce the learning. He cares, and explains the why, which is necessary for me to understand.
Tags: Clear grading criteria, Caring, Respected
#10 · distance 0.5405 · rrf 0.0251 · source kamlesh-naik.txt · review · id kamlesh-naik-review-73

Course: CS630
He's one of the best Professors I've ever met in my entire life. Prof. Kamlesh is extremely dedicated to his work and keeps his class interesting. His immense knowledge, active communication and easily approachable personality makes learning fun. He's very handsome and friendly. Also, I'd definitely take his class once again.
Tags: Accessible outside class, Amazing lectures, Caring
```

### Hybrid Generation

```
Professors who offer extra credit include the one teaching CS356 and CS656, as both courses have the "Extra credit" tag. The professor for these courses is knowledgeable and has clear grading criteria. [samaneh-berenjian.txt]
```

### Conclusion

**Hybrid** clearly won. It surfaced two chunks with the tag "Extra credit" in them to the LLM whereas semantic-only surfaced none (one was retrieved but didn't make the single-file cut). The retrieved chunks are somewhat relevant because in both cases 1-2 chunks containing "extra credit" were retrieved.

## 5

### Query

```
Is the workload heavy for Professor Calvin?
```

### Semantic-Only Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from james-calvin.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.3939 · source james-calvin.txt · review · id james-calvin-review-28 ✅ used

Course: CIS114
Answered yes to whether I'd take him again but it really depends on who else is available. Calvin doesn't need to avoided at all costs. Not the greatest lecturer. The assignments are hard with a few exceptions. The difficulty is a good thing in this class as it really forces you to learn data structures. He made me much better at problem solving.
Tags: Lots of homework, Get ready to read, Clear grading criteria
#2 · distance 0.4089 · source james-calvin.txt · review · id james-calvin-review-27 ✅ used

Course: CS114
Prof. Calvin is a pretty boring teacher overall. The class only has a final exam, quizzes and homework. The homework can be tough but it's doable if you put in the time. He drops the 3 lowest quiz grades so that's a plus. The final is half changing your hw code and half time complexity/ data structure questions. The final is just like the quizzes.
Tags: Lots of homework, Lecture heavy
#3 · distance 0.5092 · source james-calvin.txt · review · id james-calvin-review-30 ✅ used

Course: CS114
Professor Calvin is a cool guy. Like the guys said here, he tries his best to make you understand concepts of the class which is super hard. Honestly I didn't learn anything straight from him. But his exercises are really good and if you put the effort to understand the material on your own you will be fine.
Tags: Clear grading criteria, Caring
#4 · distance 0.5219 · source james-calvin.txt · overall · id james-calvin-overall ✅ used

Overall quality rating: 2.5 out of 5, based on 55 ratings.
40% of students would take James Calvin again.
Average level of difficulty: 3.4 out of 5.
Rating distribution: 7 students rated Awesome (5 stars), 7 Great (4 stars), 11 Good (3 stars), 12 OK (2 stars), 18 Awful (1 star).
#5 · distance 0.5480 · source kumar-mani.txt · review · id kumar-mani-review-28

Course: CS356
Workload is ridiculous for the amount of guidance given. He expects endless hours on his projects and gets annoyed if you ask basic questions.
Tags: Tough grader, Get ready to read, Group projects
#6 · distance 0.5850 · source kumar-mani.txt · review · id kumar-mani-review-59

Course: CS656
In my 5 years at this school, I don't think I have ever seen a more stuck up professor than this one. He barely teaches and picks kids out who read the textbook to do the teaching for him and just confirms the answer. He takes weeks to grade exams if there is any technical issues. So for your own sake, follow his instructions EXACTLY or else...
Tags: Tough grader, Group projects, Lots of homework
#7 · distance 0.5868 · source james-calvin.txt · review · id james-calvin-review-7 ✅ used

Course: CS114
Professor Calvin reads off of the slideshow every class, making it very boring. The PS's are long and tedious but are necessary to attempt an A. Labs were of equal difficulty to the PS's. The quizzes were unexpectedly rather hard, but if you do the lab for the week he'll give you a 10/10. Final was difficult as well. Take Kapleau/CBE instead
#8 · distance 0.5928 · source andrew-sohn.txt · review · id andrew-sohn-review-64

Course: CS433
Exams are tough, and homeworks are _very_ time consuming (few of them took more than 10 hours). But he's a very lenient grader, so long as you actually get them done. Overall, a difficult class.. but the prof does his best to make the material more palatable.
#9 · distance 0.5949 · source james-calvin.txt · review · id james-calvin-review-53 📄 same file

Course: CIS341
Only had a few interactions with Prof Calvin over email, and the exams were pretty much everything, but they were nothing unreasonable.
#10 · distance 0.5963 · source kamlesh-naik.txt · review · id kamlesh-naik-review-4

Course: CS630
Intense weekly workload. Expect a project, quiz, discussion, and homework all due the same day. Exams are extremely wordy; it can take 5 minutes just to read one question. Grading is harsh, with points deducted for minor things like word counts. Tough scheduling—he even assigned a quiz over the Spring Break weekend.
Tags: Tough grader, Lots of homework, Test heavy
```

</details>

### Semantic-Only Generation

```
The workload for Professor Calvin is considered heavy, with assignments and homework being described as hard and long, but doable with effort. However, some students found the workload necessary to learn the material, while others found it tedious. [james-calvin.txt]
```

### Hybrid Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from james-calvin.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.4089 · rrf 0.0325 · source james-calvin.txt · review · id james-calvin-review-27 ✅ used

Course: CS114
Prof. Calvin is a pretty boring teacher overall. The class only has a final exam, quizzes and homework. The homework can be tough but it's doable if you put in the time. He drops the 3 lowest quiz grades so that's a plus. The final is half changing your hw code and half time complexity/ data structure questions. The final is just like the quizzes.
Tags: Lots of homework, Lecture heavy
#2 · distance 0.5480 · rrf 0.0320 · source kumar-mani.txt · review · id kumar-mani-review-28

Course: CS356
Workload is ridiculous for the amount of guidance given. He expects endless hours on his projects and gets annoyed if you ask basic questions.
Tags: Tough grader, Get ready to read, Group projects
#3 · distance 0.5092 · rrf 0.0318 · source james-calvin.txt · review · id james-calvin-review-30 ✅ used

Course: CS114
Professor Calvin is a cool guy. Like the guys said here, he tries his best to make you understand concepts of the class which is super hard. Honestly I didn't learn anything straight from him. But his exercises are really good and if you put the effort to understand the material on your own you will be fine.
Tags: Clear grading criteria, Caring
#4 · distance 0.3939 · rrf 0.0312 · source james-calvin.txt · review · id james-calvin-review-28 ✅ used

Course: CIS114
Answered yes to whether I'd take him again but it really depends on who else is available. Calvin doesn't need to avoided at all costs. Not the greatest lecturer. The assignments are hard with a few exceptions. The difficulty is a good thing in this class as it really forces you to learn data structures. He made me much better at problem solving.
Tags: Lots of homework, Get ready to read, Clear grading criteria
#5 · distance 0.5963 · rrf 0.0304 · source kamlesh-naik.txt · review · id kamlesh-naik-review-4

Course: CS630
Intense weekly workload. Expect a project, quiz, discussion, and homework all due the same day. Exams are extremely wordy; it can take 5 minutes just to read one question. Grading is harsh, with points deducted for minor things like word counts. Tough scheduling—he even assigned a quiz over the Spring Break weekend.
Tags: Tough grader, Lots of homework, Test heavy
#6 · distance 0.5868 · rrf 0.0299 · source james-calvin.txt · review · id james-calvin-review-7 ✅ used

Course: CS114
Professor Calvin reads off of the slideshow every class, making it very boring. The PS's are long and tedious but are necessary to attempt an A. Labs were of equal difficulty to the PS's. The quizzes were unexpectedly rather hard, but if you do the lab for the week he'll give you a 10/10. Final was difficult as well. Take Kapleau/CBE instead
#7 · distance 0.5949 · rrf 0.0299 · source james-calvin.txt · review · id james-calvin-review-53 ✅ used

Course: CIS341
Only had a few interactions with Prof Calvin over email, and the exams were pretty much everything, but they were nothing unreasonable.
#8 · distance 0.6193 · rrf 0.0252 · source andrew-sohn.txt · review · id andrew-sohn-review-32

Course: CS288
This professor is probably the toughest one I've ever taken with. He makes things unnecessarily complex. The way he teaches doesn't click with majority of the students, there are a few that likes him but generally in the minority. I hope you enjoy doing projects that takes 20-30hours+ for 1% of your grade, while the awful exams are worth 25%.
Tags: Skip class? You won't pass., Test heavy, Lecture heavy
#9 · distance 0.5972 · rrf 0.0252 · source andrew-sohn.txt · review · id andrew-sohn-review-30

Course: CS288
(Online via COVID). Sohn was a pretty tough professor, but 288 is a pretty tough class. The homeworks are doable, but his starter code can be pretty confusing. He usually goes over similar stuff to the homework in the lecutres. The exams are hard, but if you do the hw "from scratch" and study past exams you should be alright.
Tags: Test heavy, Lecture heavy, Tough grader
#10 · distance 0.6284 · rrf 0.0250 · source andrew-sohn.txt · review · id andrew-sohn-review-19

Course: C350
Sohn the destroyer do i need to say more? Hes not a bad professor but the class is extremely hard. A decent chunk of the class always fails . Just makesure the first two tests you do good because after that its pretty much checkmate second half of class is just a blur no one understood anything .
Tags: Clear grading criteria, Lecture heavy, Test heavy
```

</details>

### Hybrid Generation

```
The workload for Professor Calvin's class can be considered heavy, with many sources mentioning "Lots of homework" and describing the assignments as "tough" and "long and tedious". However, some students found the difficulty to be a positive aspect, as it forced them to learn the material. [james-calvin.txt]
```

### Conclusion

There is **no** clear winner. Both surfaced some of the same reviews (`7`, `27`, `28`, and `30`) to the LLM, and the generation was equally naunced in both cases, mentioning that some students found the workload necessary for learning. The retrieved chunks are relevant for both search algorithms because at least half of them are from `james-calvin.txt` (matching the professor named in the query), and of those, multiple mention either workload or difficulty.
