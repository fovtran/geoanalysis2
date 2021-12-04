from PIL import Image, ImageDraw
from metaballs import MetaBallManager, Ball

WIDTH = 640
HEIGHT = 480

balls = []
size = (WIDTH, HEIGHT)
RADUIS = 3
STEP_SIZE = 1

GOO = 3.0
THRESHOLD = 0.004

image = Image.new('RGBA', size)

balls.append(Ball(100, 100, RADUIS))
balls.append(Ball(110, 110, RADUIS))
balls.append(Ball(130, 130, 6*RADUIS))
balls.append(Ball(150, 130, 16*RADUIS))
balls.append(Ball(180, 180, RADUIS))

manager = MetaBallManager(balls, GOO, THRESHOLD, (255, 0, 0), image, WIDTH*HEIGHT)

manager.DrawBalls(manager.rungeKutta2, STEP_SIZE)
image.save("image.png", "PNG")
