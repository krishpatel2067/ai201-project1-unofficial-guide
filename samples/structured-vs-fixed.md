# Structured vs Fixed Chunking Comparison

Control:

- Conversational memory: **Disabled**
- Hybrid search: **Disabled**
- Filters applied: **None**

## 1

### Query

```
What is Professor Arafeh's overall rating and how many students would take him again?
```

### Structured Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from bassel-arafeh.txt (4 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.3128 · source bassel-arafeh.txt · review · id bassel-arafeh-review-45 ✅ used


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A+ in this course easily.
#2 · distance 0.3242 · source bassel-arafeh.txt · overall · id bassel-arafeh-overall ✅ used


Overall quality rating: 1.8 out of 5, based on 119 ratings.
21% of students would take Bassel Arafeh again.
Average level of difficulty: 3.8 out of 5.
Rating distribution: 15 students rated Awesome (5 stars), 3 Great (4 stars), 7 Good (3 stars), 13 OK (2 stars), 81 Awful (1 star).
#3 · distance 0.3501 · source bassel-arafeh.txt · review · id bassel-arafeh-review-115 ✅ used


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A in this course easily.
Tags: Respected, Inspirational, Amazing lectures
#4 · distance 0.3586 · source bassel-arafeh.txt · review · id bassel-arafeh-review-74 ✅ used


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A in this course easily.
Tags: Amazing lectures, Respected
#5 · distance 0.3972 · source samaneh-berenjian.txt · overall · id samaneh-berenjian-overall


Overall quality rating: 4.2 out of 5, based on 89 ratings.
78% of students would take Samaneh Berenjian again.
Average level of difficulty: 3.6 out of 5.
Rating distribution: 65 students rated Awesome (5 stars), 6 Great (4 stars), 3 Good (3 stars), 2 OK (2 stars), 13 Awful (1 star).
#6 · distance 0.4042 · source abdul-rahman-itani.txt · overall · id abdul-rahman-itani-overall


Overall quality rating: 4.0 out of 5, based on 138 ratings.
71% of students would take Abdul-Rahman Itani again.
Average level of difficulty: 4.2 out of 5.
Rating distribution: 82 students rated Awesome (5 stars), 18 Great (4 stars), 11 Good (3 stars), 7 OK (2 stars), 20 Awful (1 star).
#7 · distance 0.4057 · source kumar-mani.txt · overall · id kumar-mani-overall


Overall quality rating: 2.6 out of 5, based on 113 ratings.
41% of students would take Kumar Mani again.
Average level of difficulty: 4.5 out of 5.
Rating distribution: 38 students rated Awesome (5 stars), 7 Great (4 stars), 3 Good (3 stars), 3 OK (2 stars), 62 Awful (1 star).
#8 · distance 0.4200 · source andrew-sohn.txt · overall · id andrew-sohn-overall


Overall quality rating: 3.5 out of 5, based on 84 ratings.
67% of students would take Andrew Sohn again.
Average level of difficulty: 4.1 out of 5.
Rating distribution: 32 students rated Awesome (5 stars), 18 Great (4 stars), 15 Good (3 stars), 5 OK (2 stars), 14 Awful (1 star).
#9 · distance 0.4346 · source michael-renda.txt · overall · id michael-renda-overall


Overall quality rating: 2.1 out of 5, based on 15 ratings.
27% of students would take Michael Renda again.
Average level of difficulty: 3.1 out of 5.
Rating distribution: 3 students rated Awesome (5 stars), 1 Great (4 stars), 0 Good (3 stars), 2 OK (2 stars), 9 Awful (1 star).
#10 · distance 0.4356 · source marvin-nakayama.txt · overall · id marvin-nakayama-overall


Overall quality rating: 4.3 out of 5, based on 47 ratings.
67% of students would take Marvin Nakayama again.
Average level of difficulty: 3.2 out of 5.
Rating distribution: 33 students rated Awesome (5 stars), 6 Great (4 stars), 5 Good (3 stars), 2 OK (2 stars), 1 Awful (1 star).
```

</details>

### Structured Generation

```
Professor Arafeh has an overall quality rating of 1.8 out of 5, and 21% of students would take him again. However, some students have praised his work and curriculum, achieving high grades in his course. [bassel-arafeh.txt]
```

### Fixed Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from bassel-arafeh.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.3638 · source bassel-arafeh.txt · fixed · id bassel-arafeh-fixed-93 ✅ used


--
Quality: 5.0
Difficulty: 2.0
Course: CS280
Date: Dec 19, 2020
For Credit: Yes
Attendance: Not Mandatory
Would Take Again: Yes
Grade: A
Textbook: No
Online Class: Yes
Review: Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A in this course easily.
Tags: Respected, Inspirational, Amazing lectures
Thumbs Up: 2
Thumbs Down: 6

--- Review 116 ---
Quality: 1.0
Difficulty: 5.
#2 · distance 0.3805 · source marvin-nakayama.txt · fixed · id marvin-nakayama-fixed-1


=== OVERALL ===
Professor: Marvin Nakayama
Overall Quality: 4.3/5 (based on 47 ratings)
Would Take Again: 67%
Level of Difficulty: 3.2
Rating Distribution: Awesome (5): 33 | Great (4): 6 | Good (3): 5 | OK (2): 2 | Awful (1): 1

=== REVIEWS ===
--- Review 1 ---
Quality: 5.0
Difficulty: 3.0
Course: CIS341
Date: Oct 31, 2025
For Credit: Yes
Attendance: Not Mandatory
Would Take Again: Yes
Grade: Not sure yet
Textbook: N/A
Review: He is a good professor but the lessons themselves are nothing special. However, he gives SO many external sources like, past exams & answer keys, recorded lectures, and practice questions. His grading scale regarding pr
#3 · distance 0.3823 · source bassel-arafeh.txt · fixed · id bassel-arafeh-fixed-54 ✅ used


andatory
Would Take Again: Yes
Grade: A+
Textbook: Yes
Review: Professor Bassel Arafeh is an amazing educator and communicator. He has a true passion for teaching and a talent for explaining complex concepts in a way that is easy to understand. His dedication to his students is remarkable, and he always goes above and beyond to ensure that they have the knowledge and skills they need to succeed.
Tags: Amazing lectures, Inspirational, Caring
Thumbs Up: 0
Thumbs Down: 6

--- Review 73 ---
Quality: 5.0
Difficulty: 2.0
Course: CS280
Date: May 6, 2023
For Credit: Yes
Attendance: Not Mandatory
Would Take Again: Yes
Grade: A
Review: Great professor.
#4 · distance 0.3994 · source bassel-arafeh.txt · fixed · id bassel-arafeh-fixed-56 ✅ used


Yes
Attendance: Not Mandatory
Would Take Again: Yes
Grade: A+
Textbook: N/A
Review: Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A in this course easily.
Tags: Amazing lectures, Respected
Thumbs Up: 1
Thumbs Down: 11

--- Review 75 ---
Quality: 5.0
Difficulty: 1.0
Course: CS280
Date: Feb 28, 2023
For Credit: Yes
Attendance: Not Mandatory
Would Take Again: Yes
Grade: A
#5 · distance 0.4307 · source bassel-arafeh.txt · fixed · id bassel-arafeh-fixed-66 ✅ used


y
Thumbs Up: 0
Thumbs Down: 1

--- Review 85 ---
Quality: 5.0
Difficulty: 3.0
Course: CS280
Date: Oct 14, 2022
For Credit: Yes
Attendance: Not Mandatory
Would Take Again: Yes
Grade: Incomplete
Textbook: N/A
Review: Arafeh is undoubtedly the best professor at NJIT. His lectures are some of the finest in the nation. He guides us all to perfection. Arafeh is very accessable and knowledgeable and personal. I am now a math major thanks to his wonderful insight. Please, if you have the chance, take Arafeh's class. It will change your perspective of life.
Tags: Amazing lectures, Inspirational, Respected
Thumbs Up: 2
Thumbs Down: 3

--- Review 86 ---
#6 · distance 0.4409 · source kumar-mani.txt · fixed · id kumar-mani-fixed-1


=== OVERALL ===
Professor: Kumar Mani
Overall Quality: 2.6/5 (based on 113 ratings)
Would Take Again: 41%
Level of Difficulty: 4.5
Rating Distribution: Awesome (5): 38 | Great (4): 7 | Good (3): 3 | OK (2): 3 | Awful (1): 62

=== REVIEWS ===
--- Review 1 ---
Quality: 1.0
Difficulty: 5.0
Course: CS656
Date: May 29, 2026
Attendance: Not Mandatory
Grade: C+
Textbook: N/A
Online Class: Yes
Review: Homework and group assignment instructions had convoluted instructions. Grading was harsh and he expected part-time masters students to put 20+ hours a week into his class. Used ProctorU Live when he's not supposed to. Overall was not pleasant to deal w
#7 · distance 0.4486 · source bassel-arafeh.txt · fixed · id bassel-arafeh-fixed-33 ✅ used


12, 2024
For Credit: Yes
Attendance: Not Mandatory
Grade: B
Textbook: N/A
Review: I would say to avoid him at all costs for CS280, but unfortunately, he's the only professor for 280. good luck
Tags:
Thumbs Up: 0
Thumbs Down: 0

--- Review 44 ---
Quality: 1.0
Difficulty: 2.0
Course: CS280
Date: Apr 11, 2024
Attendance: Not Mandatory
Grade: A
Review: easy class, but lectures are pointless
Tags:
Thumbs Up: 0
Thumbs Down: 0

--- Review 45 ---
Quality: 5.0
Difficulty: 1.0
Course: CS280
Date: Apr 11, 2024
For Credit: Yes
Attendance: Not Mandatory
Would Take Again: Yes
Grade: A+
Textbook: N/A
Review: Dr. Professor Arafeh is one of the brightest pe
#8 · distance 0.4492 · source abdul-rahman-itani.txt · fixed · id abdul-rahman-itani-fixed-1


=== OVERALL ===
Professor: Abdul-Rahman Itani
Overall Quality: 4.0/5 (based on 138 ratings)
Would Take Again: 71%
Level of Difficulty: 4.2
Rating Distribution: Awesome (5): 82 | Great (4): 18 | Good (3): 11 | OK (2): 7 | Awful (1): 20

=== REVIEWS ===
--- Review 1 ---
Quality: 1.0
Difficulty: 5.0
Course: CS350
Date: May 31, 2026
For Credit: Yes
Attendance: Mandatory
Grade: C
Textbook: Yes
Review: (opposite) This professor gives a lot of details during lecture. The exams have the same difficulty as the textbook problems. Itani likes to tutor his students and he explicitly says that he likes to do so in his office hours. Make sure to take him i
#9 · distance 0.4573 · source bassel-arafeh.txt · fixed · id bassel-arafeh-fixed-1 📄 same file


=== OVERALL ===
Professor: Bassel Arafeh
Overall Quality: 1.8/5 (based on 119 ratings)
Would Take Again: 21%
Level of Difficulty: 3.8
Rating Distribution: Awesome (5): 15 | Great (4): 3 | Good (3): 7 | OK (2): 13 | Awful (1): 81

=== REVIEWS ===
--- Review 1 ---
Quality: 1.0
Difficulty: 5.0
Course: CS280
Date: May 4, 2026
For Credit: Yes
Attendance: Not Mandatory
Grade: Drop/Withdrawal
Textbook: Yes
Review: Honestly, one of the most frustrating classes I've ever taken. It constantly felt like questions weren't really being answered. Lectures are basically a Lil Pump concert, just straight mumbling. I'm not even exaggerating when I say this cl
#10 · distance 0.4619 · source bassel-arafeh.txt · fixed · id bassel-arafeh-fixed-6 📄 same file


Review 8 ---
Quality: 5.0
Difficulty: 3.0
Course: CS280
Date: Nov 8, 2025
For Credit: Yes
Attendance: Not Mandatory
Would Take Again: Yes
Grade: Not sure yet
Textbook: Yes
Review: When I first looked at a snippet of code I thought "Oh it's just a piece of code" but when I stepped into my first lecture with Professor Arafeh, I gained severe Enlightenment. Every word of his speech eminates some sort of "aura" as they say nowadays. Arafeh has truly made me a better coder and has shown what it's like to be an exceptional teacher
Tags: Amazing lectures, Inspirational, Hilarious
Thumbs Up: 1
Thumbs Down: 0

--- Review 9 ---
Quality: 1.0
Difficulty
```

</details>

### Fixed Generation

```
Professor Arafeh's overall rating varies, with some students giving him a high rating of 5.0 and others a low rating of 1.0, and the difficulty of his course also varies, with some students finding it easy (difficulty: 1.0 or 2.0) and others finding it hard (difficulty: 5.0). Many students would take him again, with several reviews stating "Would Take Again: Yes". [bassel-arafeh.txt]
```

### Conclusion

**Structured** chunking won in a subtle way. While both chunking strategies led to a useable generated response, the structured version had the advantage of receiving an `-overall` chunk for this professor, which clearly answers the query. The fixed version does not get this chunk and so the generated response sounds plausible, but it is in fact cherry-picked to a few reviews. (Another curious thing this test reveals is that both strategies' retrievals surfaced what seem like illegitimate reviews due to a suspiciously identical format e.g. "His tireless work educating students..." - this is an example of an overall system limitation due to the nature of uncurated reviews.)

## 2

### Query

```
Which courses does Professor Berenjian teach online?
```

### Structured Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from samaneh-berenjian.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.2648 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-62 ✅ used


Course: CS656
Professor Berenjian is a very good teacher who genuinely cares about her students' learning. Her ability to simplify complex concepts and make them understandable is great.
Tags: Amazing lectures
#2 · distance 0.2991 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-56 ✅ used


Course: CS656
Professor Berenjian is a great teacher! She really knows her stuff and explains things in a way that's easy to understand. She's always willing to help and genuinely cares about her students. Definitely recommend taking her class!
#3 · distance 0.3023 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-36 ✅ used


Course: CS656
Professor Berenjian is a fantastic teacher for the Networking course. She explains things clearly, keeps the class engaging and is great at managing the classroom.
Tags: Participation matters, Amazing lectures, Lecture heavy
#4 · distance 0.3303 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-35 ✅ used


Course: CS356
Professor Berenjian is an excellent teacher who explains concepts clearly and keeps the class engaging. She's very organized and always makes sure students are on track. Even though the course was challenging, I learned a lot and appreciated her support throughout. Highly recommend her for CS356!
Tags: Amazing lectures, Respected, Lecture heavy
#5 · distance 0.3567 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-20 ✅ used


Course: CS696
I'm currently taking the CS696 online class with Professor Berenjian. I enjoy the course content—it's both engaging and informative. She's also thoughtful and supportive. I do feel the number of office hours is a bit limited though.
Tags: Group projects, Caring, Lecture heavy
#6 · distance 0.3685 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-28 📄 same file


Course: CS656
Professor Berenjian is very respectful. She is caring and very supportive.
Tags: Caring, Respected
#7 · distance 0.3781 · source bassel-arafeh.txt · review · id bassel-arafeh-review-74


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A in this course easily.
Tags: Amazing lectures, Respected
#8 · distance 0.3783 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-6 📄 same file


Course: CS656
I took CS656 with Professor Berenjian. The class was well-structured and she really knows the material. However, the course relies heavily on the Kurose and Ross textbook, and sometimes it feels like the lectures just follow the book too closely. Still, I think the class is worth taking, especially if you stay on top of the readings.
Tags: Amazing lectures, Respected
#9 · distance 0.3794 · source bassel-arafeh.txt · review · id bassel-arafeh-review-115


Course: CS280
Dr. Professor Arafeh is one of the brightest people in his field across the USA. His tireless work educating students has been praised by the majority of students I have spoken to. His cutting-edge curriculum has received numerous awards from some of our countries finest institutions, which is why I was able to achieve an A in this course easily.
Tags: Respected, Inspirational, Amazing lectures
#10 · distance 0.3845 · source samaneh-berenjian.txt · review · id samaneh-berenjian-review-8 📄 same file


Course: CS356
Everyone loves to say things like "this prof just read off the slides" which is terribly unproductive criticism. Berenjian is simply not good at teaching She struggles immensely to explain the concepts that she clearly understands. There should be a minimum communication skills requirement for anyone who wants to be a teacher or professor.
Tags: Beware of pop quizzes
```

</details>

### Structured Generation

```
Professor Berenjian teaches CS656, CS356, and CS696, with CS696 being specifically mentioned as an online class. [samaneh-berenjian.txt]
```

### Fixed Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from samaneh-berenjian.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.3714 · source samaneh-berenjian.txt · fixed · id samaneh-berenjian-fixed-28 ✅ used


Berenjian is a fantastic teacher for the Networking course. She explains things clearly, keeps the class engaging and is great at managing the classroom.
Tags: Participation matters, Amazing lectures, Lecture heavy
Thumbs Up: 0
Thumbs Down: 0

--- Review 37 ---
Quality: 5.0
Difficulty: 4.0
Course: CS656
Date: Dec 23, 2024
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: B+
Textbook: Yes
Review: I think she is perfect she is knowledgeable about the course, she cares about students a lot and if she present another course that I can take, i will take it with her. Definitely take it.
Tags: Extra credit, Amazing lectures, Clear g
#2 · distance 0.3930 · source samaneh-berenjian.txt · fixed · id samaneh-berenjian-fixed-18 ✅ used


Take Again: Yes
Grade: Not sure yet
Textbook: Yes
Online Class: Yes
Review: I'm currently taking the CS696 online class with Professor Berenjian. I enjoy the course content—it's both engaging and informative. She's also thoughtful and supportive. I do feel the number of office hours is a bit limited though.
Tags: Group projects, Caring, Lecture heavy
Thumbs Up: 0
Thumbs Down: 2

--- Review 21 ---
Quality: 5.0
Difficulty: 3.0
Course: CS356
Date: Apr 16, 2025
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: Not sure yet
Textbook: Yes
Review: She is very knowledgeable about the course material.
Tags: Amazing lectures, Clear gra
#3 · distance 0.4217 · source samaneh-berenjian.txt · fixed · id samaneh-berenjian-fixed-27 ✅ used


ook: Yes
Review: Professor Berenjian is an excellent teacher who explains concepts clearly and keeps the class engaging. She's very organized and always makes sure students are on track. Even though the course was challenging, I learned a lot and appreciated her support throughout. Highly recommend her for CS356!
Tags: Amazing lectures, Respected, Lecture heavy
Thumbs Up: 0
Thumbs Down: 0

--- Review 36 ---
Quality: 5.0
Difficulty: 4.0
Course: CS656
Date: Dec 25, 2024
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: B+
Textbook: Yes
Review: Professor Berenjian is a fantastic teacher for the Networking course. She explains th
#4 · distance 0.4455 · source samaneh-berenjian.txt · fixed · id samaneh-berenjian-fixed-8 ✅ used


or Credit: Yes
Attendance: Mandatory
Grade: A
Textbook: Yes
Review: Everyone loves to say things like "this prof just read off the slides" which is terribly unproductive criticism. Berenjian is simply not good at teaching She struggles immensely to explain the concepts that she clearly understands. There should be a minimum communication skills requirement for anyone who wants to be a teacher or professor.
Tags: Beware of pop quizzes
Thumbs Up: 8
Thumbs Down: 1

--- Review 9 ---
Quality: 1.0
Difficulty: 5.0
Course: CS656
Date: Aug 12, 2025
For Credit: Yes
Attendance: Mandatory
Grade: Not sure yet
Textbook: Yes
Online Class: Yes
Review: Profes
#5 · distance 0.4485 · source samaneh-berenjian.txt · fixed · id samaneh-berenjian-fixed-44 ✅ used


t
Textbook: Yes
Online Class: Yes
Review: I took CS696 online class with her. The modules were good including supporting materials, videos, … I recommend this course.
Tags:
Thumbs Up: 0
Thumbs Down: 1

--- Review 62 ---
Quality: 5.0
Difficulty: 4.0
Course: CS656
Date: Nov 7, 2024
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: Not sure yet
Textbook: Yes
Review: Professor Berenjian is a very good teacher who genuinely cares about her students' learning. Her ability to simplify complex concepts and make them understandable is great.
Tags: Amazing lectures
Thumbs Up: 0
Thumbs Down: 0

--- Review 63 ---
Quality: 5.0
Difficulty
#6 · distance 0.4592 · source abdul-rahman-itani.txt · fixed · id abdul-rahman-itani-fixed-40


ke Again: Yes
Grade: A
Textbook: Yes
Review: Professor Itani is a standout at NJIT. His deep knowledge and passion for the subject make classes both informative and engaging. He challenges students to think critically and apply concepts in real-world scenarios. Highly recommend taking his classes if you want to learn and be inspired.
Tags: Amazing lectures, Inspirational, Caring
Thumbs Up: 12
Thumbs Down: 0

--- Review 44 ---
Quality: 3.0
Difficulty: 5.0
Course: CS288
Date: Nov 28, 2024
For Credit: Yes
Attendance: Mandatory
Grade: B
Textbook: Yes
Review: Dr. Itani is an excellent lecturer and the actual course material is really good at makin
#7 · distance 0.4691 · source samaneh-berenjian.txt · fixed · id samaneh-berenjian-fixed-41 📄 same file


yet
Textbook: Yes
Review: Professor Berenjian is a great teacher! She really knows her stuff and explains things in a way that's easy to understand. She's always willing to help and genuinely cares about her students. Definitely recommend taking her class!
Tags:
Thumbs Up: 0
Thumbs Down: 0

--- Review 57 ---
Quality: 5.0
Difficulty: 5.0
Course: CS356
Date: Nov 15, 2024
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: Not sure yet
Textbook: Yes
Review: She is really good at this subject. Highly recommend her.
Tags: Participation matters, Amazing lectures, Inspirational
Thumbs Up: 0
Thumbs Down: 0

--- Review 58 ---
Quality:
#8 · distance 0.4718 · source samaneh-berenjian.txt · fixed · id samaneh-berenjian-fixed-6 📄 same file


es
Attendance: Not Mandatory
Would Take Again: Yes
Grade: B+
Textbook: Yes
Online Class: Yes
Review: I took CS656 with Professor Berenjian. The class was well-structured and she really knows the material. However, the course relies heavily on the Kurose and Ross textbook, and sometimes it feels like the lectures just follow the book too closely. Still, I think the class is worth taking, especially if you stay on top of the readings.
Tags: Amazing lectures, Respected
Thumbs Up: 3
Thumbs Down: 4

--- Review 7 ---
Quality: 3.0
Difficulty: 1.0
Course: CS356
Date: Oct 15, 2025
For Credit: Yes
Attendance: Mandatory
Grade: A-
Textbook: Yes
Review: G
#9 · distance 0.4780 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-65


ity and an excellent teaching style along with his ability to set goals. Prof. Naik is always elaborative, bold and confident during the delivery of lectures which makes the students understand the concepts well.
Tags: Accessible outside class, Clear grading criteria, Amazing lectures
Thumbs Up: 1
Thumbs Down: 0

--- Review 73 ---
Quality: 5.0
Difficulty: 4.0
Course: CS630
Date: Jan 17, 2022
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: B
Textbook: Yes
Review: He's one of the best Professors I've ever met in my entire life. Prof. Kamlesh is extremely dedicated to his work and keeps his class interesting. His immense knowl
#10 · distance 0.4781 · source marvin-nakayama.txt · fixed · id marvin-nakayama-fixed-3


and homework all on his website. It's a lot of material and if you want to do well don't slack off and stay updated with the lectures and videos.
Tags: Lecture heavy, Test heavy, Online savvy
Thumbs Up: 0
Thumbs Down: 0

--- Review 3 ---
Quality: 3.0
Difficulty: 5.0
Course: CIS341
Date: Nov 1, 2023
For Credit: Yes
Attendance: Not Mandatory
Grade: Not sure yet
Textbook: N/A
Review: Prof Nakayama is a nice guy, but my main gripe is that when I registered for this class, it was supposed to meet in person twice a week, but was later converted to a hybrid course. This class requires so much more work outside of class time than I was prepared for.
```

</details>

### Fixed Generation

```
Professor Berenjian teaches CS696 online, according to one review, and possibly CS656, as another review mentions an online class but the course number is cut off. [samaneh-berenjian.txt]
```

### Conclusion

**Fixed** chunking won by a little bit. The generation in both strategies correctly mention CS696 as an online course by this professor, but fixed chunking generation also mentions CS656, which is also another online course. However, the LLM itself breaks the 4th wall and expresses uncertainty on CS656 becasue the "course number is cut off." This is a key weakness of fixed chunking, but it won in this case because of ample "Online Class: Yes" lines that, for structured chunking, end up only in the metadata, not the chunks going to the LLM. A simple listing would fix this and may lead structured chunking to prevail, but this test demonstrates that fixed chunking can be a decent strategy in some cases.

## 3

### Query

```

```

### Structured Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from kamlesh-naik.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.4221 · source kamlesh-naik.txt · review · id kamlesh-naik-review-78 ✅ used


Course: CS332
Professor Naik is great! Seriously, if you show up, pay attention, and take notes, it's literally a free A. He explains exactly what you need to know for homework, quizzes, and exams.
#2 · distance 0.4401 · source kamlesh-naik.txt · review · id kamlesh-naik-review-76 ✅ used


Course: CS332
Professor Naik is caring and straightforward. The class requires you to put in effort, which means not an easy A. However, he is very clear in terms of what will be asked in the exams. If you attend his classes and do the homework then things will be easier. Do not wait for the last moment to study for exams, he does tell you that.
Tags: Skip class? You won't pass., Clear grading criteria, Caring
#3 · distance 0.4450 · source kamlesh-naik.txt · review · id kamlesh-naik-review-17 ✅ used


Course: CS332
Professor Naik is a good lecturer and goes over all problems. However he is a harsh grader, if you make one mistake, the rest of the question is marked wrong, takes off many points. He also has somehow voided exceptions from the dean of students, and makes a point to mention that none of his quizzes or homework can be made up even if you're dying.
Tags: Tough grader, Clear grading criteria, Test heavy
#4 · distance 0.4478 · source kamlesh-naik.txt · review · id kamlesh-naik-review-67 ✅ used


Course: CS332
Professor Kamlesh cares about his students and he teaches very clearly. You will know what will be on the quiz and what the exam material will be exactly there is nothing arbitrary at all. Don't listen to any low review because they are sore that they just didn't study the material. Take this professor and only him!
Tags: Amazing lectures, Clear grading criteria, Caring
#5 · distance 0.4522 · source kamlesh-naik.txt · review · id kamlesh-naik-review-36 ✅ used


Course: CS332
Professor Naik is by far one of the best professors I've come across.Cares a lot for your success. You will lose points in your answer from the point where a mistake has been made solving the question. So be sure to double check your answers! Note: THE MATERIAL IS NOT HARD! Pay attention in his class and you will be amazed at how much you learn!
Tags: Tough grader, Participation matters, Amazing lectures
#6 · distance 0.4604 · source james-calvin.txt · review · id james-calvin-review-2


Course: CS114
He is an ok professor. He reads off the slides in a quiet voice. Quizzes are fine since they are open notes/internet. PS are difficult and take a lot of time, but a little helpful. Final was open notes/internet as well. He's not the greatest but you be fine if you do all the work. TA lowkey clutches with labs, so feel free to ask him.
Tags: Lots of homework, Caring
#7 · distance 0.4629 · source james-calvin.txt · review · id james-calvin-review-8


Course: CS337
If you're taking him for 337, skip the lectures and only show up on quiz days. On quiz days, he will give you the opportunity to work on a lab. If you do good on the lab you can skip out on the quiz. Quizzes are open internet, but they are still hard to do good on. The final is all the quizzes chained together.
#8 · distance 0.4746 · source kamlesh-naik.txt · review · id kamlesh-naik-review-23 📄 same file


Course: CS332
Naik is amazing at explaining concepts and I loved having him as a teacher. Problem is the midterm and final which basically make up 70% of your final grade have problems that are much much harder than anything done in class or on quizzes. But that given he does make it basically impossible to fail the class if you do the work and try you'll pass.
Tags: Tough grader, Amazing lectures, Test heavy
#9 · distance 0.4768 · source kamlesh-naik.txt · review · id kamlesh-naik-review-72 📄 same file


Course: CS630
Prof. Naik's class has always been interesting. He has a fascinating personality and an excellent teaching style along with his ability to set goals. Prof. Naik is always elaborative, bold and confident during the delivery of lectures which makes the students understand the concepts well.
Tags: Accessible outside class, Clear grading criteria, Amazing lectures
#10 · distance 0.4853 · source kamlesh-naik.txt · review · id kamlesh-naik-review-6 📄 same file


Course: CS630
The lectures are easy, but the exams are brutal. Questions are word-heavy and feel like puzzles, requiring intense logic rather than just memory. He does oral quizzes every class on any past topic, so stay ready. No practice sheets are given until the very end of the semester—only homework and quizes. It's a tough gap to bridge.
Tags: Amazing lectures, Clear grading criteria, Beware of pop quizzes
```

</details>

### Structured Generation

```
I can't find the answer to that question.
```

### Fixed Retrieval

<details>
<summary>View</summary>

```
Retrieved 10 chunks. Answer drawn from kamlesh-naik.txt (5 chunk(s) sent to the LLM). ✅ = sent to the LLM · 📄 = same professor, over the 5-chunk cap.

#1 · distance 0.3906 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-70 ✅ used


class and he was the best professor I had in that semester. If you attend every class and listen carefully and practice, it's an easy A. His exams will be amazing, you will get to see some slightly tricked questions. Very helpful with the doubts. Even though he is a young professor you can learn a lot.
Tags: Get ready to read, Test heavy, Clear grading criteria
Thumbs Up: 1
Thumbs Down: 0

--- Review 78 ---
Quality: 5.0
Difficulty: 2.0
Course: CS332
Date: Jan 2, 2022
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: A
Textbook: Yes
Review: Professor Naik is great! Seriously, if you show up, pay attention, and take notes, it's
#2 · distance 0.3941 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-67 ✅ used


passionately. He truly understands students and goes out of his way to help them. He is truly a professor of my dreams. He's exams are brain triggering, yet interesting. NJIT has really received a gem like him. Prof. Naik is very young, dynamic and handsome to the core.
Tags: Test heavy, Clear grading criteria, Amazing lectures
Thumbs Up: 1
Thumbs Down: 0

--- Review 75 ---
Quality: 1.0
Difficulty: 4.0
Course: CS630
Date: Jan 13, 2022
For Credit: Yes
Attendance: Mandatory
Would Take Again: No
Grade: B+
Textbook: Yes
Review: Fair teacher in terms of knowledge of the subject but is immature and needs experience. He will often make personal rem
#3 · distance 0.4182 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-35 ✅ used


ader, Beware of pop quizzes, Test heavy
Thumbs Up: 2
Thumbs Down: 3

--- Review 41 ---
Quality: 5.0
Difficulty: 3.0
Course: CS332
Date: Oct 25, 2023
For Credit: Yes
Attendance: Not Mandatory
Would Take Again: Yes
Grade: A
Textbook: N/A
Review: Professor Naik might just be the best CS professor at NJIT. The material is not always easy but he teaches it so clearly and tells you exactly what you need to know from each chapter. He regularly gives quizzes but they are usually on one topic and keep you sharp for exams. I wish he taught more classes because I miss having a professor like him.
Tags: Amazing lectures, Inspirational, Caring
Thumbs Up:
#4 · distance 0.4339 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-60 ✅ used


eview: Professor Kamlesh cares about his students and he teaches very clearly. You will know what will be on the quiz and what the exam material will be exactly there is nothing arbitrary at all. Don't listen to any low review because they are sore that they just didn't study the material. Take this professor and only him!
Tags: Amazing lectures, Clear grading criteria, Caring
Thumbs Up: 2
Thumbs Down: 0

--- Review 68 ---
Quality: 4.0
Difficulty: 4.0
Course: CS332
Date: Apr 6, 2022
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: B+
Textbook: Yes
Review: One of the few professors at NJIT whose lectures actually won't bore y
#5 · distance 0.4405 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-51 ✅ used


an oral quiz at the beginning of each class where he randomly picks students and asks questions that if you can't answer right away you get a zero on that. Be prepared for tests with "trick questions" that are based on class material but the question method is not taught.
Tags: Tough grader, Participation matters, Test heavy
Thumbs Up: 2
Thumbs Down: 2

--- Review 58 ---
Quality: 5.0
Difficulty: 4.0
Course: CS332
Date: May 13, 2022
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: B+
Textbook: Yes
Review: He's a great professor who really cares about his students. He may seem harsh at first glance, but he genuinely loves his
#6 · distance 0.4475 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-14 📄 same file


rt. His lectures are detailed and the concepts he teaches are very simplified so that students can understand. I took the undergraduate version of this course (CS 332) and since then I was willing to take his class again when I started my Masters.
Tags: Get ready to read, Amazing lectures, Lots of homework
Thumbs Up: 0
Thumbs Down: 0

--- Review 17 ---
Quality: 3.0
Difficulty: 3.0
Course: CS332
Date: Dec 11, 2025
For Credit: Yes
Attendance: Not Mandatory
Grade: D
Textbook: N/A
Review: Professor Naik is a good lecturer and goes over all problems. However he is a harsh grader, if you make one mistake, the rest of the question is marked wrong, t
#7 · distance 0.4483 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-19 📄 same file


derstand the concepts in class. He also gives you the exact layout of the exam (# of from each topic) beforehand.
Tags:
Thumbs Up: 0
Thumbs Down: 0

--- Review 22 ---
Quality: 4.0
Difficulty: 4.0
Course: CS332
Date: May 17, 2025
For Credit: Yes
Attendance: Not Mandatory
Would Take Again: Yes
Grade: Not sure yet
Textbook: N/A
Review: Prof. Naik is an amazing teacher. I recommend taking him over any other prof for 332. I was doing really well in his class and his class was the only one I looked forward to. I really have great respect for him but it deeply saddens me that because of negative comments in the past, he is much more strict & diffic
#8 · distance 0.4556 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-68 📄 same file


bject but is immature and needs experience. He will often make personal remarks and publicly humiliate students to receive giggles from the class to gain acceptance. He stalks student groups, linkdin and even your insta profiles!Sets beautiful exams but holds grudges and often has angry and crazy outbreak
Tags: Test heavy
Thumbs Up: 1
Thumbs Down: 3

--- Review 76 ---
Quality: 5.0
Difficulty: 3.0
Course: CS332
Date: Jan 6, 2022
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: B
Textbook: Yes
Review: Professor Naik is caring and straightforward. The class requires you to put in effort, which means not an easy A. However, he i
#9 · distance 0.4600 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-7 📄 same file


: 0
Thumbs Down: 0

--- Review 7 ---
Quality: 5.0
Difficulty: 3.0
Course: CS332
Date: Jan 5, 2026
For Credit: Yes
Attendance: Not Mandatory
Would Take Again: Yes
Textbook: Yes
Review: I took professor Naik for cs241. He has very good lectures and explains a lot of the material very well. His quizzes are very easy however his homeworks and exams are a lot more difficult. Some homeworks may take a few hours to complete. He also does not hand out much review material other than problems in class. Watch out for the exams.
Tags: Tough grader, Amazing lectures, Lecture heavy
Thumbs Up: 0
Thumbs Down: 0

--- Review 8 ---
Quality: 5.0
Difficulty: 3.0
#10 · distance 0.4611 · source kamlesh-naik.txt · fixed · id kamlesh-naik-fixed-65 📄 same file


ity and an excellent teaching style along with his ability to set goals. Prof. Naik is always elaborative, bold and confident during the delivery of lectures which makes the students understand the concepts well.
Tags: Accessible outside class, Clear grading criteria, Amazing lectures
Thumbs Up: 1
Thumbs Down: 0

--- Review 73 ---
Quality: 5.0
Difficulty: 4.0
Course: CS630
Date: Jan 17, 2022
For Credit: Yes
Attendance: Mandatory
Would Take Again: Yes
Grade: B
Textbook: Yes
Review: He's one of the best Professors I've ever met in my entire life. Prof. Kamlesh is extremely dedicated to his work and keeps his class interesting. His immense knowl
```

</details>

### Fixed Generation

```
Professor Naik gives quizzes, but it's unclear if all of them are oral. However, one review mentions that he gives an oral quiz at the beginning of each class where he randomly picks students and asks questions. [kamlesh-naik.txt]
```

### Conclusion

**Fixed** chunking won. Structured chunking tripped up because the only chunk that got retrieved with the word "oral" in it got ranked last, definitely not making the final cut to be sent to the LLM. In, fixed chunking such a chunk _does_ get sent to the LLM, causing it to generate a useful and accurate response. Perhaps structured chunking alongside hybrid search may prevail over fixed chunking due to the rarity of the word "oral," demonstrating that one strategy may be better than the other in isolation, but in the context of multiple tunable parameters, the reality is more complicated.
