# pyrefly: ignore [missing-import]
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

def prepare_data(df: pd.DataFrame, target_column: str = 'status'):
    """
    Encodes labels and splits the RAW data. 
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test, label_encoder


def tune_and_train_pipeline(X_train, y_train):
    """
    Creates a pipeline and uses RandomizedSearchCV to find the best ML settings.
    """
    pipeline = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(random_state=42)) 
    ])
    
    param_distributions = {
        'classifier__n_estimators': [50, 100, 200],
        'classifier__max_depth': [None, 10, 20, 30],
        'classifier__min_samples_split': [2, 5, 10]
    }
    
    searcher = RandomizedSearchCV(
        estimator=pipeline, 
        param_distributions=param_distributions,
        n_iter=5,              
        cv=3,                  
        scoring='f1_macro',    
        random_state=42,       
        n_jobs=-1              
    )
    
    print("Hunting for the best Random Forest settings... (This may take a few minutes)")
    searcher.fit(X_train, y_train)
    
    print(f"\nThe Winning Settings: {searcher.best_params_}")
    
    return searcher.best_estimator_


from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_pipeline(pipeline, X_test, y_test, label_encoder):
    """
    Evaluates the unified pipeline on the raw test data and plots a confusion matrix.
    """
    print("\nEvaluating pipeline...")
    predictions = pipeline.predict(X_test)
    
    target_names = label_encoder.classes_
    
    print("\n--- PIPELINE EVALUATION REPORT ---")
    print(classification_report(y_test, predictions, target_names=target_names))
    
    # Extract specific Recall for the system (assuming 'Failed' or similar is in our labels)
    # Average='macro' means it treats all classes equally, which is good for severe class imbalance.
    macro_precision = precision_score(y_test, predictions, average='macro')
    macro_recall = recall_score(y_test, predictions, average='macro')
    
    print(f"\nOverall System Precision: {macro_precision:.3f} (When it cries wolf, how often is it right?)")
    print(f"Overall System Recall: {macro_recall:.3f} (How many REAL failures did it successfully catch?)")
    print("In aviation, we want Recall to be as close to 1.0 as absolutely possible!")
    
    # 7. Generate and save the Confusion Matrix Plot
    cm = confusion_matrix(y_test, predictions)
    plt.figure(figsize=(8, 6))
    
    # Seaborn makes beautiful heatmaps out of confusing number grids
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=target_names, yticklabels=target_names)
    
    plt.title('Hydraulic System Prediction Confusion Matrix')
    plt.ylabel('Actual True Status')
    plt.xlabel('AI Predicted Status')
    plt.tight_layout()
    
    # Save the plot instead of flashing it on screen, so you can review it!
    plt.savefig('confusion_matrix_results.png')
    print("\n[!] Confusion Matrix visual plot saved to 'confusion_matrix_results.png'")
