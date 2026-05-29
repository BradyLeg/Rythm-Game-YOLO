# stt

Store local speech-to-text assets and configuration.

What to store
- Whisper-small weights and any tokenizer/asset files required to run locally.
- Mapping configuration files (e.g. `phrase_map.yaml`) that map recognized phrases to normalized action names.
- Example transcripts and test fixtures for unit tests.

Recommendation
- Keep model weights outside version control and document download steps in this folder.
