# pyrefly: ignore [missing-import]
import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def prepare_and_scale_data(df: pd.DataFrame, target_column: str= 'status' ):
    """
    Encodes labels, splits data, and scales features.
    """
    # 1. separate features 
    X= df.drop(columns=[target_column])
    y= df[target_column]

    #2 Encode labels 
    le= LabelEncoder()
    y_encoded= le.fit_transform(y)

    #3.split data 
    X_train,X_test,y_train,y_test= train_test_split( X , y_encoded, test_size=0.2 ,random_state=42)

    #4.scale features 
    #Initialize and apply the StandardScaler (only fit on training data)
    scaler= StandardScaler()
    X_train_scaled=scaler.fit_transform(X_train)
    X_test_scaled=scaler.transform(X_test)

    #Convert scaled numpy arrays back to Pandas DataFrames for readability
    X_train_scaled_df= pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled_df= pd.DataFrame(X_test_scaled, columns=X_test.columns)

    return X_train_scaled_df, X_test_scaled_df, y_train, y_test, scaler, le

def train_model(X_train_scaled , y_train):
    """
    Trains a random forest clasifier on our scaled data 
    """

    # 1. Initialize the Model (The "Brain")
    model= RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    #2.train the model 
    print('training the model ...')
    model.fit(X_train_scaled, y_train)
    return model

def evaluate_model(model,X_test_scaled,y_test,le):
    """
    Tests the model on unseen data and prints a performance report.
    """
    print('Evaluating model performance...')
    predictions=model.predict(X_test_scaled)
    
    #  Bring the labels back to words so humans can read the report
    target_names=le.classes_
    print()
  

   