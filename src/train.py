
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from src.model import VoiceDetectionCNN


def train_model(X_train, y_train, X_val, y_val,
                epochs=10, batch_size=32, learning_rate=0.001):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    X_train = torch.as_tensor(X_train, dtype=torch.float32)
    y_train = torch.as_tensor(y_train, dtype=torch.long)
    X_val = torch.as_tensor(X_val, dtype=torch.float32)
    y_val = torch.as_tensor(y_val, dtype=torch.long)

    train_loader = DataLoader(
        TensorDataset(X_train, y_train),
        batch_size=batch_size,
        shuffle=True
    )

    model = VoiceDetectionCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        model.eval()
        with torch.no_grad():
            outputs = model(X_val.to(device))
            predictions = outputs.argmax(dim=1)
            accuracy = (
                predictions == y_val.to(device)
            ).float().mean().item()

        print(
            f"Epoch {epoch + 1}/{epochs} | "
            f"Loss: {total_loss / len(train_loader):.4f} | "
            f"Validation accuracy: {accuracy:.2%}"
        )

    return model


def save_model(model, path="member2_model.pth"):
    torch.save(
        {"model_state_dict": model.state_dict()},
        path
    )
    print(f"Model saved to {path}")
