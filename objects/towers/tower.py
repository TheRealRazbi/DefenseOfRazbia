import pygame
import math
from objects.projectiles.healingshot import HealingShot
import functions


class Tower(pygame.sprite.Sprite):
    tower_size = 0, 0

    def __init__(self, location: tuple, game):
        super().__init__()
        self.game = game
        self.width, self.height = self.game.width, self.game.height
        self.x = location[0]
        self.y = location[1]
        self.custom_hit_box = [0, 0]
        self.damage = 0
        self.range = 0
        self.img = ''
        self.cost = 0
        self.power = 0
        self.attack_speed = 1
        self.target_screen = self.game.screen
        self._selected = False
        self.cooldown = 0
        self.projectile_group = pygame.sprite.Group()
        self.projectile = ''
        left = self.width - 100
        right = self.width
        self.writing_font = pygame.font.Font("lib/fonts/big_noodle_titling.ttf", 30)
        self.writing_font_upgrade = pygame.font.Font("lib/fonts/big_noodle_titling.ttf", 22)
        self.menu_hit_box = {"sell_button": [left, 265, self.width, 300],
                             "upgrade_button": [left, 230, right, 260]}
        self.upgrade_count = 0
        self.upgrade_menu = {1: ["cost", "range", "damage", "attack_speed", "misc"]}
        self.icons = {"attack_speed": pygame.transform.scale(pygame.image.load("lib/images/icons/attack_speed.png"),
                                                             (25, 25)),
                      "attack_damage": pygame.transform.scale(pygame.image.load("lib/images/icons/attack_damage.png"),
                                                              (25, 25)),
                      "attack_range": pygame.transform.scale(pygame.image.load("lib/images/icons/attack_range.png"),
                                                             (25, 25))}
        self.accident_selling = False
        self.accident_upgrade = False
        self.black, self.white = (0, 0, 0), (255, 255, 255)

    def check_for_units(self, group):
        if self.selected:
            if self.accident_selling:
                sell_button_speech = "COMFIRM"
            else:
                sell_button_speech = "SELL"
            if self.accident_upgrade and self.upgrade_button_speech != "":
                self.upgrade_button_speech = "COMFIRM"
            else:
                self.upgrade_button_speech = "UPGRADE"
            left = self.width - 100
            right = self.width
            white = 255, 255, 255
            black = 0, 0, 0
            pygame.draw.circle(self.target_screen, black, (int(self.middle[0]), int(self.middle[1])),
                               self.range, 5)
            pygame.draw.rect(self.target_screen, white, (left, 80, 100, 220))
            pygame.draw.line(self.target_screen, black, (left, 265), (right, 265), 3)
            self.target_screen.blit(self.icons["attack_speed"], (left+45, 100))
            self.target_screen.blit(self.icons["attack_damage"], (left, 100))
            self.target_screen.blit(self.icons["attack_range"], (left, 135))
            # pygame.draw.line(self.target_screen, white, (left+50, 265), (left+50, 225), 3)
            self.write_text(sell_button_speech, (left, 265))
            self.write_text(f"Level {self.upgrade_count}", (left+20, 80), size=20)
            self.write_text(self.attack_speed, (left+75, 98))
            self.write_text(self.power, (left+30, 98))
            self.write_text(self.range, (left+30, 130), size=25)
            if self.upgrade_count % 4 or self.upgrade_count == 0:
                pygame.draw.line(self.target_screen, black, (left, 225), (right, 225), 3)
                to_render_upgrade = self.writing_font.render(self.upgrade_button_speech, True, black)
                self.target_screen.blit(to_render_upgrade, (left, 230))


        for unit in group:
            distance = math.sqrt(abs(unit.x - self.middle[0])**2 + abs(unit.y - self.middle[1])**2)

            if distance <= self.range:
                # print(f'{unit} is inside the tower range')
                if self.cooldown <= 0:
                    self.cooldown = 40
                    if self.projectile == HealingShot and unit.hp == unit.max_hp:
                        pass
                    else:
                        if unit.in_arena:
                            pass
                        else:
                            projectile = self.projectile((self.middle), (unit), self.power)
                            self.projectile_group.add(projectile)
                            # print(f"SHOT {unit}")
                            break
                else:
                    self.cooldown -= 1 * self.attack_speed
                    break

    def draw(self):
        self.target_screen.blit(self.img, (self.x, self.y))

    @property
    def hit_box(self):
        return self.x, self.y,\
                self.x+self.custom_hit_box[0],\
                self.y+self.custom_hit_box[1]

    @property
    def centred(self):
        return self.x-self.custom_hit_box[0]/2, self.y-self.custom_hit_box[1]/2

    def scale_img(self):
        self.img = pygame.transform.scale(self.img, (50, 50))

    @property
    def middle(self):
        return self.x + self.custom_hit_box[0]/2, self.y + self.custom_hit_box[1]/2

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        for the_only_group_this_sprite_will_exist in self.groups():
            if value:
                the_only_group_this_sprite_will_exist.try_to_select(self)
            else:
                self._selected = False

    def sell(self, just_view=False):
        cost = self.cost * 0.75
        for key, value in self.upgrade_menu.items():
            if key <= self.upgrade_count:
                cost += value[0] * 0.75
        if just_view:
            return cost

        if self.selected:
            self.game.gold_manager.gold += cost
            self.kill()

    def check_click(self, click):
        if functions.clicked_in_a_box(self.menu_hit_box["sell_button"], click=click):
            if self.accident_selling:
                self.sell()
            self.accident_selling = True
        else:
            self.accident_selling = False

        if functions.clicked_in_a_box(self.menu_hit_box["upgrade_button"], click=click):
            before_upgrade, after_upgrade = 0, 0
            if self.accident_upgrade:
                before_upgrade = self.upgrade_count
                self.upgrade()
                after_upgrade = self.upgrade_count

            if before_upgrade == after_upgrade:
                self.accident_upgrade = True
        else:
            self.accident_upgrade = False

        if functions.clicked_in_a_box(self.hit_box, click=click):
            self.selected = True

    def upgrade(self, just_description=False):
        try:
            cost, attack_range, damage, attack_speed, description, misc = self.upgrade_menu[self.upgrade_count+1]
            if just_description:
                return description
            cost = int(cost)
        except KeyError:
            return
        except ValueError:
            return

        if cost > self.game.gold_manager.gold:
            print('NOT ENOUGH GOLD')
            return
        else:
            self.game.gold_manager.gold -= cost
            self.upgrade_count += 1
            self.range = attack_range
            self.power = damage
            self.attack_speed = attack_speed
            self.accident_upgrade = False

    def hovering(self):
        if self.selected:
            pos = pygame.mouse.get_pos()
            self.view_upgrade(pos)
            self.view_sell(pos)

    def view_upgrade(self, pos):
        if functions.clicked_in_a_box(self.menu_hit_box["upgrade_button"], pos):
            description = self.upgrade(just_description=True)
            if description is None:
                description = ['Not implemented']
            button_hit_box = 140, 20 + 20 * len(description)


            pygame.draw.rect(self.target_screen, self.black, (pos[0]-button_hit_box[0],
                                                             pos[1]-button_hit_box[1],
                                                             button_hit_box[0], button_hit_box[1]))

            for index, line in enumerate(description):
                to_render = self.writing_font_upgrade.render(line, True, self.white)
                self.target_screen.blit(to_render, (pos[0]-button_hit_box[0]+2, pos[1]-button_hit_box[1]+22*index))

    def view_sell(self, pos):
        if functions.clicked_in_a_box(self.menu_hit_box["sell_button"], pos):
            gold_value = self.sell(just_view=True)
            sell_hit_box = 11*(1+len(str(int(gold_value)))), 30

            to_render = self.writing_font.render(str(int(gold_value))+"$", True, self.white)
            pygame.draw.rect(self.target_screen, self.black, (pos[0]-sell_hit_box[0],
                                                             pos[1]-sell_hit_box[1],
                                                         sell_hit_box[0], sell_hit_box[1]))
            self.target_screen.blit(to_render, (pos[0]-sell_hit_box[0], pos[1]-sell_hit_box[1]))

    def write_text(self, text, where, color=(0, 0, 0), size=30):
        writing_font = pygame.font.Font("lib/fonts/big_noodle_titling.ttf", size)

        to_render = writing_font.render(str(text), True, color)
        self.target_screen.blit(to_render, where)



