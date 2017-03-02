# AIsteroids
### An artificial Intelligence agent for playing asteroids.
In this project, we are developing a self-playing asteroids game, using a reinforcement learning strategy called Q-learning. As the game progresses, each game state (s) is calculated and the learning agent must then make a choice for what action (a) the ship is to do next to bring it to a state prime (s'). From s' we can then measure what the preferred choice for the next action a' as the agent learns what to do. 

Usually, this type of learning is taught on a grid, where each square on the grid will have 4 actions that may be chosen given the state of the game at that time. Here, we are attempting to let other game attributes (whether an asteroid is near, or whether the ship has collided with an asteroid) as parts of the state. The ship is free to move anywhere in it's 2D world, and of course shoot.

The game itself was created in Python as part of a class from Rice University, and then modified to run outside of it's normal environment [CodeSkulptor](http://www.codeskulptor.org/), which is an online wrapper around Python 2, by using [SimpleGUICS2Pygame](https://bitbucket.org/OPiMedia/simpleguics2pygame). If you are taking the online Coursera course, the code likely won't help you, it's been changed quite a bit. SimpleGUICS2Pygame module utilizes [PyGame](http://www.pygame.org/lofi.html). 

### Resources
- CS188 Intro to AI from the University of California Berkeley 
- An Introduction to Interactive Programming in Python from Rice University / Coursera

### Developers
- Michael Liu [GitHub](https://github.com/mikey084) [LinkedIn](https://www.linkedin.com/in/michael-liu-b07446b5/)
- David Shin [GitHub](https://github.com/datadaveshin/) [LinkedIn](https://www.linkedin.com/in/davidshin1/)
