# ⚽ CV Botão - Retro Soccer with Computer Vision

Experience a classic game of pocket soccer (futebol de botão) enhanced by modern **Computer Vision** technology. Control your team with a simple pinch of your fingers and lead them to victory!

---

## 🚀 Features

- **Gesture Control**: Use your bare hands to play! Pinched fingers allow you to drag and release players with physical feedback.
- **Realistic Physics**: Built-in collision detection and friction simulation provide an authentic "on-the-grass" feel.
- **Strategic Formations**: Default 2-1-2 formation inspired by *Soccer Stars* for balanced defense and attack.
- **Configurable Teams**: Easily change team names and visual assets in the configuration file.
- **Immersive Effects**: Smooth animations, firework celebrations for goals, and retro sound effects.
- **Real-time PiP**: Monitor your hand detection stream in a sleek Picture-in-Picture window.

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [repository-url]
   cd CVButtonGame
   ```

2. **Create and activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the ML Model**:
   The game requires the MediaPipe Hand Landmarker model. It should be placed in the `assets/` directory.
   ```bash
   wget -P assets https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
   ```

---

## 🎮 How to Play

1. **Run the game**:
   ```bash
   python main.py
   ```
2. **The Goal**: Scorer the maximum number of goals (default 3) to win the match.
3. **Controls**:
   - Align your hand with the camera.
   - **Pinch** (thumb and index finger meeting) near a player of your color to select them.
   - **Drag** back to set the kick force and direction (indicated by an aim line).
   - **Release** the pinch to execute the move!
4. **Turns**: The game alternates turns between Team A and Team B. The current turn is displayed at the bottom of the screen.

---

## ⚙️ Configuration

Open `config.py` to customize your experience:
- `TEAM_A_NAME` / `TEAM_B_NAME`: Change the display names.
- `MAX_GOALS`: Adjust the match length.
- `FIELD_FRICTION`: Fine-tune the physics.
- `CV_SMOOTH_FACTOR`: Adjust hand tracking responsiveness.

---

## 🎨 Credits
**Developed by**: Renato Gritti
**Version**: 2.0.1
**Engine**: Pygame + OpenCV + MediaPipe
