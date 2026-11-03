
import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


def evaluate_model(model, X_test, y_test):
    device = next(model.parameters()).device

    X_test = torch.as_tensor(X_test, dtype=torch.float32).to(device)
    y_test = torch.as_tensor(y_test, dtype=torch.long)

    model.eval()

    with torch.no_grad():
        outputs = model(X_test)
        predictions = outputs.argmax(dim=1).cpu().numpy()

    actual = y_test.cpu().numpy()

    accuracy = accuracy_score(actual, predictions)

    print("Test Accuracy:", f"{accuracy:.2%}")
    print("\nClassification Report:")
    print(
        classification_report(
            actual,
            predictions,
            target_names=["Genuine", "Spoof"],
            zero_division=0
        )
    )

    print("Confusion Matrix:")
    print(confusion_matrix(actual, predictions))

    return accuracy
