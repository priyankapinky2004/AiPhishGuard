import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import classification_report, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# Make sure the directories exist
os.makedirs('models/saved', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

def load_and_preprocess_data(file_path='data/raw/phishing_dataset.csv'):
    """
    Load and preprocess the phishing URL dataset
    """
    # Load the dataset
    print(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    
    # Display basic information
    print(f"Dataset shape: {df.shape}")
    print("\nFeature statistics:")
    print(df.describe())
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        print("\nMissing values per column:")
        print(missing_values[missing_values > 0])
        
        # Fill missing values with appropriate strategies
        # For numeric columns, fill with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())
    
    # Split features and target
    X = df.drop(['url', 'is_phishing'], axis=1)
    y = df['is_phishing']
    
    print(f"\nFeatures: {X.columns.tolist()}")
    print(f"Target: is_phishing (0: legitimate, 1: phishing)")
    
    return X, y

def train_and_evaluate_models(X, y, test_size=0.2, random_state=42):
    """
    Train multiple models and evaluate their performance
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define models to evaluate
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=random_state),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=random_state)
    }
    
    # Dictionary to store results
    results = {}
    
    # Train and evaluate each model
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        
        # Train the model
        model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # Store results
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'predictions': y_pred
        }
        
        # Print metrics
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
        
        # Print classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Cross-validation
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
        print(f"\n5-Fold Cross-validation Accuracy: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
    
    # Return the results and test data for further analysis
    return results, X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, scaler

def visualize_results(results, X_test_scaled, y_test):
    """
    Visualize model performance
    """
    # Compare models
    model_names = list(results.keys())
    accuracy_scores = [results[name]['accuracy'] for name in model_names]
    precision_scores = [results[name]['precision'] for name in model_names]
    recall_scores = [results[name]['recall'] for name in model_names]
    f1_scores = [results[name]['f1'] for name in model_names]
    
    # Create a bar chart comparing models
    metrics_df = pd.DataFrame({
        'Accuracy': accuracy_scores,
        'Precision': precision_scores,
        'Recall': recall_scores,
        'F1 Score': f1_scores
    }, index=model_names)
    
    plt.figure(figsize=(10, 6))
    metrics_df.plot(kind='bar', figsize=(10, 6))
    plt.title('Model Performance Comparison')
    plt.ylabel('Score')
    plt.xlabel('Model')
    plt.xticks(rotation=0)
    plt.ylim(0, 1.0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('models/saved/model_comparison.png')
    
    # Plot confusion matrix for the best model
    best_model_name = model_names[np.argmax(f1_scores)]
    best_model_preds = results[best_model_name]['predictions']
    
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, best_model_preds)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Legitimate', 'Phishing'],
                yticklabels=['Legitimate', 'Phishing'])
    plt.title(f'Confusion Matrix - {best_model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('models/saved/confusion_matrix.png')
    
    # Plot ROC curve for each model
    plt.figure(figsize=(8, 6))
    for name, result in results.items():
        model = result['model']
        y_prob = model.predict_proba(X_test_scaled)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.3f})')
    
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('models/saved/roc_curve.png')
    
    # For Random Forest, show feature importance
    if 'Random Forest' in results:
        rf_model = results['Random Forest']['model']
        feature_names = X_test_scaled.shape[1]
        
        # Get feature importances
        importances = rf_model.feature_importances_
        
        # Create a DataFrame for better visualization
        feature_importance_df = pd.DataFrame({
            'Feature': [f'Feature_{i}' for i in range(feature_names)],
            'Importance': importances
        })
        feature_importance_df = feature_importance_df.sort_values('Importance', ascending=False)
        
        # Plot feature importances
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
        plt.title('Feature Importances (Random Forest)')
        plt.tight_layout()
        plt.savefig('models/saved/feature_importances.png')
    
    print("\nVisualization completed. Check the 'models/saved/' directory for plots.")

def save_best_model(results, X, y, scaler):
    """
    Save the best performing model
    """
    # Find the best model based on F1 score
    model_names = list(results.keys())
    f1_scores = [results[name]['f1'] for name in model_names]
    best_model_idx = np.argmax(f1_scores)
    best_model_name = model_names[best_model_idx]
    best_model = results[best_model_name]['model']
    
    print(f"\nBest model: {best_model_name} (F1 Score: {f1_scores[best_model_idx]:.4f})")
    
    # Train the best model on the entire dataset for production
    print("Training the best model on the entire dataset...")
    X_scaled = scaler.transform(X)
    best_model.fit(X_scaled, y)
    
    # Save the model and scaler
    joblib.dump(best_model, 'models/saved/best_model.pkl')
    joblib.dump(scaler, 'models/saved/scaler.pkl')
    
    # Save model info
    model_info = {
        'model_type': best_model_name,
        'accuracy': results[best_model_name]['accuracy'],
        'precision': results[best_model_name]['precision'],
        'recall': results[best_model_name]['recall'],
        'f1': results[best_model_name]['f1']
    }
    pd.DataFrame([model_info]).to_csv('models/saved/model_info.csv', index=False)
    
    print(f"Model and scaler saved to 'models/saved/' directory")
    
    return best_model, scaler

def main():
    """
    Main function to execute the entire pipeline
    """
    print("====== Phishing URL Detection Model Training ======\n")
    
    # Load and preprocess data
    X, y = load_and_preprocess_data()
    
    # Save the processed data
    processed_data = pd.concat([X, y], axis=1)
    processed_data.to_csv('data/processed/processed_data.csv', index=False)
    
    # Train and evaluate models
    results, X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, scaler = train_and_evaluate_models(X, y)
    
    # Visualize results
    visualize_results(results, X_test_scaled, y_test)
    
    # Save the best model
    best_model, scaler = save_best_model(results, X, y, scaler)
    
    print("\n====== Model Training Completed Successfully ======")
    return best_model, scaler, results

if __name__ == "__main__":
    main()