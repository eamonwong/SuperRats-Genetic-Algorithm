# SuperRats-Genetic-Algorithm 🐀⚡
A Python-PyGame genetic algorithm simulation, inspired by "Breeding Giant Rats with Genetic Algorithms" from "Impractical Python Projects" by Lee Vaughan, that evolves rats to reach an enormous 50,000g weight goal! Watch natural selection in action as you breed, mutate, and select the fittest rats across generations.

# Features ✨
## 🧬 Genetic Algorithm Core
- Natural Selection: Keep only the fittest 50% of rats for breeding
- Smart Breeding: Offspring inherit traits from both parents with weighted averages
- Controlled Mutation: 15% mutation rate with 0.7-1.5x weight changes
- Elite Preservation: Best performers carry over to next generations unchanged

## 🎮 Interactive Simulation
- Real-time Visualization: Watch rats move and grow with size proportional to weight
- Auto-advance: Generations progress automatically every 2 seconds
- Manual Control: Pause/resume, adjust speed, or step through generations manually
- Progress Tracking: Live graphs show average and maximum weight progression

## 📊 Analytics & Feedback
- Dual Graph System: Track both average population weight and maximum individual weight
- Goal Progress Bar: Visual indicator showing proximity to 50,000g target
- Generation Statistics: Real-time display of population metrics and evolutionary progress
- Success Detection: Automatic celebration when super rats reach the goal!

# Technologies Used 🛠️
| Component	| Description |
| ---- | ---- |
| Python 3.9+	| Core simulation logic and genetic algorithms |
| PyGame | Interactive visualization and user interface |
| Statistics | Population metrics and fitness calculations |
| Random	| Genetic variation and mutation simulation |
| Math | Movement algorithms and graphical calculations |

# How It Works 🔬
## 🧪 The Genetic Process
- Initialisation: Create initial population with triangular weight distribution (200-600g)
- Selection: Retain top 50% of rats by weight for breeding
- Crossover: Breed pairs to produce offspring with blended traits
- Mutation: Randomly alter weights with controlled probability and range
- Evaluation: Measure fitness and repeat until goal is achieved

# ⚙️ Simulation Parameters

```bash
python
GOAL = 50000                # Target weight in grams
num_rats = 20               # Population size
mutate_odds = 0.15          # 15% mutation chance
mutate_range = (0.7, 1.5)   # Mutation strength
litter_size = 12            # Offspring per breeding pair
litters_per_year = 12       # Generations per simulated year
```

# Installation & Setup 🚀
## Prerequisites

```bash
pip install pygame
```

Running the Simulation
```bash
python super_rats_simulation.py
```

# Controls 🎮
- Pause/Resume: Freeze or continue the simulation
- Speed +/-: Adjust simulation speed (0.5x to 5x)
- Reset: Start over with new random population
- Next Generation: Manually advance one generation

# Why This Project? 🎯
## The Scientific Inspiration
Genetic algorithms mimic natural evolution to solve optimisation problems. This project demonstrates:
- Selection Pressure: How environmental goals drive evolutionary change
- Genetic Diversity: The importance of mutation and variation
- Convergence: Populations adapting toward specific objectives

## Educational Value
- Visual Learning: See abstract genetic concepts in action
- Parameter Experimentation: Test how mutation rates and selection strategies affect evolution
- Algorithm Understanding: Learn how fitness functions drive optimization

# Performance Notes ⚡
## Expected Results
- **Generations to Goal**: ~100-200 generations with optimized parameters
- **Time to Success**: 3-8 minutes of simulation time at default speed
- **Visual Feedback**: Clear progression visible in both graph and rat sizes

# Future Enhancements 🌟
## Planned Features
- Multiple Traits: Add metabolism, appetite, and lifespan genetics
- Environmental Factors: Food availability, predation risk, disease pressure
- Advanced Selection: Tournament selection, fitness-proportional methods
- Data Export: Save simulation results for analysis
- Educational Mode: Step-by-step explanations of genetic concepts

# Research Applications
- Parameter Optimisation: Find ideal mutation rates and selection strategies
- Convergence Studies: Analyze how quickly populations adapt to goals
- Diversity Metrics: Measure genetic variation throughout evolution

  <img width="1002" height="692" alt="Screenshot 2025-09-13 at 10 39 18" src="https://github.com/user-attachments/assets/140f3e59-aede-41bf-979d-74e7b3f32932" />


https://github.com/user-attachments/assets/b2453293-aad2-43dc-9d8f-e87a12abd50f


