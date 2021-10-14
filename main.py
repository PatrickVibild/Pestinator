from src.engine import Engine
from src.pestinator.action.random_agent import RandomAgent

if __name__ == '__main__':
    sim_engine = Engine()
    agent = RandomAgent(4, 4, 1200, 1000)
    sim_engine.add_agent(agent)
    sim_engine.run()
