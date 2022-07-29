# Expert System with Jess in Eclipse - Applied Artificial Intelligence
## Aquaponics expert system

### Domain

The domain of this project is agriculture and sustainability. A widely used technique to grow plants without having to use thousands of land is Hydroponic. Hydroponics is not new. In fact, the earliest records of Hydroponics dated back to the ancient civilizations. And modern Hydroponics has been used widely in the commercial greenhouses as well as at home for over 30 years. 

Deriving from hydroponics there is another technique called Aquaponics. It refers to any system that combines conventional aquaculture (raising aquatic animals such as fish in tanks) with hydroponics (cultivating plants in water) in a symbiotic environment. In normal aquaculture, excretions from the animals being raised can accumulate in the water, increasing toxicity. In an aquaponic system, water from an aquaculture system is fed to a hydroponic system where the by-products are broken down by nitrifying bacteria initially into ammonia, then nitrites and subsequently into nitrates that are utilized by the plants as nutrients. Then, the water is recirculated back to the aquaculture system.

![Image 1](https://github.com/charicf/AI-Fundamentals/tree/main/Expert_System_Jess/images/aqua_img1.png?raw=true)

Aquaponics presents an option for sustainable food production. The system is not very hard to maintain and it could be a solution for areas where growing food traditionally is not possible. People can install the system in their houses and enjoy their own food. Moreover, it does not hurt the environment.

### Variables

There are many variables that influence the system. Most importantly, each one of them contributes to the balance that the symbiotic system needs. The variables are:

* Fishes
* Plants
* Bacteria
* pH of water
* Water Temperature
* Dissolved Oxygen (DO)
* Total nitrogen: ammonia, nitrite, nitrate
* Water hardness, specially carbonate hardness (KH)

For this project, the last 5 will be considered.


### Reasoning task

Aquaponics depends on an equilibrium between the agents involved. Fishes, plants and bacteria are living organisms that depend on each other. However, there is another element that connects them and therefore it is of great importance. Water is the blood of the system. It transports elements from the fishes to bacteria and then to the plants. 
A system like this one requires different reasoning tasks. One of them is the control and surveillance of the water. This is the task that is going to be automated. 

The main elements that need to be analyzed are pH of water, water temperature, dissolved oxygen, total nitrogen (ammonia, nitrite, nitrate) and water hardness (carbonate hardness). 

Each one of these variables have a range so that the system can function. These values are obtained from compromising each one of them to obtain the best efficiency. The optimal values are shown in the next table.
 
![Image 2](https://github.com/charicf/AI-Fundamentals/tree/main/Expert_System_Jess/images/aqua_img2.png?raw=true)
*Ammonia and Nitrite can be between 0 and 1

As it is expected, having these many variables is complicated for constructing an Expert System. Therefore, the project will be focused in major cases that have been identified in the literature. These cases were considered to construct the rules of the system. They are shown in the following table.
 
![Image 3](https://github.com/charicf/AI-Fundamentals/tree/main/Expert_System_Jess/images/aqua_img3.png?raw=true)

## Instructions
This project uses Jess rule engine to construct an expert system. You should have Eclipse Jess plugin. To run the expert system:

* Copy the file aqua_sys.clp to the bin folder of jess directory
* Run Eclipse, open Jess and execute “batch aqua_sys.clp”
* Give the inputs and you will be able to see the respective output

### Example cases
The program will ask for 4 initial values. Then, depending on the values it might ask for others.

#### 1.	Temperature is high

Temperature has a strong relationship with the amount of Oxygen that the water can have. If temperature increases, the dissolved oxygen decreases. This is toxic for the fishes and it causes a low absorption for plants.

Once the program has started please enter the following values:
![Image 4](https://github.com/charicf/AI-Fundamentals/tree/main/Expert_System_Jess/images/aqua_img4.png?raw=true)

Then enter: 
![Image 5](https://github.com/charicf/AI-Fundamentals/tree/main/Expert_System_Jess/images/aqua_img5.png?raw=true)

#### 2.	Temperature and pH are high
Temperature and pH are very important for the system. They have a strong relationship with the Nitrogen cycle and therefore with the nutrients for plants. If they are high the ammonia is not well processed and it becomes toxic.

Once the program has started please enter the following values:
![Image 6](https://github.com/charicf/AI-Fundamentals/tree/main/Expert_System_Jess/images/aqua_img6.png?raw=true)

Then enter:
![Image 7](https://github.com/charicf/AI-Fundamentals/tree/main/Expert_System_Jess/images/aqua_img7.png?raw=true)

#### 3.	All values are between ranges
The goal of the expert system is to maintain the balance and inform if something is wrong. If all variables are within ranges, the system should be in balance. 

Once the program has started please enter the following values:
![Image 8](https://github.com/charicf/AI-Fundamentals/tree/main/Expert_System_Jess/images/aqua_img8.png?raw=true)

Finally, it is important to remember that the system will return an output if the cases that were taken into account are provided.


## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)