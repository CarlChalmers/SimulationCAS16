# CAS Course: Simulation of Complex Systems Group 16
# Group Members: Carl Kylebäck Wennerlöf, Calle Olin, Robin Oscarsson, Miranda Carlsson, Mattias Qian, Youliang Zhu

## Discuss area:

Make disscussion and comments here.

Comments for code version 2 from kyrie: add loss function and a results file for plots and graphs. Adjust the parameters to make simulation more realistic, details see <time dimension definition> in README.md. And suggest that we can do test in current test files instead of in main.py, like codes in vaxinate_test.py under test folder, we can run this file directly and test it

## Model basic assumptions and prevention methods

### Basic assumptions for the model: 
   Initialize a two-dimensional forest grid with a certain coverage rate, and then randomly introduce diseases to infect 10 trees. The trees have a total of STATES = ["HEALTHY", "LATENT", "SICK", "DEAD", "EMPTY", "IMMUNE_LATENT", "IMMUNE_HEALTHY"]. The various states will transform into each other in each round of iteration. Only trees in latent and sick states will spread the disease. Finally, the simulation stops when there are no trees in sick and latent states.

### Time dimension definition:
   An iteration represents one day. We assume the following timeframes for state transitions: it takes 15 days for a tree to transition from LATENT to SICK, 10 days from SICK to DEAD, and 3 days from DEAD to EMPTY. Since disease propagation occurs in every iteration, it would be unrealistic for a large number of healthy trees to be infected daily. Therefore, we set the probabilities for disease propagation relatively low:
      infect_prob_sick = 0.05  
      infect_prob_latent = 0.02
   We consider the vaccine to be highly effective, with a failure probability of only unsuccessful_vaccination = 0.15. Furthermore, we set latent_days_immune_threshold = 20, meaning that a LATENT tree successfully vaccinated will recover and become healthy after 15 days. During this recovery period, it continues to spread the disease.

### Vaccination prevention method description:
   In each iteration, using the cluster detection method, if it is detected that the cluster formed by a sick tree is larger than a certain value, the healthy trees and latent trees in the perimeter trees of this cluster are vaccinated (only healthy trees can be seen, not latent trees). There is a certain probability that the vaccination fails, and the successfully vaccinated trees will be immune to the disease. The trees that were originally "HEALTHY" will become "IMMUNE_HEALTHY" and will never be infected with the disease again. The trees that were originally "LATENT" will become "IMMUNE_LATENT". After a period of time, "IMMUNE_LATENT" will become "IMMUNE_HEALTHY", but during this period, the disease will still be spread. After becoming "IMMUNE_HEALTHY", it will no longer be infected.

### Cutting down trees prevention method description:
   **** add something here ****



## Project Structure

The project is organized as follows:

src/ ├── cutting_down.py # Library for cut down diseased trees prevention method functions, implements tree cutting logic ├── forest_model.py # Library for forest modeling functions, core forest simulation logic ├── vaxinate_model.py # Library for vaccination prevention method functions, implements vaccination strategy test/ ├── cutting_down_test.py # Tests for cutting_down.py ├── vaxinate_test.py # Tests for vaxinate_model.py main.py # Entry point for running the simulation README.md # Project documentation







