# A wrong answer is fixed by ticking another box of the same question

Seen on 2026-11-08 in Sphinx (https://github.com/parthh01/sphinx): after a wrong answer, its grader explains and asks
a new scenario on the same concept, and its stamp counts the first tries ("3 questions, 2 first try").

Here, a wrong answer writes a hint under the question and the commit fails (`quiz.py:29-31`); the dev ticks another
box of the same question and commits again. With 2 to 4 boxes, trying them all passes any quiz in three commits, and
`Quiz: 3/3` reads the same as three right answers at once. Nothing counts the tries.

Leads, to settle:

- the key holds a second question per question, on the same point with another input, which the hook puts in place of
  the first after a wrong answer: still offline, no token at commit, but twice the reviewer's writing;
- the trailer says the first tries, `Quiz: 3/3, 2 first try, covers 5/7`: a fact about the batch's quiz, like the
  coverage, never a score kept about a dev;
- the first tries go to the local journal, so the cockpit can tell a module whose quizzes are often missed at once.

The trailer alone is one batch and tells whether the second question is worth it.
