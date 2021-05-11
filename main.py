import arcade

# константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Game"

# Константы, используемые для масштабирования наших спрайтов от их исходного размера
SPRITE_SCALING = 0.5
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
# Скорость движения игрока, в пикселях на кадр
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# Указатель текстур, первый элемент обращен влево, второй - вправо
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

# Сколько пикселей оставить в качестве минимального поля между символом и краем экрана.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.scale = SPRITE_SCALING
        self.textures = []


        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture(":resources:images/enemies/bee.png")
        self.textures.append(texture)
        texture = arcade.load_texture(":resources:images/enemies/bee.png",
                                      flipped_horizontally=True)
        self.textures.append(texture)

        # By default, face right.
        self.texture = texture

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]


class MyGame(arcade.Window):
    """
    #Основной класс приложения.
    """

    def __init__(self):

        # Вызвать родительский класс и настроить окно
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Это «списки», которые отслеживают наши спрайты. Каждый спрайт должен быть внесен в список.
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.player_sprite_list = None
        self.total_time = 0.0

        # Отдельная переменная, в которой хранится спрайт игрока
        self.player_sprite = None

        # Наш физический движок
        self.physics_engine = None
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

        # Используется для отслеживания нашей прокрутки
        self.view_bottom = 0
        self.view_left = 0

        # Следите за счетом
        self.score = 0

        # Загрузка звуков
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)

    def setup(self):
        """ Настройте игру здесь. Вызовите эту функцию, чтобы перезапустить игру. """

        # Используется для отслеживания нашей прокрутки
        self.view_bottom = 0
        self.view_left = 0

        # Следите за счетом
        self.score = 0
        self.total_time = 0.0

        # Создать спрайтлист
        self.player_list = arcade.SpriteList()
        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        # Настройте игрока, специально поместив его в эти координаты.
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_sprite_list.append(self.player_sprite)

        # Создать землю
        # Это показывает использование цикла для размещения нескольких спрайтов по горизонтали.
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Поставить ящики на землю
        # Это показывает использование списка координат для размещения спрайтов
        coordinate_list = [[512, 96],
                           [512, 160],
                           [448, 96],
                           [512, 224],
                           [256, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            # Добавьте ящик на землю
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

            # Используйте петлю, чтобы поместить несколько монет, которые наш персонаж сможет подобрать.
            for x in range(128, 1250, 256):
                coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
                coin.center_x = x
                coin.center_y = 96
                self.coin_list.append(coin)

            # Создайте "физический движок"
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """ Визуализируйте экран. """

        arcade.start_render()
        # Код для рисования экрана находится здесь
        # Рисуем наши спрайты
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_sprite_list.draw()
        self.player_list.draw()

        # Вычислить минуты
        minutes = int(self.total_time) // 60

        # Вычислить секунды, используя модуль (остаток)
        seconds = int(self.total_time) % 60

        # Выясните наш результат
        time_text = f"Time: {minutes:02d}:{seconds:02d}"

        # Вывод текста таймера

        arcade.draw_text(time_text, 450 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)

        # Нарисуйте наш счет на экране, прокручивая его с помощью области просмотра
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        """Вызывается при каждом нажатии клавиши."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Вызывается, когда пользователь отпускает клавишу. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Движение и игровая логика """

        # Переместите игрока с физическим движком
        self.physics_engine.update()

        self.player_sprite_list.update()
        self.total_time += delta_time

        # Посмотрим, попали ли мы в какие-нибудь монеты
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)

        # Прокрутите каждую попавшуюся монету (если есть) и удалите ее.
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Добавить +1 к монетам
            self.score += 1

        # --- Управление прокруткой ---

        # Отслеживайте, нужно ли нам изменить область просмотра

        changed = False

        # Прокрутка влево
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Прокрутка вправо
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Прокрутка вверх
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Прокрутка вниз
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Прокрутите только до целых чисел. В противном случае мы получим пиксели, которые не выстраиваются в линию на экране.
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
