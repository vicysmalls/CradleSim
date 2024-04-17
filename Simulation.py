from Pendulum import*


class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ball_radius = width * 0.025
        self.pendulums = []
        right_strings = [0.6]
        left_strings = [0.4, 0.45, 0.5, 0.55]
        strings = [0.4, 0.45, 0.5, 0.55, 0.6]
        colors = ['white', 'white', 'white', 'white', 'white']
        # self.pendulum_init(colors, strings, 0)
        self.pendulum_init(colors, left_strings, 0)
        self.pendulum_init(['white'], right_strings, math.pi / 2)

        # Variables for collision logic
        self.no_left_ball = False
        self.no_right_ball = False

    def pendulum_init(self, colors, strings, starting_theta):
        for index in range(0, len(strings)):
            self.pendulums.append\
            (Pendulum(self.width * strings[index], self.height * 0.5,
                      radius=self.ball_radius, color=colors[index],
                      a=starting_theta))


    def moving_logic(self, surface):
        for pendulum in self.pendulums:
            pendulum.step()
            pendulum.draw(surface)

    def distance(self, pendulum1, pendulum2):
        x_dif = pendulum2.x - pendulum1.x
        y_dif = pendulum2.y - pendulum1.y
        dist = np.sqrt(x_dif**2 + y_dif**2)
        return dist

    def ball_position_check(self, index):
        # Check if there are left and right balls
        if (index - 1) == -1:
            self.no_left_ball = True
            self.no_right_ball = False
        if (index + 1) == len(self.pendulums):
            self.no_right_ball = True
            self.no_left_ball = False

    def collision_logic(self):
        for index in range(0, len(self.pendulums) - 1):
            dist = self.distance(self.pendulums[index], self.pendulums[index + 1])
            if dist < (self.pendulums[index].radius * 2):
                print("collision")
                # Swap Angular Velocity
                self.pendulums[index].av, self.pendulums[index + 1].av =\
                    self.pendulums[index + 1].av, self.pendulums[index].av

    def setPos_collision_logic(self):
        for index in range(0, len(self.pendulums) - 1):
            dist = self.distance(self.pendulums[index], self.pendulums[index + 1])
            if self.pendulums[index].STATE == FREE_STATE:
                if dist <= (self.pendulums[index].radius * 2):
                    # Swap Angular Velocity
                    self.pendulums[index].av, self.pendulums[index + 1].av =\
                        self.pendulums[index + 1].av, self.pendulums[index].av
                    # Switch to Collision State
                    self.pendulums[index].STATE = COLLISION_STATE
            elif self.pendulums[index].STATE == COLLISION_STATE:
                if dist >= (self.pendulums[index].radius * 2):
                    self.pendulums[index].STATE = FREE_STATE


    def new_collision_logic(self):
        for index in range(0, len(self.pendulums) - 1):
            self.ball_position_check(index)
            if self.no_left_ball:
                # Get Distance from right ball
                dist = self.distance(self.pendulums[index], self.pendulums[index + 1])
                if dist < (self.pendulums[index].radius * 2):
                    print("collision")
                    # Swap Angular Velocity
                    self.pendulums[index].av, self.pendulums[index + 1].av = \
                        self.pendulums[index + 1].av, self.pendulums[index].av
            elif self.no_right_ball:
                # Get Distance from right ball
                dist = self.distance(self.pendulums[index], self.pendulums[index - 1])
                if dist < (self.pendulums[index].radius * 2):
                    print("collision")
                    # Swap Angular Velocity
                    self.pendulums[index].av, self.pendulums[index - 1].av = \
                        self.pendulums[index - 1].av, self.pendulums[index].av
            else:
                left_dist = self.distance(self.pendulums[index], self.pendulums[index - 1])
                right_dist = self.distance(self.pendulums[index], self.pendulums[index + 1])
                # check if two collisions
                if left_dist < (self.pendulums[index].radius * 2) and right_dist < (self.pendulums[index].radius * 2):
                    # Swap End Angular Velocity
                    self.pendulums[index - 1].av, self.pendulums[index + 1].av = \
                        self.pendulums[index + 1].av, self.pendulums[index - 1].av
                elif left_dist > (self.pendulums[index].radius * 2):
                    # Swap Angular Velocity
                    self.pendulums[index].av, self.pendulums[index + 1].av = \
                        self.pendulums[index + 1].av, self.pendulums[index].av
                elif right_dist > (self.pendulums[index].radius * 2):
                    # Swap Angular Velocity
                    self.pendulums[index].av, self.pendulums[index - 1].av = \
                        self.pendulums[index - 1].av, self.pendulums[index].av

