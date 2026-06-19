# Gabby — YOLO Vision (Teaching a Computer to See the Game)

## What You're Building

You're training a computer to **look at a rhythm game** and **recognize the notes** on screen. Think of it like teaching a dog tricks — you show it lots of examples until it learns what to look for. Once it can "see" the notes, the rest of the team's code will press the right keys automatically.

You'll use **Google Teachable Machine** to do the training — no coding required for that part!

🔗 **Teachable Machine:** https://teachablemachine.withgoogle.com/

---

## Your Working Folders

| Folder | What goes here |
|--------|---------------|
| `app/models/vision/` | Your trained model files + screenshots |
| `app/integrations/yolo/` | Code that uses your model (Dani/Brady will help here) |

---

## Tools You'll Need

| Tool | What it does | How to get it |
|------|-------------|---------------|
| Google Teachable Machine | Train your model (in a web browser, no install) | https://teachablemachine.withgoogle.com/ |
| Snipping Tool / ShareX | Take screenshots of the game | Built into Windows (`Win + Shift + S`) |
| A web browser (Chrome recommended) | Run Teachable Machine | Already installed |

```powershell
# From the project root (Rythm-Game-YOLO/)
python -m venv venv
.\venv\Scripts\Activate.ps1
source venv/Scripts/activate

## Tasks (Do These In Order)

### Task 1: Collect Screenshots from the Game

**Goal:** Get lots of pictures of the game showing different notes.

1. Open the rhythm game and start playing (or watch a YouTube video of gameplay)
2. Use the **Snipping Tool** (`Win + Shift + S`) to screenshot moments when:
   - An **up arrow / note** is on screen
   - A **down arrow / note** is on screen
   - A **left arrow / note** is on screen
   - A **right arrow / note** is on screen
   - **Nothing important** is on screen (just background)
3. Save your screenshots into separate folders like this:
   ```
   app/models/vision/screenshots/
   ├── note_up/        ← put all "up note" screenshots here
   ├── note_down/      ← put all "down note" screenshots here
   ├── note_left/      ← put all "left note" screenshots here
   ├── note_right/     ← put all "right note" screenshots here
   └── nothing/        ← put "no notes / just background" here
   ```
4. **Aim for at least 30 screenshots per folder** (more = better accuracy)

> 💡 **Tip:** The more examples you give the model, the smarter it gets. Try to get screenshots with notes in different positions on screen.

---

### Task 2: Train Your Model on Teachable Machine

**Goal:** Teach the computer to tell the difference between each note type.

- [x] Record gameplay footage from the target rhythm game (screen capture or video files)
- [x] Extract frames at a consistent rate (e.g., every 50ms for fast note detection)
- [ ] Annotate note objects using bounding boxes (LabelImg or Roboflow)
- [ ] Define classes: `note_up`, `note_down`, `note_left`, `note_right` (adjust per game)
- [ ] Split dataset: 80% train / 10% val / 10% test
- [ ] Store dataset config in `app/models/vision/dataset.yaml`

> 🎯 **Goal:** The model should get the right answer at least 8 out of 10 times. If it's making mistakes, add more screenshots of the ones it's confused about and retrain.

---

### Task 3: Export and Save Your Model

**Goal:** Download the trained model so the app can use it.

1. After training, click **"Export Model"**
2. Choose the **"Tensorflow.js"** tab
3. Click **"Download"** — you'll get a `.zip` file
4. Unzip it and put the files in: `app/models/vision/teachable_model/`
   - You should have files like `model.json`, `metadata.json`, and some `.bin` files
5. Also try the **"Tensorflow Lite"** export — save that too as `app/models/vision/model.tflite`

> 📝 Write a short note in `app/models/vision/training_notes.md` about:
> - How many screenshots you used per class
> - How accurate it seemed during testing
> - Any classes it mixed up

---

### Task 4: Test Your Model with New Screenshots

**Goal:** Make sure the model works on images it hasn't seen before.

1. Take **5 brand new screenshots** of each note type (ones you DIDN'T use for training)
2. Save them in `app/models/vision/test_screenshots/`
3. Go back to Teachable Machine and use the preview to test each one
4. Write down how many it got right vs wrong in `training_notes.md`

**What "good enough" looks like:**
- ✅ Gets it right 8+ out of 10 times = Great, move on!
- ⚠️ Gets it right 5-7 out of 10 = Add more training screenshots and retrain
- ❌ Gets it right less than 5 = Ask Dani for help troubleshooting

---

### Task 5: Help Connect It to the App (Team Task)

**Goal:** Work with the team to plug your model into the game automation.

Once your model is exported and accurate, the team will help write Python code that:
1. Captures the game screen automatically
2. Feeds each frame into your model
3. Reads what note type it detected
4. Presses the matching keyboard key

**Your part:** Be available to retrain the model if it's not working well on live gameplay. You might need to add more screenshots of tricky scenarios.

---

## Quick Reference

| Question | Answer |
|----------|--------|
| Where do I train the model? | https://teachablemachine.withgoogle.com/ |
| How do I take screenshots? | `Win + Shift + S` (Snipping Tool) |
| How many screenshots do I need? | At least 30 per class (more is better) |
| Where do I save screenshots? | `app/models/vision/screenshots/<class_name>/` |
| Where does the exported model go? | `app/models/vision/teachable_model/` |
| What if the model isn't accurate? | Add more screenshots and retrain |
| Who do I ask for help? | Dani or Brady |

---

## Notes for the Team

- Gabby's trained model will be in `app/models/vision/teachable_model/` (TF.js) or `app/models/vision/model.tflite` (TFLite)
- Integration code will need to load either the TF.js model (via `@aspect/tfjs` or a Python wrapper) or the TFLite model (via `tflite-runtime`)
- If Teachable Machine accuracy caps out, we can graduate to YOLOv8 training later using the same screenshot dataset Gabby collected
