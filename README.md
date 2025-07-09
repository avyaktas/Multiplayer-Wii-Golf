# Multiplayer Wii Golf 

- **Course**: CMU 15-112, Spring '25 term-project (https://www.cs.cmu.edu/~112-s25/)
- **Languages**: Python
- **Technologies**: cmu_graphics, OpenCV, PhyPhox intergration

# Features
- **Multiplayer**: 1–4 players, with custom name input  
- **Motion controls**: Swing the club using smartphone acceleration data via PhyPhox  
- **Full 9-hole course**: Unique hole layouts designed using openCV, pars, and hazards  
- **Full course mapping**: Ability to move around each course using the arrow keys
- **Wind and ground physics**: Realistic wind speed/direction affects ball trajectory, varied bounces with differnt surfaces
- **Scorecard & leaderboard**: See hole-by-hole scores and overall standings culminating in an overall leaderboad  

# Contributions

- Architected and implemented the complete hole-rendering pipeline, mapping OpenCV-generated course contours into CMU Graphics–compatible coordinates for all nine holes.
- Manually designed and optimized each hole outline, then imported and cached them via a high-performance getHoleData function.
- Engineered the 2D grid–based scorecard system, including total-score and over/under calculations, and drew the interactive podium display.
- Built the landing page UI with dynamic player-count selection, name entry, and seamless transitions between landing, scorecard, and hole views.
- Developed robust game-flow controls: start, restart, next-hole, and in-play button hit-detection (e.g. isInPlayButton, isInNextHoleButton).
- Coded input handlers (onMousePress, onKeyPress, onKeyHold) to manage name input, IP address entry, camera-movement controls, and player-alternation logic.
- Created utility graphics functions—drawPolygons, drawCoursePolygon, drawCardButton, drawHoleButton, drawRestartButton—and streamlined redrawing logic in redrawAll.
- Produced and integrated high-resolution hole JPEG assets, optimizing load times and visual fidelity across devices.

# Gameplay and Explanation: 

Here is a video made by my teammate highlighting the gameplay and important characteristics of the game: https://drive.google.com/file/d/1-Jps9EZcox3wfAshlPcyZmjvF6jKSHus/view?usp=sharing

# Setup and Installation

These instructions will get you a copy of the project up and running on your local machine.

### 1. Clone the repo
```bash
git clone https://github.com/avyaktasharma/15-112-s25.git
cd 15-112-s25
2. (Optional) Create & activate a virtual environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
3. Install Python dependencies
Create a requirements.txt at the root with:

text
Copy
Edit
cmu-graphics
numpy
opencv-python
Then run:

bash
Copy
Edit
pip install -r requirements.txt
4. Assets
Make sure you have the assets/ folder with these subdirectories:

bash
Copy
Edit
assets/
├── images/     # all .jpg, .png used by holeSketch & ocean rendering
└── audio/      # .mp3 files for music and sound effects
Your repo already points at them via:

python
Copy
Edit
ASSETS = os.path.join(ROOT, 'assets')
5. Run the app
From the project root:

bash
Copy
Edit
python src/main.py