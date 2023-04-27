"""
Author Name: Dheeraj Tommandru
E-mail: dtomman1@binghamton.edu/dheerajtls1234@gmail.com
Description:
This model is a variation of Rob Axtell's and Joshua Epstein's basic Sugarscape Model.
The agents in this model produce vinegar when they move to specific location.
The agents prioritize the locations with less vinegar within their possible location within the vision.
The Vinegar also has healing capacity and each position has maximum capacity it holds the vinegar just like the sugar.

"""

import pycxsimulator
from pylab import *
from itertools import product
import random
from scipy.stats import multivariate_normal
from scipy.stats import randint as rd



x_lim,y_lim = 50,50
num_agents = 400

def mirrorImage( a, b, c, x1, y1):
    temp = -2 * (a * x1 + b * y1 + c) /(a * a + b * b)
    x = temp * a + x1
    y = temp * b + y1
    return (x, y)


class agent:
    pass

def initialize():
    global sugar, agents, wealth, deathcount, available_positions,sugar_positions,wealth,acount,vinegar,vinegar_positions
    agents = [agent() for i in range(num_agents)]
    vinegar = []
    sugar = []
    a,b = np.arange(x_lim),np.arange(y_lim)
    available_positions = set(product(a, b))
    # assign genetic properties and initial positions to agents
    for ag in agents:
        #print(len(available_positions))
        element = random.randrange(0, len(available_positions))
        ap = {i:key for i,key in enumerate(available_positions)}
        available_positions.discard(ap[element])
        ag.x,ag.y  = ap[element]
        ag.metabolism = random.randint(50, 90)
        ag.sugar = random.randint(200,300)
        ag.vision = random.randint(3,10)
        ag.vinegar_tolerance =  random.randint(1,10)
        ag.vinegar_production = random.randint(10,15)
        ap = None

    sugar_positions = {}
    vinegar_positions= {}

    for x in range(x_lim):
        for y in range(y_lim):
            sugar.append(agent())
            vinegar.append(agent())
            sugar[-1].x, sugar[-1].y = x,y
            sugar_positions[(x,y)] = len(sugar)-1
            sugar[-1].max_capacity = random.randint(2,10)
            sugar[-1].growth_rate = random.randint(20,50)

            vinegar[-1].x, vinegar[-1].y = x,y
            vinegar_positions[(x,y)] = len(sugar)-1
            vinegar[-1].available_vinegar = random.normalvariate(10,25)
            vinegar[-1].max_capacity = random.normalvariate(40,50)
            vinegar[-1].healing_rate = 5
            if x <= 24 and y <= 24:
                rv = multivariate_normal([37,37], [[24, 0], [0, 24]])
                x_m , y_m = mirrorImage(1,1,-50,x,y)
                sugar[-1].available_sugar =int(np.round(rv.pdf([(abs(x_m)-1) , (abs(y_m)-1)])*100000,0))
                sugar[-1].growth_rate = int(np.round(rv.pdf([(abs(x_m)-1) , (abs(y_m)-1)])*100000,0))
                sugar[-1].max_capacity = sugar[-1].available_sugar+sugar[-1].growth_rate
            elif x > 24 and y <= 24:
                sugar[-1].available_sugar = rd.rvs(0, 5, size=1)[0]
                sugar[-1].growth_rate = random.randint(0,3)
                sugar[-1].max_capacity = sugar[-1].available_sugar+sugar[-1].growth_rate

            elif x <= 24 and y > 24: 
                sugar[-1].available_sugar = rd.rvs(0, 4, size=1)[0]
                sugar[-1].growth_rate = random.randint(0,2)
                sugar[-1].max_capacity = sugar[-1].available_sugar+sugar[-1].growth_rate

            else:
                rv = multivariate_normal([37, 37], [[24, 0], [0, 24]])
                sugar[-1].available_sugar =int(np.round(rv.pdf([x,y])*100000,0))
                sugar[-1].growth_rate = int(np.round(rv.pdf([x,y])*100000,0))
                sugar[-1].max_capacity = sugar[-1].available_sugar+sugar[-1].growth_rate


    wealth = [agent.sugar for agent in agents]
    deathcount = [0]
    acount = [len(agents)]




def observe():
    global sugar, agents, wealth, deathcount, available_positions,wealth,sugar_positions,acount,vinegar,vinegar_positions
    subplot(1, 3, 1)
    cla()
    scatter([a.x for a in agents], [a.y for a in agents],c = [a.sugar for a in agents])
    axis('image')
    xlim([0, 49])
    ylim([0, 49])
    xticks([])
    yticks([])
    subplot(1, 3, 2)
    cla()
    scatter([s.x for s in sugar], [s.y for s in sugar],c = [s.available_sugar for s in sugar],cmap="jet")
    title('Sugar Distribution')
    axis('image')
    xlim([0, 49])
    ylim([0, 49])
    xticks([])
    yticks([])
    subplot(1, 3, 3)
    cla()
    scatter([v.x for v in vinegar], [v.y for v in vinegar],c = [v.available_vinegar for v in vinegar],cmap="coolwarm")
    title('Vinegar Distribution')
    axis('image')
    xlim([0, 49])
    ylim([0, 49])
    xticks([])
    yticks([])





def update():
    global sugar, agents, wealth, deathcount, available_positions, wealth,sugar_positions,acount,vinegar,vinegar_positions
        
    dcount = 0
    for a in agents[:]:
        if (a.sugar <= 0):
            current_position = (a.x,a.y)
            agents.remove(a)
            if random.random() > 0.1:
                new_agent = agent()
                new_agent.x,new_agent.y  = current_position
                new_agent.metabolism = random.randint(1, 5)
                new_agent.sugar = random.randint(50,100)
                new_agent.vision = random.randint(1,4)
                new_agent.life = rd.rvs(50,100,size=1)[0]
                new_agent.age = 0
                new_agent.vinegar_tolerance =  random.randint(1,10)
                new_agent.vinegar_production = random.randint(10,15)
                agents.append(new_agent)
            else:
                available_positions.add(current_position)
            dcount = dcount+1

            
        else:
            current_position = (a.x,a.y)
            #print("Current Position",current_position)
            neighbourhood_sugar_availability = {}
            neighbourhood_sugar_availability[current_position] = sugar[sugar_positions[(a.x,a.y)]].available_sugar
                                                                        
            for prospective_x in range(current_position[0] - a.vision, current_position[0] + a.vision+1):
                for prospective_y in range(current_position[1] - a.vision, current_position[1] + a.vision+1): 
                    if prospective_x > x_lim-1:
                        prospective_x = prospective_x - x_lim
                    if prospective_y > y_lim-1:
                        prospective_y = prospective_y - x_lim
                    if prospective_x < 0:
                        prospective_x = x_lim - prospective_x
                    if prospective_y < 0:
                        prospective_y = y_lim - prospective_y
                    if ((prospective_x,prospective_y) in available_positions) and ((prospective_x == current_position[0]) or (prospective_y == current_position[1]) and (sugar[sugar_positions[(prospective_x,prospective_y)]].available_sugar > 100)):
                            neighbourhood_sugar_availability[(prospective_x,prospective_y)] = sugar[sugar_positions[(prospective_x,prospective_y)]].available_sugar
            
            max_sugar_index = list(neighbourhood_sugar_availability.values()).index(max(list(neighbourhood_sugar_availability.values())))
            max_sugar_position = list(neighbourhood_sugar_availability.keys())[max_sugar_index]
            
            if random.random() > 0.6:
                if len(neighbourhood_sugar_availability) != 1:
                    while (vinegar[vinegar_positions[max_sugar_position]].available_vinegar > a.vinegar_tolerance):
                        del neighbourhood_sugar_availability[max_sugar_position]
                        max_sugar_index = list(neighbourhood_sugar_availability.values()).index(max(list(neighbourhood_sugar_availability.values())))
                        max_sugar_position = list(neighbourhood_sugar_availability.keys())[max_sugar_index]
                        if len(neighbourhood_sugar_availability) == 1:
                            break

            #print("Next Position",max_sugar_position)
            available_positions.discard(max_sugar_position)
            a.x , a.y = max_sugar_position
            available_positions.add(current_position)
            a.sugar = a.sugar - a.metabolism
            sugar[sugar_positions[max_sugar_position]].available_sugar = sugar[sugar_positions[max_sugar_position]].available_sugar - 100
            vinegar[vinegar_positions[max_sugar_position]].available_vinegar = vinegar[vinegar_positions[max_sugar_position]].available_vinegar + a.vinegar_production

            a.sugar = a.sugar + 100

    wealth = [agent.sugar for agent in agents]
    deathcount.append(dcount)
    acount.append(len(agents))


            

    for s in sugar:
        s.available_sugar = min(s.available_sugar + s.growth_rate, s.max_capacity)

    for v in vinegar:
        if v.available_vinegar > 0:
             v.available_vinegar = v.available_vinegar - v.healing_rate
        else:
            v.available_vinegar = max(v.available_vinegar - v.healing_rate,v.max_capacity)



    
    # update acceleration and state
    
        
       
    
        
    # update observations
    #acount.append(len([a for a in agents if a.s == 0]))

pycxsimulator.GUI().start(func=[initialize, observe, update])
