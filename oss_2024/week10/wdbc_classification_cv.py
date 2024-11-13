import numpy as np
from sklearn import datasets, model_selection, pipeline, preprocessing, ensemble, neighbors
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier, ExtraTreesClassifier, RandomForestClassifier, StackingClassifier, BaggingClassifier, HistGradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

if __name__ == '__main__':
    # Load dataset
    wdbc = datasets.load_breast_cancer()

    # Define base models with initial parameters
    random_forest = RandomForestClassifier(max_depth=10, n_estimators=100, random_state=42)
    gradient_boosting = GradientBoostingClassifier(n_estimators=200, learning_rate=0.01, random_state=42)
    svc = SVC(C=1, probability=True, random_state=42)
    extra_trees = ExtraTreesClassifier(max_depth=5, n_estimators=100, random_state=42)
    knn = neighbors.KNeighborsClassifier(n_neighbors=3)
    logistic = LogisticRegression(max_iter=100, C=10)


    
    # Stack the models with a meta-model
    base_models = [
        ('rf', random_forest),
        ('gb', gradient_boosting),
        ('svc', svc),
        ('et', extra_trees),
        ('knn', knn),
        ('lr', logistic),
    ]

    # Meta-model for stacking
    meta_model = LogisticRegression(max_iter=50, C=1)

    # Define the stacking classifier
    stacking_model = StackingClassifier(estimators=base_models, final_estimator=meta_model, cv=5)

    # Create pipeline with StandardScaler and StackingClassifier
    pipeline_model = pipeline.Pipeline([
        ('scaler', preprocessing.StandardScaler()),
        ('stacking_classifier', stacking_model)
    ])

    # Perform cross-validation with the best model found
    cv_results = model_selection.cross_validate(pipeline_model, wdbc.data, wdbc.target, cv=5, return_train_score=True)

    # Evaluate the optimized ensemble model
    acc_train = np.mean(cv_results['train_score'])
    acc_test = np.mean(cv_results['test_score'])
    print(f'* Accuracy @ training data: {acc_train:.3f}')
    print(f'* Accuracy @ test data: {acc_test:.3f}')
    print(f'* Your score: {max(10 + 100 * (acc_test - 0.9), 0):.0f}')