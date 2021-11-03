import pygame


class Engine:
    agents = []
    x_dim: int
    y_dim: int

    def __init__(self):
        self.x_dim = 1200
        self.y_dim = 1000
        self.win = None

    def add_agent(self, agent):
        self.agents.append(agent)

    def run(self):
        pygame.init()
        self.win = pygame.display.set_mode((self.x_dim, self.y_dim))
        pygame.display.set_caption("Pestinator")

        # object current co-ordinates
        x = 600
        y = 600

        # dimensions of the object
        width = 5
        height = 5

        # velocity / speed of movement
        vel = 3

        # Indicates pygame is running
        run = True

        # infinite loop
        while run:
            # creates time delay of 10ms
            pygame.time.delay(10)

            # iterate over the list of Event objects
            # that was returned by pygame.event.get() method.
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # it will make exit the while loop
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and x > 0:
                x -= vel

            if keys[pygame.K_RIGHT] and x < self.x_dim - width:
                x += vel

            if keys[pygame.K_UP] and y > 0:
                y -= vel

            if keys[pygame.K_DOWN] and y < self.y_dim - height:
                y += vel

            # fill the screen with black
            self.win.fill((0, 0, 0))

            # drawing object on screen which is rectangle here
            pygame.draw.rect(self.win, (255, 0, 0), (x, y, width, height))
            # make individual actions from agents.
            self.__run_agents()
            # it refreshes the window
            pygame.display.update()

        # closes the pygame window
        pygame.quit()


    def __run_agents(self):
        for agent in self.agents:
            agent.action(self.win)
