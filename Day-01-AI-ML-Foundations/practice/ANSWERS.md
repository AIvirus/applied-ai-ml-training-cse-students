# Answers - Day 1 Practice Workbook

Try the questions in [WORKBOOK.md](WORKBOOK.md) first. Your wording can be different - what matters is the meaning.

## Section A - What is AI?

1. AI is making computers do tasks that normally need human intelligence, such as seeing, understanding language and deciding.
2. Examples: face unlock, voice assistant, keyboard word suggestions, photo search ("show my photos of dogs"), spam filter, map traffic prediction.
3. Narrow AI is good at one kind of task (or a limited range). General AI would learn and do any intellectual task a human can. Only narrow AI exists today.
4. Automation. It follows a fixed rule (change every 60 seconds) and never learns. If it used cameras to count cars and changed timing by learning traffic patterns, that would be AI.
5. AI is the biggest circle. Machine Learning is inside AI. Deep Learning is inside Machine Learning.
6. Two reasons: much more **data** (internet, phones) and much more **computing power** (faster chips, GPUs).

## Section B - How machines learn

7. Traditional programming: a person writes rules; rules + data give answers. Machine learning: we give data + answers (examples); the computer finds the rules (the model).
8. Features: area in square feet, number of bedrooms, location, age of building. Label: price.
9. (a) unsupervised, (b) supervised, (c) reinforcement, (d) semi-supervised.
10. Runs = regression (a number). Rain yes/no = classification (a category).

## Section C - Maths intuition

11. Mean = (20+40+40+60+90)/5 = 50. Median = 40. Mode = 40.
12. Class A students all scored close to 60 (similar). Class B students are very spread out - some very low, some very high.
13. 30 / 120 = 0.25 (25 percent).
14. Positive: study hours and marks. Negative: speed and travel time. Near zero: shoe size and marks.
15. You stand on a dark hill and want to reach the lowest point. You feel the slope and step downhill, again and again, until it is flat. In ML, the "height" is the loss; each step changes the model's numbers to reduce the loss. The learning rate is the size of each step - too big jumps over the valley, too small is very slow.

## Section D - Data

16. Analyst: studies data to find facts and make reports. Scientist: uses statistics and ML to predict and build data products. Engineer: builds the systems that collect, clean, store and move data.
17. Structured: marks sheet, bank transactions. Unstructured: photos, voice messages, emails, PDFs.
18. Volume (amount), Velocity (speed), Variety (types). Extra: Veracity (trust) and Value.
19. `df.shape`, `df.head()`, `df.describe()`, `df.groupby("city_type")["final_score"].mean()`.
20. Histogram; bar chart; scatter plot.
21. Drop rows (few missing, lots of data); fill with median or mean (number columns); fill with mode (category columns). Also: drop the column if most of it is empty.
22. Numbers 1, 2, 3 suggest an order and size (rural "3 times" urban), which is false. One-hot gives each group its own 0/1 column without fake order.
23. KNN measures distance. Columns with big numbers (attendance, up to 100) would dominate columns with small numbers (sleep, 4 to 9) unless all are scaled.
24. Using information that contains the answer, which will not be available in real life. Example: using `final_score` as a feature to predict `result`.
25. Examples: `time_on_site_minutes`, `visits_in_last_7_days`, `has_item_in_cart`, `is_weekend`, `days_since_last_purchase`.

## Section E - Algorithms

26.
- Linear regression: draws the best straight line through the data to predict a number.
- Logistic regression: gives the probability of a class (0 to 1) and picks the class with a cut-off, usually 0.5.
- Decision tree: asks a chain of yes/no questions about the features to reach an answer.
- Random forest: many decision trees trained on random parts of the data vote; the majority wins.
- KNN: finds the K most similar examples and uses their majority answer.
- SVM: finds the widest road (margin) that separates the classes.
- K-means: finds K groups in data without labels by moving K centre points until they settle.
27. One tree can memorise noise (overfit). Many different trees voting cancel out each other's mistakes, so the forest is more stable and accurate.
28. `model = Algorithm()`, `model.fit(X_train, y_train)`, `model.predict(X_test)`.
29. (a) linear regression, (b) K-means, (c) random forest.

## Section F - Evaluation

30. To check if the model really learned the pattern instead of memorising. Only unseen data shows how it will do in real life.
31. Validation is used many times to choose models and settings. The test set is used once at the end for the honest final score.
32. An epoch is one full pass over all the training data. Loss is a number that measures how wrong the model is; lower is better.
33. Overfitting. Fixes: simpler model (for example smaller tree depth), more training data, regularisation, fewer useless features, cross-validation to choose settings.
34. High bias: darts all land together but in the wrong place - the model is too simple (underfitting). High variance: darts land all over - the model changes too much with the data (overfitting).
35. Total = 200. Accuracy = (40+130)/200 = 0.85. Precision = 40/(40+10) = 0.80. Recall = 40/(40+20) = 0.667. F1 = 2 x 0.80 x 0.667 / (0.80 + 0.667) = about 0.727.
36. Recall. Missing a real cancer case (false negative) is much more dangerous than a false alarm, which can be checked with more tests.
37. If one class is rare (for example 5 percent sick), a model that always predicts the common class gets 95 percent accuracy but never finds the rare cases. Its recall is 0.
38. MAE is the average size of the mistakes in real units (for example 4 marks). R2 says how much of the variation the model explains: 1 is perfect, 0 is no better than guessing the average.
