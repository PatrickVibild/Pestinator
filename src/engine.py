import pygame


class Engine:
    agents = []
    x_dim: int
    y_dim: int

    def drawGrid(self, width, height):
        for x in range(0, width, self.blockSize):
            for y in range(0, height, self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.win, self.WHITE, rect, 1)

    def __init__(self):
        self.drone_fuel = 100
        self.x_dim = 800
        self.y_dim = 600
        self.win = None
        self.BLACK = (0, 0, 0)
        self.WHITE = (200, 200, 200)
        self.blockSize = 20  # Set the size of the grid block
        self.drone_width = 5
        self.drone_height = 5
        self.drone_x = 10
        self.drone_y = 10
        self.next_grid_x = 0
        self.next_grid_y = 0
        self.grid_column = 1
        self.last = pygame.time.get_ticks()
        self.pause = 2000
        self.scan = False

    def add_agent(self, agent):
        self.agents.append(agent)

    def flying(self):
        if self.drone_x < int(self.next_grid_x):
            self.drone_x += 1
        elif self.drone_x > int(self.next_grid_x):
            self.drone_x -= 1
        if self.drone_y < int(self.next_grid_y):
            self.drone_y += 1
        elif self.drone_y > int(self.next_grid_y):
            self.drone_y -= 1
        else:
            self.scan = True

    def fly_to(self, drone_x, drone_y):
        self.flying()
        pygame.draw.rect(self.win, (255, 0, 0), (drone_x, drone_y, self.drone_width, self.drone_height))

    def go_next_field(self, drone_x, drone_y):
        if drone_y < self.y_dim - int(self.blockSize - self.drone_width / 2) and self.grid_column % 2 == 1:
            # print("y-field: " + str(self.y_dim-int(self.blockSize/2 - self.drone_width/2)))
            self.next_grid_y += 20
        elif drone_y > int(self.blockSize / 2 - self.drone_width / 2) and self.grid_column % 2 == 0:
            self.next_grid_y -= 20
        elif drone_y >= self.y_dim - int(self.blockSize - self.drone_width / 2) \
                or drone_y <= int(self.blockSize / 2 - self.drone_width / 2):
            self.next_grid_x += 20
            self.grid_column += 1

    def scanning(self, drone_x, drone_y):
        now = pygame.time.get_ticks()
        if now - self.last >= self.pause:
            self.last = now
            self.go_next_field(drone_x, drone_y)
            self.scan = False

    def run(self):
        pygame.init()
        self.win = pygame.display.set_mode((self.x_dim, self.y_dim))
        pygame.display.set_caption("Pestinator")

        self.drawGrid(self.x_dim, self.y_dim)
        # object current co-ordinates

        # dimensions of the object
        width = 5
        height = 5

        # velocity / speed of movement
        vel = 3

        # fuel for the drone
        drone_fuel = 1000

        # Indicates pygame is running
        run = True

        # starting to fly the Drone
        start = False

        self.next_grid_x = self.blockSize/2 - self.drone_width/2
        self.next_grid_y = self.blockSize/2 - self.drone_height/2
        print("next x: " + str(self.next_grid_x))
        print("next y: " + str(self.next_grid_y))

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

            # keys = pygame.key.get_pressed()

            # fill the screen with black
            self.win.fill((0, 0, 0))
            self.drawGrid(800, 600)

            # drawing object on screen which is rectangle here
            self.fly_to(self.drone_x, self.drone_y)

            # simulates scanning and gives the next coordinates for the drone to fly to
            if self.scan:
                self.scanning(self.drone_x, self.drone_y)

            # make individual actions from agents.
            self.__run_agents()
            # drone losing fuel as it flies

            # if the drone starts moving, then it will start losing fuel
            if start:
                drone_fuel -= 0.1

            # when fuel reaches 0 it will stop using fuel
            if drone_fuel == 0:
                start = False

            # it refreshes the window
            pygame.display.update()

        # closes the pygame window
        pygame.quit()

    def __run_agents(self):
        for agent in self.agents:
            agent.action(self.win)
