# import required packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import seaborn as sns

!wget -O MushroomDataset.zip https://archive.ics.uci.edu/static/public/848/secondary+mushroom+dataset.zip

"""### <font color='blue'> Task - 2 [Marks 1] </font>:
:
Check if there are duplicate entries in the data and missing values of features. Remove duplicate entries and handle entries having missing feature values using Imputation method(Like Mean, Mediaan, Mode etc).  
"""

# Solution code

!unzip MushroomDataset.zip -d MushroomDataset
!unzip MushroomDataset/MushroomDataset.zip -d MushroomDataset/InnerZip

# Specify the path to the extracted CSV file
csv_file_path = '/content/MushroomDataset/InnerZip/MushroomDataset/secondary_data.csv'  # Replace with the actual CSV file name

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# getting keys of dataset stored as bunch type
df.keys()

df.head()

# Adjust the file path if necessary
input_path = '/content/MushroomDataset/InnerZip/MushroomDataset/secondary_data.csv'  # Replace with the actual file name
output_path = '/content/MushroomDataset/InnerZip/MushroomDataset/final_data.csv'  # Path to save the file with commas

# Step 1: Read the dataset with semicolon delimiter
data = pd.read_csv(input_path, delimiter=';')

# Step 2: Save the dataset with comma delimiter
data.to_csv(output_path, index=False)

# Verify by loading the newly saved CSV
df = pd.read_csv(output_path)
print(df.head())

df['class'].unique()

# Remove duplicate entries
df = df.drop_duplicates()
print(f"Number of duplicate entries after removal: {df.duplicated().sum()}")

print('----------------------------------------------')

# Check for missing values
missing_values = df.isnull().sum()
print("Missing values in each column:")
print(missing_values)

# Fill missing values for numeric columns with the median (more robust to outliers)
numeric_cols = df.select_dtypes(include=['number']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Fill missing values for categorical columns with the mode (most frequent value)
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Verify that missing values are handled
missing_values_after_filling = df.isnull().sum()
print("Missing values after filling:")
print(missing_values_after_filling)

df.head()

# Get the unique class labels with their corresponding counts
class_counts = df['class'].value_counts().sort_index()

# Display the unique classes with their counts
for class_label, count in class_counts.items():
    print(f"Class {class_label}: {count} instances")

"""### <font color='blue'> Task - 3 [Marks 3] </font>:

1.Preprocess the dataset as required, i.e. feature scaling or standardization

2.Is the dataset balanced or imbalanced?

3.Split data into training and test set
"""

# Identify categorical and continuous features
categorical_features = df.select_dtypes(include=['object', 'category']).columns
continuous_features = df.select_dtypes(include=['number']).columns

print("Categorical Features:", categorical_features)
print("Continuous Features:", continuous_features)

from sklearn.preprocessing import LabelEncoder

# Initialize LabelEncoder
label_encoder = {feature: LabelEncoder() for feature in categorical_features}

class_mappings = {}
# Apply LabelEncoder to each categorical feature
for feature in categorical_features:
    df[feature] = label_encoder[feature].fit_transform(df[feature])

print(df.head())

# Separate features and target
X = df.drop('class', axis=1)  # Assuming 'target' is your target column
y = df['class']

df['class'].value_counts()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()

y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

print(X_train.shape)  # (num_samples_train, num_features)
print(y_train.shape)  # (num_samples_train,)
print(X_test.shape)   # (num_samples_test, num_features)
print(y_test.shape)   # (num_samples_test,)

# # Convert y_train, y_val, and y_test to 1D NumPy arrays
# y_train = y_train.ravel()  # or y_train.squeeze()
# y_test = y_test.ravel()    # or y_test.squeeze()

"""### <font color='blue'> Task - 4 [Marks 7] </font>:

Implement Naive Bayes’ classifier from scratch on this dataset, by appropriately choosing the likelihood distribution for each feature. This dataset has mixed feature types (i.e. continuous and categorical features), and the likelihood distribution of each feature must consider the corresponding feature type. Mention the type of distribution you chose for each feature’s likelihood.  

"""

# Get indices of categorical features
categorical_feature_indices = [df.columns.get_loc(col) for col in categorical_features]

# Get indices of continuous features
continuous_feature_indices = [df.columns.get_loc(col) for col in continuous_features]

print("Categorical feature indices:", categorical_feature_indices)
print("Continuous feature indices:", continuous_feature_indices)

#Solution code

import numpy as np
from scipy.stats import norm
from tqdm import tqdm

class NaiveBayesClassifier:
    def __init__(self, categorical_features):
        # Initialize dictionaries to store prior probabilities and likelihoods
        self.prior_prob = {}  # Prior probabilities for each class
        self.likelihoods = {}  # Likelihoods for feature values given each class
        self.categorical_features = categorical_features  # Indices of categorical features

    def fit(self, X, y):
        # Identify unique classes and number of features from the training data
        self.classes = np.unique(y)  # Unique class labels
        self.num_features = X.shape[1]  # Number of features

        # Compute prior probabilities based on class frequencies
        self.prior_prob = self._calculate_prior_probabilities(y)

        # Compute likelihoods for each feature value given each class
        self.likelihoods = self._calculate_likelihoods(X, y)

    def _calculate_prior_probabilities(self, y):
        # Calculate prior probabilities of each class
        classes, counts = np.unique(y, return_counts=True)  # Get unique classes and their counts
        total_count = len(y)  # Total number of samples
        # Compute prior probability for each class and return as a dictionary
        return dict(zip(classes, counts / total_count))

    def _calculate_likelihoods(self, X, y):
        # Initialize a dictionary to store likelihoods for each class and feature
        likelihoods = {cls: {} for cls in self.classes}

        for cls in tqdm(self.classes):
            # Filter the training data for the current class
            X_cls = X[y == cls]
            num_cls = X_cls.shape[0]  # Number of samples for this class

            for feature_idx in range(self.num_features):
                if feature_idx in self.categorical_features:
                    # Categorical feature: calculate feature value counts and their probabilities
                    feature_values, counts = np.unique(X_cls[:, feature_idx], return_counts=True)
                    # Store the likelihoods as a dictionary of feature values and their probabilities
                    likelihoods[cls][feature_idx] = dict(zip(feature_values, counts / num_cls))
                else:
                    # Continuous feature: calculate mean and variance for Gaussian distribution
                    mean = np.mean(X_cls[:, feature_idx])
                    variance = np.var(X_cls[:, feature_idx])
                    # Store mean and variance
                    likelihoods[cls][feature_idx] = (mean, variance)

        return likelihoods

    def predict(self, X):
        # List to store the predicted class for each sample
        predictions = []

        for x in X:
            # Initialize scores for each class with the log of the prior probability
            class_scores = {cls: np.log(prior) for cls, prior in self.prior_prob.items()}

            for cls in self.classes:
                for feature_idx, value in enumerate(x):
                    if feature_idx in self.categorical_features:
                        # Categorical feature: get the likelihood of the feature value given the class
                        feature_likelihoods = self.likelihoods[cls].get(feature_idx, {})
                        class_scores[cls] += np.log(feature_likelihoods.get(value, 1e-10))
                    else:
                        # Continuous feature: calculate the likelihood using Gaussian distribution
                        mean, variance = self.likelihoods[cls][feature_idx]
                        # Use Gaussian distribution to get the likelihood
                        likelihood = norm.pdf(value, mean, np.sqrt(variance))
                        class_scores[cls] += np.log(likelihood + 1e-10)  # Avoid log(0)

            # Predict the class with the highest score
            predicted_class = max(class_scores, key=class_scores.get)
            predictions.append(predicted_class)

        return np.array(predictions)

import numpy as np
from sklearn.metrics import accuracy_score

categorical_features = [0, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# Initialize the custom Naive Bayes classifier
nb_classifier = NaiveBayesClassifier(categorical_features=categorical_features)

# Fit the model on the training data
nb_classifier.fit(X_train, y_train)

"""### <font color='blue'> Task - 5 [Marks 2] </font>:

Report the classification performance using the appropriate metrics (accuracy, precision, recall, confusion matrix, AUPRC) using suitable plots.
"""

# Solution code

from sklearn.metrics import confusion_matrix, classification_report

# Make predictions on the test set
y_test_pred = nb_classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming y_test and y_test_pred are your test labels and predictions

# Generate confusion matrix
cm = confusion_matrix(y_test, y_test_pred, labels=nb_classifier.classes)

# Convert class labels to strings if they are numeric (replace this with actual class names if needed)
class_names = ['edible', 'not edible']  # Replace these with your actual class names

# Generate classification report
report = classification_report(y_test, y_test_pred, target_names=class_names)

# Print confusion matrix
print("Confusion Matrix:")
print(cm)

# Print classification report
print("\nClassification Report:")
print(report)

# Plotting confusion matrix
plt.figure(figsize=(4, 3))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

from sklearn.metrics import roc_curve, auc

# Compute ROC curve and AUC
fpr, tpr, _ = roc_curve(y_test, y_test_pred)
roc_auc = auc(fpr, tpr)

# Plot ROC curve
plt.figure()
plt.plot(fpr, tpr, color='blue', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc='lower right')
plt.show()

"""### <font color='blue'> Task - 6 [Marks 5] </font>:
Fit a Naive Bayes’ model for this dataset using MixedNB (from the package https://pypi.org/project/mixed-naive-bayes/)


"""

# Solution code

!pip install mixed-naive-bayes

from mixed_naive_bayes import MixedNB

# Initialize and fit the MixedNB model
model = MixedNB()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

"""### <font color='blue'> Task - 7 [Marks 2] </font>:

Compare the performance obtained by your implementation with that obtained using MixedNB
"""

# Solution code

from sklearn.metrics import confusion_matrix, classification_report

from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming y_test and y_test_pred are your test labels and predictions

# Generate confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=nb_classifier.classes)

# Convert class labels to strings if they are numeric (replace this with actual class names if needed)
class_names = ['edible', 'not edible']  # Replace these with your actual class names

# Generate classification report
report = classification_report(y_test, y_pred, target_names=class_names)

# Print confusion matrix
print("Confusion Matrix:")
print(cm)

# Print classification report
print("\nClassification Report:")
print(report)

# Plotting confusion matrix
plt.figure(figsize=(4, 3))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

# Compute ROC curve and AUC
fpr, tpr, _ = roc_curve(y_test, y_pred)
roc_auc = auc(fpr, tpr)

# Plot ROC curve
plt.figure()
plt.plot(fpr, tpr, color='blue', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc='lower right')
plt.show()
