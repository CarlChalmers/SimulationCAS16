# CAS Course: Simulation of Complex Systems
# Group 16
# Group Members: Carl Kylebäck Wennerlöf, Calle Olin, Robin Oscarsson, Miranda Carlsson, Mattias Qian, Youliang Zhu

Basic asuumptions for the model: 
   This project simulates the dynamics of a forest ecosystem, including tree growth, disease spread, vaccination strategies, and cutting-down mechanisms. The simulation is implemented in Python and visualized using `matplotlib`.

Time dimension definition:
   An iteration represents one day. We assume the following timeframes for state transitions: it takes 15 days for a tree to transition from LATENT to SICK, 10 days from SICK to DEAD, and 3 days from DEAD to EMPTY. Since disease propagation occurs in every iteration, it would be unrealistic for a large number of healthy trees to be infected daily. Therefore, we set the probabilities for disease propagation relatively low:
      infect_prob_sick = 0.05  
      infect_prob_latent = 0.02
   We consider the vaccine to be highly effective, with a failure probability of only unsuccessful_vaccination = 0.15. Furthermore, we set latent_days_immune_threshold = 20, meaning that a LATENT tree successfully vaccinated will recover and become healthy after 15 days. During this recovery period, it continues to spread the disease.



## Project Structure

The project is organized as follows:

src/ 
    ├── cutting_down.py # Library for cut down diseased trees prevention method functions, implements tree cutting logic
    ├── forest_model.py # Library for forest modeling functions, core forest simulation logic 
    ├── vaxinate_model.py # Library for vaccination prevention method functions, implements vaccination strategy
test/ 
    ├── cutting_down_test.py #  Tests for cutting_down.py 
    ├── vaxinate_test.py # Tests for vaxinate_model.py 
main.py # Entry point for running the simulation
README.md # Project documentation







