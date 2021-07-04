# Introduction

This file will attempt to track development of this repo.

## Timeline

### 4_18_21

Reading through old Distributed Systems and Sensor Networks (**DSSN**) project. Initial project proposal copied below.

#### Initial Project Proposal Review

```
October 21, 2016

Mobile Communication Network for Moving Targets
```

The date on the final project presentation is *December 12, 2016* which gives ~60-ish days that I could have worked on this. The final project title was **Flexible Network Simulation** which is a more succint title than this original one and was a pretty difficult/good experience. I'm looking to translate the code from Matlab to Python.

```
The goal of this project will be to simulate a distributed node network that provides communication support for multiple targets moving throughout the network, while also attempting to have the node network track target movement. The nodes in the network will be capable of movement in order to support targets that begin to move outside the range of the network.
```

Same stuff, more words. The second sentence is more interesting and seems to be talking about swarm movement of a drone network.

```
The motivation and underlying example that will be focused on is the idea of military/search and rescue application. It can be imagined as multiple teams with certain short range communication moving through an area supported by a network of drones, such that the drones can establish connections between distant teams and also move with the target teams such that communication between them is always possible.
```

It's useful to provide examples of why you're building what you're building but I would encourage more positive/interesting scenarios than *military applications*. Who likes the idea of military with drones. When I recreate this, I want to take a more defender role to the same thing I am proposing. *Simulating a flexible network hiding from another flexible network.*

```
The approach to this project will follow basic steps in building up the functionality of the network algorithm. 

First, I will make simplifying assumptions regarding node architecture and capabilities to appropriately frame the project’s scope and incorporate those decisions into the analysis of the system later. 
```

Lord I am wordy.

```
The next step will involve researching potential tracking algorithms and assessing which would provide the best functionality for a mobile communications network. Once an appropriate algorithm is selected, I will build simulations in Matlab to model its performance for multiple scenarios. 

After I have ensured the tracking algorithm is in place, the next research will focus on routing algorithms and establishing shortest path communications between the moving targets.

I will attempt to analyze the various options for viability based on robustness and speed, and will note energy consumption as well but do not expect it to be the main qualifying factor. 

Once the routing method is established, I will again simulate it in Matlab for the same tracking scenarios and ensure communication between all targets is consistent. 

Finally, I will decide a method for the nodes to move with the targets such that communication between all targets is maintained. 
```

Since I'm going in reverse here, I'll be re-implementing the simulation and provided behavior. After it's working, I can understand and compare tracking algorithms.

```
I expect to do research into basic swarm movement and theory, with direction for the swarm to move based on local target movement and node switching to be based on either entire node migration or independent movement of unused nodes. 

I will also do some small level research into drone capabilities to find out what kind of energy consumption this kind of application would cost, in order to have more accurate simulations. 

I will analyze the requirements and energy costs of the implementations and ideally have an entire simulation of the three converging algorithms/principles in Matlab for multiple example scenarios.
```

Let's find out how well these expectations held out. x.x

### 7_3_21

Coming back to this, I see that I may have completed some amount of the Python to a running status, though remains to be seen how well and to what end.

I've had thoughts about expanding the basic knowledge in this repo to cover silicon/transistor basics so I can have some sort of personalized math tool to evaluate that kind of information. I think I would need to rearrange this documentation structure to support that but minor stuff.

I really need to get a visualization up for this, I think it was probably running before. I accidentally ran it in Python2 and cleaned up some Int conversion stuff that I imagine Python3 is handling implicitly until I got to a library problem that became fixed by actually running in Python3.
That said, I need the visual in order to check that messages are set or something.


#### Project Initial Presentation

5 slides that collapse the above text into a Powerpoint presentation.

#### Python Implimentation