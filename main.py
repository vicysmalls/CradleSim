from Simulation import*

def init_surface(size, caption):
    pygame.init()
    pygame.display.set_caption(caption)
    surface = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    return surface, clock

def run():
    width, height = 600, 600
    fps = 60

    surface, clock = init_surface((width, height), 'Simple Pendulum')
    simulation = Simulation(width, height)
    stop = False

    while not stop:
        clock.tick(fps)
        surface.fill(black)

        for event in pygame.event.get():
            stop = event.type == pygame.QUIT
            
        simulation.collision_logic()
        simulation.moving_logic(surface)

        pygame.display.flip()

    pygame.quit()

run()
