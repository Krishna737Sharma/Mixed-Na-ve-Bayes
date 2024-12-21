# Mixed Naïve Bayes

## Objective
In this assignment, you will learn how to handle and preprocess a real-world dataset, including dealing with duplicates, missing values, and feature scaling. You'll implement the Naive Bayes classifier from scratch, selecting appropriate likelihood distributions for different feature types. You'll also compare your implementation with an existing model (MixedNB) and assess its performance using various metrics. Finally, you'll learn to effectively evaluate and visualize the results to communicate your findings.

## Tasks

### Task 1: Load the Secondary Mushroom Dataset [Marks - 0]
- Load the Secondary Mushroom dataset using Pandas. 
- This dataset has 20 features, and the target variable is binary, indicating if the mushroom is edible or not.

### Task 2: Check for Duplicate Entries and Missing Values [Marks - 1]
- Check if there are duplicate entries in the data and missing values of features.
- Remove duplicate entries.
- Handle entries with missing feature values using imputation methods (e.g., mean, median, mode).

### Task 3: Preprocess the Dataset [Marks - 3]
1. Preprocess the dataset as required (e.g., feature scaling or standardization).
2. Determine if the dataset is balanced or imbalanced.
3. Split the data into training and test sets.

### Task 4: Implement Naïve Bayes Classifier [Marks - 7]
- Implement a Naïve Bayes classifier from scratch by appropriately choosing the likelihood distribution for each feature.
- The dataset has mixed feature types (continuous and categorical features), so the likelihood distribution must consider the corresponding feature type.
- Clearly mention the type of distribution chosen for each feature’s likelihood.

### Task 5: Evaluate Classification Performance [Marks - 2]
- Report classification performance using appropriate metrics:
  - Accuracy
  - Precision
  - Recall
  - Confusion Matrix
  - Area Under the Precision-Recall Curve (AUPRC)
- Use suitable plots to visualize the results.

### Task 6: Fit a MixedNB Model [Marks - 5]
- Fit a Naïve Bayes model for this dataset using MixedNB from the package [mixed-naive-bayes](https://pypi.org/project/mixed-naive-bayes/).

### Task 7: Compare Performance [Marks - 2]
- Compare the performance of your implementation with that obtained using MixedNB.
- Highlight similarities and differences in metrics such as accuracy, precision, recall, and AUPRC.

## Files
- `secondary_mushroom_dataset.csv`: Dataset file containing the Secondary Mushroom dataset.
- `mushroom_classification.py`: Python script containing the implementation for all tasks.
- `README.md`: Project documentation in Markdown format.

## How to Run
1. Clone the repository.
2. Ensure the dataset `secondary_mushroom_dataset.csv` is in the working directory.
3. Install the required Python libraries: `numpy`, `pandas`, `matplotlib`, `mixed-naive-bayes`.
4. Run the `mushroom_classification.py` file to execute all tasks.

## Results
- Detailed analysis and visualization for each task.
- Comparison between custom Naïve Bayes implementation and MixedNB implementation.

## License
This project is licensed under the MIT License.
