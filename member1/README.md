# Member 1 – Antony

## Responsibility
Dataset collection, audio preprocessing and Mel spectrogram preparation.

## Tasks
1. Identify genuine and AI-generated voice samples.
2. Organize audio labels.
3. Convert audio to mono.
4. Resample audio to 16000 Hz.
5. Crop or pad audio to 4 seconds.
6. Generate 64-band Mel spectrograms.
7. Prepare processed audio features for Member 2.

## Dataset
ASVspoof 2019 Logical Access (LA).

## Integration
Processed audio features will be compatible with Member 2's PyTorch CNN model.

## Important
Large datasets and model files must not be uploaded directly to GitHub.
